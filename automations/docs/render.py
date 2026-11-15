"""Render a CV or cover letter written in the house markdown format to a styled .docx (and PDF).

The style mirrors the June 2026 GoCardless CSAM CV: Calibri, one A4 page, blue name and
section headings with a rule beneath, grey details, right-aligned dates.

Needs python-docx (pip install python-docx). PDF export needs LibreOffice (soffice).

Usage, from the repo root:
    python3 -m automations.docs.render cv APPLICATION_DIR/cv-v2.md OUT_DIR/Name_CV.docx [--pdf]
    python3 -m automations.docs.render letter APPLICATION_DIR/cover-letter-v2.md OUT_DIR/Name_Letter.docx [--pdf]

CV styles: --style classic (default: blue headings with rules, centred header, 10pt) or --style plain
(black only, no rules, left-aligned, 10.5pt, wider margins: the consulting look Harry prefers).

CV markdown: "# NAME", a contact line, "## SECTION", "### Title | Company | Dates" (or "### Company | Dates" then "#### Role | Dates"),
"*context line*", "- bullet", "**Label:** text", "**Bold line**" and plain paragraphs.
Letter markdown: the first two lines are name and contact; the last line is the signature.
"""
import re
import subprocess
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

FONT = "Calibri"
BLUE = RGBColor(0x1A, 0x52, 0x76)
INK = RGBColor(0x2C, 0x3E, 0x50)
GREY = RGBColor(0x55, 0x55, 0x55)
A4 = (Pt(595.3), Pt(841.9))


def _page(doc, left, right, top, bottom):
    s = doc.sections[0]
    s.page_width, s.page_height = A4
    s.left_margin, s.right_margin, s.top_margin, s.bottom_margin = Pt(left), Pt(right), Pt(top), Pt(bottom)
    normal = doc.styles["Normal"]
    normal.font.name = FONT
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    normal.paragraph_format.space_after = Pt(0)
    normal.paragraph_format.space_before = Pt(0)
    return s


def _para(doc, align=None, before=0, after=0, line=1.0):
    p = doc.add_paragraph()
    f = p.paragraph_format
    f.space_before, f.space_after, f.line_spacing = Pt(before), Pt(after), line
    if align is not None:
        p.alignment = align
    return p


def _inline(p, text, size, color=INK, bold=False, italic=False):
    """Add text, honouring **bold** spans."""
    for i, part in enumerate(re.split(r"\*\*(.+?)\*\*", text)):
        if not part:
            continue
        r = p.add_run(part.replace("\\*", "*"))
        r.font.size, r.font.color.rgb = Pt(size), color
        r.font.name = FONT
        r.bold = bold or i % 2 == 1
        r.italic = italic
    return p


def _rule(p, color="1A5276"):
    pPr = p._p.get_or_add_pPr()
    bdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    for k, v in (("val", "single"), ("sz", "4"), ("space", "1"), ("color", color)):
        bottom.set(qn("w:" + k), v)
    bdr.append(bottom)
    pPr.append(bdr)


BLACK = RGBColor(0, 0, 0)
STYLES = {
    # The June 2026 look: blue name and headings with a rule, grey details, centred header, 10pt.
    "classic": dict(margins=(41, 46, 34, 30), centre=True, head=BLUE, ink=INK, soft=GREY, rule=True,
                    name=16, contact=9, section=11, employer=10.5, role=10, dates=10, body=10, small=9.5,
                    sec_before=7, sec_after=3, emp_before=4, role_before=3, bullet_after=1),
    # Plain consulting look: black only, no rules, left-aligned, larger type, wider margins.
    "plain": dict(margins=(46, 46, 36, 30), centre=False, head=BLACK, ink=BLACK, soft=BLACK, rule=False,
                  name=17, contact=10, section=11.5, employer=10.5, role=10.5, dates=10.5, body=10.5, small=10.5,
                  sec_before=8, sec_after=3, emp_before=5, role_before=4, bullet_after=1),
}


