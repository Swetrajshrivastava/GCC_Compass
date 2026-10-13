"""Generate a current, evidence-conscious PDF from location-engine results."""

from __future__ import annotations

import html
from collections.abc import Mapping, Sequence
from io import BytesIO
from typing import Any

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from location_scoring import CRITERIA, rounded_weight_percentages


NAVY = colors.HexColor("#101C3A")
BLUE = colors.HexColor("#213C65")
TEAL = colors.HexColor("#168F86")
INK = colors.HexColor("#17233D")
MUTED = colors.HexColor("#62708A")
PALE = colors.HexColor("#F1F5FA")
LINE = colors.HexColor("#DDE4EE")
AMBER = colors.HexColor("#8A5A0A")
WHITE = colors.white

CRITERION_LABELS = {
    "talent": "Talent",
    "office_cost": "Office cost",
    "ecosystem": "Ecosystem",
}


def _plain(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\u2013", "-")
        .replace("\u2014", "-")
        .replace("\u2018", "'")
        .replace("\u2019", "'")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
        .replace("\u00b7", " | ")
    )


def _paragraph(value: Any, style: ParagraphStyle) -> Paragraph:
    return Paragraph(_plain(value).replace("\n", "<br/>"), style)


def _valid_source_url(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    url = value.strip()
    if url.startswith(("https://", "http://")):
        return url
    return None


def _criterion_label(city: Mapping[str, Any], key: str) -> str:
    score = city.get("scores", {}).get(key)
    return f"{score:g}" if score is not None else "Not assessed"


def _weighted_reason(city: Mapping[str, Any], percentages: Mapping[str, int]) -> str:
    scores = city.get("scores", {})
    assessed = [
        (key, scores.get(key), percentages[key])
        for key in CRITERIA
        if scores.get(key) is not None
    ]
    assessed.sort(key=lambda item: item[1] * item[2], reverse=True)
    if not assessed:
        return "No city has enough assessed criteria to support a ranked result."
    details = "; ".join(
        f"{CRITERION_LABELS[key]} {score:g}/5 at {weight}% priority"
        for key, score, weight in assessed
    )
    return (
        f"{city['city']} ranks first in this indicative calculation because its "
        f"assessed ordinal inputs contribute as follows: {details}. The result "
        "does not establish a universally best city."
    )


def _styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "ReportTitle", parent=base["Title"], fontName="Helvetica-Bold",
            fontSize=21, leading=25, textColor=WHITE, alignment=TA_LEFT,
            spaceAfter=3,
        ),
        "subtitle": ParagraphStyle(
            "ReportSubtitle", parent=base["Normal"], fontName="Helvetica",
            fontSize=9, leading=13, textColor=colors.HexColor("#D9E4F6"),
        ),
        "section": ParagraphStyle(
            "Section", parent=base["Heading2"], fontName="Helvetica-Bold",
            fontSize=12, leading=15, textColor=NAVY, spaceBefore=7, spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "Body", parent=base["BodyText"], fontName="Helvetica",
            fontSize=8.5, leading=12, textColor=INK, spaceAfter=3,
        ),
        "body_bold": ParagraphStyle(
            "BodyBold", parent=base["BodyText"], fontName="Helvetica-Bold",
            fontSize=8.5, leading=12, textColor=INK, spaceAfter=3,
        ),
        "small": ParagraphStyle(
            "Small", parent=base["BodyText"], fontName="Helvetica",
            fontSize=7.2, leading=9.5, textColor=MUTED,
        ),
        "table_head": ParagraphStyle(
            "TableHead", parent=base["BodyText"], fontName="Helvetica-Bold",
            fontSize=7.2, leading=9, textColor=WHITE,
        ),
        "table_cell": ParagraphStyle(
            "TableCell", parent=base["BodyText"], fontName="Helvetica",
            fontSize=7.3, leading=9, textColor=INK,
        ),
        "table_cell_bold": ParagraphStyle(
            "TableCellBold", parent=base["BodyText"], fontName="Helvetica-Bold",
            fontSize=7.3, leading=9, textColor=NAVY,
        ),
        "link": ParagraphStyle(
            "Link", parent=base["BodyText"], fontName="Helvetica",
            fontSize=7.5, leading=9.5, textColor=TEAL, wordWrap="CJK",
        ),
        "caveat": ParagraphStyle(
            "Caveat", parent=base["BodyText"], fontName="Helvetica",
            fontSize=8, leading=11, textColor=AMBER,
        ),
    }


