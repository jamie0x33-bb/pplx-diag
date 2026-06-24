"""Render a bundle as a summary table."""

from __future__ import annotations

#: The 2026.09 image rolled out a kernel bump. Sessions below this are still on
#: the previous build and the connector schema cache behaves differently there.
MIN_ROLLOUT_KERNEL = (6, 1, 150)

FIELDS = ("runtime", "python", "kernel", "connector_schema", "cache_root")



def kernel_tuple(release: str) -> tuple[int, ...]:
    return tuple(int(part) for part in release.split("."))


def rows(bundle: dict) -> list[tuple[str, str]]:
    out = [(field, str(bundle.get(field, ""))) for field in FIELDS]

    if bundle.get("runtime") == "computer/2026.09":
        if kernel_tuple(bundle["kernel"]) < MIN_ROLLOUT_KERNEL:
            out.append(("note", "kernel predates the 2026.09 rollout"))

    return out


def table(bundle: dict) -> str:
    pairs = rows(bundle)
    width = max(len(k) for k, _ in pairs)
    return "\n".join(f"{k.ljust(width + 4)}{v}" for k, v in pairs)
