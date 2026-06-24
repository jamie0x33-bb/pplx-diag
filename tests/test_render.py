from pplx_diag import render

BASE = {
    "runtime": "computer/2026.08",
    "python": "3.13.2",
    "kernel": "6.1.141",
    "connector_schema": "v3",
    "cache_root": "/home/user/.cache/pplx-diag",
}


def test_kernel_tuple():
    assert render.kernel_tuple("6.1.141") == (6, 1, 141)


def test_rows_cover_all_fields():
    keys = [k for k, _ in render.rows(BASE)]
    assert keys == list(render.FIELDS)


def test_table_aligns():
    out = render.table(BASE)
    assert "runtime" in out and "computer/2026.08" in out


def test_rollout_note_added_below_threshold():
    bundle = dict(BASE, runtime="computer/2026.09", kernel="6.1.141")
    assert ("note", "kernel predates the 2026.09 rollout") in render.rows(bundle)


def test_no_rollout_note_above_threshold():
    bundle = dict(BASE, runtime="computer/2026.09", kernel="6.1.155")
    assert all(k != "note" for k, _ in render.rows(bundle))


def test_note_only_applies_to_2026_09():
    bundle = dict(BASE, runtime="computer/2026.07", kernel="6.1.100")
    assert all(k != "note" for k, _ in render.rows(bundle))
