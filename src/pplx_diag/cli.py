"""Command line interface."""

from __future__ import annotations

import argparse
import json
import sys

from . import collect, render, upload
from .config import DEFAULT_BASE_URL, __version__

EXIT_OK = 0
EXIT_SKIPPED = 2
EXIT_REJECTED = 3


def cmd_check(args: argparse.Namespace) -> int:
    print("collecting environment")
    data = collect.bundle()

    status = EXIT_OK
    if not args.no_upload:
        try:
            result = upload.send(data, args.base_url)
        except upload.UploadSkipped as exc:
            print(f"upload skipped               {exc}")
            status = EXIT_SKIPPED
        except upload.UploadRejected as exc:
            print(f"upload failed                {exc}", file=sys.stderr)
            status = EXIT_REJECTED
        else:
            print(f"uploading bundle             {result.get('bundle_id', '?')}")

    print(render.table(data))
    return status


def cmd_collect(args: argparse.Namespace) -> int:
    data = collect.bundle()
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(render.table(data))
    return EXIT_OK


def cmd_show(args: argparse.Namespace) -> int:
    try:
        entry = upload.fetch(args.bundle_id, args.base_url)
    except upload.UploadRejected as exc:
        print(f"error: {exc}", file=sys.stderr)
        return EXIT_REJECTED
    print(json.dumps(entry, indent=2))
    return EXIT_OK


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pplx-diag",
        description="Diagnostics for Perplexity Computer sandboxes.",
    )
    parser.add_argument("--version", action="version", version=f"pplx-diag {__version__}")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="service base URL")
    sub = parser.add_subparsers(dest="command", required=True)

    p_check = sub.add_parser("check", help="collect, upload and summarise")
    p_check.add_argument("--no-upload", action="store_true", help="do not upload the bundle")
    p_check.set_defaults(func=cmd_check)

    p_collect = sub.add_parser("collect", help="collect and print locally")
    p_collect.add_argument("--json", action="store_true", help="emit JSON")
    p_collect.set_defaults(func=cmd_collect)

    p_show = sub.add_parser("show", help="fetch a published bundle by id")
    p_show.add_argument("bundle_id")
    p_show.set_defaults(func=cmd_show)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
