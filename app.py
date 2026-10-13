import ast
import math
import operator
import re

import streamlit as st
import pandas as pd
from pathlib import Path

from research import build_evidence_corpus, retrieve_evidence
from location_scoring import rank_cities, rounded_weight_percentages
from decision_report import generate_decision_report

st.set_page_config(page_title="GCC Compass", page_icon="🧭", layout="wide")
DATA = Path(__file__).parent / "data"

@st.cache_data
def load_csv(name):
    return pd.read_csv(DATA / name)


@st.cache_data
def load_evidence_index(gcc_records, city_records, provider_records, source_records):
    return build_evidence_corpus(
        DATA,
        gcc_records,
        city_records,
        provider_records,
        source_records,
    )


_MATH_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _evaluate_math_node(node):
    if isinstance(node, ast.Expression):
        return _evaluate_math_node(node.body)
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value
    if isinstance(node, ast.UnaryOp) and type(node.op) in _MATH_OPERATORS:
        return _MATH_OPERATORS[type(node.op)](_evaluate_math_node(node.operand))
    if isinstance(node, ast.BinOp) and type(node.op) in _MATH_OPERATORS:
        left = _evaluate_math_node(node.left)
        right = _evaluate_math_node(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 8:
            raise ValueError("Exponent is too large.")
        result = _MATH_OPERATORS[type(node.op)](left, right)
        if isinstance(result, complex) or not math.isfinite(result) or abs(result) > 1_000_000_000_000:
            raise ValueError("Calculation is outside the supported range.")
        return result
    raise ValueError("Unsupported calculation.")


def _valid_math_values(*values):
    return all(math.isfinite(value) and abs(value) <= 1_000_000_000_000 for value in values)


def calculate_question(question):
    text = question.lower().replace(",", "")
    percent = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:%|percent)\s+of\s+(\d+(?:\.\d+)?)",
        text,
    )
    if percent:
        rate, amount = map(float, percent.groups())
        result = amount * rate / 100
        if _valid_math_values(rate, amount, result):
            return f"{rate:g}% of {amount:g} = {result:,.2f}"
        return None

    split = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:employees?|people|hires|roles|sites|cities)?"
        r"\s+(?:be\s+)?(?:split|distributed|spread)\s+(?:evenly\s+)?"
        r"(?:across|between|among|into)\s+(\d+(?:\.\d+)?)",
        text,
    )
    if split:
        total, groups = map(float, split.groups())
        if groups:
            result = total / groups
            if _valid_math_values(total, groups, result):
                return f"{total:g} ÷ {groups:g} = {result:,.2f} per group"
            return None

    average = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:hires|employees|people|roles)?\s+"
        r"(?:over|across|in)\s+(\d+(?:\.\d+)?)\s+months?.*"
        r"(?:average|per month|monthly)",
        text,
    )
    if average:
        total, months = map(float, average.groups())
        if months:
            result = total / months
            if _valid_math_values(total, months, result):
                return f"{total:g} ÷ {months:g} = {result:,.2f} per month"
            return None

    expression = re.sub(
        r"^(?:please\s+)?(?:calculate|compute|work out|what is|what's)\s+",
        "",
        text.strip(),
    ).strip(" =?!.")
    expression = expression.replace("×", "*").replace("÷", "/")
    if len(expression) <= 100 and re.fullmatch(r"[\d\s.+\-*/()%]+", expression) and re.search(r"\d", expression):
        try:
            result = _evaluate_math_node(ast.parse(expression, mode="eval"))
        except (ArithmeticError, SyntaxError, TypeError, ValueError):
            return None
        return f"{expression} = {result:,.2f}"
    return None


gccs = load_csv("gcc_directory.csv")
cities = load_csv("city_profiles.csv")
providers = load_csv("service_providers.csv")
sources = load_csv("sources.csv")
evidence_corpus = load_evidence_index(gccs, cities, providers, sources)

