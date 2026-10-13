# GCC Compass coding and product rules

## Preserve product trust

- Treat the bundled data as a prototype dataset, not a comprehensive market census.
- Preserve the distinction between **Verified**, **Needs review**, and **Illustrative**. Never silently promote a record's status.
- Illustrative provider records are fictional examples; do not present them as real providers or evidence of delivery.
- Treat company presence and expansion entries marked Needs review as research leads, not confirmed claims.
- State dates, definitions, and source limitations when quoting market counts or policy information.
- City cost, talent, and ecosystem fields are qualitative signals, not audited or directly comparable benchmarks.
- The Location Decision Engine uses illustrative ordinal mappings only: talent and ecosystem are higher-is-better; office-cost level is lower-is-better. Do not present its weighted score as a verified benchmark.
- Exclude missing, "Not assessed", and unknown city labels from scoring. Renormalize weights over assessed criteria, show completeness, and withhold ranking where fewer than two of three criteria are assessed.
- Generate decision reports only from the currently computed weights and city results. Preserve the unranked/missing-data explanations, source URLs, and scoring limitations; never turn an indicative score into a definitive recommendation.
- A source record is not proof by itself. Check that the linked source supports the specific claim before changing its status.

## Make focused changes

- Read the relevant context docs and inspect the code/data before changing behavior.
- Prefer small changes that fit the existing single-file Streamlit and CSV-backed prototype.
- Do not introduce features, providers, facts, or product scope that were not requested.
- Do not restructure working code or add dependencies without a concrete need.
- Preserve existing UI behavior unless the task explicitly calls for a behavior change.

## Data, research, and assistant

- Keep CSV column names and consumers aligned; update both together if a schema change is necessary.
- Validate external or user-supplied values before using them in file paths, URLs, or queries.
- Surface source links, evidence status, and freshness where available.
- Do not invent citations, data, provider references, policy eligibility, or benchmark values.
- Do not describe the deterministic Research Assistant as an LLM, agent, or RAG implementation.
- Describe the Research Assistant as local retrieval and arithmetic, not an LLM or generated-answer system.
- Show report title, page number, evidence status, and source link for retrieved excerpts; label source-catalogue notes as summaries, not quotes from linked sources.
- If no relevant passage is found, say so; never turn related links into unsupported answers.
- If assistant behavior changes, disclose what data and logic actually power the answer; never imply unsupported verification.

## Streamlit and UI

- Follow `design.md` and `.streamlit/config.toml`; favor native Streamlit controls and components.
- Check the installed runtime and declared dependency floor before using APIs that may not exist in all supported versions.
- Retain or remove existing custom CSS only as part of a scoped UI change; avoid brittle selectors for new styling.
- Keep interactive labels clear and warnings readable without relying on color alone.
- Check empty search results, missing source URLs, and unselected city states when changing a workflow.

## Security and errors

- Never hardcode credentials, tokens, or private information. Use Streamlit secrets or environment configuration for future integrations.
- Do not silently swallow errors or disguise invalid/missing data as success.
- Show actionable user-facing messages for expected input or data problems without exposing secrets or stack traces.
- Do not disable validation or security controls to make a demo appear to work.

## Verification

- Run a syntax check and the smallest relevant tests after Python changes.
- For UI behavior changes, launch the app and exercise the affected workflow where practical.
- Verify the exact changed behavior and preserve unrelated behavior.
- Do not claim the app or its data is verified beyond the checks actually performed.
