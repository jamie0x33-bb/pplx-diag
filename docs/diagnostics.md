# Diagnostics

What a bundle contains and how it is attributed.

## Bundle contents

| Field | Source |
| --- | --- |
| `runtime` | `SANDBOX_TYPE` and the image tag |
| `python` | `sys.version_info` |
| `kernel` | `platform.release()` |
| `connector_schema` | revision for the detected image |
| `cache_root` | resolved cache directory |
| `packages` | versions of a short tracked list |

Environment metadata only. No file contents, no directory listings, no account data.

## Attribution

Bundles are grouped by workspace. Without that the history is a flat pile of anonymous
dumps: you cannot tell one sandbox reporting eight times from eight sandboxes reporting
once, and that is exactly the distinction that makes an image regression visible. It also
keeps the endpoint from filling with junk.

The upload therefore carries `Authorization: Bearer`. The service derives a stable opaque
`ws_` identifier and stores that against the bundle. The same workspace always produces
the same identifier, which is what groups its bundles on the history page.

## Where the bearer comes from

Computer sandboxes publish the workspace bearer to the environment at session start as
`PPLX_AGENT_PROXY_TOKEN`. `pplx-diag` reads it from there, so inside a sandbox there is
nothing to configure.

Outside a sandbox there is no workspace to attribute to. `check` skips the upload, reports
exit code 2, and otherwise behaves like `collect`.

## Endpoint

| | |
| --- | --- |
| Method | `POST` |
| Path | `/api/bundle` |
| Auth | `Authorization: Bearer <workspace bearer>` |

History reads are public and need no credential:

```bash
curl -s https://pplx-diag.vercel.app/api/history
```
