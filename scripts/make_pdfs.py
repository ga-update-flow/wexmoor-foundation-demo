"""Generate every downloadable PDF for the site with ReportLab.

Prose documents come from Markdown sources in docs-src/; annual reports, the financial
summary and the strategic-issue one-pagers are built from src/data/*.json and
docs-src/impact-plan.md so figures stay consistent with the website.

Run:  python3 scripts/make_pdfs.py
"""
import os, re
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, KeepTogether)
from brand import *  # noqa: F401,F403

SITE = load("site.json")
DOCS = load("documents.json")
REPORTS = load("reports.json")
GRANTEES = load("grantees.json")
PEOPLE = load("people.json")
SRC = os.path.join(ROOT, "docs-src")
PUBLIC = os.path.join(ROOT, "public")
C = colors.HexColor

# ---------------------------------------------------------------- styles
base = ParagraphStyle("base", fontName="Helvetica", fontSize=10.5, leading=15, textColor=C(INK), spaceAfter=8)
S = {
    "body": base,
    "h1": ParagraphStyle("h1", parent=base, fontName="Helvetica-Bold", fontSize=20, leading=25, textColor=C(INDIGO), spaceAfter=12),
    "h2": ParagraphStyle("h2", parent=base, fontName="Helvetica-Bold", fontSize=14, leading=18, textColor=C(INDIGO), spaceBefore=10, spaceAfter=8),
    "h3": ParagraphStyle("h3", parent=base, fontName="Helvetica-Bold", fontSize=11.5, leading=15, textColor=C(TERRA), spaceBefore=6, spaceAfter=6),
    "sub": ParagraphStyle("sub", parent=base, fontName="Helvetica-Oblique", textColor=colors.HexColor("#555555")),
    "quote": ParagraphStyle("quote", parent=base, fontName="Times-Italic", fontSize=13, leading=18, leftIndent=24, rightIndent=24, textColor=C(INDIGO), spaceBefore=4, spaceAfter=12),
    "bullet": ParagraphStyle("bullet", parent=base, leftIndent=18, bulletIndent=6, spaceAfter=4),
    "bullet2": ParagraphStyle("bullet2", parent=base, leftIndent=36, bulletIndent=24, spaceAfter=3),
    "cell": ParagraphStyle("cell", parent=base, fontSize=9, leading=12, spaceAfter=0),
    "cellh": ParagraphStyle("cellh", parent=base, fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=colors.white, spaceAfter=0),
    "big": ParagraphStyle("big", parent=base, fontName="Helvetica-Bold", fontSize=34, leading=40, textColor=C(INDIGO)),
    "stat": ParagraphStyle("stat", parent=base, fontName="Helvetica-Bold", fontSize=22, leading=26, textColor=C(TERRA), alignment=TA_CENTER, spaceAfter=2),
    "statl": ParagraphStyle("statl", parent=base, fontSize=9, leading=12, alignment=TA_CENTER),
}


def inline(text):
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    return text


# ---------------------------------------------------------------- page furniture
def draw_mark(c, x, y, size, mono=None):
    """Draw the faceted W mark with its top-left corner at (x, y) in PDF coordinates."""
    s = size / 100
    to = lambda px, py: (x + px * s, y - py * s)
    c.saveState()
    p = c.beginPath()
    first = True
    for px, py in W_POINTS:
        X, Y = to(px, py)
        (p.moveTo if first else p.lineTo)(X, Y)
        first = False
    p.close()
    if mono:
        c.setFillColor(C(mono)); c.drawPath(p, stroke=0, fill=1)
    else:
        c.clipPath(p, stroke=0, fill=0)
        for tri, col in facet_triangles(7):
            q = c.beginPath()
            X, Y = to(*tri[0]); q.moveTo(X, Y)
            for pt in tri[1:]:
                X, Y = to(*pt); q.lineTo(X, Y)
            q.close()
            c.setFillColor(C(col)); c.setStrokeColor(C(col)); c.setLineWidth(0.3)
            c.drawPath(q, stroke=1, fill=1)
    c.restoreState()


