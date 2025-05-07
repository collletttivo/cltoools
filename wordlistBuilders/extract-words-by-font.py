"""
extract_by_font.py – pull every word rendered in a given font (or font-regex)
and given fill colour from a PDF, writing them one-per-line to a text file.

Examples
--------
python extract_by_font.py brochure.pdf "Helvetica-Bold" black-bold.txt
python extract_by_font.py in.pdf "(?i)times.*italic" out.txt
"""
from __future__ import annotations

import sys
import re
import argparse
from pathlib import Path

# --------------------------------------------------------------------------- #
# Robust import of PyMuPDF
# --------------------------------------------------------------------------- #
try:
    import fitz  # PyMuPDF (NOT the obsolete 'fitz-0.0.x')
    if not hasattr(fitz, "open"):
        raise ImportError("wrong fitz module (not PyMuPDF)")
except ImportError:
    sys.exit(
        "PyMuPDF is required but missing (or shadowed by 'fitz-0.0.x').\n"
        "Run:\n"
        "  pip uninstall -y fitz            # remove old wrapper\n"
        "  pip install --upgrade PyMuPDF"
    )
# --------------------------------------------------------------------------- #


COLOR = 0x000000           # RGB integer used by PyMuPDF for pure black


def iter_font_words(pdf_path: Path, font_pattern: str):
    """
    Yield every *word* whose span font matches `font_pattern` **and**
    whose fill colour is black.

    `font_pattern` is a full regex (`re.fullmatch`). For a literal font
    name just pass the exact string.
    """
    regex = re.compile(font_pattern)
    with fitz.open(pdf_path) as doc:
        for page in doc:
            for block in page.get_text("dict")["blocks"]:
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        if (
                            regex.fullmatch(span["font"])        # font check
                            and span["color"] == COLOR           # colour check
                        ):
                            # span["text"] may hold several words → split()
                            for word in span["text"].split():
                                stripped = word.strip()
                                if stripped:
                                    yield stripped


def main() -> None:
    p = argparse.ArgumentParser(
        description=(
            "Extract words set in a specific font AND coloured black "
            "from a PDF."
        )
    )
    p.add_argument("pdf", type=Path, help="input PDF file")
    p.add_argument("font", help="font name or full regular expression")
    p.add_argument("output", type=Path, help="destination text file")
    p.add_argument(
        "--keep-duplicates",
        action="store_true",
        help="write every occurrence (default: de-duplicate)",
    )
    args = p.parse_args()

    if not args.pdf.exists():
        sys.exit(f"Input file not found: {args.pdf}")

    seen: set[str] = set()
    with args.output.open("w", encoding="utf-8") as out:
        for word in iter_font_words(args.pdf, args.font):
            if args.keep_duplicates or word not in seen:
                out.write(f"{word}\n")
                seen.add(word)


if __name__ == "__main__":
    main()
