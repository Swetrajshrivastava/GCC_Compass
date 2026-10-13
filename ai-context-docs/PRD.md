# Product requirements: GCC Compass

## Project name

GCC Compass

## One-line description

An evidence-led research workspace that helps companies understand India's Global Capability Centre (GCC) ecosystem before choosing where to enter and whom to work with.

## Problem

Companies entering India must make location, operating-model, and partner decisions using information spread across reports, government pages, company announcements, providers, and personal networks. Definitions and dates vary, public claims can be hard to compare, and there is no easy way to see what supports a claim or what remains uncertain.

The result is slow, referral-heavy research and a risk of treating marketing claims or stale information as facts. GCC Compass should make evidence discoverable and comparable while showing provenance and uncertainty; it should not present a prototype dataset as a definitive market census.

## Target users

- **Primary:** Global companies and internal strategy, site-selection, and GCC setup teams assessing an India entry or expansion.
- **Secondary:** Ecosystem service providers and advisors who want to understand market activity and demonstrate their experience with verifiable evidence.

## Product goals

- Make relevant GCC, location, provider, and source records easier to find in one workspace.
- Help users compare candidate cities against decision factors without pretending to provide a universal ranking.
- Make the source, freshness, and verification status of claims visible.
- Turn broad research questions into useful, source-grounded next steps.

## Non-goals for the prototype

- A complete or authoritative census of India's GCCs, providers, or market activity.
- Audited salary, rent, talent-supply, incentive-eligibility, or provider-performance benchmarks.
- Automated legal, tax, investment, or site-selection advice.
- A live web crawler, production database, multi-user workflow, vector-search service, or connected LLM.

## Opportunities and initial priority

1. **Evidence-backed discovery and comparison (highest):** helps a new entrant orient quickly and addresses the core information-asymmetry problem.
2. **Source and claim provenance:** builds trust by exposing what supports a record, when it was checked, and what still needs review.
3. **Provider due diligence:** valuable once provider identities, delivery evidence, and references can be independently verified.
4. **Live alerts, policy eligibility, talent and real-estate benchmarks:** potentially valuable, but require reliable, current, consistently defined data and are out of prototype scope.

## Core prototype features

| Feature | Description | Priority |
|---|---|---|
| Market overview | Show the size of the bundled sample and orient users to the main research decisions. | High |
| GCC directory | Search and filter company research leads by text, sector, and city; expose evidence status and source link. | High |
| City comparison | Compare qualitative city signals and surface the need to validate role-specific assumptions. | High |
| Location decision engine | Let users weight talent availability, office cost, and ecosystem maturity; show transparent ordinal scores, completeness, and ranked cities only when at least two criteria are assessed. | High |
| Decision report export | Download a PDF reflecting the current weights and ranking, with a summary, comparison, rationale, sources, unranked cities, and limitations. | High |
| Evidence desk | Browse source records and explain the meanings of Verified, Needs review, and Illustrative. | High |
| Provider finder | Filter sample provider profiles and make illustrative records unmistakable. | Medium |
| Research assistant | Retrieve relevant passages from bundled reports and records, cite page/record and source links, calculate supported arithmetic from user-supplied numbers, and state when no matching evidence is found; disclose that it is not an LLM. | Medium |

## Key user flows

### Assess a possible India location

1. A user opens the overview and chooses to compare locations.
2. The user sets relative importance for talent, office cost, and ecosystem maturity.
3. The prototype applies disclosed ordinal mappings, reverses the cost direction, and re-normalizes weights over assessed criteria only.
4. The user sees ranked cities only when at least two of three signals are assessed, checks completeness and source links, and treats the result as decision support rather than a market benchmark.
5. The user uses the Evidence Desk to inspect relevant source records.

### Research a company or provider

1. A user searches the directory or filters provider records by city, sector, or service line.
2. The app shows the matching prototype records and their evidence status.
3. The user opens the linked source where one exists and treats Needs review / Illustrative records accordingly.
4. The user records unresolved evidence needs before using the information in a decision.

### Ask a research question

1. A user submits a question to the Research Assistant.
2. The prototype ranks local report passages and CSV records using lexical matching and query synonyms, or calculates supported arithmetic from user-provided values.
3. The app presents citations and evidence status for matches, or says when no passage was found and separates general research references from evidence.

## Functional requirements

- The app shall offer overview, directory, city comparison, location decision engine, provider finder, evidence desk, and research assistant views.
- Directory and provider views shall support text search and their available categorical filters.
- The comparison view shall allow up to four selected cities and display the available qualitative fields.
- The Location Decision Engine shall normalize relative user weights to 100% and disclose its qualitative score mapping.
- Higher talent and ecosystem signals shall score better; higher office-cost signals shall score worse.
- Missing, "Not assessed", and unknown criterion labels shall be excluded from the weighted score rather than treated as zero.
- City score weights shall be re-normalized over that city's assessed criteria. Profiles with fewer than two of three criteria shall show Insufficient data and receive no rank.
- The engine shall show criterion-level scores, evidence completeness, fit notes, validation caveats, and a listed source link when available.
- The engine shall provide an in-memory PDF export generated from the currently selected weights and computed city ranking.
- The report shall include an executive summary, normalized priorities, scores, criterion values, evidence completeness, fit notes, source URLs, insufficient-data explanations, and scoring limitations.
- The report shall label scores as indicative ordinal decision support, not verified market benchmarks, and shall not make claims beyond the bundled data.
- Source URLs shall be rendered as links where available.
- Evidence statuses and the prototype's data limitations shall remain visible to users.
- Empty or missing data must not be described as verified evidence.
- The assistant shall disclose that it uses local lexical retrieval and bundled data, not a connected LLM or generative model.
- The assistant shall not invent answers to unsupported questions and shall show related source links with an explicit relevance limitation.
- The assistant may calculate supported arithmetic from values supplied by the user, and shall identify those values as user-provided rather than market benchmarks.
- Retrieved report excerpts shall include document title, page number, evidence status, and source URL; catalogue notes shall be clearly distinguished from extracted report text.

## Non-functional requirements

- **Data integrity:** Preserve source names, URLs, dates, and status labels; avoid strengthening claims beyond their evidence.
- **Performance:** Keep the small CSV-backed prototype responsive; retain caching for CSV loading.
- **Security:** Do not place credentials in source files or expose secrets in user-facing content.
- **Accessibility:** Keep controls labelled, content readable, and important warnings available as text rather than color alone.
- **Compatibility:** Follow the project's declared Streamlit dependency floor; verify APIs against the runtime before adopting newer features.

## Success criteria

- A reviewer can complete the core discovery, city-comparison, provider, and evidence flows.
- Sample and uncertain records are distinguishable from verified claims.
- The app's limitations are accurately disclosed in the UI and in demos.
- Research can be traced back to source records rather than relying on unsupported assertions.

## Open questions

- Which user segment should be served first: corporate GCC setup teams, ecosystem providers, or advisors?
- Which data domains can be maintained with sufficiently fresh and consistently defined evidence?
- What evidence threshold should qualify a provider record as verified delivery?
- What access, contribution, and monetization model best preserves trust?
