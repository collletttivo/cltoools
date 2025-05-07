"""
Extract words from a PDF that contain at least one character from a list.
"""
from __future__ import annotations
import re, sys
from pathlib import Path
from pdfminer.high_level import extract_text


# ╔══════════════════════════════════════════════════════════════╗
# ║                         USER CONFIG                         ║
# ╚══════════════════════════════════════════════════════════════╝
PDF_PATH        = Path("input.pdf")      # source PDF
OUTPUT_PATH     = Path("words_by_char.txt")      # destination text file
LANGUAGE        = "Romanian"
TARGET_CHAR     = "ĂÂÎȘŞȚŢăâîșşțţ"        # characters of interest
KEEP_DUPLICATES = False                  # True = list every hit
# ╔══════════════════════════════════════════════════════════════╗
# ║                      END USER CONFIG                        ║
# ╚══════════════════════════════════════════════════════════════╝


WORD_RE = re.compile(rf"[A-Za-z{TARGET_CHAR}]+", re.UNICODE)


def main() -> None:
    if not PDF_PATH.exists():
        sys.exit(f"❌ PDF not found: {PDF_PATH}")

    text = extract_text(str(PDF_PATH))
    words = [w for w in WORD_RE.findall(text) if any(c in TARGET_CHAR for c in w)]
    if not KEEP_DUPLICATES:
        words = list(dict.fromkeys(words))

    OUTPUT_PATH.write_text("\n".join(words), encoding="utf-8")
    print(f"✅ {LANGUAGE}: wrote {len(words):,} words → {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
