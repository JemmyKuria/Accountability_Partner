"""
cv_utils.py
-----------
CV parsing, keyword extraction, and match scoring.
Pure functions only — no Streamlit, no Supabase.
"""

import io
import re

import PyPDF2
import docx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


KNOWN_SKILLS = [
    "power bi", "python", "pandas", "scikit-learn", "sklearn", "nltk", "sql",
    "mysql", "postgresql", "etl", "streamlit", "php", "mern", "react", "node",
    "mongodb", "express", "data analysis", "data science", "machine learning",
    "data visualization", "dashboard", "cloud", "aws", "azure", "gcp",
    "cyber security", "cybersecurity", "network security", "excel", "tableau",
    "r programming", "statistics", "nlp", "deep learning", "data engineering",
    "business intelligence", "data modeling", "data warehousing", "reporting",
    "kpi", "javascript", "html", "css", "ui design", "ui/ux", "git", "github",
    "api", "rest api", "django", "flask", "power query", "dax", "vba",
]

STOPWORDS_EXTRA = {
    "experience", "years", "work", "worked", "working", "using", "including",
    "skills", "ability", "strong", "responsible", "responsibilities", "team",
    "various", "proficient", "knowledge",
}


def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    pages = []
    for page in reader.pages:
        try:
            pages.append(page.extract_text() or "")
        except Exception:
            continue
    return "\n".join(pages)


def extract_text_from_docx(file_bytes: bytes) -> str:
    document = docx.Document(io.BytesIO(file_bytes))
    return "\n".join(p.text for p in document.paragraphs)


def extract_cv_text(uploaded_file) -> str:
    name = uploaded_file.name.lower()
    file_bytes = uploaded_file.read()
    if name.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    if name.endswith(".docx"):
        return extract_text_from_docx(file_bytes)
    if name.endswith(".txt"):
        return file_bytes.decode("utf-8", errors="ignore")
    raise ValueError("Unsupported file type. Use PDF, DOCX, or TXT.")


def extract_keywords(cv_text: str, extra_terms: int = 8) -> list:
    """Known skills present in the CV, plus a few extra TF-IDF terms."""
    if not cv_text:
        return []
    text_lower = cv_text.lower()
    found_skills = [s for s in KNOWN_SKILLS if s in text_lower]

    try:
        vectorizer = TfidfVectorizer(stop_words="english", max_features=60, ngram_range=(1, 1))
        tfidf = vectorizer.fit_transform([cv_text])
        scores = tfidf.toarray()[0]
        terms = vectorizer.get_feature_names_out()
        ranked = sorted(zip(terms, scores), key=lambda x: x[1], reverse=True)
        tfidf_terms = [
            t for t, s in ranked
            if s > 0 and t not in STOPWORDS_EXTRA and len(t) > 2 and t not in found_skills
        ][:extra_terms]
    except ValueError:
        tfidf_terms = []

    merged = list(found_skills)
    for term in tfidf_terms:
        if term not in merged:
            merged.append(term)
    return merged


def score_matches(cv_text: str, jobs: list) -> list:
    """Attach `match_score` (0-100) to each job and return sorted desc."""
    if not jobs:
        return jobs
    documents = [cv_text] + [f"{j['title']} {j.get('snippet', '')}" for j in jobs]
    try:
        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf = vectorizer.fit_transform(documents)
        sims = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()
    except ValueError:
        sims = [0] * len(jobs)
    for job, score in zip(jobs, sims):
        job["match_score"] = round(float(score) * 100, 1)
    return sorted(jobs, key=lambda j: j["match_score"], reverse=True)