def _draw_page(canvas, document) -> None:
    canvas.saveState()
    width, height = landscape(A4)
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(document.leftMargin, 13 * mm, width - document.rightMargin, 13 * mm)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(MUTED)
    canvas.drawString(document.leftMargin, 8.5 * mm, "GCC COMPASS | INDICATIVE DECISION SUPPORT")
    canvas.drawRightString(width - document.rightMargin, 8.5 * mm, f"Page {document.page}")
    canvas.restoreState()


def generate_decision_report(
    ranked_cities: Sequence[Mapping[str, Any]],
    weights: Mapping[str, float],
) -> bytes:
    """Create an in-memory PDF report from the current engine output."""
    percentages = rounded_weight_percentages(weights)
    ranked = sorted(
        (city for city in ranked_cities if city.get("rank") is not None),
        key=lambda city: city["rank"],
    )
    unranked = sorted(
        (city for city in ranked_cities if city.get("rank") is None),
        key=lambda city: str(city.get("city", "")).casefold(),
    )
    leader = ranked[0] if ranked else None
    styles = _styles()
    buffer = BytesIO()

    page_width, page_height = landscape(A4)
    margin_x = 16 * mm
    margin_top = 14 * mm
    margin_bottom = 18 * mm
    doc = BaseDocTemplate(
        buffer,
        pagesize=landscape(A4),
        leftMargin=margin_x,
        rightMargin=margin_x,
        topMargin=margin_top,
        bottomMargin=margin_bottom,
        title="GCC Compass - Location Decision Report",
        author="GCC Compass",
        subject="Indicative comparison based on user-selected qualitative priorities",
    )
    frame = Frame(
        margin_x,
        margin_bottom,
        page_width - 2 * margin_x,
        page_height - margin_top - margin_bottom,
        id="main",
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
    )
    doc.addPageTemplates([PageTemplate(id="report", frames=[frame], onPage=_draw_page)])

    story = []
    header = Table(
        [[
            Paragraph("GCC Compass", styles["title"]),
            Paragraph("LOCATION DECISION REPORT<br/>Generated from your current priorities", styles["subtitle"]),
        ]],
        colWidths=[75 * mm, 105 * mm],
    )
    header.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8 * mm),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8 * mm),
        ("TOPPADDING", (0, 0), (-1, -1), 5 * mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5 * mm),
    ]))
    story.append(header)
    story.append(Spacer(1, 5 * mm))

    story.append(Paragraph("Executive summary", styles["section"]))
    if leader:
        story.append(_paragraph(
            f"Under the selected priorities, {leader['city']} ranks first with an "
            f"indicative score of {leader['score']:.2f}/5 based on "
            f"{leader['assessed_criteria']} of 3 assessed criteria. This is a "
            "prototype decision-support result, not a verified market benchmark "
            "or a definitive location recommendation.",
            styles["body_bold"],
        ))
        story.append(_paragraph(_weighted_reason(leader, percentages), styles["body"]))
    else:
        story.append(_paragraph(
            "No city has enough assessed criteria to receive a rank under the "
            "current rules. Add or verify comparable inputs before drawing a "
            "location conclusion.",
            styles["body_bold"],
        ))

    story.append(Paragraph("Your normalized priorities", styles["section"]))
    weight_data = [[
        Paragraph(f"{label}<br/><b>{percentages[key]}%</b>", styles["body"])
        for key, label in [
            ("talent", "Talent availability"),
            ("office_cost", "Office cost"),
            ("ecosystem", "Ecosystem maturity"),
        ]
    ]]
    weight_table = Table(weight_data, colWidths=[58 * mm] * 3)
    weight_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALE),
        ("BOX", (0, 0), (-1, -1), 0.5, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4 * mm),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5 * mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5 * mm),
    ]))
    story.append(weight_table)

    story.append(Paragraph("City comparison", styles["section"]))
    headers = [
        "City", "Rank", "Score / 5", "Talent / 5",
        "Cost favorability / 5*", "Ecosystem / 5", "Completeness",
    ]
    table_data = [[Paragraph(label, styles["table_head"]) for label in headers]]
    for city in [*ranked, *unranked]:
        score = city.get("score")
        rank = city.get("rank")
        complete = city.get("assessed_criteria", 0)
        completeness = city.get("evidence_completeness", 0)
        table_data.append([
            _paragraph(city.get("city", ""), styles["table_cell_bold"]),
            _paragraph(str(rank) if rank is not None else "Unranked", styles["table_cell"]),
            _paragraph(f"{score:.2f}" if score is not None else "Insufficient data", styles["table_cell"]),
            _paragraph(_criterion_label(city, "talent"), styles["table_cell"]),
            _paragraph(_criterion_label(city, "office_cost"), styles["table_cell"]),
            _paragraph(_criterion_label(city, "ecosystem"), styles["table_cell"]),
            _paragraph(f"{complete}/3 ({completeness:.0%})", styles["table_cell"]),
        ])
    widths = [44 * mm, 19 * mm, 34 * mm, 31 * mm, 37 * mm, 35 * mm, 40 * mm]
    comparison = Table(table_data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    comparison.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLUE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, PALE]),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2.3 * mm),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2.3 * mm),
        ("TOPPADDING", (0, 0), (-1, -1), 2 * mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2 * mm),
    ]))
    story.append(comparison)
    story.append(Spacer(1, 2 * mm))
    story.append(_paragraph(
        "* Cost-favorability score is reversed: a higher cost level receives a lower "
        "favorability score. Criterion scores are illustrative ordinal mappings.",
        styles["small"],
    ))

    story.append(Paragraph("Rationale, sources and validation needs", styles["section"]))
    for city in [*ranked, *unranked]:
        label = (
            f"#{city['rank']} {city['city']}"
            if city.get("rank") is not None
            else f"{city['city']} - unranked"
        )
        completeness = city.get("evidence_completeness", 0)
        story.append(_paragraph(
            f"{label} | Evidence completeness: {city.get('assessed_criteria', 0)}/3 "
            f"criteria ({completeness:.0%}).",
            styles["body_bold"],
        ))
        scores = city.get("scores", {})
        assessed_signals = ", ".join(
            f"{CRITERION_LABELS[key]} {scores[key]:g}/5 at {percentages[key]}% priority"
            for key in CRITERIA
            if scores.get(key) is not None
        )
        story.append(_paragraph(
            f"Assessed score inputs: {assessed_signals or 'None'}. "
            f"Fit notes: {city.get('fit_notes') or 'None supplied.'} "
            f"Validation needs: {city.get('validation_note') or 'None supplied.'}",
            styles["small"],
        ))
        if city.get("rank") is None:
            story.append(_paragraph(
                "Unranked because fewer than 2 of 3 criteria are assessed; "
                "this is not evidence that the city is unsuitable.",
                styles["caveat"],
            ))
        source_url = _valid_source_url(city.get("source_url"))
        if source_url:
            safe_url = html.escape(source_url, quote=True)
            visible_url = html.escape(source_url)
            story.append(Paragraph(
                f'<link href="{safe_url}" color="#168F86">{visible_url}</link>',
                styles["link"],
            ))
        else:
            story.append(_paragraph("Source URL: none supplied in the city profile.", styles["small"]))
        story.append(Spacer(1, 1.5 * mm))

    story.append(Paragraph("Scoring methodology and limitations", styles["section"]))
    caveats = [
        "Signals are qualitative source fields mapped to illustrative ordinal scores: Very low 1, Low 2, Medium-low 2.5, Medium 3, Medium-high 3.5, High 4, Very high 5.",
        "Talent availability and ecosystem maturity use higher-is-better direction. Office-cost level is reversed, so a higher cost label scores lower.",
        "A city score is the weighted average over that city's assessed criteria only; the selected weights are renormalized across those criteria. At least 2 of 3 criteria are required for a rank.",
        "Missing, Not assessed, and unknown values are excluded, not treated as zero. Completeness reports the share of the three criteria with recognized values; it is not a source-quality audit.",
        "The city profiles are qualitative prototype signals, not audited or directly comparable market benchmarks. Linked sources are provided as listed in the dataset and may not substantiate every city claim. Verify primary evidence before making a business decision.",
    ]
    for caveat in caveats:
        story.append(_paragraph(f"- {caveat}", styles["small"]))
        story.append(Spacer(1, 1 * mm))

    doc.build(story)
    return buffer.getvalue()
