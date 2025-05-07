#!/usr/bin/env python3
"""
extract_romanian_with_diacritics.py
───────────────────────────────────
• Extracts *only* those words that contain at least one of
  ĂÂÎȘŞȚŢăâîșşțţ from a PDF and writes them one‑per‑line.

Dependencies: pdfminer.six
    pip install pdfminer.six
"""

from __future__ import annotations
import re
from pathlib import Path
from pdfminer.high_level import extract_text

# ╔════════════════════════════════════════════════════════════════╗
# ║                        USER ‑ CONFIG                          ║
# ╚════════════════════════════════════════════════════════════════╝

PDF_PATH   = Path("input.pdf")              # ← your PDF
OUTPUT_PATH = Path("romanian_words.txt")    # ← result file

ROM_DIACRITICS = "ĂÂÎȘŞȚŢăâîșşțţ"

# ╔════════════════════════════════════════════════════════════════╗
# ║                      END  USER ‑ CONFIG                       ║
# ╚════════════════════════════════════════════════════════════════╝

ROM_WORD_RE = re.compile(rf"[A-Za-z{ROM_DIACRITICS}]+", re.UNICODE)

def extract_pdf_text(pdf_path: Path) -> str:
    """Return full text of the PDF using pdfminer.six."""
    return extract_text(str(pdf_path))

def main() -> None:
    if not PDF_PATH.exists():
        raise FileNotFoundError(f"Cannot find PDF: {PDF_PATH}")

    print(f"Extracting Romanian words (must contain a diacritic) from {PDF_PATH.name} …")

    text = extract_pdf_text(PDF_PATH)
    candidates = ROM_WORD_RE.findall(text)

    kept: list[str] = [
        w for w in candidates
        if any(ch in ROM_DIACRITICS for ch in w)
    ]

    # Optional: unique + preserve original order
    kept = list(dict.fromkeys(kept))

    OUTPUT_PATH.write_text("\n".join(kept), encoding="utf-8")
    print(f"✓ Wrote {len(kept):,} words → {OUTPUT_PATH.as_posix()}")

if __name__ == "__main__":
    main()
