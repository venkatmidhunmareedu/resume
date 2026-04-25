"""Resume and job description parsing utilities."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def extract_text_from_pdf(pdf_path: str | Path) -> str:
    """Extract plain text from a PDF file using pdfplumber."""
    try:
        import pdfplumber
    except ImportError:
        sys.exit("pdfplumber is not installed. Run: uv add pdfplumber")

    path = Path(pdf_path)
    if not path.exists():
        sys.exit(f"File not found: {path}")

    lines: list[str] = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text(x_tolerance=2, y_tolerance=3)
            if text:
                lines.append(text)

    return "\n".join(lines)


def read_text_file(file_path: str | Path) -> str:
    """Read plain text from a .txt file."""
    path = Path(file_path)
    if not path.exists():
        sys.exit(f"File not found: {path}")
    return path.read_text(encoding="utf-8")


def load_document(source: str | Path) -> str:
    """Load a document from a PDF or text file path."""
    path = Path(source)
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return extract_text_from_pdf(path)
    elif suffix in {".txt", ".md", ""}:
        return read_text_file(path)
    else:
        sys.exit(f"Unsupported file type: {suffix}. Use .pdf or .txt")


def clean_text(text: str) -> str:
    """Normalize whitespace and remove non-ASCII noise."""
    text = re.sub(r"[^\x00-\x7F]+", " ", text)   # strip non-ASCII (bullets etc.)
    text = re.sub(r"[ \t]+", " ", text)            # collapse horizontal whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)         # collapse excessive blank lines
    return text.strip()
