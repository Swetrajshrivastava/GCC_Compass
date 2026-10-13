"""Local evidence extraction and retrieval for the GCC Compass prototype."""

from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Any

import pandas as pd
from pypdf import PdfReader


STOP_WORDS = {
    "a", "about", "across", "an", "and", "are", "as", "at", "be", "been",
    "between", "by", "can", "do", "does", "for", "from", "give", "has",
    "have", "how", "i", "in", "india", "is", "it", "its", "me", "of",
    "on", "or", "our", "please", "should", "some", "than", "that", "the",
    "their", "them", "there", "this", "to", "us", "was", "we", "what",
    "when", "where", "which", "who", "why", "will",     "with", "would", "gcc", "gccs", "team", "teams",
}

SYNONYM_GROUPS = (
    {"cluster", "clusters", "hub", "hubs", "city", "cities", "location", "locations"},
    {"talent", "workforce", "employees", "people", "skills", "hiring", "recruitment"},
    {"incentive", "incentives", "policy", "policies", "scheme", "schemes", "support"},
    {"rent", "rents", "office", "offices", "lease", "leases", "property", "commercial"},
    {"count", "number", "size", "scale", "landscape", "market"},
    {"revenue", "income", "turnover"},
    {"provider", "providers", "partner", "partners", "vendor", "vendors"},
)


def normalize_terms(text: str) -> list[str]:
    terms = []
    for term in re.findall(r"[a-z0-9]+", text.casefold()):
        if term in STOP_WORDS or len(term) < 2:
            continue
        if term.endswith("ies") and len(term) > 4:
            term = term[:-3] + "y"
        elif term.endswith("s") and len(term) > 3 and not term.endswith("ss"):
            term = term[:-1]
        terms.append(term)
    return terms


def expand_query_terms(question: str) -> set[str]:
    terms = set(normalize_terms(question))
    expanded = set(terms)
    for group in SYNONYM_GROUPS:
        normalized_group = {term for word in group for term in normalize_terms(word)}
        if terms & normalized_group:
            expanded.update(normalized_group)
    return expanded


def _split_passages(text: str, max_words: int = 95) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+", " ".join(text.split()))
    passages: list[str] = []
    current: list[str] = []
    word_count = 0
    for sentence in sentences:
        words = sentence.split()
        if not words:
            continue
        if current and word_count + len(words) > max_words:
            passages.append(" ".join(current))
            current = []
            word_count = 0
        current.append(sentence)
        word_count += len(words)
    if current:
        passages.append(" ".join(current))
    return passages


def build_evidence_corpus(
    data_dir: Path,
    gccs: pd.DataFrame,
    cities: pd.DataFrame,
    providers: pd.DataFrame,
    sources: pd.DataFrame,
) -> list[dict[str, Any]]:
    """Build a searchable corpus from the bundled report and local records."""
    source_rows = {
        str(row["source_name"]): row
        for _, row in sources.iterrows()
    }
    corpus: list[dict[str, Any]] = []
    government_source = source_rows.get("Government of India GCC report 2025")
    document_path = data_dir / "documents" / "government-india-gcc-report-2025.pdf"
    if document_path.exists():
        reader = PdfReader(str(document_path), strict=False)
        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            for passage in _split_passages(text):
                corpus.append({
                    "document": "From Policy to Prosperity: GCCs Leading India’s Growth Journey",
                    "passage": passage,
                    "citation": f"Government of India report, p. {page_number}",
                    "status": government_source["status"] if government_source is not None else "Needs review",
                    "url": government_source["url"] if government_source is not None else "",
                    "kind": "report",
                })
    else:
        raise FileNotFoundError(f"Evidence report not found: {document_path}")

    for _, row in gccs.iterrows():
        url = row.get("source_url", "")
        if not isinstance(url, str) or not url.startswith(("https://", "http://")):
            continue
        company = str(row["company"])
        corpus.append({
            "document": f"GCC directory: {company}",
            "passage": (
                f"{company} is a GCC research lead in {row['sector']}, {row['city']}. "
                f"Recorded signal: {row['signal']}. The record is marked "
                f"{row['evidence_status']}; it is not independently verified by this dataset."
            ),
            "citation": "GCC directory record",
            "status": row["evidence_status"],
            "url": url,
            "kind": "record",
        })

    for _, row in cities.iterrows():
        url = row.get("source_url", "")
        if not isinstance(url, str) or not url.startswith(("https://", "http://")):
            url = ""
        corpus.append({
            "document": f"City profile: {row['city']}",
            "passage": (
                f"{row['city']}: talent signal {row['talent_signal']}; office cost signal "
                f"{row['office_cost_signal']}; ecosystem depth {row['ecosystem_depth']}. "
                f"{row['fit_notes']} {row['policy_or_validation_note']} "
                "These prototype fields are qualitative, not audited benchmarks."
            ),
            "citation": "City profiles dataset; qualitative prototype signal",
            "status": "Not assessed" if str(row["talent_signal"]) == "Not assessed" else "Needs review",
            "url": url,
            "kind": "record",
        })

    for _, row in providers.iterrows():
        url = row.get("source_url", "")
        if not isinstance(url, str) or not url.startswith(("https://", "http://")):
            continue
        corpus.append({
            "document": f"Provider profile: {row['provider']}",
            "passage": (
                f"{row['provider']} lists {row['service_line']} services with coverage "
                f"{row['coverage']}. {row['description']} The profile is marked "
                f"{row['evidence_status']}; this does not independently verify GCC delivery."
            ),
            "citation": "Provider directory record",
            "status": row["evidence_status"],
            "url": url,
            "kind": "record",
        })

    for _, row in sources.iterrows():
        url = row.get("url", "")
        if not isinstance(url, str) or not url.startswith(("https://", "http://")):
            continue
        corpus.append({
            "document": str(row["source_name"]),
            "passage": (
                f"Source catalogue entry about {row['topic']}. {row['notes']} "
                "This is a catalogue note, not an extracted passage from the linked source."
            ),
            "citation": "Evidence Desk catalogue note",
            "status": row["status"],
            "url": url,
            "kind": "catalogue",
        })
    return corpus


def retrieve_evidence(
    question: str,
    corpus: list[dict[str, Any]],
    limit: int = 5,
) -> list[dict[str, Any]]:
    """Rank relevant local passages with BM25-style lexical scoring."""
    query_terms = expand_query_terms(question)
    if not query_terms or not corpus:
        return []

    tokenized = [normalize_terms(item["passage"]) for item in corpus]
    document_count = len(corpus)
    average_length = sum(map(len, tokenized)) / document_count
    document_frequency = {
        term: sum(term in set(tokens) for tokens in tokenized)
        for term in query_terms
    }
    scored: list[tuple[float, dict[str, Any]]] = []
    for item, tokens in zip(corpus, tokenized):
        frequencies: dict[str, int] = {}
        for token in tokens:
            frequencies[token] = frequencies.get(token, 0) + 1
        score = 0.0
        for term in query_terms:
            frequency = frequencies.get(term, 0)
            if not frequency:
                continue
            idf = math.log(1 + (document_count - document_frequency[term] + 0.5)
                           / (document_frequency[term] + 0.5))
            length_norm = 1 - 0.75 + 0.75 * len(tokens) / max(average_length, 1)
            score += idf * frequency * 2.2 / (frequency + 1.2 * length_norm)
        if score > 0:
            scored.append((score, item))

    scored.sort(key=lambda result: result[0], reverse=True)
    results = []
    for score, item in scored[:limit]:
        result = dict(item)
        result["relevance"] = round(score, 3)
        results.append(result)
    return results
