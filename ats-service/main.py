"""
ATS Match Scorer — outputs a single match percentage to stdout.

Usage:
  uv run python main.py --resume ../resume.pdf --jd "We are looking for..."
  uv run python main.py --resume ../resume.pdf --jd-file job.txt
  uv run python main.py --resume ../resume.pdf --show-text
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import typer

from parser import clean_text, load_document
from scorer import score

app = typer.Typer(add_completion=False)


@app.command()
def main(
    resume: Path = typer.Option(..., "--resume", "-r", help="Path to resume PDF or .txt"),
    jd: Optional[str] = typer.Option(None, "--jd", help="Job description as a string"),
    jd_file: Optional[Path] = typer.Option(None, "--jd-file", help="Path to JD .txt file"),
    show_text: bool = typer.Option(False, "--show-text", help="Print extracted resume text and exit"),
) -> None:
    resume_text = clean_text(load_document(resume))

    if not resume_text:
        print("error: could not extract text from resume", file=sys.stderr)
        raise typer.Exit(1)

    if show_text:
        print(resume_text)
        raise typer.Exit()

    if jd and jd_file:
        print("error: use --jd or --jd-file, not both", file=sys.stderr)
        raise typer.Exit(1)

    if jd_file:
        jd_text = clean_text(load_document(jd_file))
    elif jd:
        jd_text = clean_text(jd)
    else:
        print("error: provide --jd or --jd-file", file=sys.stderr)
        raise typer.Exit(1)

    result = score(resume_text, jd_text)
    print(f"{result.overall_score:.1f}%")


if __name__ == "__main__":
    app()
