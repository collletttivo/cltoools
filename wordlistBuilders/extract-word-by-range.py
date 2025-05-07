"""
Extract words from a PDF consisting only of characters in a certain Unicode Range.
"""
from __future__ import annotations
import re, sys
from pathlib import Path
from pdfminer.high_level import extract_text


# ╔══════════════════════════════════════════════════════════════╗
# ║                         USER CONFIG                         ║
# ╚══════════════════════════════════════════════════════════════╝
PDF_PATH        = Path("input.pdf")
OUTPUT_PATH     = Path("words_by_range.txt")
LANGUAGE        = "Farsi"
UNICODE_RANGES: list[tuple[int, int]] = [
    (0x0600, 0x06FF),  # Arabic block
    (0x0750, 0x077F),
    (0x0870, 0x089F),
    (0x08A0, 0x08FF),
    (0xFB50, 0xFDFF),
]
KEEP_DUPLICATES = False
# ╔══════════════════════════════════════════════════════════════╗
# ║                      END USER CONFIG                        ║
# ╚══════════════════════════════════════════════════════════════╝


def ranges_to_regex(ranges) -> re.Pattern[str]:
    classes = [f"{chr(lo)}-{chr(hi)}" for lo, hi in ranges]
    return re.compile(fr"[{''.join(classes)}]+")


def main() -> None:
    if not PDF_PATH.exists():
        sys.exit(f"❌ PDF not found: {PDF_PATH}")

    word_re = ranges_to_regex(UNICODE_RANGES)
    text = extract_text(str(PDF_PATH))
    words = word_re.findall(text)
    if not KEEP_DUPLICATES:
        words = list(dict.fromkeys(words))

    OUTPUT_PATH.write_text("\n".join(words), encoding="utf-8")
    print(f"✅ {LANGUAGE}: wrote {len(words):,} words → {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
