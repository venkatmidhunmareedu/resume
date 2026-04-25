"""
ATS scoring engine.

Technique breakdown — mirrors how real ATS platforms work:

  1. TF-IDF Cosine Similarity  (weight: 55%)
     Industry-standard baseline. Vectorises both documents with term
     frequency–inverse document frequency, then measures the cosine angle
     between the two vectors.  Catches every keyword overlap while
     down-weighting filler words automatically.

  2. Keyword / Hard-skill Match  (weight: 30%)
     Extracts meaningful unigrams and bigrams (after stop-word removal and
     lemmatisation) from the JD and counts how many appear verbatim in the
     resume.  This mirrors the exact-match keyword gate most ATS parsers
     run before semantic scoring.

  3. Bigram Phrase Match  (weight: 15%)
     ATS systems specifically flag multi-word skills and titles
     ("machine learning", "product manager", "continuous integration").
     We extract JD bigrams and measure their presence in the resume.
"""

from __future__ import annotations

import re
import string
from dataclasses import dataclass

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ---------------------------------------------------------------------------
# NLTK bootstrap – download data silently if missing
# ---------------------------------------------------------------------------

def _ensure_nltk_data() -> None:
    required = [
        ("tokenizers/punkt_tab", "punkt_tab"),
        ("corpora/stopwords", "stopwords"),
        ("corpora/wordnet", "wordnet"),
        ("taggers/averaged_perceptron_tagger_eng", "averaged_perceptron_tagger_eng"),
    ]
    for resource_path, package in required:
        try:
            nltk.data.find(resource_path)
        except LookupError:
            nltk.download(package, quiet=True)


# ---------------------------------------------------------------------------
# Text pre-processing
# ---------------------------------------------------------------------------

_STOP_WORDS: set[str] | None = None
_LEMMATIZER: WordNetLemmatizer | None = None


def _get_nlp_tools() -> tuple[set[str], WordNetLemmatizer]:
    global _STOP_WORDS, _LEMMATIZER
    if _STOP_WORDS is None:
        _ensure_nltk_data()
        _STOP_WORDS = set(stopwords.words("english"))
        _LEMMATIZER = WordNetLemmatizer()
    return _STOP_WORDS, _LEMMATIZER  # type: ignore[return-value]


def _tokenize(text: str) -> list[str]:
    """Lowercase, remove punctuation, tokenize."""
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return nltk.word_tokenize(text)


def _preprocess(text: str) -> list[str]:
    """Return lemmatized, stop-word-filtered tokens."""
    stop_words, lemmatizer = _get_nlp_tools()
    tokens = _tokenize(text)
    return [
        lemmatizer.lemmatize(t)
        for t in tokens
        if t.isalpha() and t not in stop_words and len(t) > 1
    ]


def _bigrams(tokens: list[str]) -> set[str]:
    return {f"{tokens[i]} {tokens[i + 1]}" for i in range(len(tokens) - 1)}


# ---------------------------------------------------------------------------
# Individual scoring components
# ---------------------------------------------------------------------------

def _tfidf_cosine(resume_text: str, jd_text: str) -> float:
    """TF-IDF cosine similarity between resume and JD (0–1)."""
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        stop_words="english",
        sublinear_tf=True,       # log-scaled TF, standard ATS practice
        min_df=1,
    )
    tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
    score: float = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(float(score), 4)


def _keyword_match(resume_tokens: list[str], jd_tokens: list[str]) -> tuple[float, list[str], list[str]]:
    """
    Jaccard-style keyword match: proportion of JD keywords present in the resume.
    Returns (score, matched_keywords, missing_keywords).
    """
    jd_set = set(jd_tokens)
    resume_set = set(resume_tokens)

    matched = sorted(jd_set & resume_set)
    missing = sorted(jd_set - resume_set)

    score = len(matched) / len(jd_set) if jd_set else 0.0
    return round(score, 4), matched, missing


def _bigram_match(resume_tokens: list[str], jd_tokens: list[str]) -> tuple[float, list[str], list[str]]:
    """Proportion of JD bigrams present in the resume."""
    jd_bg = _bigrams(jd_tokens)
    resume_bg = _bigrams(resume_tokens)

    matched = sorted(jd_bg & resume_bg)
    missing = sorted(jd_bg - resume_bg)

    score = len(matched) / len(jd_bg) if jd_bg else 0.0
    return round(score, 4), matched, missing


# ---------------------------------------------------------------------------
# Public result type
# ---------------------------------------------------------------------------

@dataclass
class ATSResult:
    overall_score: float   # 0–100 weighted final score
    tfidf_score: float
    keyword_score: float
    bigram_score: float


_WEIGHTS = {"tfidf": 0.55, "keyword": 0.30, "bigram": 0.15}


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def score(resume_text: str, jd_text: str) -> ATSResult:
    """
    Compute ATS match score between a resume and a job description.

    Parameters
    ----------
    resume_text : str
        Plain-text content of the resume.
    jd_text : str
        Plain-text content of the job description.

    Returns
    -------
    ATSResult
        Dataclass containing the overall score and all sub-scores.
    """
    _ensure_nltk_data()

    resume_tokens = _preprocess(resume_text)
    jd_tokens = _preprocess(jd_text)

    tfidf = _tfidf_cosine(resume_text, jd_text)
    kw_score, _, _ = _keyword_match(resume_tokens, jd_tokens)
    bg_score, _, _ = _bigram_match(resume_tokens, jd_tokens)

    weighted = (
        _WEIGHTS["tfidf"] * tfidf
        + _WEIGHTS["keyword"] * kw_score
        + _WEIGHTS["bigram"] * bg_score
    )
    overall = round(weighted * 100, 1)

    return ATSResult(
        overall_score=overall,
        tfidf_score=round(tfidf * 100, 1),
        keyword_score=round(kw_score * 100, 1),
        bigram_score=round(bg_score * 100, 1),
    )
