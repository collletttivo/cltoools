"""
PDF Words extractor


"""

from __future__ import annotations
import re
from pathlib import Path
from pdfminer.high_level import extract_text

# ╔════════════════════════════════════════════════════════════════╗
# ║                              CONFIG                            ║
# ╚════════════════════════════════════════════════════════════════╝

# 1) Friendly name of the writing system (used for messages & file name)
WRITING_SYSTEM_NAME: str = "Farsi"

# 2) Unicode ranges as (start, end) integer tuples
#    ––– Example for modern Russian –––
UNICODE_RANGES: list[tuple[int, int]] = [
    (0x0600, 0x06FF),   # Arabic (basic)                ﹙U+0600–U+06FF﹚
    (0x0750, 0x077F),   # Arabic Supplement             ﹙U+0750–U+077F﹚
    (0x0870, 0x089F),   # Arabic Extended‑B             ﹙U+0870–U+089F﹚
    (0x08A0, 0x08FF),   # Arabic Extended‑A             ﹙U+08A0–U+08FF﹚
    (0xFB50, 0xFDFF),   # Arabic Presentation‑Forms‑A   ﹙U+FB50–U+FDFF﹚
    (0xFE70, 0xFEFF),   # Arabic Presentation‑Forms‑B   ﹙U+FE70–U+FEFF﹚
    (0x10EC0, 0x10EFF), # Arabic Extended‑C (BMP‑plane1)﹙U+10EC0–U+10EFF﹚
]


# 3) PDF to process
PDF_PATH: Path = Path("input.pdf")   # ← point to your PDF

# 4) Result file (one “word” per line)
OUTPUT_PATH: Path = Path(f"{WRITING_SYSTEM_NAME.lower()}_words.txt")

# ╔════════════════════════════════════════════════════════════════╗
# ║                           END CONFIG                           ║
# ╚════════════════════════════════════════════════════════════════╝


def build_regex(ranges: list[tuple[int, int]]) -> re.Pattern:
    """
    Turn [(lo, hi), …] into one big character‑class like:
       '[\u0400-Я\u0500-...\U0001E08F]'
    Any (lo, hi) order is accepted.
    """
    segments: list[str] = []
    for lo, hi in ranges:
        if lo > hi:
            lo, hi = hi, lo
        segments.append(f"{chr(lo)}-{chr(hi)}")
    charclass = "".join(segments)
    return re.compile(fr"[{charclass}]+")


def extract_pdf_text(pdf_path: Path) -> str:
    """Return all text from the PDF (uses pdfminer.six)."""
    return extract_text(str(pdf_path))


def main() -> None:
    if not PDF_PATH.exists():
        raise FileNotFoundError(f"Cannot find PDF: {PDF_PATH}")

    pattern = build_regex(UNICODE_RANGES)

    print(f"Using regex   : {pattern.pattern}")
    print(f"Extracting {WRITING_SYSTEM_NAME} words from {PDF_PATH.name} …")

    raw = extract_pdf_text(PDF_PATH)
    matches = pattern.findall(raw)

    OUTPUT_PATH.write_text("\n".join(matches), encoding="utf‑8")

    print(f"✅ Wrote {len(matches):,} {WRITING_SYSTEM_NAME} words → {OUTPUT_PATH.as_posix()}")


if __name__ == "__main__":
    main()
