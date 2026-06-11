import json

from pplx_diag import collect


def test_runtime_local_outside_sandbox(monkeypatch):
    monkeypatch.delenv("SANDBOX_TYPE", raising=False)
    assert collect.detect_runtime() == "local"


def test_runtime_tagged(monkeypatch):
    monkeypatch.setenv("SANDBOX_TYPE", "asi_session")
    monkeypatch.setenv("SANDBOX_IMAGE_TAG", "2026.09")
    assert collect.detect_runtime() == "computer/2026.09"


def test_runtime_untagged(monkeypatch):
    monkeypatch.setenv("SANDBOX_TYPE", "asi_session")
    monkeypatch.delenv("SANDBOX_IMAGE_TAG", raising=False)
    assert collect.detect_runtime() == "computer/unknown"


def test_bundle_is_serialisable():
    assert json.loads(json.dumps(collect.bundle()))["python"].count(".") == 2


def test_bundle_carries_no_credential(monkeypatch):
    monkeypatch.setenv("PPLX_AGENT_PROXY_TOKEN", "agp_should_not_appear")
    assert "agp_should_not_appear" not in json.dumps(collect.bundle())


def test_schema_for_known_image(monkeypatch):
    monkeypatch.setenv("SANDBOX_TYPE", "asi_session")
    monkeypatch.setenv("SANDBOX_IMAGE_TAG", "2026.06")
    assert collect.bundle()["connector_schema"] == "v1"


def test_cache_root_honours_xdg(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path))
    assert collect.cache_root() == tmp_path / "pplx-diag"