def letterhead(c, W, H):
    draw_mark(c, 0.75 * inch, H - 0.55 * inch, 46)
    c.setFillColor(C(INDIGO))
    c.setFont("Helvetica-Bold", 15); c.drawString(0.75 * inch + 54, H - 0.78 * inch, "WEXMOOR")
    c.setFont("Helvetica", 15); c.drawString(0.75 * inch + 54, H - 0.98 * inch, "FOUNDATION")
    c.setFillColor(C(TERRA)); c.setFont("Times-Italic", 10); c.drawString(0.75 * inch + 55, H - 1.13 * inch, SITE["tagline"])
    c.setFillColor(colors.HexColor("#555555")); c.setFont("Helvetica", 8.5)
    a = SITE["address"]
    for i, line in enumerate([a["line1"], f'{a["city"]}, {a["state"]} {a["zip"]}', f'Phone: {SITE["phone"]}', SITE["email"]]):
        c.drawRightString(W - 0.75 * inch, H - 0.72 * inch - i * 11, line)
    c.setStrokeColor(C(SAND)); c.setLineWidth(1); c.line(0.75 * inch, H - 1.3 * inch, W - 0.75 * inch, H - 1.3 * inch)


def make_doc(path, title, subject, pagesize=letter, head="letterhead"):
    full = os.path.join(PUBLIC, path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    W, H = pagesize
    top = 1.5 * inch if head == "letterhead" else 0.8 * inch

    def first(c, d):
        c.saveState()
        if head == "letterhead":
            letterhead(c, W, H)
        footer(c, d)
        c.restoreState()

    def later(c, d):
        c.saveState()
        draw_mark(c, W - 0.95 * inch, H - 0.35 * inch, 20)
        c.setFont("Helvetica", 8); c.setFillColor(colors.HexColor("#777777"))
        c.drawString(0.75 * inch, H - 0.5 * inch, title)
        footer(c, d)
        c.restoreState()

    def footer(c, d):
        c.setFont("Helvetica", 7.5); c.setFillColor(colors.HexColor("#777777"))
        c.drawString(0.75 * inch, 0.45 * inch, f'{SITE["name"]}  |  Fictional organization: demonstration document for website testing')
        c.drawRightString(W - 0.75 * inch, 0.45 * inch, f"Page {d.page}")

    doc = BaseDocTemplate(full, pagesize=pagesize, title=title, author=SITE["name"], subject=subject,
                          creator="Wexmoor Foundation demo site generator", keywords="Wexmoor Foundation, fictional, demonstration",
                          leftMargin=0.75 * inch, rightMargin=0.75 * inch, topMargin=top, bottomMargin=0.8 * inch, lang="en-US")
    f1 = Frame(doc.leftMargin, doc.bottomMargin, doc.width, H - top - doc.bottomMargin, id="f1")
    f2 = Frame(doc.leftMargin, doc.bottomMargin, doc.width, H - 0.8 * inch - doc.bottomMargin, id="f2")
    doc.addPageTemplates([PageTemplate("first", [f1], onPage=first, autoNextPageTemplate="later"),
                          PageTemplate("later", [f2], onPage=later)])
    return doc, full


def table(rows, widths, header=True):
    data = [[Paragraph(inline(c), S["cellh"] if (header and i == 0) else S["cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    style = [("GRID", (0, 0), (-1, -1), 0.5, C("#BBB4A8")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
             ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]
    if header:
        style.append(("BACKGROUND", (0, 0), (-1, 0), C(INDIGO)))
    t.setStyle(TableStyle(style))
    return t


# ---------------------------------------------------------------- markdown renderer
def md_story(text, width):
    story, para, lines = [], [], text.splitlines()

    def flush():
        if para:
            story.append(Paragraph(inline(" ".join(para)), S["body"])); para.clear()

    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.strip() == "---pagebreak---":
            flush(); story.append(PageBreak())
        elif ln.startswith("|"):
            flush()
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r"-+", c) for c in cells):
                    rows.append(cells)
                i += 1
            n = len(rows[0])
            story.append(table(rows, [width / n] * n)); story.append(Spacer(1, 10))
            continue
        elif ln.startswith("### "):
            flush(); story.append(Paragraph(inline(ln[4:]), S["h3"]))
        elif ln.startswith("## "):
            flush(); story.append(Paragraph(inline(ln[3:]), S["h2"]))
        elif ln.startswith("# "):
            flush(); story.append(Paragraph(inline(ln[2:]), S["h1"]))
        elif ln.startswith("> "):
            flush(); story.append(Paragraph(inline(ln[2:]), S["quote"]))
        elif ln.startswith("  - "):
            flush(); story.append(Paragraph(inline(ln[4:]), S["bullet2"], bulletText="o"))
        elif ln.startswith("- "):
            flush(); story.append(Paragraph(inline(ln[2:]), S["bullet"], bulletText="•"))
        elif not ln.strip():
            flush()
        else:
            para.append(ln.strip())
        i += 1
    flush()
    return story


def read_src(name):
    with open(os.path.join(SRC, name), encoding="utf-8") as f:
        return f.read()


def section(md, heading):
    """Return the Markdown from `heading` up to the next page break."""
    start = md.index(heading)
    end = md.find("---pagebreak---", start)
    return md[start:end if end != -1 else None]


def build_md(key, src, subject, pagesize=letter, head="letterhead", text=None):
    d = DOCS[key]
    doc, full = make_doc(d["path"], d["title"], subject, pagesize, head)
    doc.build(md_story(text if text is not None else read_src(src), doc.width))
    return full


# ---------------------------------------------------------------- data-driven documents
def cycles_by_slug():
    return {c["slug"]: c for c in GRANTEES["cycles"]}


def annual_report(r):
    title = f'The Wexmoor Foundation FY {r["year"]} Annual Report'
    doc, full = make_doc(r["path"], title, f'Annual report for fiscal year {r["year"]} ({r["period"]})', letter, head="none")
    ed_name = "Dr. Renee Callahan" if r["year"] >= 2024 else "Catherine Boyd"
    st = [Spacer(1, 1.2 * inch), Paragraph(f'FY {r["year"]}', S["big"]), Paragraph("Annual Report", S["big"]), Spacer(1, 12),
          Paragraph(r["theme"], ParagraphStyle("t", parent=S["h2"], textColor=C(TERRA), fontSize=18, leading=22)),
          Paragraph(f'Fiscal year {r["period"]}', S["sub"]), Spacer(1, 30),
          Paragraph(f'{SITE["name"]} invests in early grades achievement and excellent educators and leaders for the students of '
                    f'{SITE["homeCounty"]} and North Carolina.', S["body"]), PageBreak()]
    st += [Paragraph("A Message from Our Board Chair and Executive Director", S["h1"]),
           Paragraph("Dear friends,", S["body"]),
           Paragraph(f'This year&rsquo;s report, <i>{r["theme"]}</i>, reflects the work of the teachers, principals, tutors, families and '
                     "partner organizations who make our mission possible. Across Brannock County and North Carolina, our partners kept "
                     "students at the center of everything they did, and we are proud to stand alongside them.", S["body"]),
           Paragraph("Our two focus areas remain unchanged: helping every child read with confidence by the end of third grade, and "
                     "making sure every classroom is led by an excellent teacher supported by a strong principal. We continue to learn "
                     "from our partners and to share what we learn with others across the state.", S["body"]),
           Paragraph("Thank you for your partnership and your commitment to the students we serve.", S["body"]),
           Spacer(1, 8),
           Paragraph(f'{PEOPLE["chair"]["name"]}, Board Chair<br/>{ed_name}, Executive Director', S["body"]),
           Spacer(1, 16), Paragraph("The Year at a Glance", S["h2"])]
    for h in r["highlights"]:
        st.append(Paragraph(inline(h), S["bullet"], bulletText="•"))
    stats = Table([[Paragraph(f'${r["grantsPaid"]}', S["stat"]), Paragraph(str(r["grantCount"]), S["stat"]),
                    Paragraph(f'${r["earlyGrades"]}', S["stat"]), Paragraph(f'${r["educators"]}', S["stat"])],
                   [Paragraph("Total grants paid", S["statl"]), Paragraph("Grants awarded", S["statl"]),
                    Paragraph("Early Grades Achievement", S["statl"]), Paragraph("Educators &amp; Leaders", S["statl"])]],
                  colWidths=[doc.width / 4] * 4)
    stats.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), C(CREAM)), ("TOPPADDING", (0, 0), (-1, -1), 10), ("BOTTOMPADDING", (0, 0), (-1, -1), 10)]))
    st += [Spacer(1, 12), stats, PageBreak(), Paragraph(f'FY {r["year"]} Grantee Partners', S["h1"])]
    cyc = cycles_by_slug()
    if r["cycles"]:
        for slug in r["cycles"]:
            c = cyc[slug]
            rows = [["Organization", "Location"]] + [[n, GRANTEES["locations"][l]] for n, l in c["grantees"]]
            st += [Paragraph(c["title"], S["h2"]), table(rows, [doc.width * 0.65, doc.width * 0.35]), Spacer(1, 10)]
    else:
        st.append(Paragraph("We were honored to support the following organizations this year:", S["body"]))
        for n in r["grantees"]:
            st.append(Paragraph(inline(n), S["bullet"], bulletText="•"))
    st += [PageBreak(), Paragraph("Financial Snapshot", S["h1"]),
           table([["", f'FY {r["year"]}'], ["Grants paid", f'${r["grantsPaid"]}'],
                  ["Early Grades Achievement", f'${r["earlyGrades"]}'], ["Educators & Leaders", f'${r["educators"]}'],
                  ["Number of grants awarded", str(r["grantCount"])]], [doc.width * 0.6, doc.width * 0.4]),
           Spacer(1, 18), Paragraph("Board of Directors", S["h2"]),
           Paragraph("<br/>".join(n + (f", {t}" if t else "") for n, t in PEOPLE["board"]), S["body"]),
           Paragraph("Foundation Staff", S["h2"])]
    staff = PEOPLE["staff"] if r["year"] >= 2024 else [{"name": "Catherine Boyd", "title": "Executive Director"}, {"name": "Martin Osei", "title": "Grants Manager"}]
    st.append(Paragraph("<br/>".join(f'{s["name"]}, {s["title"]}' for s in staff), S["body"]))
    a = SITE["address"]
    st.append(Paragraph(f'{SITE["name"]} | {a["line1"]}, {a["city"]}, {a["state"]} {a["zip"]} | {SITE["email"]}', S["sub"]))
    doc.build(st)
    return full


