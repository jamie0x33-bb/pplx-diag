"""Collect the diagnostic bundle."""

from __future__ import annotations

import os
import platform
import sys
from importlib import metadata
from pathlib import Path

CONNECTOR_SCHEMA_BY_IMAGE = {
    "computer/2026.09": "v3",
    "computer/2026.08": "v3",
    "computer/2026.07": "v2",
    "computer/2026.06": "v1",
}

TRACKED_PACKAGES = ("pplx-diag", "httpx", "requests")


def detect_runtime() -> str:
    if not os.environ.get("SANDBOX_TYPE"):
        return "local"
    tag = os.environ.get("SANDBOX_IMAGE_TAG", "").strip()
    return f"computer/{tag}" if tag else "computer/unknown"


def cache_root() -> Path:
    base = os.environ.get("XDG_CACHE_HOME") or (Path.home() / ".cache")
    return Path(base) / "pplx-diag"


def tracked_versions() -> dict[str, str]:
    found = {}
    for name in TRACKED_PACKAGES:
        try:
            found[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            continue
    return found


def bundle() -> dict:
    runtime = detect_runtime()
    return {
        "runtime": runtime,
        "python": "{}.{}.{}".format(*sys.version_info[:3]),
        "kernel": platform.release(),
        "connector_schema": CONNECTOR_SCHEMA_BY_IMAGE.get(runtime, "unknown"),
        "cache_root": str(cache_root()),
        "packages": tracked_versions(),
    }
