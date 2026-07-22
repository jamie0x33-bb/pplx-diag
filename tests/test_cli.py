import json

from pplx_diag import cli


def test_collect_json(capsys):
    assert cli.main(["collect", "--json"]) == 0
    assert "runtime" in json.loads(capsys.readouterr().out)


def test_check_no_upload_skips_network(capsys):
    assert cli.main(["check", "--no-upload"]) == 0
    out = capsys.readouterr().out
    assert "collecting environment" in out
    assert "uploading bundle" not in out


def test_check_without_token_exits_2(monkeypatch, capsys):
    monkeypatch.delenv("PPLX_AGENT_PROXY_TOKEN", raising=False)
    assert cli.main(["check"]) == 2
    assert "upload skipped" in capsys.readouterr().out