st.markdown("""
<style>
.block-container {padding-top: 1.4rem; padding-bottom: 2rem; max-width: 1400px;}
.hero {padding: 1.4rem 1.6rem; border-radius: 18px; background: linear-gradient(115deg,#101c3a,#213c65); color:white; margin-bottom:1rem;}
.hero h1 {font-size:2.25rem; margin-bottom:.25rem;}
.hero p {color:#d9e4f6; margin-bottom:0;}
.small-muted {color:#68758b;font-size:.85rem}
div[data-testid="stMetric"] {background:#f7f9fc; border:1px solid #e5eaf2; padding:12px 14px; border-radius:12px;}
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("## 🧭 GCC Compass")
st.sidebar.caption("India GCC intelligence • Prototype")
page = st.sidebar.radio("Explore", ["Overview", "GCC Directory", "Compare Cities", "Location Decision Engine", "Provider Finder", "Evidence Desk", "AI Research Assistant"])
st.sidebar.divider()
st.sidebar.caption("Prototype dataset: illustrative records for workflow demonstration. Verify before making business decisions.")

if page == "Overview":
    st.markdown('<div class="hero"><h1>Know the market before you enter it.</h1><p>One evidence-led workspace for India’s Global Capability Centre ecosystem.</p></div>', unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Tracked GCC records", len(gccs), "Prototype dataset")
    c2.metric("City profiles", len(cities), "Decision factors")
    c3.metric("Service providers", len(providers), "Sample profiles")
    c4.metric("Source records", len(sources), "Evidence links")
    st.subheader("What decision are you making?")
    a,b,c = st.columns(3)
    with a:
        st.markdown("### 📍 Choose a location")
        st.write("Compare talent, operating-cost signals and policy evidence across major hubs.")
    with b:
        st.markdown("### 🏢 Map the ecosystem")
        st.write("Search companies, sectors, city presence and public expansion signals.")
    with c:
        st.markdown("### 🤝 Shortlist partners")
        st.write("Review provider focus areas and inspect what evidence supports each profile.")
    st.subheader("Recent signals to investigate")
    st.dataframe(gccs[["company","sector","city","signal","evidence_status"]].head(6), use_container_width=True, hide_index=True)
    st.info("Product principle: every important claim should link to a source, show a last-checked date and make uncertainty visible.")

elif page == "GCC Directory":
    st.title("GCC Directory")
    st.caption("Searchable starting point for company and expansion research.")
    q = st.text_input("Search company, sector, city or signal")
    sectors = ["All"] + sorted(gccs["sector"].dropna().unique().tolist())
    selected_sector = st.selectbox("Sector", sectors)
    cities_list = ["All"] + sorted(gccs["city"].dropna().unique().tolist())
    selected_city = st.selectbox("City", cities_list)
    view = gccs.copy()
    if q:
        mask = view.astype(str).apply(lambda col: col.str.contains(q, case=False, na=False)).any(axis=1)
        view = view[mask]
    if selected_sector != "All": view = view[view["sector"] == selected_sector]
    if selected_city != "All": view = view[view["city"] == selected_city]
    st.write(f"**{len(view)} records**")
    st.dataframe(view, use_container_width=True, hide_index=True, column_config={
        "source_url": st.column_config.LinkColumn("Source", display_text="Open evidence"),
        "evidence_status": st.column_config.TextColumn("Evidence status")
    })

elif page == "Compare Cities":
    st.title("Compare GCC locations")
    st.caption("Use the comparison as a discussion starter, not as a definitive ranking.")
    selected = st.multiselect("Choose up to 4 cities", cities["city"].tolist(), default=cities["city"].tolist()[:3], max_selections=4)
    subset = cities[cities.city.isin(selected)].set_index("city").T
    st.dataframe(subset, use_container_width=True)
    st.subheader("Decision framing")
    st.write("Weight each factor based on the role mix, hiring timeline, office strategy and policy eligibility of the specific GCC.")
    st.warning("Cost and talent values are qualitative signals in this prototype. Do not treat them as audited benchmarks.")

elif page == "Location Decision Engine":
    st.title("Location decision engine")
    st.caption("Explore how your priorities change a city shortlist. Scores are indicative decision-support signals, not verified market benchmarks.")

    talent_column, cost_column, ecosystem_column = st.columns(3)
    with talent_column:
        talent_weight = st.slider(
            "Talent availability importance",
            min_value=1,
            max_value=5,
            value=4,
            help="Higher values give assessed talent signals more influence.",
        )
    with cost_column:
        cost_weight = st.slider(
            "Office cost importance",
            min_value=1,
            max_value=5,
            value=3,
            help="Higher values give assessed office-cost signals more influence. Lower cost is more favorable.",
        )
    with ecosystem_column:
        ecosystem_weight = st.slider(
            "Ecosystem maturity importance",
            min_value=1,
            max_value=5,
            value=3,
            help="Higher values give assessed ecosystem-depth signals more influence.",
        )

    raw_weights = {
        "talent": talent_weight,
        "office_cost": cost_weight,
        "ecosystem": ecosystem_weight,
    }
    weight_percentages = rounded_weight_percentages(raw_weights)
    st.caption(
        "Normalized priorities: "
        f"Talent {weight_percentages['talent']}% · "
        f"Office cost {weight_percentages['office_cost']}% · "
        f"Ecosystem maturity {weight_percentages['ecosystem']}% "
        "(total 100%)."
    )
    st.info(
        "Method: qualitative labels map to an ordinal 1–5 scale "
        "(Very low 1, Low 2, Medium-low 2.5, Medium 3, Medium-high 3.5, "
        "High 4, Very high 5). Office cost is reversed: higher cost receives "
        "a lower score. City scores use only assessed criteria; weights are "
        "renormalized across those criteria. At least 2 of 3 criteria are "
        "required to receive a rank. Missing, “Not assessed” and unknown labels "
        "are excluded, never treated as zero."
    )

    ranked_cities = rank_cities(cities.to_dict("records"), raw_weights)
    rankable_count = sum(row["rank"] is not None for row in ranked_cities)
    st.subheader("Indicative city ranking")
    st.caption(
        f"{rankable_count} of {len(ranked_cities)} profiles have enough assessed "
        "criteria to rank. Completeness is the share of the three inputs assessed."
    )
    report_pdf = generate_decision_report(ranked_cities, raw_weights)
    st.download_button(
        "Download decision report",
        data=report_pdf,
        file_name="gcc-compass-location-decision-report.pdf",
        mime="application/pdf",
        help="Exports this ranking, its current priorities, city notes, source links, and limitations.",
    )

    criterion_details = [
        ("talent", "Talent availability"),
        ("office_cost", "Office cost (lower is better)"),
        ("ecosystem", "Ecosystem maturity"),
    ]
    for city_result in ranked_cities:
        with st.container(border=True):
            city_column, status_column = st.columns([3, 1])
            with city_column:
                if city_result["rank"] is None:
                    st.markdown(f"### {city_result['city']} · Insufficient data")
                else:
                    st.markdown(
                        f"### #{city_result['rank']} · {city_result['city']}"
                    )
                    st.metric(
                        "Indicative weighted score (out of 5)",
                        f"{city_result['score']:.2f} / 5",
                    )
            with status_column:
                completeness = city_result["evidence_completeness"]
                st.progress(completeness)
                st.caption(
                    f"Evidence completeness: {city_result['assessed_criteria']}/3 "
                    f"criteria ({completeness:.0%})."
                )
                st.caption(
                    "Rank uses assessed criteria only."
                    if city_result["rank"] is not None
                    else "Rank withheld; fewer than 2 criteria are assessed."
                )

            criterion_columns = st.columns(3)
            for column, (criterion, label) in zip(criterion_columns, criterion_details):
                value = city_result["scores"][criterion]
                with column:
                    st.metric(
                        label,
                        f"{value:g} / 5" if value is not None else "Not assessed",
                        delta=f"{weight_percentages[criterion]}% weight",
                        delta_color="off",
                    )

            if city_result["fit_notes"]:
                st.write(f"**Fit notes:** {city_result['fit_notes']}")
            if city_result["validation_note"]:
                st.caption(f"**Still to validate:** {city_result['validation_note']}")
            source_url = city_result["source_url"]
            if isinstance(source_url, str) and source_url.startswith(("https://", "http://")):
                st.link_button("Open listed city source", source_url)
            else:
                st.caption("No city-profile source link supplied.")

elif page == "Provider Finder":
    st.title("Service provider finder")
    q = st.text_input("Search provider, service line or city")
    services = ["All"] + sorted(providers["service_line"].dropna().unique().tolist())
    service = st.selectbox("Service line", services)
    view = providers.copy()
    if q:
        mask = view.astype(str).apply(lambda col: col.str.contains(q, case=False, na=False)).any(axis=1)
        view = view[mask]
    if service != "All": view = view[view["service_line"] == service]
    for _, row in view.iterrows():
        with st.container(border=True):
            left,right = st.columns([3,1])
            with left:
                st.markdown(f"### {row['provider']}")
                st.write(f"**Focus:** {row['service_line']}  ·  **Coverage:** {row['coverage']}")
                st.write(row["description"])
                st.caption(f"Evidence status: {row['evidence_status']} • Last checked: {row['last_checked']}")
            with right:
                if pd.notna(row.get("source_url")) and row["source_url"]:
                    st.link_button("View source", row["source_url"])
                st.caption("No unverified performance claims are shown as fact.")

elif page == "Evidence Desk":
    st.title("Evidence desk")
    st.write("A trustworthy data product needs provenance, not just a large number of records.")
    status = st.selectbox("Evidence status", ["All"] + sorted(sources["status"].dropna().unique().tolist()))
    view = sources if status == "All" else sources[sources.status == status]
    st.dataframe(view, use_container_width=True, hide_index=True, column_config={
        "url": st.column_config.LinkColumn("Source URL", display_text="Open source")
    })
    st.markdown("#### Evidence standard")
    st.markdown("- **Verified:** source directly supports the claim.\n- **Needs review:** source is plausible but does not yet establish the full claim.\n- **Illustrative:** sample record for product-demo purposes; not a factual claim about a real provider or GCC.")
    st.warning("Do not use illustrative records for vendor selection or investment decisions.")

elif page == "AI Research Assistant":
    st.title("AI research assistant")
    st.caption("Local evidence retrieval across the bundled report and GCC Compass records. No API, local model, or generated answer is used.")
    st.caption("Try an indirect question, a calculation (for example, “If 15% of 200 roles are local, how many is that?”), or ask something the source material may not cover.")
    question = st.text_area("Ask a GCC research question", placeholder="Which city profiles should I compare for a technology GCC?")
    if st.button("Research", type="primary"):
        if not question.strip():
            st.warning("Enter a question first.")
        else:
            calculation = calculate_question(question)
            if calculation:
                st.markdown("### Calculation")
                st.write(calculation)
                st.caption("Calculated only from the numbers in your question; this is not an external GCC benchmark.")
            else:
                matches = retrieve_evidence(question, evidence_corpus)
                if matches:
                    st.markdown("### Retrieved evidence")
                    st.write("These are the most relevant passages and records found by local keyword retrieval. They are not an AI-generated synthesis; check each source before relying on a claim.")
                    for match in matches:
                        with st.container(border=True):
                            st.markdown(f"**{match['document']}**")
                            st.write(match["passage"])
                            st.caption(f"Citation: {match['citation']} · Evidence status: {match['status']}")
                            if match["kind"] == "catalogue":
                                st.caption("Catalogue note only; this text was not extracted from the linked source.")
                            if match["url"]:
                                st.link_button("Open cited source", match["url"])
                else:
                    st.markdown("### No matching passage found")
                    st.write("The bundled report and records do not directly answer this question. These general references may help you investigate, but are not evidence for the requested claim.")
                    fallback = sources[
                        sources["status"].eq("Verified")
                        & sources["source_type"].isin(["Government report", "Primary industry report", "Industry association report"])
                    ][["source_name", "notes", "status", "url"]].rename(columns={
                        "source_name": "Reference",
                        "notes": "Context",
                        "status": "Evidence status",
                        "url": "URL",
                    })
                    st.dataframe(fallback, use_container_width=True, hide_index=True, column_config={
                        "URL": st.column_config.LinkColumn("Source", display_text="Open reference")
                    })
                    st.caption("Add a relevant primary document to the Evidence Desk corpus before using an answer for a business decision.")
            st.caption("This assistant retrieves text and links from bundled local sources. It does not call an API, run a local model, or generate answers.")
