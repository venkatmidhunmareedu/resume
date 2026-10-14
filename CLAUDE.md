# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A single-file LaTeX resume ([resume.tex](resume.tex), Jake Gutierrez / sb2nov template) plus a small Python ATS scorer in [ats-service/](ats-service/). The compiled [resume.pdf](resume.pdf) is committed; LaTeX aux files (`*.aux`, `*.log`, `*.fls`, etc.) are gitignored.

## Commands

- Build PDF: `pdflatex -interaction=nonstopmode resume.tex` (or `latexmk -pdf resume.tex`). In VS Code, LaTeX Workshop builds on save.
- Linux deps: `sudo apt install texlive-latex-base texlive-fonts-recommended latexmk texlive-latex-extra`
- Score resume against a job description (run from `ats-service/`, uses `uv`):
  - `uv run python main.py --resume ../resume.pdf --jd "<text>"` or `--jd-file job.txt`
  - `uv run python main.py --resume ../resume.pdf --show-text` prints the text extracted from the PDF
  - Prints a single percentage (TF-IDF cosine 55%, keyword Jaccard 30%, bigram match 15%). Logic is in `scorer.py`; PDF text extraction in `parser.py`.
- `make cleanup-ignored` runs `git clean -fdX` (deletes all gitignored files).

No tests or linter.

## Tailoring workflow

[.cursor/skills/overmind-tune/SKILL.md](.cursor/skills/overmind-tune/SKILL.md) defines the resume-tuning procedure (baseline score → edit `resume.tex` → recompile → rescore, up to 3 iterations, target ≥75%, snapshots to `versions/vN/`). Key constraints from it:

- Keep the PDF ATS-parsable: single column, no icons/tables/graphics, standard section names (Professional Summary, Skills, Professional Experience, Education, optional Projects), `MM/YYYY` dates.
- Never invent employers, dates, or achievements; mark unknown data `[REPLACE]`.
- Its hardcoded `REPO_ROOT` uses `.../Resume` (capital R); the actual path is `.../resume`. `versions/` doesn't exist yet and is created on first save.
- [.cursor/skills/overmind-setup/SKILL.md](.cursor/skills/overmind-setup/SKILL.md) covers environment setup.

Always recompile `resume.pdf` after editing `resume.tex`, since the scorer reads the PDF, not the source.
