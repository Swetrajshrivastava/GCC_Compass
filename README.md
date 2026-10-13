# GCC Compass — Flexiple Product Intern Assignment

A Streamlit prototype for an evidence-led India GCC intelligence workspace.

## Run locally (Windows / VS Code)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL shown in the terminal (usually http://localhost:8501).

## AI project context

Project-specific product, architecture, coding, design, and task context lives in [`ai-context-docs/`](ai-context-docs/). Read `Memory.md` and `Task.md` when resuming work; consult the PRD and architecture before changing product behavior.

## Flexiple assignment deck

The editable [GCC Compass Product Intern Assignment deck](GCC_Compass_Product_Intern_Assignment.pptx) presents the problem, prioritized opportunity, product wedge, stakeholder positioning, prototype boundaries, and a validation plan. It distinguishes sourced report facts from product hypotheses and prototype-only sample data.

To regenerate it, install `requirements-deck.txt` in the project environment and run `python tools/build_assignment_deck.py`.

## Included product flows
- Overview dashboard
- Search/filter GCC directory
- Compare city profiles
- Location Decision Engine with adjustable normalized priorities, transparent completeness-aware ranking, and downloadable PDF decision reports
- Browse service provider categories
- Evidence desk with source status
- Local evidence retrieval with report-page citations, CSV record citations, and bounded arithmetic (no LLM/API)

## Important data integrity note
This is an assignment prototype, not a production data source. Company entries marked **Needs review** are research leads, and official company homepages do not by themselves verify a GCC or its location. Provider records include self-published service descriptions and illustrative profiles; none establish independently verified GCC delivery or performance. The city profiles include qualitative signals and candidates marked **Not assessed**. The Location Decision Engine applies illustrative ordinal mappings (with higher office-cost levels scoring lower) and shows only an indicative decision-support score; it is not an audited city benchmark. Its PDF export uses the current selected weights/ranking and preserves missing-data and evidence caveats. Do not claim comprehensive coverage or verified provider performance. The Research Assistant extracts and ranks local report/CSV passages and cites them, but does not use an LLM, call an API, or generate a synthesis. Explain these limits in the demo.

## Suggested 3-minute demo
1. Open Overview and frame the problem.
2. Search the GCC Directory by sector/city.
3. Compare Bengaluru, Hyderabad and Pune, then try the Location Decision Engine with talent-first and cost-first weights.
4. Open Provider Finder and explain the evidence standard.
5. Open Evidence Desk and show provenance / uncertainty.
6. Ask the Research Assistant a location or market-count question and open the cited source page.
7. Close with the product thesis: decisions backed by traceable evidence, not another generic chatbot.

## Before submission
- Verify every named company/city claim and update the source URL / status.
- Validate provider references and delivery independently; the linked provider pages establish only what the providers publicly describe about their services.
- Verify every company GCC/city claim and assess the additional city candidates before presenting them as comparable options.
- Test the app from a fresh virtual environment.
- Deploy to Streamlit Community Cloud or another host if a public link is required. Do not send a localhost URL to reviewers.
