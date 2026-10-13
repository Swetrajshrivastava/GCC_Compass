# GCC Compass project memory

## Important project context

- This is a Streamlit prototype for a Flexiple Product Intern assignment about India's fragmented GCC ecosystem.
- The intended product thesis is an evidence-led workspace that makes scattered GCC ecosystem information easier to discover and compare.
- Product trust depends on showing provenance and uncertainty, not just displaying a larger dataset.
- The prototype is not a comprehensive GCC census or production-grade decision tool.

## Decisions

| Date | Decision | Rationale |
|---|---|---|
| 2026-10-11 | Adapt the AI Context Docs framework into project-specific docs rather than adding it as a runtime dependency. | The framework is documentation, and the project needs durable product/code context rather than new application behavior. |
| 2026-10-11 | Keep the current Streamlit and CSV-backed architecture while documenting future work separately. | The existing app is a focused assignment prototype; no request or evidence requires a rewrite. |
| 2026-10-11 | Treat source status and provenance as first-class product behavior. | Market counts, company leads, city claims, and provider claims can vary in definition, freshness, or verification. |
| 2026-10-11 | Keep dataset files below 50 rows each and prefer real links where available, but mark leads and self-reported claims as needing review. | The reviewer needs useful discovery examples without mistaking marketing pages or unassessed city candidates for independently verified evidence. |
| 2026-10-11 | Keep the Research Assistant deterministic, add bounded arithmetic and useful fallbacks, and label links as references rather than proof. | This improves indirect-question handling without pretending to have an LLM or verified answers unsupported by the small dataset. |
| 2026-10-11 | Add local extractive lexical retrieval and page/record citations; do not use Ollama, a local model, or an API. | Retrieval makes existing source material discoverable while respecting the no-model constraint and avoiding generated or unsupported synthesis. |
| 2026-10-11 | Add an indicative, completeness-aware Location Decision Engine over the existing qualitative city labels. | User-adjustable weights demonstrate decision support without inventing numeric market benchmarks; insufficient profiles remain unranked. |

## Current implementation state