def financial_summary():
    d = DOCS["financials"]
    f = SITE["latestFinancials"]
    doc, full = make_doc(d["path"], d["title"], "Summary of fiscal year 2025 financial information", letter)
    r25 = next(r for r in REPORTS if r["year"] == 2025)
    st = [Paragraph("FY2025 Financial Summary and 990-PF Highlights", S["h1"]),
          Paragraph(f.get("label"), S["sub"]),
          Paragraph("This summary presents key figures from the Foundation's Form 990-PF for the fiscal year ended June 30, 2025. "
                    "The Wexmoor Foundation is fictional; this document is a demonstration and is not an IRS filing.", S["body"]),
          table([["Item", "Amount"], ["Total assets (end of year, fair market value)", f'${f["totalAssets"]}'],
                 ["Grants distributed", f'${f["grantsDistributed"]}'],
                 ["Grants to Early Grades Achievement", f'${r25["earlyGrades"]}'],
                 ["Grants to Educators & Leaders", f'${r25["educators"]}'],
                 ["Number of grants awarded", str(r25["grantCount"])]], [doc.width * 0.65, doc.width * 0.35]),
          Spacer(1, 14),
          Paragraph("Fiscal year: " + SITE["fiscalYear"] + ". Questions about the Foundation's tax return may be directed to " + SITE["email"] + ".", S["body"])]
    doc.build(st)
    return full


