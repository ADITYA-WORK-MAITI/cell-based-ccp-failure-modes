"""
Render REPORT.md to a typeset PDF with a title page.

Uses only matplotlib, already a dependency, so the PDF is reproducible from this
repository with no extra install. Text is measured with real font metrics at
72 dpi, so one display pixel is one point and wrapping is exact.

    python rebuild/md2pdf.py

Writes rebuild/out/REPORT.pdf. Title-page metadata is read from CITATION.cff so
it cannot drift from the citation record.
"""
import os
import re

import matplotlib
matplotlib.use("pdf")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.backends.backend_agg import FigureCanvasAgg  # noqa: E402
from matplotlib.backends.backend_pdf import PdfPages  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE_W, PAGE_H = 8.27, 11.69
ML, MR, MT, MB = 1.00, 1.00, 0.95, 0.85
SERIF, MONO = "DejaVu Serif", "DejaVu Sans Mono"
BODY, LEAD = 9.6, 1.42

TW = (PAGE_W - ML - MR) * 72
TOP = (PAGE_H - MT) * 72
BOT = MB * 72

from matplotlib.font_manager import FontProperties, findfont  # noqa: E402
try:  # matplotlib >= 3.10
    from matplotlib.ft2font import FT2Font, LoadFlags  # noqa: E402
    LOAD_NO_HINTING = LoadFlags.NO_HINTING
except ImportError:  # matplotlib < 3.10
    from matplotlib.ft2font import FT2Font, LOAD_NO_HINTING  # noqa: E402

_FONTS = {}


def _font(size, weight, style, family):
    """Cached FT2Font at the requested size.

    The Agg renderer measures text in whole pixels, so get_window_extent gives
    integer widths and the accumulated rounding closes gaps between words.
    FreeType advance widths are exact floats, which is what the PDF backend
    itself lays out with.
    """
    key = (weight, style, family)
    f = _FONTS.get(key)
    if f is None:
        f = FT2Font(findfont(FontProperties(family=family, weight=weight, style=style)))
        _FONTS[key] = f
    f.set_size(size, 72)
    return f


def w_pt(s, size, weight="normal", style="normal", family=SERIF):
    """Advance width in points, whitespace included."""
    if not s:
        return 0.0
    f = _font(size, weight, style, family)
    f.set_text(s, 0.0, flags=LOAD_NO_HINTING)
    return f.get_width_height()[0] / 64.0


TOKEN = re.compile(r"(\*\*.+?\*\*|`[^`]+`|\*[^*\n]+?\*|\[[^\]\n]+?\]\([^)\s]+\))", re.S)


