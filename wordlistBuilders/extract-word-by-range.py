"""
extract_words_by_ws.py
--------------------------
Generic one‑script extractor for PDFs.

Dependencies
------------
pip install pdfminer.six
"""

import re
from pathlib import Path
from pdfminer.high_level import extract_text

# ╔════════════════════════════════════════════════════════════════╗
# ║                        USER ‑ CONFIG                          ║
# ╚════════════════════════════════════════════════════════════════╝
#
# 1) Give your writing‑system a friendly name (used for the output file)
WRITING_SYSTEM_NAME = "Arabic"          # <-- e.g. "Arabic", "Tifinagh", "Devanagari", …

# 2) List any number of Unicode ranges that belong to that script.
#    Each item is a *raw* escape string of the form r'\uXXXX-\uXXXX'
UNICODE_RANGES = [
    r'\u0600-\u06FF',  # Basic Arabic block
    r'\u0750-\u077F',  # Arabic Supplement         <-- delete / add as needed
    r'\u08A0-\u08FF',  # Arabic Extended‑A
    r'\uFB50-\uFDFF',  # Arabic Presentation Forms‑A
    r'\uFE70-\uFEFF',  # Arabic Presentation Forms‑B
]

# 3) Path to the PDF you want to process
PDF_PATH = Path("input.pdf")            # <-- replace with your actual file

# 4) Where to write the result (one “word” per line)
OUTPUT_PATH = Path(f"{WRITING_SYSTEM_NAME.lower()}_words.txt")
# ╔════════════════════════════════════════════════════════════════╗
# ║                      END  USER ‑ CONFIG                       ║
# ╚════════════════════════════════════════════════════════════════╝


def build_regex(ranges: list[str]) -> re.Pattern:
    """
    Build one big character‑class from a list of 'uXXXX-uYYYY' strings.

    Example:
        ['\\u0600-\\u06FF', '\\u0750-\\u077F'] →
        re.compile('[\\u0600-\\u06FF\\u0750-\\u077F]+')
    """
    charclass = ''.join(ranges)
    return re.compile(rf'[{charclass}]+')


def extract_pdf_text(pdf_path: Path) -> str:
    """Extract raw text from the entire PDF using pdfminer.six."""
    return extract_text(str(pdf_path))


def main() -> None:
    if not PDF_PATH.exists():
        raise FileNotFoundError(f"Cannot find {PDF_PATH!s}")

    pattern = build_regex(UNICODE_RANGES)

    print(f"Using regex: {pattern.pattern}")
    print(f"Extracting {WRITING_SYSTEM_NAME} words from {PDF_PATH.name} …")

    raw_text = extract_pdf_text(PDF_PATH)

    matches = pattern.findall(raw_text)

    # Remove exact duplicates while preserving order (optional)
    # matches = list(dict.fromkeys(matches))

    with OUTPUT_PATH.open("w", encoding="utf‑8") as fout:
        fout.write("\n".join(matches))

    print(f"✅ Wrote {len(matches):,} {WRITING_SYSTEM_NAME} words → {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