- `app.py` loads CSV data with pandas and `st.cache_data`.
- The sidebar offers Overview, GCC Directory, Compare Cities, Provider Finder, Evidence Desk, and AI Research Assistant.
- Four local datasets live under `data/`.
- The assistant uses local BM25-style lexical retrieval over the bundled Government of India GCC report and local CSV records, with hand-authored query synonyms. It is extractive, not an LLM or answer-generating RAG pipeline; no API or local model is used.
- Theme values are in `.streamlit/config.toml`; the overview hero and metric surface use additional inline CSS.
- The datasets contain needs-review and illustrative content in addition to source catalogue entries.
- The current CSVs contain 12 company leads, 10 city profiles (four candidates have Not assessed signals), 11 provider examples (four illustrative and seven linked to provider-published service descriptions), and 18 source records.
- The new company leads link to official India pages, but their GCC scope and locations are explicitly unverified.
- The 2026 NASSCOM-Zinnov PDF URL in `sources.csv` and the Research Assistant was aligned to the publisher URL that returned HTTP 200 as `application/pdf`; the previous app URL returned HTML instead.
- Provider pages were reachable during the check; this confirms URL availability, not service quality or GCC client references.
- All six UI flows were exercised in the local browser; the directory search returned one match for Microsoft, city selection worked, and the assistant returned its deterministic city guidance.
- The Research Assistant handles indirect location/provider/market phrasing, percentage-of, even-split, monthly-average, and restricted arithmetic-expression questions. It does not use Python `eval`; calculations are constrained to numeric AST operations and bounded results.
- `research.py` extracts page text from `data/documents/government-india-gcc-report-2025.pdf`, creates record passages from local CSVs, and ranks matches using lexical BM25-style scoring. The UI identifies report pages, CSV record types, evidence status, and source URLs; catalogue notes are explicitly not presented as extracted source text.
- The 2026 NASSCOM-Zinnov PDF is not bundled or indexed because its text extraction was not reliably legible. Keep it as a catalogue reference only unless a reliable text source is found.
- `pypdf` is declared in `requirements.txt`. `tests/test_research.py` covers indirect location and count queries, unsupported claims, city-signal caveats, and synonym expansion; five focused tests and Python compilation passed.
- `location_scoring.py` maps qualitative city labels to an ordinal 1–5 scale (`Very high` 5, `High` 4, `Medium-high` 3.5, `Medium` 3, `Medium-low` 2.5, `Low` 2, `Very low` 1). Office cost reverses this direction. The UI slider values are normalized to 100%; a city's score re-normalizes over assessed criteria only. At least two of three criteria are required to rank. Missing, unknown and Not assessed labels remain excluded.
- With default 40/30/30 priorities, the assessed prototype cities order Bengaluru first, then Chennai, Hyderabad and Pune (tie broken alphabetically), Gurugram / NCR and Mumbai; the four candidate cities show Insufficient data. A cost-heavy 20/60/20 configuration moves Chennai and Pune above Bengaluru. These are illustrative scores from qualitative prototype labels, not verified benchmarks.
- `tests/test_location_scoring.py` tests direction, normalized weights, missing and unknown labels, insufficient-data handling, re-normalization, rank ordering, and tie stability. The full test suite contains 13 tests (8 scoring and 5 retrieval).
- The Location Decision Engine now offers a downloadable, in-memory PDF generated by `decision_report.py` and ReportLab. The report uses the current `ranked_cities` and slider weights, includes an executive summary, current normalized priorities, rank/score/criterion/completeness table, per-city fit and validation notes, available source URLs, unranked-city explanations, and ordinal-scoring limitations. `reportlab>=4.0` is in app `requirements.txt`.
- `tests/test_decision_report.py` confirms the PDF reflects altered weights and rank leaders, includes source URL/fit notes, and retains the missing-data and benchmark caveats. The full suite now contains 16 tests (3 report, 8 scoring, 5 retrieval). The real CSV export was also generated in memory under cost-heavy priorities and verified as a 3-page PDF with Chennai ranked first and unassessed cities unranked.
- The editable `GCC_Compass_Product_Intern_Assignment.pptx` is a 10-slide assignment deck. It frames customer pain and workarounds as hypotheses, prioritizes the entry-research wedge, explains the product and evidence rules, identifies the current prototype boundary, and ends with clickable sources and data caveats.
- `tools/build_assignment_deck.py` regenerates the deck; its build-only dependency is in `requirements-deck.txt`, separate from the Streamlit app's runtime requirements. Deck package validation confirmed ten slides, two clickable reference links, and no shapes outside slide bounds.
- Unanswered questions show matched Evidence Desk sources or a small baseline reference set. Numeric location requests also show relevant provider-published real-estate references while explicitly stating that they are not verified benchmarks.
- Tested examples included 15% of 200, 500 people split across four sites, 120 hires across 12 months, an indirect location trade-off, an indirect market-growth question, an unknown workweek question with baseline source links, and a future office-rent question with JLL/Cushman references.

## Known limitations and issues to validate

- The prototype's displayed market count and source metadata should be checked for correct period, definitions, and current availability before external use.
- Company records with Needs review status are research leads, not confirmation of the named signal.
- The four illustrative provider examples are not recommendations; self-published service pages and Needs review profiles do not prove GCC delivery or performance.
- City cost, talent, policy, and ecosystem fields are qualitative and not audited comparisons.
- No production database, source-refresh pipeline, or deployment configuration is documented in the app folder. Focused retrieval tests exist, but CSV-schema and UI tests do not.
- City comparison includes four additional candidate cities whose signal fields are deliberately Not assessed; do not interpret these rows as location recommendations.

## User preferences and constraints

- Prefer focused changes that preserve the current working prototype.
- Avoid adding dependencies without necessity.
- Keep prototype limitations honest in UI, demos, and written claims.
- Never add real credentials or secrets to tracked files.

## Useful commands

Run from the `gcc_compass` directory:

```powershell
streamlit run app.py
```

The root README also documents creating a virtual environment, installing `requirements.txt`, and running the app on Windows.

## Important references

- Reusable structure: [AI Context Docs](https://github.com/RahulMirji/vibe-coding-context-kit/tree/main/ai-context-docs)
- Product and demo notes: `../README.md`
- App entry point: `../app.py`
- Source inventory: `../data/sources.csv`

## Remember next session

Read this file and `Task.md` first. Review the assignment deck and obtain user feedback before submission. Check the current app and CSVs before acting on the documented assumptions. Resolve data verification tasks before presenting prototype records as established ecosystem facts.
