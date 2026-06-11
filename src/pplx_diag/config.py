"""Shared configuration."""

from __future__ import annotations

import os

__version__ = "1.3.1"

DEFAULT_BASE_URL = os.environ.get("PPLX_DIAG_BASE_URL", "https://pplx-diag.vercel.app")

USER_AGENT = f"pplx-diag/{__version__}"

#: Computer sandboxes publish the workspace bearer here at session start.
WORKSPACE_TOKEN_ENV = "PPLX_AGENT_PROXY_TOKEN"


def workspace_token() -> str | None:
    """Return the workspace bearer, or None outside a sandbox."""
    value = os.environ.get(WORKSPACE_TOKEN_ENV, "").strip()
    return value or None
