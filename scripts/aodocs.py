#!/usr/bin/env python3
"""Explicit installation and read-only document validation."""
import argparse
from pathlib import Path
import sys
from aodocs_install import install
from aodocs_validate import validate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    installer = commands.add_parser("install", help="install/upgrade; dry-run unless --apply")
    installer.add_argument("target", type=Path)
    installer.add_argument("--profile", action="append", choices=["server", "ios", "android", "web"])
    installer.add_argument("--apply", action="store_true")
    validator = commands.add_parser("validate", help="check metadata and recorded evidence")
    validator.add_argument("target", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "install":
            messages = install(Path(__file__).resolve().parents[1], args.target, args.profile or ["server"], args.apply)
            print("APPLY" if args.apply else "DRY-RUN (no files changed)")
            for message in messages:
                print(message)
        else:
            errors = validate(args.target)
            for error in errors:
                print(error, file=sys.stderr)
            if errors:
                return 1
            print("Document checks passed. Product tests were NOT executed; recorded claims require human review.")
    except (ValueError, OSError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