def render_cv(md, out, style="classic"):
    st = STYLES[style]
    doc = Document()
    s = _page(doc, *st["margins"])
    width = s.page_width - s.left_margin - s.right_margin
    head_align = WD_ALIGN_PARAGRAPH.CENTER if st["centre"] else None
    ink, soft = st["ink"], st["soft"]
    lines = [l.rstrip() for l in md.splitlines()]
    contact_done = False
    for line in lines:
        if not line.strip():
            continue
        if line.startswith("# "):
            _inline(_para(doc, head_align), line[2:], st["name"], st["head"], bold=True)
        elif not contact_done and "|" in line and "@" in line:
            _inline(_para(doc, head_align, after=2), line, st["contact"], soft)
            contact_done = True
        elif line.startswith("## "):
            p = _para(doc, before=st["sec_before"], after=st["sec_after"])
            _inline(p, line[3:].upper(), st["section"], st["head"], bold=True)
            if st["rule"]:
                _rule(p)
        elif line.startswith("#### "):
            # A role within the employer above: "#### Title | Dates".
            title, _, dates = (x.strip() for x in line[5:].rpartition("|"))
            p = _para(doc, before=st["role_before"], after=0)
            p.paragraph_format.tab_stops.add_tab_stop(width, WD_TAB_ALIGNMENT.RIGHT)
            _inline(p, title, st["role"], ink, bold=True)
            _inline(p, "\t" + dates, st["dates"] - (0.5 if st["rule"] else 0), soft, italic=True)
        elif line.startswith("### "):
            # "### Title | Company | Dates", or "### Company | Dates" when roles follow as "####".
            parts = [x.strip() for x in line[4:].split("|")]
            title, company, dates = parts[0], " | ".join(parts[1:-1]), parts[-1]
            p = _para(doc, before=st["emp_before"], after=0)
            p.paragraph_format.tab_stops.add_tab_stop(width, WD_TAB_ALIGNMENT.RIGHT)
            _inline(p, title, st["employer"], ink, bold=True)
            if company:
                _inline(p, " | " + company, st["employer"], soft)
            _inline(p, "\t" + dates, st["dates"], soft)
        elif line.startswith("- "):
            p = _para(doc, after=st["bullet_after"])
            f = p.paragraph_format
            f.left_indent, f.first_line_indent = Pt(18), Pt(-10)
            f.tab_stops.add_tab_stop(Pt(18))
            _inline(p, "•\t" + line[2:], st["body"], ink)
        elif line.startswith("*") and line.endswith("*") and not line.startswith("**"):
            _inline(_para(doc, after=1), line.strip("*"), st["small"], soft, italic=True)
        elif re.match(r"^\*\*[^*]+:\*\*", line):
            _inline(_para(doc, after=1), line, st["small"], ink)
        elif line.startswith("**") and line.endswith("**"):
            _inline(_para(doc, before=2), line, st["body"], ink, bold=True)
        else:
            _inline(_para(doc, after=1), line, st["small"] if "|" in line else st["body"], soft if "|" in line else ink)
    doc.save(out)


def render_letter(md, out):
    doc = Document()
    _page(doc, 54, 54, 54, 54)
    blocks = [b.strip() for b in md.strip().split("\n\n") if b.strip()]
    name, contact, rest = blocks[0], blocks[1], blocks[2:]
    _inline(_para(doc), name, 13, INK, bold=True)
    _inline(_para(doc, after=14), contact, 9.5, GREY)
    for i, b in enumerate(rest):
        last = i == len(rest) - 1
        p = _para(doc, after=10, line=1.08)
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        _inline(p, " ".join(b.splitlines()), 10 if i == 0 else 11, INK, bold=last)
    doc.save(out)


def to_pdf(docx_path):
    out_dir = str(Path(docx_path).parent)
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", out_dir, str(docx_path)],
                   check=True, capture_output=True)
    return Path(docx_path).with_suffix(".pdf")


def main(argv):
    if len(argv) < 3 or argv[0] not in ("cv", "letter"):
        print(__doc__)
        return 2
    kind, src, out = argv[0], Path(argv[1]), Path(argv[2])
    out.parent.mkdir(parents=True, exist_ok=True)
    style = argv[argv.index("--style") + 1] if "--style" in argv else "classic"
    if kind == "cv":
        render_cv(src.read_text(encoding="utf-8"), out, style)
    else:
        render_letter(src.read_text(encoding="utf-8"), out)
    print(out)
    if "--pdf" in argv:
        print(to_pdf(out))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
