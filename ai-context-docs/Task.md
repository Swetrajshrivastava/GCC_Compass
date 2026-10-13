# Task board

## Current milestone

**Milestone:** Evidence-led prototype and assignment handoff

## Current objective

Keep the prototype's research flows understandable, make evidence limits explicit, and validate the location decision workflow.

## Priorities

1. Ensure every factual record and market claim has an appropriate, traceable source.
2. Replace illustrative provider examples before using the directory for real vendor discovery.
3. Keep evidence status, dates, and dataset limitations visible as coverage expands.

## Next

- [ ] Review the cited market-count claim, its reporting period, unit definitions, and source URL before using it in a reviewer-facing demo.
- [ ] Verify company presence and expansion signals against sources that support each specific claim.
- [ ] Check city policy links and validate policy details against current official documents.
- [ ] Validate provider references and delivery independently; public service pages alone do not prove GCC delivery.
- [ ] Assess the new candidate-city rows with comparable, source-backed evidence before using them in a location ranking.

## In progress

- None

## Completed

- [x] Create project-specific AI context docs from the reusable context-kit structure.
- [x] Build the initial six-view Streamlit prototype and CSV-backed research workflows.
- [x] Expand each CSV while staying below 50 rows per file; add company research leads, provider discovery profiles, unassessed city candidates, and source records with verification limits stated.
- [x] Run through all six existing UI workflows, including a directory search and a submitted research question.
- [x] Improve assistant handling for indirect questions, common safe calculations, and unknown-answer references.
- [x] Verify indirect market/location prompts, percentage/split/monthly arithmetic, unknown-question references, and unverified office-rent handling in the running app.
- [x] Add local report/record retrieval with page-level citations, visible evidence status, and an explicit no-LLM/no-API disclosure.
- [x] Add focused retrieval tests for indirect questions, an unsupported claim, citations, and query synonyms.
- [x] Compile the app and retrieval code and run the focused retrieval tests.
- [x] Verify the updated assistant in-browser with a cited hub question, a calculation, and an unsupported question.
- [x] Create an editable 10-slide Flexiple assignment deck with source links and explicit evidence limits.
- [x] Add a transparent Location Decision Engine using normalized user priorities and completeness-aware city rankings.
- [x] Add unit tests for score direction, weight normalization, missing/unknown signals, ranking behavior, and insufficient data.
- [x] Add a downloadable in-memory PDF decision report generated from current weights and rankings, with rationale, sources, and caveats.
- [x] Test report content for changed weights/rankings, source URLs, unranked records, and missing-data limitations.

## Blocked

- None

## Backlog

- [ ] Expand the local evidence corpus with quality-checked documents and page-level citation metadata.
- [ ] Add focused tests for CSV schemas and search/filter behavior.
- [ ] Decide on user-contributed data, source refresh, and correction workflows.
- [ ] Decide first customer segment, access model, and monetization.

## Notes

The current dataset remains intentionally small and includes research leads, self-described provider services, and city candidates with no assessed signals. Do not infer verified coverage from the record count shown in the app.
