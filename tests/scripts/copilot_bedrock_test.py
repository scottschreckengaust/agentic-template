"""Tests for the Bedrock Copilot launcher."""

from __future__ import annotations

import json
import threading
import unittest
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib.machinery import SourceFileLoader
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "copilot-bedrock"
launcher = SourceFileLoader("copilot_bedrock", str(SCRIPT)).load_module()


class StripSamplingParametersTest(unittest.TestCase):
    def test_drops_sampling_fields_and_keeps_the_model(self) -> None:
        raw = json.dumps(
            {
                "model": "global.anthropic.claude-opus-4-7",
                "temperature": 0,
                "top_p": 1,
                "top_k": 5,
                "messages": [{"role": "user", "content": "hi"}],
            }
        ).encode()
        cleaned = json.loads(launcher.strip_sampling_parameters(raw))
        self.assertEqual(
            cleaned,
            {
                "model": "global.anthropic.claude-opus-4-7",
                "messages": [{"role": "user", "content": "hi"}],
            },
        )

    def test_leaves_a_body_without_sampling_fields_unchanged(self) -> None:
        raw = b'{"model":"anthropic.claude-sonnet-4-6"}'
        self.assertEqual(launcher.strip_sampling_parameters(raw), raw)

    def test_leaves_non_json_unchanged(self) -> None:
        raw = b"temperature: 0"
        self.assertEqual(launcher.strip_sampling_parameters(raw), raw)


class AnthropicPathTest(unittest.TestCase):
    def test_allows_messages_path(self) -> None:
        self.assertTrue(launcher.anthropic_path_allowed("/anthropic/v1/messages"))

    def test_rejects_other_hosts_and_traversal(self) -> None:
        self.assertFalse(launcher.anthropic_path_allowed("http://evil.test/anthropic/v1/messages"))
        self.assertFalse(launcher.anthropic_path_allowed("/anthropic/../openai/v1/responses"))
        self.assertFalse(launcher.anthropic_path_allowed("/openai/v1/responses"))


class _Upstream(BaseHTTPRequestHandler):
    received: dict[str, object] = {}

    def log_message(self, fmt: str, *args: object) -> None:
        return

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length", "0"))
        _Upstream.received = {
            "path": self.path,
            "body": self.rfile.read(length),
            "host": self.headers.get("Host"),
        }
        payload = b'data: {"ok":true}\n\n'
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


class SamplingProxyTest(unittest.TestCase):
    def setUp(self) -> None:
        self.upstream = ThreadingHTTPServer(("127.0.0.1", 0), _Upstream)
        self.upstream_thread = threading.Thread(target=self.upstream.serve_forever, daemon=True)
        self.upstream_thread.start()
        host, port = self.upstream.server_address[:2]
        self.proxy = launcher.start_sampling_proxy(f"http://{host}:{port}")
        proxy_host, proxy_port = self.proxy.server_address[:2]
        self.proxy_url = f"http://{proxy_host}:{proxy_port}"

    def tearDown(self) -> None:
        self.proxy.shutdown()
        self.proxy.server_close()
        self.upstream.shutdown()
        self.upstream.server_close()

    def test_forwards_messages_without_sampling_parameters(self) -> None:
        body = json.dumps(
            {"model": "global.anthropic.claude-opus-4-7", "temperature": 0, "max_tokens": 16}
        ).encode()
        request = urllib.request.Request(
            self.proxy_url + "/anthropic/v1/messages",
            data=body,
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=5) as response:
            streamed = response.read()
        self.assertEqual(streamed, b'data: {"ok":true}\n\n')
        forwarded = json.loads(_Upstream.received["body"])
        self.assertEqual(
            forwarded,
            {"model": "global.anthropic.claude-opus-4-7", "max_tokens": 16},
        )
        self.assertEqual(_Upstream.received["path"], "/anthropic/v1/messages")

    def test_rejects_a_non_anthropic_path(self) -> None:
        request = urllib.request.Request(
            self.proxy_url + "/openai/v1/responses",
            data=b"{}",
            method="POST",
        )
        with self.assertRaises(urllib.error.HTTPError) as raised:
            urllib.request.urlopen(request, timeout=5)
        self.assertEqual(raised.exception.code, 404)


if __name__ == "__main__":
    unittest.main()