def runs(text):
    out = []
    for part in TOKEN.split(text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            out.append((part[2:-2], dict(weight="bold")))
        elif part.startswith("`") and part.endswith("`"):
            out.append((part[1:-1], dict(family=MONO, size_mul=0.92)))
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            out.append((part[1:-1], dict(style="italic")))
        elif part.startswith("["):
            m = re.match(r"\[([^\]]+)\]\(([^)\s]+)\)", part)
            out.append((m.group(1), dict(style="italic")))
        else:
            out.append((part, {}))
    return out


class Doc:
    def __init__(self, path):
        self.pdf = PdfPages(path)
        self.fig = None
        self.y = 0.0
        self.pageno = 0

    def _stamp(self):
        self.fig.text(0.5, MB * 0.45 / PAGE_H, str(self.pageno), ha="center",
                      va="center", fontsize=8.2, family=SERIF, color="0.35")
        self.pdf.savefig(self.fig)
        plt.close(self.fig)

    def newpage(self):
        if self.fig is not None:
            self._stamp()
        self.fig = plt.figure(figsize=(PAGE_W, PAGE_H))
        self.pageno += 1
        self.y = TOP

    def space(self, pts):
        self.y -= pts

    def need(self, pts):
        if self.y - pts < BOT:
            self.newpage()

    def put(self, x_pt, s, size, **kw):
        self.fig.text(x_pt / (PAGE_W * 72), self.y / (PAGE_H * 72), s, ha="left",
                      va="baseline", fontsize=size, family=kw.get("family", SERIF),
                      fontweight=kw.get("weight", "normal"),
                      fontstyle=kw.get("style", "normal"), color=kw.get("color", "0.1"))

    def _emit(self, line, xstart, color):
        cx = xstart
        for w_, s_, z_, wd_ in line:
            if w_.strip():
                self.put(cx, w_, z_, color=color,
                         **{k: v for k, v in s_.items() if k != "size_mul"})
            cx += wd_

    def flow(self, text, size=BODY, indent=0.0, lead=LEAD, color="0.1"):
        x0 = ML * 72 + indent
        avail = TW - indent
        line, x, xstart = [], 0.0, x0
        for txt, st in runs(text):
            sz = size * st.get("size_mul", 1.0)
            for word in re.split(r"(\s+)", txt):
                if word == "":
                    continue
                ww = w_pt(word, sz, st.get("weight", "normal"),
                          st.get("style", "normal"), st.get("family", SERIF))
                if not word.strip():
                    if line:
                        line.append((word, st, sz, ww))
                        x += ww
                    continue
                if x + ww > avail and line:
                    self.need(size * lead)
                    self._emit(line, xstart, color)
                    self.space(size * lead)
                    line, x, xstart = [], 0.0, x0
                line.append((word, st, sz, ww))
                x += ww
        if line:
            self.need(size * lead)
            self._emit(line, xstart, color)
            self.space(size * lead)

    def rule(self, color="0.75", lw=0.6):
        yf = self.y / (PAGE_H * 72)
        self.fig.add_artist(plt.Line2D(
            [(ML * 72) / (PAGE_W * 72), (ML * 72 + TW) / (PAGE_W * 72)],
            [yf, yf], color=color, lw=lw, transform=self.fig.transFigure))

    def table(self, rows, size=8.5):
        ncol = max(len(r) for r in rows)
        rows = [r + [""] * (ncol - len(r)) for r in rows]
        raw = [max(w_pt(re.sub(r"[*`]", "", r[c]), size, "bold") for r in rows) + 10
               for c in range(ncol)]
        scale = min(1.0, TW / sum(raw))
        wid = [v * scale for v in raw]
        self.need(size * 1.8 * min(len(rows) + 1, 8))
        self.space(size * 0.7)
        self.rule("0.35", 0.9)
        for i, r in enumerate(rows):
            self.space(size * 1.55)
            self.need(size * 1.8)
            cx = ML * 72 + 2
            for c in range(ncol):
                cell = r[c].replace("`", "").replace("**", "")
                mono = "`" in r[c] or bool(re.fullmatch(r"[\d.\-+e%/ ]+", cell.strip() or "x"))
                fam = MONO if mono else SERIF
                sz = size * (0.92 if mono else 1.0)
                while cell and w_pt(cell, sz, "bold" if i == 0 else "normal", family=fam) > wid[c] - 6:
                    cell = cell[:-1]
                self.put(cx, cell, sz, weight="bold" if i == 0 else "normal", family=fam)
                cx += wid[c]
            if i == 0:
                self.space(size * 0.45)
                self.rule("0.55", 0.7)
        self.space(size * 0.55)
        self.rule("0.35", 0.9)
        self.space(size * 0.9)

    def code(self, lines, size=8.1):
        self.space(4)
        for ln in lines:
            self.need(size * 1.4)
            self.put(ML * 72 + 8, ln.rstrip()[:118], size, family=MONO, color="0.22")
            self.space(size * 1.40)
        self.space(4)

    def close(self):
        if self.fig is not None:
            self._stamp()
        self.pdf.close()


def read_cff(path):
    t = open(path, encoding="utf-8").read()

    def g(p, d=""):
        m = re.search(p, t, re.M)
        return m.group(1).strip().strip('"') if m else d

    # [^\n]* not .* -- a DOTALL dot swallows the rest of the file
    abs_ = g(r"^abstract:\s*>-\n((?:[ ]{2,}[^\n]*\n)+)")
    return {
        "title": g(r'^title:\s*"(.+?)"'),
        "orcid": g(r'orcid:\s*"(.+?)"'),
        "doi": g(r'^doi:\s*"(.+?)"'),
        "version": g(r"^version:\s*(\S+)"),
        "date": g(r'^date-released:\s*"(.+?)"'),
        "repo": g(r'^repository-code:\s*"(.+?)"'),
        "abstract": re.sub(r"\s+", " ", abs_).strip(),
        "author": (g(r"given-names:\s*(\S+)") + " " + g(r"family-names:\s*(\S+)")).strip(),
    }


def title_page(doc, m):
    doc.newpage()
    doc.space(140)
    doc.flow("**" + m["title"] + "**", size=18.5, lead=1.30)
    doc.space(32)
    doc.rule("0.3", 1.1)
    doc.space(30)
    doc.flow("**" + m["author"] + "**", size=12.4)
    doc.space(5)
    doc.flow("ORCID " + m["orcid"].replace("https://orcid.org/", ""), size=10.0, color="0.3")
    doc.space(3)
    doc.flow("Independent research", size=10.0, color="0.3")
    doc.space(26)
    doc.flow("**Abstract.** " + m["abstract"], size=9.9, lead=1.48)
    doc.space(28)
    doc.rule("0.75", 0.6)
    doc.space(18)
    for k, v in (("Version", m["version"]), ("Released", m["date"]), ("DOI", m["doi"]),
                 ("Code", m["repo"].replace("https://", "")),
                 ("Licence", "MIT for code, CC BY 4.0 for text and figures")):
        if not v:
            continue  # omit the row entirely rather than print an empty label
        doc.flow("**" + k + "**   " + v, size=9.2, color="0.2", lead=1.52)
    doc.space(16)
    doc.flow("This PDF is generated from `REPORT.md` by `rebuild/md2pdf.py`. The markdown "
             "file is authoritative. Every number is traceable through "
             "`docs/TRACEABILITY.md`.", size=8.6, color="0.4", lead=1.45)


def render(md_path, out_path, cff_path):
    m = read_cff(cff_path)
    src = open(md_path, encoding="utf-8").read()
    i = src.find("\n## ")
    body = src[i + 1:] if i > 0 else src
    doc = Doc(out_path)
    title_page(doc, m)
    doc.newpage()
    lines = body.split("\n")
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("```"):
            blk = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                blk.append(lines[i])
                i += 1
            i += 1
            doc.code(blk)
            continue
        if re.match(r"^\|.*\|\s*$", ln):
            rows = []
            while i < len(lines) and re.match(r"^\|.*\|\s*$", lines[i]):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c or "-") for c in cells):
                    rows.append(cells)
                i += 1
            doc.table(rows)
            continue
        if ln.startswith("### "):
            doc.need(44)
            doc.space(13)
            doc.flow("**" + ln[4:] + "**", size=10.8, lead=1.32)
            doc.space(4)
            i += 1
            continue
        if ln.startswith("## "):
            doc.need(60)
            doc.space(19)
            doc.flow("**" + ln[3:] + "**", size=13.2, lead=1.30)
            doc.space(6)
            doc.rule("0.8", 0.5)
            doc.space(9)
            i += 1
            continue
        if ln.startswith("# "):
            i += 1
            continue
        if re.match(r"^\s*[-*]\s+", ln):
            doc.flow("\u2022  " + re.sub(r"^\s*[-*]\s+", "", ln), indent=12, lead=1.38)
            doc.space(2.0)
            i += 1
            continue
        if re.match(r"^\s*\d+\.\s+", ln):
            doc.flow(ln.strip(), indent=12, lead=1.38)
            doc.space(2.0)
            i += 1
            continue
        if ln.startswith(">"):
            doc.flow(re.sub(r"^>\s?", "", ln), indent=16, color="0.3", lead=1.40)
            doc.space(1.5)
            i += 1
            continue
        if ln.strip() in ("", "---"):
            if ln.strip() == "":
                doc.space(5.0)
            i += 1
            continue
        para = [ln]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(
                r"^(#{1,3} |\||```|>|\s*[-*]\s|\s*\d+\.\s|---$)", lines[i]):
            para.append(lines[i])
            i += 1
        doc.flow(" ".join(x.strip() for x in para), lead=LEAD)
        doc.space(3.0)
    doc.close()
    return doc.pageno


if __name__ == "__main__":
    out = os.path.join(ROOT, "rebuild", "out", "REPORT.pdf")
    n = render(os.path.join(ROOT, "REPORT.md"), out, os.path.join(ROOT, "CITATION.cff"))
    print("wrote " + os.path.relpath(out, ROOT) + "  (" + str(n) + " pages, "
          + str(os.path.getsize(out)) + " bytes)")
