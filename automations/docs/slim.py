"""Shrink a rendered .docx for uploading to Google Drive.

python-docx's template carries ~800 KB of unused built-in styles. This drops the parts Word and
Google Docs don't need (stylesWithEffects, thumbnail, customXml) and keeps only the styles the
document uses (plus the styles they are based on), so the file is a few KB.

    python3 -m automations.docs.slim <in.docx> <out.docx> [--b64 <out.b64>]
"""
import base64
import re
import sys
import zipfile

DROP = ("word/stylesWithEffects.xml", "docProps/thumbnail.jpeg", "customXml/")


def _used_styles(doc_xml, numbering_xml, styles_xml):
    used = set(re.findall(r'w:(?:pStyle|rStyle|tblStyle) w:val="([^"]+)"', doc_xml + numbering_xml))
    used |= {"Normal", "DefaultParagraphFont", "TableNormal", "NoList"}
    blocks = {sid: block for block, sid in
              re.findall(r'(<w:style\b[^>]*w:styleId="([^"]+)"[^>]*>.*?</w:style>)', styles_xml, re.S)}
    todo = list(used)
    while todo:
        sid = todo.pop()
        b = blocks.get(sid, "")
        for ref in re.findall(r'<w:(?:basedOn|link|next) w:val="([^"]+)"', b):
            if ref not in used:
                used.add(ref)
                todo.append(ref)
    return used


def slim(src, dst):
    zin = zipfile.ZipFile(src)
    doc = zin.read("word/document.xml").decode()
    num = zin.read("word/numbering.xml").decode() if "word/numbering.xml" in zin.namelist() else ""
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            name = item.filename
            if any(name == d or (d.endswith("/") and name.startswith(d)) for d in DROP):
                continue
            data = zin.read(name)
            if name == "word/styles.xml":
                s = data.decode()
                used = _used_styles(doc, num, s)
                s = re.sub(r'<w:latentStyles\b.*?</w:latentStyles>', "", s, flags=re.S)
                s = re.sub(r'<w:style\b[^>]*w:styleId="([^"]+)"[^>]*>.*?</w:style>',
                           lambda m: m.group(0) if m.group(1) in used else "", s, flags=re.S)
                data = s.encode()
            elif name == "[Content_Types].xml":
                s = data.decode()
                s = re.sub(r'<Override PartName="/(?:word/stylesWithEffects\.xml|docProps/thumbnail\.jpeg|customXml/[^"]*)"[^>]*/>', "", s)
                data = s.encode()
            elif name.endswith(".rels"):
                s = data.decode()
                s = re.sub(r'<Relationship [^>]*Target="[^"]*(?:stylesWithEffects\.xml|thumbnail\.jpeg|customXml/[^"]*)"[^>]*/>', "", s)
                data = s.encode()
            zout.writestr(item, data)


if __name__ == "__main__":
    a = sys.argv[1:]
    slim(a[0], a[1])
    if "--b64" in a:
        open(a[a.index("--b64") + 1], "w").write(base64.b64encode(open(a[1], "rb").read()).decode())
