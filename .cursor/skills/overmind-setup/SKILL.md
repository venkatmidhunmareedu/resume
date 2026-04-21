---
name: overmind-setup
description: Sets up the Overmind LaTeX resume project for local development and preview. Use when the user asks to setup, install dependencies, configure LaTeX tooling, or get the resume build working.
---

# Overmind Setup Guide

## When to use

Apply this skill when the user asks to:
- setup this repository
- install prerequisites
- configure LaTeX tooling
- make resume build/preview work locally

## Setup workflow

1. Confirm you are in the project root.
2. Ensure the LaTeX Workshop extension is installed in Cursor/VS Code:
   - Marketplace: <https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop>
3. Install OS-specific prerequisites:
   - **Linux**:
     - `sudo apt install texlive-latex-base texlive-fonts-recommended latexmk`
   - **Windows**:
     - Install Perl from <https://strawberryperl.com/>
     - Open MikTeX Package Manager and install `latexmk` if missing.
   - **macOS**:
     - If needed, open TeX Live Utility and install `latexmk`.
     - Terminal alternative: `sudo tlmgr install latexmk`
4. Build the resume:
   - Command palette: `LaTex Workshop: Build LaTex Project`
   - Or keyboard shortcut: `Ctrl + Shift + B`
5. Verify output:
   - Confirm `resume.pdf` is generated/updated.
   - Ask the user to open and review the PDF.

## Agent behavior

- If the user asks for setup, execute the relevant shell commands directly when possible.
- If a step requires GUI interaction (extension install, command palette action), instruct the user with concise steps.
- Keep setup guidance focused on this repo and avoid unrelated tooling.
