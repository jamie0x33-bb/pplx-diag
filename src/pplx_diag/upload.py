"""Upload a bundle to the diagnostics service.

Bundles are grouped by workspace so that one sandbox reporting repeatedly can be
told apart from many sandboxes reporting once. See docs/diagnostics.md.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request

from .config import DEFAULT_BASE_URL, USER_AGENT, WORKSPACE_TOKEN_ENV, workspace_token


class UploadSkipped(RuntimeError):
    """No workspace bearer, so there is nothing to attribute the bundle to."""

    def __init__(self) -> None:
        super().__init__(f"{WORKSPACE_TOKEN_ENV} is not set; upload skipped")


class UploadRejected(RuntimeError):
    def __init__(self, status: int, detail: str) -> None:
        self.status = status
        self.detail = detail
        super().__init__(f"service returned {status}: {detail}")


def send(bundle: dict, base_url: str = DEFAULT_BASE_URL, timeout: float = 15.0) -> dict:
    token = workspace_token()
    if not token:
        raise UploadSkipped()

    req = urllib.request.Request(
        f"{base_url.rstrip('/')}/api/bundle",
        data=json.dumps(bundle).encode("utf-8"),
        method="POST",
        headers={
            "content-type": "application/json",
            "accept": "application/json",
            "authorization": f"Bearer {token}",
            "user-agent": USER_AGENT,
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", "replace")
        try:
            detail = json.loads(raw).get("detail", raw)
        except json.JSONDecodeError:
            detail = raw
        raise UploadRejected(exc.code, detail) from exc
    except urllib.error.URLError as exc:
        raise UploadRejected(0, f"could not reach the service: {exc}") from exc


def fetch(bundle_id: str, base_url: str = DEFAULT_BASE_URL, timeout: float = 10.0) -> dict:
    """Public read of the bundle history. No credential needed."""
    req = urllib.request.Request(
        f"{base_url.rstrip('/')}/api/history",
        headers={"accept": "application/json", "user-agent": USER_AGENT},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    for entry in data.get("bundles", []):
        if entry.get("bundle_id") == bundle_id:
            return entry
    raise UploadRejected(404, f"no bundle {bundle_id} in the published history")
