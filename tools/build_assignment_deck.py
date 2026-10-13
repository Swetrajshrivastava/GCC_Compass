from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "GCC_Compass_Product_Intern_Assignment.pptx"

NAVY = "101C3A"
NAVY_MID = "213C65"
INK = "17233D"
MUTED = "62708A"
PAPER = "F5F7FB"
WHITE = "FFFFFF"
LINE = "DFE5EF"
TEAL = "16AFA2"
TEAL_PALE = "DDF5F1"
GOLD = "E7A846"
GOLD_PALE = "FFF1D8"
CORAL = "E56B62"
CORAL_PALE = "FCE7E5"
BLUE_PALE = "E9EFFA"


def color(value: str) -> RGBColor:
    return RGBColor.from_string(value)


def add_background(slide, fill: str = PAPER) -> None:
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = color(fill)
    shape.line.fill.background()
    slide.shapes._spTree.remove(shape._element)
    slide.shapes._spTree.insert(2, shape._element)


def add_text(
    slide,
    text: str,
    x: float,
    y: float,
    w: float,
    h: float,
    size: float = 16,
    fill: str = INK,
    bold: bool = False,
    font: str = "Aptos",
    align=PP_ALIGN.LEFT,
    valign=MSO_ANCHOR.TOP,
    margin: float = 0,
    italic: bool = False,
):
    box = slide.shapes.add_textbox(
        Inches(x), Inches(y), Inches(w), Inches(h)
    )
    frame = box.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.margin_left = Inches(margin)
    frame.margin_right = Inches(margin)
    frame.margin_top = Inches(margin)
    frame.margin_bottom = Inches(margin)
    frame.vertical_anchor = valign
    for index, line in enumerate(text.split("\n")):
        paragraph = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
        paragraph.text = line
        paragraph.alignment = align
        paragraph.space_after = Pt(4)
        paragraph.font.name = font
        paragraph.font.size = Pt(size)
        paragraph.font.bold = bold
        paragraph.font.italic = italic
        paragraph.font.color.rgb = color(fill)
    return box


def add_shape(slide, x, y, w, h, fill, radius=True, line=None):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE,
        Inches(x),
        Inches(y),
        Inches(w),
        Inches(h),
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = color(fill)
    if line:
        shape.line.color.rgb = color(line)
        shape.line.width = Pt(0.8)
    else:
        shape.line.fill.background()
    return shape


def add_pill(slide, text, x, y, w, fill, text_fill, size=9):
    add_shape(slide, x, y, w, 0.29, fill, radius=True)
    add_text(
        slide, text, x + 0.06, y + 0.015, w - 0.12, 0.24, size,
        text_fill, bold=True, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE
    )


def add_header(slide, eyebrow, title, subtitle=None):
    add_text(slide, eyebrow.upper(), 0.72, 0.38, 11.8, 0.25, 9, TEAL, True)
    add_text(slide, title, 0.72, 0.72, 11.9, 0.52, 28, NAVY, True, "Aptos Display")
    if subtitle:
        add_text(slide, subtitle, 0.74, 1.34, 11.8, 0.38, 12, MUTED)


def add_footer(slide, number, source=""):
    if source:
        add_text(slide, source, 0.74, 6.93, 10.8, 0.22, 7.5, MUTED)
    add_text(slide, f"GCC COMPASS  /  PRODUCT INTERN ASSIGNMENT          {number:02d}", 9.1, 7.18, 3.5, 0.16, 7, MUTED, True, align=PP_ALIGN.RIGHT)


def add_card(slide, x, y, w, h, title, body, accent=TEAL, fill=WHITE, title_size=15, body_size=11.5):
    add_shape(slide, x, y, w, h, fill, line=LINE if fill == WHITE else None)
    add_shape(slide, x, y, 0.055, h, accent, radius=False)
    add_text(slide, title, x + 0.22, y + 0.18, w - 0.42, 0.4, title_size, NAVY, True)
    add_text(slide, body, x + 0.22, y + 0.7, w - 0.42, h - 0.85, body_size, INK)


