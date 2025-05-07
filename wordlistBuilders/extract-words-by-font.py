"""
Extract every word from a PDF rendered in a specific font and color.
"""
from __future__ import annotations
import re, sys
from pathlib import Path
import fitz  # PyMuPDF


# ╔══════════════════════════════════════════════════════════════╗
# ║                         USER CONFIG                         ║
# ╚══════════════════════════════════════════════════════════════╝
PDF_PATH        = Path("input.pdf")
OUTPUT_PATH     = Path("word_by_font.txt")
FONT_PATTERN    = r"LucidaSansUnicode"   # exact name or regex
COLOR_RGB_INT   = 0x000000            # only collect pure-black text
KEEP_DUPLICATES = False
# ╔══════════════════════════════════════════════════════════════╗
# ║                      END USER CONFIG                        ║
# ╚══════════════════════════════════════════════════════════════╝


def iter_target_words(pdf: Path, font_rx: re.Pattern[str]):
    with fitz.open(pdf) as doc:
        for page in doc:
            for block in page.get_text("dict")["blocks"]:
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        if span["color"] != COLOR_RGB_INT:
                            continue
                        if not font_rx.fullmatch(span["font"]):
                            continue
                        yield from span["text"].split()


def main() -> None:
    if not PDF_PATH.exists():
        sys.exit(f"❌ PDF not found: {PDF_PATH}")

    font_rx = re.compile(FONT_PATTERN)
    seen, collected = set(), []

    for word in iter_target_words(PDF_PATH, font_rx):
        if KEEP_DUPLICATES or word not in seen:
            collected.append(word)
            seen.add(word)

    OUTPUT_PATH.write_text("\n".join(collected), encoding="utf-8")
    print(f"✅ Font filter: wrote {len(collected):,} words → {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
