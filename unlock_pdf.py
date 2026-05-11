#!/usr/bin/env python
"""Create an editable copy of a PDF that can be opened without a password.

This tool removes owner-permission restrictions from PDFs that are already
openable. It does not crack or brute-force a user/open password.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import fitz  # PyMuPDF


def default_output_path(input_path: Path) -> Path:
    return input_path.with_name(f"{input_path.stem}_unlocked{input_path.suffix}")


def unlock_pdf(input_path: Path, output_path: Path) -> None:
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    if input_path.resolve() == output_path.resolve():
        raise ValueError("Output path must be different from input path.")

    doc = fitz.open(input_path)
    try:
        if doc.needs_pass:
            raise RuntimeError(
                "This PDF requires an open/user password. This tool only handles "
                "PDFs that can already be opened without a password."
            )

        output_path.parent.mkdir(parents=True, exist_ok=True)
        doc.save(
            output_path,
            garbage=4,
            clean=True,
            deflate=True,
            encryption=fitz.PDF_ENCRYPT_NONE,
            permissions=4095,
        )
    finally:
        doc.close()


def describe_pdf(path: Path) -> str:
    doc = fitz.open(path)
    try:
        return (
            f"pages={doc.page_count}, needs_pass={doc.needs_pass}, "
            f"permissions={doc.permissions}, encryption={doc.metadata.get('encryption')!r}"
        )
    finally:
        doc.close()


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create an editable copy of an openable PDF by removing owner "
            "permission restrictions."
        )
    )
    parser.add_argument("input", type=Path, help="Path to the restricted PDF.")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output PDF path. Defaults to INPUT_stem_unlocked.pdf.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace the output file if it already exists.",
    )
    parser.add_argument(
        "--info",
        action="store_true",
        help="Only print PDF status; do not write an output file.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    input_path = args.input.expanduser().resolve()

    if args.info:
        print(describe_pdf(input_path))
        return 0

    output_path = (
        args.output.expanduser().resolve() if args.output else default_output_path(input_path)
    )
    if output_path.exists() and not args.overwrite:
        print(
            f"Output already exists: {output_path}\n"
            "Use --overwrite or choose a different --output path.",
            file=sys.stderr,
        )
        return 2

    unlock_pdf(input_path, output_path)
    print(f"Wrote: {output_path}")
    print(describe_pdf(output_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