def build_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    # 1. Cover
    slide = prs.slides.add_slide(blank)
    add_background(slide, NAVY)
    add_text(slide, "FLEXIPLE  /  PRODUCT INTERN ASSIGNMENT  /  OCT 2026", 0.82, 0.58, 7.4, 0.25, 9, "9EB3D1", True)
    add_text(slide, "India’s GCC market\nneeds an evidence layer —\nnot another list.", 0.82, 1.48, 8.2, 2.28, 31, WHITE, True, "Aptos Display")
    add_text(slide, "GCC Compass", 0.84, 4.32, 4.6, 0.48, 22, "6BE0D3", True, "Aptos Display")
    add_text(slide, "A traceable research workspace for the decisions behind an India launch.", 0.86, 4.92, 6.5, 0.76, 16, "D9E4F6")
    add_pill(slide, "PRODUCT THESIS", 0.84, 6.3, 1.48, NAVY_MID, "B9D4F2", 8)
    add_text(slide, "DISCOVER  →  COMPARE  →  VERIFY", 2.55, 6.32, 3.8, 0.22, 9, "C1D2E8", True)
    # Abstract connected evidence map.
    for x, y, diameter, fill in [
        (10.05, 1.35, 1.12, TEAL),
        (11.38, 2.18, 0.72, GOLD),
        (9.42, 3.15, 0.73, "7293C4"),
        (11.0, 4.55, 1.05, CORAL),
        (9.6, 5.35, 0.47, "A7BEDC"),
    ]:
        node = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(diameter), Inches(diameter))
        node.fill.solid()
        node.fill.fore_color.rgb = color(fill)
        node.line.fill.background()
    for x, y, w, h in [(10.7, 1.95, 1.25, 0.03), (9.98, 2.8, 0.55, 0.03), (10.05, 3.55, 1.1, 0.03), (10.0, 5.55, 0.9, 0.03)]:
        add_shape(slide, x, y, w, h, "456184", radius=False)
    add_text(slide, "SOURCE", 10.05, 1.74, 1.0, 0.2, 8, NAVY, True, align=PP_ALIGN.CENTER)
    add_text(slide, "CITY", 11.42, 2.42, 0.62, 0.2, 8, NAVY, True, align=PP_ALIGN.CENTER)
    add_text(slide, "GCC", 9.48, 3.42, 0.62, 0.2, 8, WHITE, True, align=PP_ALIGN.CENTER)
    add_text(slide, "PROOF", 11.04, 4.95, 0.95, 0.2, 8, WHITE, True, align=PP_ALIGN.CENTER)

    # 2. Problem
    slide = prs.slides.add_slide(blank)
    add_background(slide)
    add_header(slide, "01 / The problem", "The data exists. The connective tissue doesn’t.", "India-entry decisions join facts that live with different owners, in different formats, on different dates.")
    columns = [
        ("GCCs + moves", "Filings\nCompany news\nIndustry reports", BLUE_PALE, "4169A1"),
        ("Cities + policy", "State portals\nPolicy PDFs\nLocal agencies", TEAL_PALE, TEAL),
        ("Space + talent", "Broker briefs\nRecruiter views\nMarket studies", GOLD_PALE, GOLD),
        ("Providers + proof", "Service pages\nPitch decks\nClient referrals", CORAL_PALE, CORAL),
        ("Decision", "Where to locate?\nWho can deliver?\nWhat is evidenced?", NAVY_MID, WHITE),
    ]
    start, width, gap = 0.72, 2.27, 0.22
    for i, (title, body, fill, accent) in enumerate(columns):
        x = start + i * (width + gap)
        add_shape(slide, x, 2.24, width, 2.12, fill, line=LINE if fill != NAVY_MID else None)
        add_text(slide, title, x + 0.16, 2.5, width - 0.32, 0.35, 14, accent if fill != NAVY_MID else WHITE, True)
        add_text(slide, body, x + 0.16, 3.02, width - 0.32, 1.02, 11.5, INK if fill != NAVY_MID else WHITE)
        if i < len(columns) - 1:
            add_text(slide, "→", x + width + 0.01, 3.02, gap - 0.02, 0.3, 16, MUTED, True, align=PP_ALIGN.CENTER)
    add_shape(slide, 0.72, 4.82, 11.86, 1.18, NAVY)
    add_text(slide, "THE FAILURE MODE", 0.98, 5.06, 1.75, 0.22, 9, "6BE0D3", True)
    add_text(slide, "Facts get detached from date, definition, source and delivery proof — so teams fall back on referrals.", 2.75, 5.0, 9.35, 0.52, 17, WHITE, True)
    add_text(slide, "Market-fragmentation premise from the Flexiple assignment brief. No time/cost impact is quantified in this prototype.", 0.76, 6.46, 11.4, 0.24, 8, MUTED)
    add_footer(slide, 2)

    # 3. Stakeholder pain and existing workarounds
    slide = prs.slides.add_slide(blank)
    add_background(slide)
    add_header(slide, "02 / Who is hurt", "The first buyer carries the most decision risk.", "Start with the team accountable for an India location and operating-model decision; serve adjacent actors without compromising trust.")
    add_card(slide, 0.72, 2.05, 3.8, 3.65, "India-entry team", "NEEDS\nA defensible shortlist of cities, setup routes and partners.\n\nTODAY\nConsultant reports + spreadsheets + local introductions.\n\nRISK\nSlow synthesis; hard to separate comparable facts from claims.", TEAL, WHITE, 15, 11)
    add_card(slide, 4.76, 2.05, 3.8, 3.65, "Ecosystem provider", "NEEDS\nReach buyers with the right project context and show relevant delivery proof.\n\nTODAY\nBroad marketing, RFPs and relationship-led referrals.\n\nRISK\nDiscovery rewards visibility, not necessarily verified fit.", GOLD, WHITE, 15, 11)
    add_card(slide, 8.8, 2.05, 3.8, 3.65, "Advisor / ecosystem body", "NEEDS\nReusable, current evidence and a clearer handoff across stakeholders.\n\nTODAY\nRepeated desk research and private knowledge networks.\n\nRISK\nWork is hard to reuse; evidence trails are inconsistent.", CORAL, WHITE, 15, 11)
    add_pill(slide, "WORKING HYPOTHESES — VALIDATE THROUGH BUYER INTERVIEWS", 0.76, 5.98, 4.6, GOLD_PALE, "80560E", 8)
    add_footer(slide, 3, "Current workarounds and impacts are hypotheses drawn from the assignment brief, not measured outcomes.")

    # 4. Opportunity prioritization
    slide = prs.slides.add_slide(blank)
    add_background(slide)
    add_header(slide, "03 / Where to start", "Start where evidence changes a consequential decision.", "Priority is based on problem fit and evidence feasibility—not a market-size score.")
    opportunities = [
        ("01", "Entry research workspace", "GCC activity + city comparison with source-linked claims.", "NOW", TEAL, TEAL_PALE),
        ("02", "Claim provenance", "Show source, date, unit, status and what remains unverified.", "FOUNDATION", "4169A1", BLUE_PALE),
        ("03", "Proof-backed provider discovery", "Make delivery evidence and references useful in shortlisting.", "NEXT", GOLD, GOLD_PALE),
        ("04", "Live benchmarks + alerts", "Policy eligibility, talent cost, rent and emerging signals.", "LATER", CORAL, CORAL_PALE),
    ]
    for i, (num, title, body, tag, accent, pale) in enumerate(opportunities):
        y = 2.08 + i * 1.02
        add_shape(slide, 0.72, y, 11.88, 0.84, WHITE, line=LINE)
        add_text(slide, num, 0.94, y + 0.21, 0.52, 0.25, 12, accent, True)
        add_text(slide, title, 1.6, y + 0.13, 3.0, 0.3, 14, NAVY, True)
        add_text(slide, body, 4.52, y + 0.14, 6.12, 0.42, 11.5, MUTED)
        add_pill(slide, tag, 10.91, y + 0.25, 1.32, pale, accent, 8)
    add_text(slide, "Why this wedge: it tackles the core asymmetry while using public and already-published material; it does not require audited private benchmarks to be useful.", 0.82, 6.46, 11.4, 0.34, 11, NAVY, True)
    add_footer(slide, 4)

    # 5. Product
    slide = prs.slides.add_slide(blank)
    add_background(slide)
    add_header(slide, "04 / The product", "One question. An evidence trail—not a confident guess.", "GCC Compass turns a broad research prompt into passages and records a user can inspect.")
    # App-style mockup
    add_shape(slide, 0.72, 2.0, 7.55, 4.48, WHITE, line=LINE)
    add_shape(slide, 0.72, 2.0, 7.55, 0.48, NAVY, radius=True)
    add_text(slide, "GCC COMPASS  /  RESEARCH ASSISTANT", 0.98, 2.13, 5.7, 0.18, 9, WHITE, True)
    add_text(slide, "ASK", 1.02, 2.83, 0.45, 0.2, 8, TEAL, True)
    add_shape(slide, 1.02, 3.11, 6.93, 0.62, PAPER, line=LINE)
    add_text(slide, "Where are the main GCC hubs?", 1.22, 3.28, 6.5, 0.26, 15, NAVY, True)
    add_text(slide, "RETRIEVED SOURCE PASSAGE", 1.02, 3.98, 2.8, 0.2, 8, MUTED, True)
    add_shape(slide, 1.02, 4.26, 6.93, 1.27, "F7FAFE", line=LINE)
    add_text(slide, "“Major clusters in Bengaluru, Hyderabad, Pune, Chennai, Mumbai and the National Capital Region.”", 1.22, 4.46, 6.48, 0.56, 13, INK, True)
    add_text(slide, "Government of India report · p. 2", 1.22, 5.13, 3.9, 0.2, 9, MUTED)
    add_pill(slide, "VERIFIED SOURCE", 5.72, 5.12, 1.82, TEAL_PALE, TEAL, 8)
    add_text(slide, "A different prompt with no supporting passage returns “No matching passage found.”", 1.02, 5.82, 6.9, 0.42, 10.5, MUTED)
    add_card(slide, 8.62, 2.0, 3.97, 2.08, "A decision path", "Find candidate evidence\nCompare without a universal score\nOpen the original source", TEAL, WHITE, 15, 11.5)
    add_card(slide, 8.62, 4.36, 3.97, 2.12, "The user’s job", "“Help me decide where to start and who to engage — and show what each recommendation rests on.”", GOLD, WHITE, 14, 12)
    add_footer(slide, 5, "Source: Government of India / PIB report, 11 Dec 2025, p. 2. Prototype displays the original source link and page citation.")

    # 6. Trust / evidence system
    slide = prs.slides.add_slide(blank)
    add_background(slide)
    add_header(slide, "05 / Trust by design", "The moat is the evidence graph, not the chatbot.", "A useful answer starts with a defensible source chain; richer synthesis can come later, only if evidence quality supports it.")
    flow = [
        ("01", "Collect", "Public reports\npolicy pages\ncompany signals"),
        ("02", "Structure", "Normalize entity\ncity, date, unit\nand claim"),
        ("03", "Qualify", "Evidence status\nsource strength\nfreshness"),
        ("04", "Retrieve", "Rank relevant\npassages; keep\ncitation attached"),
        ("05", "Review", "User verifies,\ncorrects or flags\nthe record"),
    ]
    for i, (number, title, body) in enumerate(flow):
        x = 0.72 + i * 2.43
        add_shape(slide, x, 2.2, 2.1, 1.8, WHITE, line=LINE)
        add_text(slide, number, x + 0.16, 2.4, 0.4, 0.22, 9, TEAL, True)
        add_text(slide, title, x + 0.16, 2.77, 1.78, 0.33, 15, NAVY, True)
        add_text(slide, body, x + 0.16, 3.25, 1.78, 0.62, 10, MUTED)
        if i < 4:
            add_text(slide, "→", x + 2.12, 2.92, 0.3, 0.3, 15, TEAL, True, align=PP_ALIGN.CENTER)
    add_shape(slide, 0.72, 4.45, 7.1, 1.5, NAVY)
    add_text(slide, "PROTOTYPE TODAY", 0.98, 4.68, 2.1, 0.22, 9, "6BE0D3", True)
    add_text(slide, "Local PDF/CSV extraction + lexical ranking + citations. Arithmetic stays bounded. No LLM, API or local model.", 0.98, 5.03, 6.48, 0.62, 13, WHITE, True)
    add_shape(slide, 8.05, 4.45, 4.54, 1.5, GOLD_PALE)
    add_text(slide, "NON-NEGOTIABLE", 8.31, 4.68, 2.1, 0.22, 9, "80560E", True)
    add_text(slide, "No source, no claim. A catalogue note is not a source passage; a provider profile is not delivery proof.", 8.31, 5.03, 3.98, 0.62, 12, INK, True)
    add_footer(slide, 6)

    # 7. Positioning and stakeholder incentives
    slide = prs.slides.add_slide(blank)
    add_background(slide)
    add_header(slide, "06 / Positioning", "A decision workspace across the setup journey.", "Complement consultants and primary sources; replace the repeated stitching between PDFs, pitches, referrals and spreadsheets.")
    cards = [
        (0.72, 2.0, "GCC entrant", "Why come: a comparable first pass with claims linked to evidence.\nOver today: fewer disconnected starting points.", TEAL),
        (6.77, 2.0, "Service provider", "Why come: context-rich discovery and a way to submit proof.\nOver today: fit and evidence beside the listing.", GOLD),
        (0.72, 4.15, "Advisor / researcher", "Why come: reusable source trail and cleaner handoffs.\nOver today: evidence can travel with the recommendation.", "4169A1"),
        (6.77, 4.15, "State / ecosystem body", "Why come: make official programmes and ecosystem signals easier to discover.\nOver today: visibility without implying policy advice.", CORAL),
    ]
    for x, y, title, body, accent in cards:
        add_card(slide, x, y, 5.82, 1.78, title, body, accent, WHITE, 14, 10.5)
    add_shape(slide, 0.72, 6.2, 11.87, 0.45, NAVY)
    add_text(slide, "NEUTRALITY RULE  /  Paid participation can buy workflow — never evidence status or search rank.", 1.0, 6.31, 11.3, 0.2, 10, WHITE, True)
    add_footer(slide, 7)

    # 8. MVP and business model hypothesis
    slide = prs.slides.add_slide(blank)
    add_background(slide)
    add_header(slide, "07 / Scope + business model", "Earn trust in one wedge before expanding the data surface.", "Initial segment: strategy / site-selection teams assessing a first India GCC or a meaningful expansion.")
    add_card(slide, 0.72, 2.04, 3.8, 3.35, "Build first", "Source-backed GCC/activity directory\n\nQualitative city comparison with evidence links\n\nClaim status, date and source on every record\n\nCorrection / evidence-submission path", TEAL, WHITE, 15, 11)
    add_card(slide, 4.77, 2.04, 3.8, 3.35, "Defer until reliable", "Audited rent and salary benchmarks\n\nPolicy eligibility or legal advice\n\nProvider performance scores\n\nAutomated market-wide alerts\n\nUniversal “best city” rankings", CORAL, WHITE, 15, 11)
    add_card(slide, 8.82, 2.04, 3.77, 3.35, "Commercial hypothesis", "Paid team workspace, saved research and exportable evidence packs.\n\nPublic discovery stays accessible.\n\nProvider paid features cannot change rank or verification.", GOLD, WHITE, 15, 11)
    add_pill(slide, "HYPOTHESIS — TEST WILLINGNESS TO PAY BEFORE BUILDING BILLING", 0.76, 5.76, 4.67, GOLD_PALE, "80560E", 8)
    add_text(slide, "Why narrow scope: verified depth is more valuable than a large directory that confuses leads with facts.", 0.78, 6.25, 11.4, 0.32, 11, NAVY, True)
    add_footer(slide, 8)

    # 9. Prototype and validation plan
    slide = prs.slides.add_slide(blank)
    add_background(slide)
    add_header(slide, "08 / Proof + next test", "The prototype works; product-market fit is still a question.", "Separate what is implemented from what must be demonstrated with real decision-makers.")
    add_shape(slide, 0.72, 2.04, 5.7, 3.95, WHITE, line=LINE)
    add_text(slide, "BUILT IN GCC COMPASS", 1.0, 2.28, 3.5, 0.22, 9, TEAL, True)
    metrics = [("12", "company research leads"), ("10", "city profiles"), ("11", "provider profiles"), ("18", "source records")]
    for i, (value, label) in enumerate(metrics):
        x = 1.0 + (i % 2) * 2.55
        y = 2.8 + (i // 2) * 1.12
        add_text(slide, value, x, y, 0.74, 0.45, 26, NAVY, True, "Aptos Display")
        add_text(slide, label, x + 0.78, y + 0.08, 1.52, 0.32, 10, MUTED, True)
    add_text(slide, "Local extractive retrieval • page citations • arithmetic • explicit no-evidence state\n5 focused retrieval tests passed", 1.0, 5.18, 4.95, 0.55, 10, INK, True)
    add_pill(slide, "SAMPLE DATA — NOT A GCC CENSUS", 1.0, 5.73, 2.75, GOLD_PALE, "80560E", 8)
    add_shape(slide, 6.75, 2.04, 5.84, 3.95, NAVY)
    add_text(slide, "NEXT: A SMALL DESIGN-PARTNER TEST", 7.02, 2.28, 4.9, 0.22, 9, "6BE0D3", True)
    add_text(slide, "Give site-selection leads one task:\n“Shortlist a city and show the evidence you used.”", 7.02, 2.73, 5.1, 0.82, 18, WHITE, True, "Aptos Display")
    add_text(slide, "Observe", 7.02, 3.88, 1.0, 0.25, 11, "6BE0D3", True)
    add_text(slide, "Time to a defensible first pass • citation-open rate • claims users challenge • missing evidence.", 8.04, 3.85, 4.1, 0.62, 10.5, WHITE)
    add_text(slide, "Success looks like", 7.02, 4.83, 1.6, 0.25, 11, "6BE0D3", True)
    add_text(slide, "Less stitching, clearer uncertainty, and no unsupported claim presented as fact. Set numeric targets only after a baseline.", 8.58, 4.78, 3.55, 0.76, 10.5, WHITE)
    add_footer(slide, 9, "Prototype record counts from bundled CSVs, as at 11 Oct 2026. Company/provider records include Needs review or Illustrative entries.")

    # 10. Sources and evidence caveats
    slide = prs.slides.add_slide(blank)
    add_background(slide, NAVY)
    add_text(slide, "09 / SOURCES + EVIDENCE BOUNDARY", 0.74, 0.45, 11.7, 0.25, 9, "6BE0D3", True)
    add_text(slide, "What this deck knows — and what it does not.", 0.74, 0.82, 11.7, 0.55, 27, WHITE, True, "Aptos Display")
    add_text(slide, "Primary reference", 0.76, 1.72, 2.4, 0.25, 11, "6BE0D3", True)
    add_text(slide, "Government of India / PIB, “From Policy to Prosperity: GCCs Leading India’s Growth Journey” (11 Dec 2025). Page 1 reports 1,700+ GCCs; page 2 names major clusters. The report uses “GCCs” and “centres” in different contexts; do not treat the units or time horizons as interchangeable.", 0.76, 2.1, 5.72, 1.55, 12, WHITE)
    add_text(slide, "Open source PDF  ↗", 0.76, 3.8, 2.1, 0.25, 10, "6BE0D3", True)
    add_text(slide, "NASSCOM industry reference", 6.92, 1.72, 3.5, 0.25, 11, "6BE0D3", True)
    add_text(slide, "NASSCOM, “India GCC Landscape: The 5 Year Journey.” Included in the prototype’s source catalogue; no specific NASSCOM statistic is quoted in this deck.", 6.92, 2.1, 5.3, 1.04, 12, WHITE)
    add_text(slide, "Open source page  ↗", 6.92, 3.28, 2.2, 0.25, 10, "6BE0D3", True)
    add_shape(slide, 0.76, 4.2, 11.78, 1.55, NAVY_MID)
    add_text(slide, "READ THIS BEFORE USING A SAMPLE RECORD", 1.02, 4.46, 4.0, 0.22, 9, "F2C66D", True)
    add_text(slide, "City fields are qualitative, not audited benchmarks. Company entries are research leads; provider descriptions are self-published or illustrative. Links do not independently prove GCC presence, service delivery or performance.", 1.02, 4.83, 10.95, 0.66, 12, WHITE)
    add_text(slide, "Official PIB report: static.pib.gov.in/WriteReadData/specificdocs/documents/2025/dec/doc20251211727201.pdf", 0.76, 6.05, 11.6, 0.22, 8.5, "B9C9DE")
    add_text(slide, "NASSCOM source: community.nasscom.in/communities/nasscom-insights/india-gcc-landscape-report-5-year-journey", 0.76, 6.34, 11.6, 0.22, 8.5, "B9C9DE")
    add_text(slide, "Flexiple assignment brief supplied by the candidate. Product, customer and business-model statements are hypotheses unless explicitly sourced.", 0.76, 6.73, 11.6, 0.22, 8.5, "B9C9DE")
    add_footer(slide, 10)

    # Add clickable source links on the final slide.
    final = prs.slides[-1]
    add_text(final, " ", 0.76, 3.8, 0.01, 0.01)
    # Hyperlink visible source labels rather than adding long URLs as plain text.
    for shape in final.shapes:
        if not shape.has_text_frame:
            continue
        if shape.text == "Open source PDF  ↗":
            shape.text_frame.paragraphs[0].runs[0].hyperlink.address = (
                "https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/dec/doc20251211727201.pdf"
            )
        elif shape.text == "Open source page  ↗":
            shape.text_frame.paragraphs[0].runs[0].hyperlink.address = (
                "https://community.nasscom.in/index.php/communities/nasscom-insights/india-gcc-landscape-report-5-year-journey?page=7"
            )

    prs.core_properties.title = "GCC Compass — Flexiple Product Intern Assignment"
    prs.core_properties.subject = "Evidence-led GCC ecosystem research workspace"
    prs.core_properties.author = "GCC Compass"
    prs.core_properties.keywords = "GCC, India, product strategy, evidence, research"
    prs.save(OUTPUT)
    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    build_deck()
