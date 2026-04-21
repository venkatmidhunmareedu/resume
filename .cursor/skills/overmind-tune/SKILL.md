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

## Workflow

### 1) Extract target signals from the job description

Build a prioritized list:
- Required skills/technologies
- Preferred skills
- Role verbs (build, design, lead, optimize, automate)
- Domain terms (platform, security, cloud, data, etc.)

Keep top 10-15 high-value keywords for the resume.

### 2) Build keyword map

Create a mapping from each target keyword to at least one resume location:
- Summary
- Skills
- Experience bullet

For top-priority skills, enforce Rule of Three coverage.

### 3) Rewrite sections in ATS-safe order

Order sections as:
1. Contact
2. Professional Summary
3. Skills
4. Professional Experience
5. Education
6. Projects (optional)

### 4) Optimize bullets for ATS and hiring signal

For each bullet:
- start with a strong action verb
- include exact job keyword where natural
- add quantified impact (`%`, `$`, time saved, scale, throughput, users)
- keep one achievement per bullet

### 5) Run final quality checks

- Headers are standard and exact
- No keyword stuffing
- Dates use `MM/YYYY`
- Single-column structure
- Skills list has 10-15 targeted keywords
- Most important requirements from top half of posting appear earlier in resume

## Output style

When returning tuned resume content:
- preserve factual accuracy; do not invent employers, dates, or achievements
- if data is missing, keep placeholders explicitly marked as `[REPLACE]`
- keep language concise and achievement-first

## Example tuning pattern

Input keyword: `Project Management`

Apply in three locations:
1. Summary: `Software engineer with project management experience...`
2. Skills: `Project Management`
3. Experience: `Led project management for cross-team release planning, reducing delays by 25%.`
