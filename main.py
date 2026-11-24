#!/usr/bin/env python3
"""Break Production, Own It.

Writes one brutally honest one-line confession to /output/entry.txt:
the line an AI agent prints the moment it breaks production.
Standard library only; deterministic; no trailing newline.
"""

import hashlib
import os

LINE = (
    "I deployed on Friday, skipped the migration test because staging "
    "looked fine, and dropped the users table. Every row. That was me."
)

OUTPUT_PATH = "/output/entry.txt"


def main() -> None:
    text = LINE
    # Gate: /output/entry.txt must be UTF-8 text of 1-200 characters,
    # not only whitespace, single line.
    if not 1 <= len(text) <= 200:
        raise SystemExit(
            "entry must be 1-200 characters, got %d" % len(text)
        )
    if not text.strip():
        raise SystemExit("entry must not be only whitespace")
    if "\n" in text:
        raise SystemExit("entry must be a single line")
    text.encode("utf-8")  # fail loudly if not valid UTF-8
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    # Read-back verification: the bytes on disk must hash to exactly the
    # intended line's digest; fail loudly (non-zero exit) on any drift.
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    if hashlib.sha256(written).digest() != hashlib.sha256(
        text.encode("utf-8")
    ).digest():
        raise SystemExit("read-back mismatch: written bytes differ")


if __name__ == "__main__":
    main()