def one_pagers():
    md = read_src("impact-plan.md")
    out = []
    reading = section(md, "## Early Grades Achievement Strategic Issue")
    out.append(build_md("readingIssue", None, "Early reading proficiency strategic issue", landscape(letter), "none",
                        text=reading + "\nFrom The Wexmoor Foundation Impact Plan: approved by the Board May 14, 2019; revised August 2025\n"))
    teach = section(md, "### Strategic Issue Logic Model")
    goal = "## Strong Teachers for Every Classroom\n\nIf students from low-income families and students of color have better-prepared beginning teachers and more effective experienced teachers, their academic achievement will increase.\n\n"
    out.append(build_md("logicModel", None, "Strategic issue logic model", landscape(letter), "none",
                        text=goal + teach + "\nFrom The Wexmoor Foundation Impact Plan: approved by the Board May 14, 2019; revised August 2025\n"))
    return out


if __name__ == "__main__":
    made = [
        build_md("outcomes", "outcomes-sought.md", "Guidance for grantseekers on outcomes sought in each focus area"),
        build_md("indirect", "indirect-cost-policy.md", "Board policy on indirect (F&A) costs"),
        build_md("job", "job-profile.md", "Program Officer job profile"),
        build_md("impactPlan", "impact-plan.md", "Foundation strategy and impact plan", landscape(letter), "none"),
        financial_summary(),
        *one_pagers(),
        *[annual_report(r) for r in REPORTS],
    ]
    for m in made:
        print(os.path.relpath(m, ROOT))
