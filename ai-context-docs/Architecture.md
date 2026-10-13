# Architecture

## System overview

GCC Compass is a single-process Streamlit prototype. Its entry point reads four local CSV files, renders a sidebar radio navigation, and displays the selected research workflow. There is no separate API server, database, authentication layer, or external AI integration.

## Technology

| Layer | Current implementation | Purpose |
|---|---|---|
| UI and application | Python, Streamlit (`app.py`) | Render the workspace and handle interactions |
| Data manipulation | pandas | Read, filter, and display CSV records |
| PDF export | ReportLab | Generate the location decision report in memory |
| Data storage | CSV files under `data/` | Local prototype records and source metadata |
| Theme | `.streamlit/config.toml` plus existing inline CSS | Set Streamlit theme and prototype-specific visual treatment |
| Deployment | Not configured in the repository | A hosted deployment is a separate future step |
| Testing | Standard-library `unittest` modules under `tests/` | Focused retrieval and decision-scoring coverage |

Dependency ranges are specified in `requirements.txt`; do not assume the local runtime and minimum supported Streamlit version are identical.

## Application structure

```text
gcc_compass/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/
│   └── config.toml
├── data/
│   ├── gcc_directory.csv
│   ├── city_profiles.csv
│   ├── service_providers.csv
│   └── sources.csv
└── ai-context-docs/
    ├── README.md
    ├── PRD.md
    ├── Architecture.md
    ├── Rules.md
    ├── design.md
    ├── Task.md
    └── Memory.md
```

## Runtime and data flow

1. `app.py` sets page metadata and resolves the `data/` directory relative to its own location.
2. A cached `load_csv(name)` helper reads each of the four bundled datasets with pandas.
3. Sidebar radio selection chooses one of seven view branches.
4. Search and filter controls operate on the in-memory DataFrames; tables and text render the results.
5. Source URL columns or buttons link users to external evidence where a URL is supplied.

The Research Assistant extracts page text from the bundled Government of India GCC report with `pypdf`, indexes report passages and local CSV records in memory, and ranks them with a small BM25-style lexical retriever with hand-authored query synonyms. Results display source status, page/record citation, and a URL where available. It also retains bounded arithmetic over user-supplied values. It does not call an external API or local model, generate an answer, or independently verify linked claims. If no passages match, it says so and offers general source links separately.

## Data files and key fields

| File | Role | Key fields |
|---|---|---|
| `data/gcc_directory.csv` | GCC/company research leads | `company`, `sector`, `city`, `signal`, `evidence_status`, `source_url` |
| `data/city_profiles.csv` | Qualitative location-comparison signals | `city`, `talent_signal`, `office_cost_signal`, `ecosystem_depth`, `fit_notes`, `policy_or_validation_note`, `source_url` |
| `data/service_providers.csv` | Provider discovery examples | `provider`, `service_line`, `coverage`, `description`, `evidence_status`, `last_checked`, `source_url` |
| `data/sources.csv` | Source catalogue and status notes | `source_name`, `topic`, `source_type`, `notes`, `status`, `url` |

The datasets include a mix of research leads, sources needing review, and explicitly illustrative sample records. A source catalogue entry does not automatically validate every claim associated with that topic.

## Current product views

- **Overview:** sample counts, user decision framing, and recent company signals.
- **GCC Directory:** text search plus sector and city filters.
- **Compare Cities:** a user-selected comparison of up to four profiles.
- **Location Decision Engine:** `location_scoring.py` maps qualitative city signals to disclosed 1–5 ordinal scores, reverses office-cost direction, normalizes user weights, computes a score from assessed criteria only, and withholds ranks for profiles with fewer than two assessed criteria.
- **Decision report:** `decision_report.py` builds an in-memory landscape PDF from the current ranking and weights; it includes a summary, normalized priorities, scored/unranked city table, source URLs, rationale, and methodology caveats.
- **Provider Finder:** provider text search and service-line filter.
- **Evidence Desk:** source records filtered by status and a short evidence-status guide.
- **AI Research Assistant:** local lexical retrieval for market, location, and provider queries; guarded arithmetic; citation-linked passages; and an explicit no-evidence fallback.
- **Evidence retrieval:** `research.py` builds a local in-memory index from `data/documents/government-india-gcc-report-2025.pdf` and the structured CSV records. Report citations include PDF page numbers; catalogue notes are labeled as summaries, not source passages.

## State, API, and persistence

- Streamlit widgets provide the current interaction state.
- There is no explicit application database or external API client.
- Filter changes rerun the Streamlit script; CSV loads use `st.cache_data`.
- Decision PDFs are generated from the current in-memory results and offered as a download; no report files are written to disk.
- No user accounts or role-based access controls are implemented.
- `.streamlit/secrets.toml` is excluded by `.gitignore`; never put credentials in tracked configuration or CSV data.

## Extension guidance

- Keep the prototype's local CSV contract intact unless a migration is explicitly scoped.
- If adding a database or external source ingestion, document schema, provenance, refresh behavior, and failure handling before implementation.
- If adding retrieval or an LLM, require source-level citations and visible uncertainty, externalize credentials, and disclose model limitations.
- Add documents only with their original source URL, publication date, evidence status, and page-aware citations; test extraction quality before indexing. The 2026 Zinnov PDF remains a catalogue link because its bundled text extraction was not legible enough for reliable retrieval.
- Split `app.py` into modules only when the change warrants it; do not restructure it just to match a generic template.
