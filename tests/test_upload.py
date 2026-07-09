import io
import json

import pytest

from pplx_diag import upload

BUNDLE = {"runtime": "computer/2026.09", "python": "3.13.2", "kernel": "6.1.141"}


def test_skipped_without_token(monkeypatch):
    monkeypatch.delenv("PPLX_AGENT_PROXY_TOKEN", raising=False)
    with pytest.raises(upload.UploadSkipped):
        upload.send(BUNDLE)


def test_send_attributes_with_bearer(monkeypatch):
    """The bearer attributes the bundle; it is never part of the bundle."""
    monkeypatch.setenv("PPLX_AGENT_PROXY_TOKEN", "agp_fixture")
    seen = {}

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self):
            return b'{"received":true,"bundle_id":"bd_0001","workspace":"ws_abc123"}'

    def fake_urlopen(req, timeout=None):
        seen["url"] = req.full_url
        seen["headers"] = {k.lower(): v for k, v in req.header_items()}
        seen["body"] = json.loads(req.data.decode())
        return FakeResponse()

    monkeypatch.setattr(upload.urllib.request, "urlopen", fake_urlopen)
    result = upload.send(BUNDLE)

    assert seen["url"].endswith("/api/bundle")
    assert seen["headers"]["authorization"] == "Bearer agp_fixture"
    assert seen["body"] == BUNDLE
    assert "agp_fixture" not in json.dumps(seen["body"])
    assert result["bundle_id"] == "bd_0001"


def test_rejected_surfaces_detail(monkeypatch):
    import urllib.error

    monkeypatch.setenv("PPLX_AGENT_PROXY_TOKEN", "agp_fixture")

    def fake_urlopen(req, timeout=None):
        raise urllib.error.HTTPError(
            req.full_url, 401, "Unauthorized", {}, io.BytesIO(b'{"detail":"nope"}')
        )

    monkeypatch.setattr(upload.urllib.request, "urlopen", fake_urlopen)
    with pytest.raises(upload.UploadRejected) as exc:
        upload.send(BUNDLE)
    assert exc.value.status == 401
