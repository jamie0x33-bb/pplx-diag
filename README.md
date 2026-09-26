# pplx-diag

[![CI](https://github.com/jamie0x33-bb/pplx-diag/actions/workflows/ci.yml/badge.svg)](https://github.com/jamie0x33-bb/pplx-diag/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://pypi.org/project/pplx-diag/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Diagnostics for Perplexity Computer sandboxes.

When something breaks inside a Computer sandbox the useful context is scattered — the
image tag, the kernel, the Python build, which connector schema revision the session got,
where the cache landed. `pplx-diag` collects that into one bundle so a bug report carries
the environment it happened in.

- **Bundle history:** <https://pplx-diag.vercel.app/docs/history>
- **Docs:** <https://pplx-diag.vercel.app/docs/quickstart>

## Install

```bash
pip install pplx-diag
```

## Use

Run this before opening an issue:

```bash
pplx-diag check
```

```
collecting environment
uploading bundle             bd_4a81c7f2
runtime                      computer/2026.09
python                       3.13.2
kernel                       6.1.141
connector_schema             v3
cache_root                   /home/user/.cache/pplx-diag
```

Quote the `bd_` id in your report. A maintainer can pull the full bundle from it and
compare it against other sandboxes on the same image.

Collect without uploading:

```bash
pplx-diag collect --json
```

Look up a published bundle:

```bash
pplx-diag show bd_4a81c7f2
```

## What is in a bundle

| Field | Source |
| --- | --- |
| `runtime` | `SANDBOX_TYPE` and the image tag |
| `python` | `sys.version_info` |
| `kernel` | `platform.release()` |
| `connector_schema` | revision for the detected image |
| `cache_root` | resolved cache directory |
| `packages` | versions of a short tracked list |

Environment metadata only. No file contents, no directory listings, no account data.
`tests/test_collect.py` asserts that a credential placed in the environment never reaches
the bundle.

Bundles are grouped by workspace, which is what makes an image regression visible — one
sandbox reporting eight times looks nothing like eight sandboxes reporting once. See
[docs/diagnostics.md](docs/diagnostics.md) for how attribution works. 318 bundles from 57
workspaces so far.

## Development

```bash
pip install -e '.[dev]'
pytest
```

## License

MIT
