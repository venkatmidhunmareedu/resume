---
name: overmind-tune
description: Tunes a resume for a target job description to maximize ATS match score using keyword alignment, standard section headers, and parser-safe structure. Use when the user asks to tailor a resume, optimize ATS score, align to a job posting, or improve resume keyword match.
---

# Overmind Resume Tuning

## When to use

Apply this skill when the user asks to:
- tune or tailor a resume to a specific job description
- improve ATS score or keyword match
- optimize section structure and parser compatibility

---

## ATS-first rules (2026)

1. Use exact keyword phrasing from the job description.
2. Apply the Rule of Three for critical skills:
   - once in `Professional Summary`
   - once in `Skills`
   - once in `Professional Experience`
3. Keep semantic context: pair keywords with measurable outcomes.
4. Use standard section names only:
   - `Professional Summary`
   - `Skills`
   - `Professional Experience`
   - `Education`
5. Keep a single-column, text-first layout with no icons, tables, or graphics.
6. Prefer reverse-chronological ordering for work history.
7. Use consistent date formatting: `MM/YYYY`.

---

## Workflow

### Step 0 — Resolve paths and set up versioning

Before anything else, establish the working paths:

```
REPO_ROOT       = /home/midhun/Documents/Github/Resume
TEX_FILE        = $REPO_ROOT/resume.tex
PDF_FILE        = $REPO_ROOT/resume.pdf
ATS_SCORER      = $REPO_ROOT/ats-service/main.py
VERSIONS_DIR    = $REPO_ROOT/versions
```

Find the next version number by listing `$VERSIONS_DIR` for existing `v*` folders:

```bash
ls $VERSIONS_DIR 2>/dev/null | grep -E '^v[0-9]+$' | sort -V | tail -1
```

If none exist, start at `v1`. Otherwise increment by 1. Call this `$VN`.

### Step 1 — Baseline score

Get the current ATS score before any edits:

```bash
cd $REPO_ROOT/ats-service
uv run python main.py --resume ../resume.pdf --jd "<job description>"
```

Record this as `BASELINE_SCORE`. Print it to the user.

### Step 2 — Extract target signals from the job description

Build a prioritized list:
- Required skills/technologies
- Preferred skills
- Role verbs (build, design, lead, optimize, automate)
- Domain terms (platform, security, cloud, data, etc.)

Keep top 10–15 high-value keywords for the resume.

### Step 3 — Build keyword map

Create a mapping from each target keyword to at least one resume location:
- Summary
- Skills
- Experience bullet

For top-priority skills, enforce Rule of Three coverage.

### Step 4 — Rewrite `resume.tex` in ATS-safe order

Section order:
1. Contact
2. Professional Summary
3. Skills
4. Professional Experience
5. Education
6. Projects (optional)

For each bullet:
- start with a strong action verb
- include exact job keyword where natural
- add quantified impact (`%`, `$`, time saved, scale, throughput, users)
- keep one achievement per bullet

**CRITICAL — accuracy rules:**
- Do not invent employers, dates, or achievements
- If data is missing, keep placeholders explicitly marked as `[REPLACE]`
- Keep language concise and achievement-first

### Step 5 — Compile and score the new version

After editing `resume.tex`, compile to PDF:

```bash
cd $REPO_ROOT
pdflatex -interaction=nonstopmode resume.tex
```

Then score the new PDF:

```bash
cd $REPO_ROOT/ats-service
uv run python main.py --resume ../resume.pdf --jd "<job description>"
```

Record this as `NEW_SCORE`.

### Step 6 — Save version snapshot

If `NEW_SCORE > BASELINE_SCORE`, save the version:

```bash
mkdir -p $VERSIONS_DIR/$VN
cp $TEX_FILE $VERSIONS_DIR/$VN/resume.tex
cp $PDF_FILE $VERSIONS_DIR/$VN/resume.pdf
echo "$NEW_SCORE" > $VERSIONS_DIR/$VN/score.txt
echo "<one-line summary of changes>" > $VERSIONS_DIR/$VN/notes.txt
```

Tell the user:
- Version saved: `versions/$VN/`
- Score delta: `BASELINE_SCORE → NEW_SCORE`

### Step 7 — Iterate if score target not met

If `NEW_SCORE < 75%` and fewer than 3 iterations have been done:
- Update `BASELINE_SCORE = NEW_SCORE`
- Increment `$VN`
- Go back to Step 2, focusing on the highest-value missing keywords

Stop iterating when:
- Score ≥ 75%, OR
- 3 iterations completed, OR
- No further meaningful keywords remain to add

Report the final best version folder and score to the user.

---

## Version folder structure

```
versions/
  v1/
    resume.tex      ← LaTeX source for this version
    resume.pdf      ← Compiled PDF for this version
    score.txt       ← ATS score (e.g. "68.4%")
    notes.txt       ← One-line summary of what changed
  v2/
    ...
```

---

## Output style

- Preserve factual accuracy; never invent employers, dates, or achievements
- If data is missing, keep placeholders explicitly marked as `[REPLACE]`
- Keep language concise and achievement-first
- Report the final score and version path at the end

---

## Example tuning pattern

Input keyword: `Project Management`

Apply in three locations:
1. Summary: `Software engineer with project management experience...`
2. Skills: `Project Management`
3. Experience: `Led project management for cross-team release planning, reducing delays by 25%.`
