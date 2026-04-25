# ATS Match Scorer

Outputs a single match percentage to stdout — designed to be called by an AI agent.

## Output

```
74.3%
```

## Scoring Model

| Component | Weight | Technique |
|---|---|---|
| TF-IDF Cosine Similarity | 55% | Vectorises both documents, measures cosine angle — the ATS industry baseline |
| Keyword Match (Jaccard) | 30% | Exact keyword overlap after stop-word removal & lemmatisation |
| Bigram Phrase Match | 15% | Two-word skill phrase overlap ("machine learning", "ci/cd") |

## Usage

```bash
# JD as a string
uv run python main.py --resume ../resume.pdf --jd "We are looking for a Python engineer..."

# JD from a file
uv run python main.py --resume ../resume.pdf --jd-file job.txt

# Print extracted resume text
uv run python main.py --resume ../resume.pdf --show-text
```
