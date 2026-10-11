"""Generate the retro-desktop SVG assets for the GitHub profile README."""
import base64, io, os
from fontTools.ttLib import TTFont
from fontTools import subset
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FS = os.path.join(HERE, "fonts")
FONTS = {
    "pix":  (f"{FS}/press-start-2p-latin-400-normal.woff", "PressStart"),
    "mono": (f"{FS}/jetbrains-mono-latin-500-normal.woff", "JBMono"),
    "head": (f"{FS}/space-grotesk-latin-700-normal.woff", "GroteskBold"),
    "body": (f"{FS}/space-grotesk-latin-500-normal.woff", "GroteskMed"),
    "vt":   (f"{FS}/vt323-latin-400-normal.woff", "VT323"),
}
OUT = os.path.join(ROOT, "assets")
os.makedirs(OUT, exist_ok=True)

PAPER, PAPER2, INK, MUTED = "#F3EBDD", "#FBF6EC", "#1B1A17", "#4A463E"
ORANGE, MUSTARD, TEAL, RUST = "#E4572E", "#F2A541", "#2A7F7B", "#9C3D1F"

_tt = {k: TTFont(v[0]) for k, v in FONTS.items()}
CHARS = "".join(chr(c) for c in range(32, 127)) + "·—×"


def width(text, font, size, ls=0):
    t = _tt[font]; cm = t.getBestCmap(); hm = t["hmtx"]; upm = t["head"].unitsPerEm
    w = sum(hm[cm.get(ord(c), cm[ord("?")])][0] for c in text)
    return w / upm * size + ls * len(text)


def wrap(text, font, size, maxw):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if width(trial, font, size) <= maxw:
            cur = trial
        else:
            lines.append(cur); cur = word
    lines.append(cur)
    return lines


_cache = {}
def font_face(key):
    if key not in _cache:
        path, fam = FONTS[key]
        f = TTFont(path)
        opts = subset.Options(); opts.flavor = "woff2"; opts.layout_features = ["kern"]
        sub = subset.Subsetter(opts); sub.populate(text=CHARS); sub.subset(f)
        buf = io.BytesIO(); f.flavor = "woff2"; f.save(buf)
        b64 = base64.b64encode(buf.getvalue()).decode()
        _cache[key] = f"@font-face{{font-family:{fam};src:url(data:font/woff2;base64,{b64}) format('woff2');}}"
    return _cache[key]


def T(x, y, text, font, size, fill=INK, anchor="start", ls=0, extra=""):
    fam = FONTS[font][1]
    return (f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" letter-spacing="{ls}" {extra}>{escape(text)}</text>')


def svg(w, h, body, fonts, css="", title=""):
    faces = "".join(font_face(f) for f in fonts)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">'
            f'<title>{escape(title)}</title>'
            f'<defs><style>{faces}{css}'
            '@media (prefers-reduced-motion: reduce){*{animation:none!important}}'
            '</style>'
            '<pattern id="stripes" width="4" height="5" patternUnits="userSpaceOnUse"><rect width="4" height="2" fill="#1B1A17"/></pattern>'
            '<pattern id="dither" width="6" height="6" patternUnits="userSpaceOnUse"><rect width="1.6" height="1.6" fill="#1B1A17" opacity=".16"/><rect x="3" y="3" width="1.6" height="1.6" fill="#1B1A17" opacity=".16"/></pattern>'
            f'</defs>{body}</svg>')


def window(x, y, w, h, title, shadow=8, body_fill=PAPER2, bar=34):
    """Retro window: hard shadow, striped title bar, close box, centred title."""
    tw = width(title, "pix", 13) + 28
    cx = x + w / 2
    return (f'<rect x="{x+shadow}" y="{y+shadow}" width="{w}" height="{h}" fill="{INK}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{body_fill}" stroke="{INK}" stroke-width="3"/>'
            f'<rect x="{x+8}" y="{y+9}" width="{w-16}" height="{bar-18}" fill="url(#stripes)"/>'
            f'<line x1="{x}" y1="{y+bar}" x2="{x+w}" y2="{y+bar}" stroke="{INK}" stroke-width="3"/>'
            f'<rect x="{x+16}" y="{y+7}" width="{bar-14}" height="{bar-14}" fill="{PAPER2}" stroke="{INK}" stroke-width="2.5"/>'
            f'<rect x="{x+12}" y="{y+5}" width="{bar-6}" height="{bar-10}" fill="{PAPER2}" opacity="0"/>'
            f'<rect x="{cx - tw/2}" y="{y+4}" width="{tw}" height="{bar-8}" fill="{PAPER2}"/>'
            + T(cx, y + bar/2 + 6.5, title, "pix", 13, anchor="middle"))


def floppy(x, y, s, body, label, rot, cls=""):
    """Generic 3.5-inch floppy disk, s = side length."""
    sh = s * 0.5; lw = s * 0.72
    return (f'<g class="{cls}"><g transform="translate({x} {y}) rotate({rot})">'
            f'<rect x="7" y="7" width="{s}" height="{s}" rx="6" fill="{INK}"/>'
            f'<path d="M0 6 Q0 0 6 0 H{s-16} L{s} 16 V{s-6} Q{s} {s} {s-6} {s} H6 Q0 {s} 0 {s-6} Z" fill="{body}" stroke="{INK}" stroke-width="3"/>'
            f'<rect x="{(s-sh)/2}" y="-1" width="{sh}" height="{s*0.3}" fill="#C9C3B6" stroke="{INK}" stroke-width="3"/>'
            f'<rect x="{(s-sh)/2 + sh*0.62}" y="{s*0.05}" width="{sh*0.18}" height="{s*0.2}" fill="{INK}"/>'
            f'<rect x="{(s-lw)/2}" y="{s*0.42}" width="{lw}" height="{s*0.5}" fill="{PAPER2}" stroke="{INK}" stroke-width="3"/>'
            f'<line x1="{(s-lw)/2+12}" y1="{s*0.56}" x2="{(s+lw)/2-12}" y2="{s*0.56}" stroke="{INK}" stroke-width="2" opacity=".35"/>'
            + T(s/2, s*0.79, label, "pix", min(14, (lw - 16) / width(label, "pix", 1)), anchor="middle") + '</g></g>')


# ---------------------------------------------------------------- Momo the pixel panda
FUR = "#FFFDF7"; BLUSH = "#F3A28A"; BAMBOO = "#6E9A3C"; BAMBOO_D = "#45692A"
PANDA_BASE = [
    ".KK..........KK.",
    "KKKK.KKKKKK.KKKK",
    "KKKKKWWWWWWKKKKK",
    ".KKWWWWWWWWWWKK.",
    "..KWWWWWWWWWWK..",
    ".KWWKKWWWWKKWWK.",
    ".KWKKGKWWKGKKWK.",
    ".KWKKKKWWKKKKWK.",
    ".KWWKKWKKWKKWWK.",
    ".KPWWWWWKWWWWPK.",
    "..KWWWWWWWWWWK..",
    "...KKWWWWWWKK...",
]
BODY = {
    "sit": ["..KKKKWWWWKKKK..", ".KKKKWWWWWWKKKK.", ".KKKWWWWWWWWKKK.", "..KKWWWWWWWWKK..",
            "..KKKKKKKKKKKK..", ".KKKKK....KKKKK."],
    "walkA": ["..KKKKWWWWKKKK..", ".KKKKWWWWWWKKKK.", ".KKKWWWWWWWWKKK.", "..KKWWWWWWWWKK..",
              "..KKKKKKKKKKKK..", "..KKKK....KK....", "..KKKK.........."],
    "walkB": ["..KKKKWWWWKKKK..", ".KKKKWWWWWWKKKK.", ".KKKWWWWWWWWKKK.", "..KKWWWWWWWWKK..",
              "..KKKKKKKKKKKK..", "....KK....KKKK..", "..........KKKK.."],
    "waveA": ["..KKKKWWWWKKKK..", ".KKKKWWWWWWKKKK.", ".KKKWWWWWWWWKKK.", "..KKWWWWWWWWKK..",
              "..KKKKKKKKKKKK..", ".KKKKK....KKKKK."],
}
WAVE_UP = ["..............KK", ".............KKK", "............KKK.", "...........KKK..",
           "..KKKKWWWWKKKK..", ".KKKKWWWWWWW....", ".KKKWWWWWWWW....", "..KKWWWWWWWWKK..",
           "..KKKKKKKKKKKK..", ".KKKKK....KKKKK."]
PCOL = {"K": INK, "W": FUR, "P": BLUSH, "G": FUR}

def pixels(rows, x, y, s, skip=""):
    """Rows of pixel chars -> merged horizontal-run rects."""
    out = []
    for r, row in enumerate(rows):
        c = 0
        while c < len(row):
            ch = row[c]
            if ch == "." or ch in skip:
                c += 1; continue
            e = c
            while e < len(row) and row[e] == ch:
                e += 1
            out.append(f'<rect x="{x+c*s}" y="{y+r*s}" width="{(e-c)*s}" height="{s}" fill="{PCOL[ch]}"/>')
            c = e
    return "".join(out)

def bamboo(x, y, s, h=10):
    out = [f'<rect x="{x}" y="{y}" width="{s*2}" height="{s*h}" fill="{BAMBOO}" stroke="{INK}" stroke-width="{s*0.4}"/>']
    for k in range(3, h, 4):
        out.append(f'<rect x="{x-s*0.3}" y="{y+k*s}" width="{s*2.6}" height="{s*0.8}" fill="{BAMBOO_D}"/>')
    out.append(f'<path d="M{x} {y+s*2} q{-s*2.5} {-s*2} {-s*4} {-s*1}" stroke="{BAMBOO}" stroke-width="{s*1.4}" fill="none" stroke-linecap="round"/>')
    return "".join(out)

PANDA_CSS = (".blink{animation:blink2 4.2s steps(1) infinite}@keyframes blink2{0%,92%{opacity:1}93%,97%{opacity:0}98%{opacity:1}}"
             ".bob{animation:bob2 1.1s steps(2) infinite}@keyframes bob2{50%{transform:translateY(-4px)}}")

def panda(x, y, s, pose="sit", bob=True, extra=""):
    """Momo, 16 px wide pixel panda. pose: sit | walk | wave."""
    head = pixels(PANDA_BASE, 0, 0, s, skip="G")
    glints = f'<g class="blink">{pixels([r.replace("K", ".").replace("W", ".").replace("P", ".") for r in PANDA_BASE], 0, 0, s)}</g>'
    by = len(PANDA_BASE) * s
    if pose == "walk":
        body = (f'<g class="legA">{pixels(BODY["walkA"], 0, by, s)}</g>'
                f'<g class="legB">{pixels(BODY["walkB"], 0, by, s)}</g>')
    elif pose == "wave":
        body = (f'<g class="armA">{pixels(BODY["waveA"], 0, by, s)}</g>'
                f'<g class="armB">{pixels(WAVE_UP, 0, by - 4 * s, s)}</g>')
    else:
        body = pixels(BODY["sit"], 0, by, s)
    shadow = f'<ellipse cx="{8*s}" cy="{by + 6.3*s}" rx="{7*s}" ry="{1.1*s}" fill="{INK}" opacity=".18"/>'
    inner = f'<g class="{"bob" if bob else ""}">{head}{glints}{body}{extra}</g>'
    return f'<g transform="translate({x} {y})">{shadow}{inner}</g>'

def bubble(x, y, msgs, cycle, anim="say", tail=None):
    """Speech bubble whose text cycles through msgs."""
    w = max(width(m, "pix", 12) for m in msgs) + 32
    n = len(msgs); css = []
    tx = (x + w - 46) if tail is None else tail
    out = [f'<rect x="{x+5}" y="{y+5}" width="{w}" height="40" fill="{INK}"/>',
           f'<rect x="{x}" y="{y}" width="{w}" height="40" fill="{PAPER2}" stroke="{INK}" stroke-width="3"/>',
           f'<path d="M{tx} {y+38} l14 16 l4 -16 z" fill="{PAPER2}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>',
           f'<rect x="{tx+2}" y="{y+35}" width="20" height="5" fill="{PAPER2}"/>']
    for i, m in enumerate(msgs):
        a, b = i / n * 100, (i + 1) / n * 100
        if i == 0:
            kf = f"0%,{b-0.5:.2f}%{{opacity:1}}{b-0.4:.2f}%,100%{{opacity:0}}"
        else:
            kf = f"0%,{a-0.4:.2f}%{{opacity:0}}{a-0.3:.2f}%,{b-0.5:.2f}%{{opacity:1}}{b-0.4:.2f}%,100%{{opacity:0}}"
        css.append(f"@keyframes {anim}{i}{{{kf}}}.{anim}{i}{{animation:{anim}{i} {cycle}s infinite}}")
        out.append(T(x + w / 2, y + 26, m, "pix", 12, INK, anchor="middle",
                     extra=f'class="{anim}{i}"' + ('' if i == 0 else ' opacity="0"')))
    return "".join(out), "".join(css), w


# ---------------------------------------------------------------- stack inventory
import json
ICONS = json.load(open(os.path.join(HERE, "icons.json")))
STACK = [
    ("DOMAINS", [("dom-ml", "ML", "hybrid-search ranking and classic models"),
                 ("dom-dl", "DL", "CNN-Transformer threat detector, cardiac models"),
                 ("dom-nlp", "NLP", "RAG, Text-to-SQL, LLM extraction and agents"),
                 ("dom-cv", "Vision", "drowsiness detection, cardiac segmentation")]),
    ("LANGUAGES", [("python", "Python", "agents, RAG, vision models, tooling"),
                   ("openjdk", "Java", "object-oriented programming and DSA"),
                   ("gnubash", "Bash", "the Oracle VM grabber and server scripts")]),
    ("AI / ML TOOLS", [("pytorch", "PyTorch", "CNN-Transformer threat detector, cardiac models"),
                       ("mediapipe", "MediaPipe", "face mesh for drowsiness detection"),
                       ("ollama", "Ollama", "local LLMs for dev and the FNOL agent"),
                       ("groq", "Groq", "fast inference for Text-to-SQL and Salvage"),
                       ("qdrant", "Qdrant", "few-shot example retrieval for Text-to-SQL")]),
    ("BACKEND & DATA", [("fastapi", "FastAPI", "APIs for RAG, resume builder, interview Q&A"),
                        ("pydantic", "Pydantic", "strict schemas so LLM output stays valid"),
                        ("mysql", "MySQL", "resume builder and interview Q&A data"),
                        ("mongodb", "MongoDB", "the Salvage ledger and CTI dashboard"),
                        ("redis", "Redis", "query cache and background job queues")]),
    ("WEB", [("html5", "HTML", "page structure for web UIs"),
             ("css", "CSS", "styling, and every animation on this page"),
             ("javascript", "JavaScript", "browser logic for web frontends"),
             ("typescript", "TypeScript", "the Salvage dashboard and web frontends"),
             ("react", "React", "frontends for Salvage and the platforms")]),
    ("TOOLS & OPS", [("streamlit", "Streamlit", "quick demo UIs for the agents"),
                     ("docker", "Docker", "deploys for the interview Q&A platform"),
                     ("linux", "Linux", "servers and VPS deploys"),
                     ("git", "Git", "version control for everything")]),
]
FULL = {"dom-ml": "Machine Learning", "dom-dl": "Deep Learning", "dom-nlp": "Natural Language Processing", "dom-cv": "Computer Vision"}
GCOL = {"DOMAINS": INK, "LANGUAGES": ORANGE, "AI / ML TOOLS": TEAL, "BACKEND & DATA": MUSTARD,
        "WEB": RUST, "TOOLS & OPS": "#6B6458"}

def domain_icon(slug, cx, cy, size):
    k = size / 40; x0, y0 = cx - 20 * k, cy - 20 * k
    def P(x, y): return f"{x0 + x*k:.1f} {y0 + y*k:.1f}"
    sw = 2.6 * k
    if slug == "dom-ml":
        out = [f'<path d="M{P(3,3)} L{P(3,37)} L{P(38,37)}" stroke="{INK}" stroke-width="{sw}" fill="none"/>',
               f'<path d="M{P(6,32)} L{P(36,8)}" stroke="{ORANGE}" stroke-width="{sw}" fill="none"/>']
        for (x, y) in [(9, 26), (14, 30), (17, 20), (23, 22), (26, 13), (31, 16), (34, 7)]:
            out.append(f'<rect x="{x0+(x-2)*k:.1f}" y="{y0+(y-2)*k:.1f}" width="{4*k:.1f}" height="{4*k:.1f}" fill="{TEAL}"/>')
        return "".join(out)
    if slug == "dom-dl":
        L = [[(5, 9), (5, 20), (5, 31)], [(20, 5), (20, 15), (20, 25), (20, 35)], [(35, 14), (35, 26)]]
        out = []
        for a, b2 in ((0, 1), (1, 2)):
            for (xa, ya) in L[a]:
                for (xb, yb) in L[b2]:
                    out.append(f'<path d="M{P(xa,ya)} L{P(xb,yb)}" stroke="{INK}" stroke-width="{1.2*k:.1f}" opacity=".55"/>')
        cols = [TEAL, ORANGE, MUSTARD]
        for li, layer in enumerate(L):
            for (x, y) in layer:
                out.append(f'<circle cx="{x0+x*k:.1f}" cy="{y0+y*k:.1f}" r="{3.6*k:.1f}" fill="{cols[li]}" stroke="{INK}" stroke-width="{1.6*k:.1f}"/>')
        return "".join(out)
    if slug == "dom-nlp":
        return (f'<path d="M{P(3,5)} H{P(37,5)[:0]}{x0+37*k:.1f} V{y0+27*k:.1f} H{x0+16*k:.1f} L{P(8,35)} V{y0+27*k:.1f} H{x0+3*k:.1f} Z" '
                f'fill="{PAPER}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>'
                + T(cx, y0 + 22 * k, "Aa", "head", 15 * k, ORANGE, anchor="middle"))
    if slug == "dom-cv":
        return (f'<path d="M{P(2,20)} Q{P(20,2)} {P(38,20)} Q{P(20,38)} {P(2,20)} Z" fill="{PAPER}" stroke="{INK}" stroke-width="{sw}"/>'
                f'<circle cx="{cx}" cy="{cy}" r="{8*k:.1f}" fill="{TEAL}" stroke="{INK}" stroke-width="{2*k:.1f}"/>'
                f'<circle cx="{cx}" cy="{cy}" r="{3.4*k:.1f}" fill="{INK}"/>'
                f'<rect x="{cx+2*k:.1f}" y="{cy-5*k:.1f}" width="{2.6*k:.1f}" height="{2.6*k:.1f}" fill="{PAPER2}"/>')
    return ""

def logo(slug, cx, cy, size):
    if slug.startswith("dom-"):
        return domain_icon(slug, cx, cy, size)
    if slug == "groq":
        return T(cx, cy + 9, "groq", "head", 30, "#F55036", anchor="middle", ls=-1)
    ic = ICONS[slug]; col = {"openjdk": "#E76F00"}.get(slug, "#" + ic["hex"])
    size *= {"mysql": 1.4}.get(slug, 1)
    r, g, b_ = (int(col[i:i+2], 16) for i in (1, 3, 5))
    if 0.299 * r + 0.587 * g + 0.114 * b_ > 170:   # too light on paper -> ink
        col = INK
    sc = size / 24
    return (f'<g transform="translate({cx - size/2} {cy - size/2}) scale({sc})">'
            f'<path d="{ic["path"]}" fill="{col}"/></g>')

def stack():
    W, H = 1280, 756
    TS, STEP, GG = 104, 120, 30
    x0 = 28
    items = []           # (slug, name, desc, x, y)
    rows = [STACK[:2], STACK[2:4], STACK[4:]]
    labels = []
    for r, groups in enumerate(rows):
        y = 128 + r * 156
        x = x0
        for gname, its in groups:
            labels.append((gname, x, y - 16))
            for slug, name, desc in its:
                items.append((slug, name, desc, x, y)); x += STEP
            x += GG - (STEP - TS) + (STEP - TS)  # group gap
    N = len(items); D = 1.6; TT = N * D
    css = [PANDA_CSS,
           ".legA{animation:legA .5s steps(1) infinite}.legB{animation:legB .5s steps(1) infinite}"
           "@keyframes legA{50%{opacity:0}}@keyframes legB{0%{opacity:0}50%{opacity:1}}"
           f".walk{{animation:walk 17s linear infinite}}@keyframes walk{{from{{transform:translateX(-120px)}}to{{transform:translateX({W+20}px)}}}}"
           ".cur{animation:blink 1.05s steps(1) infinite}@keyframes blink{50%{opacity:0}}"]
    # selector keyframes
    sel = []
    for k, (_, _, _, x, y) in enumerate(items):
        a, b2 = k / N * 100, (k + 1) / N * 100
        sel.append(f"{a:.3f}%,{b2-0.001:.3f}%{{transform:translate({x-8}px,{y-14}px)}}")
    css.append(f"@keyframes sel{{{''.join(sel)}}}.sel{{animation:sel {TT}s infinite}}")
    css.append(f".fill{{animation:fill {TT}s steps({N}) infinite;transform-box:fill-box;transform-origin:0 0}}@keyframes fill{{from{{transform:scaleX({1/N:.4f})}}to{{transform:scaleX(1.0555)}}}}")

    def slot(name, k, prop_on, prop_off):
        a, b2 = k / N * 100, (k + 1) / N * 100
        if k == 0:
            kf = f"0%,{b2-0.01:.3f}%{{{prop_on}}}{b2:.3f}%,100%{{{prop_off}}}"
        else:
            kf = f"0%,{a-0.01:.3f}%{{{prop_off}}}{a:.3f}%,{b2-0.01:.3f}%{{{prop_on}}}{b2:.3f}%,100%{{{prop_off}}}"
        css.append(f"@keyframes {name}{k}{{{kf}}}.{name}{k}{{animation:{name}{k} {TT}s infinite}}")

    b = [window(4, 4, W - 18, H - 18, "modules.sys")]
    b.append(T(x0, 74, "INVENTORY", "pix", 15, INK))
    b.append(T(x0 + width("INVENTORY", "pix", 15) + 16, 74, f"{N} modules  ·  auto-scan on", "mono", 16, MUTED))
    gcol = GCOL
    for gname, x, y in labels:
        b.append(f'<rect x="{x}" y="{y-10}" width="10" height="10" fill="{gcol[gname]}"/>')
        b.append(T(x + 16, y, gname, "pix", 11, INK))
    for k, (slug, name, desc, x, y) in enumerate(items):
        slot("lift", k, "transform:translateY(-6px)", "transform:translateY(0)")
        b.append(f'<rect x="{x+5}" y="{y+5}" width="{TS}" height="{TS}" fill="{INK}"/>')
        b.append(f'<g class="lift{k}"><rect x="{x}" y="{y}" width="{TS}" height="{TS}" fill="{PAPER2}" stroke="{INK}" stroke-width="2.5"/>'
                 + logo(slug, x + TS / 2, y + 42, 40) + T(x + TS / 2, y + 90, name, "mono", 13, INK, anchor="middle") + '</g>')
    # selector frame (drawn above tiles)
    b.append(f'<g class="sel"><rect x="0" y="0" width="{TS+16}" height="{TS+16}" fill="none" stroke="{ORANGE}" stroke-width="4" stroke-dasharray="22 10"/>'
             f'<path d="M{(TS+16)/2-9} -14 h18 l-9 10 z" fill="{ORANGE}"/></g>')
    # scan meter in the header
    bw = 230; mx = W - 18 - 30 - bw; my = 58
    b.append(f'<rect x="{mx}" y="{my}" width="{bw}" height="20" fill="{PAPER2}" stroke="{INK}" stroke-width="2"/>')
    b.append(f'<rect class="fill" x="{mx+2}" y="{my+2}" width="{(bw-4)/1.0555:.1f}" height="16" fill="{TEAL}"/>')
    b.append(T(mx - 26 - width(f"{N:02d} / {N} OK", "mono", 15), my + 15, "SCAN", "pix", 11, INK, anchor="end"))
    for k in range(N):
        slot("cnt", k, "opacity:1", "opacity:0")
        b.append(T(mx - 10, my + 15, f"{k+1:02d} / {N} OK", "mono", 15, TEAL if k == N - 1 else INK, anchor="end",
                   extra=f'class="cnt{k}"' + ('' if k == 0 else ' opacity="0"')))
    # status bar synced to the selector
    sy = 584
    b.append(f'<rect x="{x0}" y="{sy}" width="{W-18-x0-24}" height="50" fill="{PAPER2}" stroke="{INK}" stroke-width="2.5"/>')
    b.append(f'<rect x="{x0}" y="{sy}" width="128" height="50" fill="{INK}"/>')
    b.append(T(x0 + 64, sy + 31, "SELECTED", "pix", 12, PAPER2, anchor="middle"))
    for k, (slug, name, desc, x, y) in enumerate(items):
        slot("cap", k, "opacity:1", "opacity:0")
        name = FULL.get(slug, name)
        nw = width(name, "head", 21)
        b.append(f'<g class="cap{k}"' + ('' if k == 0 else ' opacity="0"') + '>'
                 + T(x0 + 148, sy + 33, name, "head", 21, INK)
                 + T(x0 + 160 + nw, sy + 32, "→  " + desc if False else "· " + desc, "body", 19, MUTED) + '</g>')
    # floor + Momo walking
    fy = 734
    b.append(f'<defs><clipPath id="lane"><rect x="7" y="{fy-92}" width="{W-24}" height="94"/></clipPath></defs>')
    b.append(f'<line x1="{x0}" y1="{fy-3}" x2="{W-18-24}" y2="{fy-3}" stroke="{INK}" stroke-width="2" stroke-dasharray="4 6" opacity=".4"/>')
    b.append(f'<g clip-path="url(#lane)"><g class="walk">{panda(0, fy - 98, 5, "walk")}</g></g>')
    return svg(W, H, "".join(b), ["pix", "head", "body", "mono"], "".join(css),
               "Tech stack: " + ", ".join(i[1] for i in items))


# ---------------------------------------------------------------- about
KW, CLS, STR, NUM, CMT = TEAL, ORANGE, RUST, "#B9771E", "#8A8375"
ABOUT_CODE = [
    [("from ", KW), ("pydantic ", INK), ("import ", KW), ("BaseModel", INK)],
    [],
    [("class ", KW), ("Kamlesh", CLS), ("(BaseModel):", INK)],
    [("    role: ", INK), ("str", KW), ("      = ", INK), ('"AI/ML Engineer"', STR)],
    [("    studying: ", INK), ("str", KW), ("  = ", INK), ('"B.Tech AI & ML, Jain University"', STR)],
    [("    cgpa: ", INK), ("float", KW), ("    = ", INK), ("9.7", NUM)],
    [("    last_role: ", INK), ("str", KW), (" = ", INK), ('"SWE Intern @ Dhee Coding Lab"', STR)],
    [("    shipped: ", INK), ("str", KW), ("   = ", INK), ('"the company\'s first AI integrations"', STR)],
    [("    builds: ", INK), ("list", KW), ("   = ", INK), ('["RAG", "Text-to-SQL", "Agents", "Vision"]', STR)],
    [("    roots: ", INK), ("str", KW), ("     = ", INK), ('"medical imaging research"', STR)],
    [],
    [("    def ", KW), ("rule", CLS), ("(self) -> ", INK), ("str", KW), (":", INK)],
    [("        return ", KW), ('"LLMs understand. Rules decide."', STR)],
]

def about():
    W, H = 1280, 500
    css = [PANDA_CSS, ".cur{animation:blink 1.05s steps(1) infinite}@keyframes blink{50%{opacity:0}}"
           "@keyframes ln{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:none}}"
           ".dot{animation:dot 1.6s steps(1) infinite}@keyframes dot{50%{opacity:.25}}"]
    b = [window(4, 44, 790, 440, "about.py")]
    gx, cx, ly, lh, fs = 22, 74, 44 + 34 + 40, 26.5, 16.5
    b.append(f'<rect x="8" y="{44+36}" width="48" height="{440-40}" fill="{PAPER}"/>')
    b.append(f'<line x1="56" y1="{44+36}" x2="56" y2="{44+438}" stroke="{INK}" stroke-width="2" opacity=".25"/>')
    for i, segs in enumerate(ABOUT_CODE):
        y = ly + i * lh
        parts = [T(gx + 26, y, f"{i+1:>2}", "mono", 14, CMT, anchor="end")]
        x = cx
        for txt, col in segs:
            parts.append(T(x, y, txt, "mono", fs, col, extra='xml:space="preserve"'))
            x += width(txt, "mono", fs)
        b.append(f'<g class="l{i}">' + "".join(parts) + "</g>")
        last_x, last_y = x, y
    b.append(f'<rect class="cur" x="{last_x + 4}" y="{last_y - 15}" width="9" height="19" fill="{ORANGE}"/>')
    # dialog
    dx, dy, dw, dh = 826, 132, 430, 352
    b.append(window(dx, dy, dw, dh, "About This Human"))
    b.append(panda(dx + dw - 120, dy - 94, 5, "sit"))
    px = dx + 30
    b.append(T(px, dy + 88, "Kamlesh OS", "head", 38, INK, ls=-1))
    b.append(T(px, dy + 114, "version 9.7  (CGPA build)", "mono", 15, MUTED))
    b.append(f'<line x1="{px}" y1="{dy+134}" x2="{dx+dw-30}" y2="{dy+134}" stroke="{INK}" stroke-width="2" stroke-dasharray="3 4"/>')
    rows = [("BASED IN", "Bengaluru, India"), ("EDUCATION", "B.Tech AI & ML, semester 5"),
            ("LAST JOB", "SWE Intern, Dhee Coding Lab"), ("FOCUS", "LLM systems that hold up")]
    for i, (k, v) in enumerate(rows):
        y = dy + 166 + i * 34
        b.append(T(px, y, k, "pix", 10, MUTED))
        b.append(T(px + 118, y + 2, v, "body", 17, INK))
    sy = dy + dh - 64
    st = "OPEN TO AI/ML INTERNSHIPS"
    sw = width(st, "pix", 11) + 54
    b.append(f'<rect x="{px}" y="{sy}" width="{sw}" height="36" fill="{TEAL}" stroke="{INK}" stroke-width="2.5"/>')
    b.append(f'<rect class="dot" x="{px+14}" y="{sy+13}" width="10" height="10" fill="{PAPER2}"/>')
    b.append(T(px + 36, sy + 24, st, "pix", 11, PAPER2))
    return svg(W, H, "".join(b), ["pix", "head", "body", "mono"], "".join(css),
               "About Kamlesh: AI/ML Engineer, B.Tech AI & ML at Jain University, CGPA 9.7, former SWE intern at Dhee Coding Lab, open to AI/ML internships")


# ---------------------------------------------------------------- stats (data/stats.json, refreshed by GitHub Actions)
import datetime as _dt
HEAT = ["#E6DCCA", "#F2C46D", "#F2A541", "#E4572E", "#9C3D1F"]
LANGC = [TEAL, ORANGE, MUSTARD, RUST, "#6B6458"]

def stats(path=None):
    path = path or os.path.join(ROOT, "data", "stats.json")
    d = json.load(open(path))
    cal = d["calendar"]; counts = [c for _, c in cal]
    active = sum(1 for c in counts if c)
    best = max(cal, key=lambda x: x[1])
    streak = cur = 0
    for _, c in cal:
        cur = cur + 1 if c else 0; streak = max(streak, cur)
    W, H = 1280, 420
    css = [".cur{animation:blink 1.05s steps(1) infinite}@keyframes blink{50%{opacity:0}}"]
    b = [window(4, 4, W - 18, H - 18, "player_stats.exe")]
    x0 = 32
    b.append(f'<g class="cur">' + T(x0, 80, "1UP", "pix", 15, ORANGE) + "</g>")
    b.append(T(x0 + 62, 80, d["login"].upper(), "pix", 15, INK))
    bd = _dt.date.fromisoformat(best[0])
    scores = [("CONTRIBUTIONS", str(d["total"])), ("ACTIVE DAYS", str(active)),
              ("LONGEST STREAK", f"{streak}d"), ("BEST DAY", f"{best[1]}"),
              ("PUBLIC REPOS", str(d["repos"]))]
    lw = 380
    for i, (k, v) in enumerate(scores):
        y = 132 + i * 46
        kw = width(k, "pix", 13); vw = width(v, "head", 26)
        b.append(T(x0, y, k, "pix", 13, INK))
        b.append(f'<line x1="{x0+kw+10}" y1="{y-2}" x2="{x0+lw-vw-12}" y2="{y-2}" stroke="{INK}" stroke-width="3" stroke-dasharray="3 6" opacity=".45"/>')
        b.append(T(x0 + lw, y + 4, v, "head", 26, ORANGE if i == 0 else INK, anchor="end"))
    b.append(T(x0, 132 + 4 * 46 + 30, f"best day: {bd.strftime('%d %b %Y').lower()}", "mono", 14, MUTED))
    # heatmap
    hx, hy, cs, gp = 470, 100, 12, 2.4
    start = _dt.date.fromisoformat(cal[0][0])
    off = (start.weekday() + 1) % 7          # GitHub weeks start Sunday
    def lvl(c):
        return 0 if c == 0 else 1 if c <= 2 else 2 if c <= 5 else 3 if c <= 9 else 4
    weeks = (len(cal) + off + 6) // 7
    lastm = None
    for i, (ds, c) in enumerate(cal):
        k = i + off; wk, dw = divmod(k, 7)
        x = hx + wk * (cs + gp); y = hy + dw * (cs + gp)
        b.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cs}" height="{cs}" fill="{HEAT[lvl(c)]}"'
                 + (f' stroke="{INK}" stroke-width="1.5"' if c else "") + "/>")
        m = ds[5:7]
        if m != lastm and dw <= 1 and wk < weeks - 2:
            b.append(T(x, hy - 10, _dt.date.fromisoformat(ds).strftime("%b").lower(), "mono", 12, MUTED))
            lastm = m
    hw = weeks * (cs + gp)
    css.append(f".scan{{animation:scan 9s steps({weeks}) infinite}}@keyframes scan{{from{{transform:translateX(0)}}to{{transform:translateX({hw:.1f}px)}}}}")
    b.append(f'<rect class="scan" x="{hx-2.5}" y="{hy-3.5}" width="{cs+5}" height="{7*(cs+gp)+3}" fill="none" stroke="{ORANGE}" stroke-width="2.5"/>')
    lx = hx + hw - 5 * 16 - 70
    b.append(T(lx - 8, hy + 7 * (cs + gp) + 22, "less", "mono", 12, MUTED, anchor="end"))
    for j, c in enumerate(HEAT):
        b.append(f'<rect x="{lx + j*16}" y="{hy + 7*(cs+gp) + 12}" width="12" height="12" fill="{c}"/>')
    b.append(T(lx + 5 * 16 + 4, hy + 7 * (cs + gp) + 22, "more", "mono", 12, MUTED))
    # languages
    ly = 300
    langs = sorted(d["langs"].items(), key=lambda x: -x[1]); tot = sum(v for _, v in langs)
    top = langs[:3]; rest = tot - sum(v for _, v in top)
    segs = top + ([("Other", rest)] if rest else [])
    b.append(T(hx, ly - 14, "LANGUAGES", "pix", 12, INK))
    x = hx
    for j, (nm, v) in enumerate(segs):
        w = max(4, hw * v / tot)
        b.append(f'<rect x="{x:.1f}" y="{ly}" width="{w:.1f}" height="26" fill="{LANGC[j]}" stroke="{INK}" stroke-width="2.5"/>')
        x += w
    x = hx
    for j, (nm, v) in enumerate(segs):
        lab = f"{nm} {v/tot*100:.1f}%"
        b.append(f'<rect x="{x}" y="{ly+44}" width="12" height="12" fill="{LANGC[j]}" stroke="{INK}" stroke-width="1.5"/>')
        b.append(T(x + 20, ly + 55, lab, "mono", 14, INK))
        x += width(lab, "mono", 14) + 46
    upd = _dt.date.fromisoformat(d["updated"]).strftime("%d %b %Y").lower()
    b.append(T(W - 18 - 28, H - 46, f"synced from GitHub daily · last sync {upd}", "mono", 13, MUTED, anchor="end"))
    return svg(W, H, "".join(b), ["pix", "head", "mono"], "".join(css),
               f"GitHub stats: {d['total']} contributions in the last year, {active} active days, {d['repos']} public repos")


# ---------------------------------------------------------------- research & certifications
def stamp(x, y, w, h, title, sub, col, rot, cls="", logo_slug=""):
    out = [f'<g class="{cls}"><g transform="translate({x} {y}) rotate({rot} {w/2} {h/2})">',
           f'<rect x="6" y="6" width="{w}" height="{h}" fill="{INK}"/>',
           f'<rect width="{w}" height="{h}" fill="{PAPER2}"/>']
    for k in range(int(w // 12) + 1):                    # perforations
        out.append(f'<circle cx="{k*12}" cy="0" r="3.6" fill="{PAPER}"/><circle cx="{k*12}" cy="{h}" r="3.6" fill="{PAPER}"/>')
    for k in range(int(h // 12) + 1):
        out.append(f'<circle cx="0" cy="{k*12}" r="3.6" fill="{PAPER}"/><circle cx="{w}" cy="{k*12}" r="3.6" fill="{PAPER}"/>')
    out.append(f'<rect x="10" y="10" width="{w-20}" height="{h-20}" fill="none" stroke="{col}" stroke-width="3"/>')
    out.append(T(w / 2, 34, "CERTIFIED", "pix", 9, col, anchor="middle"))
    lines = wrap(title, "head", 19, w - 34)
    for j, ln in enumerate(lines):
        out.append(T(w / 2, 64 + j * 22, ln, "head", 19, INK, anchor="middle"))
    room = (64 + len(lines) * 22 - 4) + 36 <= h - (34 if sub else 14)
    if not room:
        pass
    elif logo_slug in ICONS:
        ic = ICONS[logo_slug]; sz = 34; ly = 64 + len(lines) * 22
        out.append(f'<g transform="translate({w/2 - sz/2} {ly - 4}) scale({sz/24})"><path d="{ic["path"]}" fill="{col}"/></g>')
    elif logo_slug in PIX:
        out.append(pixel(logo_slug, w / 2 - 18, 64 + len(lines) * 22 - 4, 4, col))
    if sub:
        out.append(T(w / 2, h - 22, sub, "mono", 12, MUTED, anchor="middle"))
    out.append("</g></g>")
    return "".join(out)

def research():
    W, H = 1280, 420
    css = ["@keyframes wig{0%,90%,100%{transform:rotate(0)}93%{transform:rotate(-2deg)}96%{transform:rotate(2deg)}}"]
    b = [f'<rect width="{W}" height="{H}" fill="{PAPER}"/>', f'<rect width="{W}" height="{H}" fill="url(#dither)"/>']
    # manuscript sheet
    mx, my, mw, mh = 36, 34, 470, 352
    b.append(f'<g transform="rotate(-2 {mx+mw/2} {my+mh/2})">')
    b.append(f'<rect x="{mx+8}" y="{my+8}" width="{mw}" height="{mh}" fill="{INK}"/>')
    b.append(f'<path d="M{mx} {my} H{mx+mw-44} L{mx+mw} {my+44} V{my+mh} H{mx} Z" fill="{FUR}" stroke="{INK}" stroke-width="3"/>')
    b.append(f'<path d="M{mx+mw-44} {my} V{my+44} H{mx+mw}" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>')
    b.append(f'<rect x="{mx+28}" y="{my+30}" width="{width("MANUSCRIPT · IN PROGRESS","pix",10)+20}" height="26" fill="{MUSTARD}" stroke="{INK}" stroke-width="2"/>')
    b.append(T(mx + 38, my + 48, "MANUSCRIPT · IN PROGRESS", "pix", 10, INK))
    b.append(T(mx + 28, my + 96, "VLP-FusionNet", "head", 30, INK, ls=-0.5))
    for j, ln in enumerate(["Deep-learning cardiac risk prediction", "from ECG signals (PTB-XL)"]):
        b.append(T(mx + 28, my + 126 + j * 24, ln, "body", 18, INK))
    b.append(T(mx + 28, my + 186, "Co-author · IEEE-style conference paper", "mono", 13.5, MUTED))
    b.append(T(mx + 28, my + 208, "CDAE + wavelets + 1D-CNN + transformer", "mono", 13.5, MUTED))
    for j, ww in enumerate([400, 380, 410, 300, 390, 250]):
        b.append(f'<rect x="{mx+28}" y="{my+234+j*16}" width="{ww}" height="6" fill="{INK}" opacity=".12"/>')
    b.append("</g>")
    # stamps
    certs = [("IIT Hyderabad (TiHAN)", "6-month AI & ML program", TEAL, "cap"),
             ("Google Cloud", "", ORANGE, "googlecloud"), ("Meta", "", RUST, "meta"), ("Oracle", "", TEAL, "star"),
             ("Wolfram Research", "", MUSTARD, "wolfram"), ("University of Illinois", "", ORANGE, "scroll"), ("HackerRank", "", RUST, "hackerrank")]
    sx0, sy0 = 556, 30
    b.append(T(sx0, sy0 + 16, "CERTIFICATIONS", "pix", 14, INK))
    pos = [(sx0, sy0 + 40, 300, 160), (sx0 + 330, sy0 + 40, 170, 160), (sx0 + 525, sy0 + 40, 170, 160),
           (sx0, sy0 + 226, 160, 140), (sx0 + 182, sy0 + 226, 160, 140), (sx0 + 364, sy0 + 226, 160, 140),
           (sx0 + 546, sy0 + 226, 150, 140)]
    rots = [-1.5, 2, -2.5, 1.5, -1, 2.5, -2]
    for i, ((t, s_, c, lg), (x, y, w, h)) in enumerate(zip(certs, pos)):
        css.append(f".st{i}{{animation:wig 7s ease-in-out {i*0.8:.1f}s infinite;transform-box:fill-box;transform-origin:center}}")
        b.append(stamp(x, y, w, h, t, s_, c, rots[i], f"st{i}", lg))
    return svg(W, H, "".join(b), ["pix", "head", "body", "mono"], "".join(css),
               "Research: VLP-FusionNet cardiac risk prediction paper in progress. Certifications: IIT Hyderabad (TiHAN), Google Cloud, Meta, Oracle, Wolfram Research, University of Illinois, HackerRank")


# ---------------------------------------------------------------- social buttons
def button(label, sub, slug, col):
    W, H = 300, 76
    b = [f'<rect x="7" y="7" width="{W-10}" height="{H-10}" fill="{INK}"/>',
         f'<rect x="2" y="2" width="{W-10}" height="{H-10}" fill="{PAPER2}" stroke="{INK}" stroke-width="3"/>',
         f'<rect x="2" y="2" width="64" height="{H-10}" fill="{col}" stroke="{INK}" stroke-width="3"/>']
    if slug in ICONS:
        b.append(f'<g transform="translate({34-14} {35-14}) scale({28/24})"><path d="{ICONS[slug]["path"]}" fill="{PAPER2}"/></g>')
    else:
        b.append(T(34, 46, "in", "head", 30, PAPER2, anchor="middle", ls=-1))
    b.append(T(84, 34, label, "head", 21, INK))
    b.append(T(84, 54, sub, "mono", 13, MUTED))
    b.append(f'<path d="M{W-38} 26 h12 v12 M{W-26} 26 l-14 14" stroke="{INK}" stroke-width="3" fill="none"/>')
    return svg(W, H, "".join(b), ["head", "mono"], "", f"{label}: {sub}")


# ---------------------------------------------------------------- banner
def banner():
    W, H = 1280, 420
    css = (".cur{animation:blink 1.05s steps(1) infinite}@keyframes blink{50%{opacity:0}}"
           ".type{animation:type 2.6s steps(31) .4s both}@keyframes type{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
           ".f1{animation:bob 5s ease-in-out infinite}.f2{animation:bob 5s ease-in-out -1.6s infinite}.f3{animation:bob 5s ease-in-out -3.2s infinite}"
           "@keyframes bob{50%{transform:translateY(-7px)}}")
    b = [f'<rect width="{W}" height="{H}" fill="{PAPER}"/>',
         f'<rect width="{W}" height="{H}" fill="url(#dither)"/>']
    # 70s stripes from the bottom-right corner
    for i, c in enumerate([ORANGE, MUSTARD, TEAL, RUST]):
        r = 330 - i * 34
        b.append(f'<circle cx="{W}" cy="{H}" r="{r}" fill="none" stroke="{c}" stroke-width="26"/>')
    b.append(f'<circle cx="{W}" cy="{H}" r="210" fill="{PAPER}"/>')
    b.append(f'<circle cx="{W}" cy="{H}" r="210" fill="url(#dither)"/>')
    # main window
    wx, wy, ww, wh = 40, 34, 820, 346
    b.append(window(wx, wy, ww, wh, "kamlesh.app"))
    px = wx + 38
    b.append(T(px, wy + 82, "HELLO, WORLD. I'M", "pix", 16, ORANGE, ls=1))
    b.append(T(px - 3, wy + 168, "Kamlesh", "head", 86, INK, ls=-2))
    b.append(T(px - 3, wy + 248, "Choudhary", "head", 86, INK, ls=-2))
    # tagline with marker highlight + typing reveal
    tag1 = "AI/ML Engineer  ·  "
    tag2 = "LLMs understand. Rules decide."
    w1 = width(tag1, "body", 25); w2 = width(tag2, "body", 25)
    ty = wy + 304
    b.append(f'<defs><clipPath id="tc"><rect class="type" x="{px}" y="{ty-30}" width="{w1+w2+30}" height="44" style="transform-origin:{px}px {ty}px"/></clipPath></defs>')
    b.append(f'<g clip-path="url(#tc)">'
             f'<rect x="{px + w1 - 4}" y="{ty-21}" width="{w2+8}" height="30" fill="{MUSTARD}"/>'
             + T(px, ty, tag1, "body", 25, MUTED) + T(px + w1, ty, tag2, "body", 25, INK) + '</g>')
    b.append(f'<rect class="cur" x="{px + w1 + w2 + 10}" y="{ty-22}" width="13" height="28" fill="{INK}"/>')
    # floppies
    b.append(floppy(900, 46, 124, TEAL, "RAG", -9, "f1"))
    b.append(floppy(1052, 30, 124, ORANGE, "AGENTS", 7, "f2"))
    b.append(floppy(880, 232, 118, MUSTARD, "VISION", -6, "f3"))
    s = 8
    b.append(panda(1098, 246, s, "sit", extra=bamboo(-1.5 * s, 7 * s, s, 12)))
    bub, bcss, bw = bubble(1016, 176, ["hi, I'm Momo!", "pip install bamboo", "hire my human :)"], 10.5, tail=1150)
    b.append(bub); css += bcss + PANDA_CSS
    return svg(W, H, "".join(b), ["pix", "head", "body"], css,
               "Kamlesh Choudhary - AI/ML Engineer. LLMs understand. Rules decide.")


# ---------------------------------------------------------------- menu bar headers
MENU = ["About", "Stack", "Projects", "Log", "Stats"]
SUBS = {"About": "who's running this machine", "Stack": "loaded modules",
        "Projects": "things I've shipped", "Log": "research, patents & wins",
        "Stats": "live from GitHub"}

def menubar(active):
    W, H = 1280, 76
    css = ".cur{animation:blink 1.05s steps(1) infinite}@keyframes blink{50%{opacity:0}}"
    b = [f'<rect x="3" y="3" width="{W-6}" height="{H-12}" fill="{PAPER2}" stroke="{INK}" stroke-width="3"/>',
         f'<rect x="9" y="{H-9}" width="{W-9}" height="6" fill="{INK}"/>',
         f'<rect x="{W-9}" y="9" width="6" height="{H-12}" fill="{INK}"/>']
    # logo: four colour squares
    for i, c in enumerate([ORANGE, MUSTARD, TEAL, RUST]):
        b.append(f'<rect x="{26 + (i%2)*13}" y="{18 + (i//2)*13}" width="12" height="12" fill="{c}"/>')
    x = 78
    for m in MENU:
        mw = width(m, "pix", 16) + 30
        if m == active:
            b.append(f'<rect x="{x}" y="13" width="{mw}" height="44" fill="{INK}"/>')
            b.append(T(x + 15, 44, m, "pix", 16, PAPER2))
        else:
            b.append(T(x + 15, 44, m, "pix", 16, INK))
        x += mw + 4
    idx = MENU.index(active) + 1
    sub = f"{idx:02d}/05  {SUBS[active]}"
    sw = width(sub, "mono", 18)
    b.append(T(W - 50 - sw, 44, sub, "mono", 18, MUTED))
    b.append(f'<rect class="cur" x="{W-42}" y="27" width="11" height="22" fill="{ORANGE}"/>')
    return svg(W, H, "".join(b), ["pix", "mono"], css, f"Section {idx}: {active} - {SUBS[active]}")


# ---------------------------------------------------------------- project cards
CARDS = [
    ("salvage", "salvage_agent", "BUILDATHON", ORANGE, "Salvage Agent",
     "Payment-recovery agent. The LLM diagnoses failed charges; hard RBI gates decide what actually runs.",
     ["webhook", "LLM diagnose", "RBI gates", "recover"], ["Python", "FastAPI", "React", "TypeScript", "MongoDB"]),
    ("drowsiness", "drowsiness.exe", "PATENT FILED", RUST, "Drowsiness & Faint Detection",
     "Real-time webcam safety system that watches eye closure and head pose to catch a drowsy or fainting driver.",
     ["webcam", "face mesh", "EAR + pose", "alert"], ["Python", "MediaPipe"]),
    ("sysmon", "sysmon_hybrid", "CYBERSECURITY", TEAL, "Hybrid CNN-Transformer",
     "Threat detection on Windows Sysmon logs: CNNs read local patterns, Transformers read the global context.",
     ["sysmon logs", "CNN", "transformer", "verdict"], ["Python", "PyTorch"]),
    ("fnol", "fnol_agent", "INSURTECH", MUSTARD, "FNOL Claims Agent",
     "Reads claim documents with an LLM, routes them with auditable rules, and falls back to regex if the model is down.",
     ["claim doc", "LLM extract", "rules", "route"], ["Python", "Ollama", "Pydantic", "Streamlit"]),
    ("template", "template_check", "COMPLIANCE", TEAL, "Outdated Template Detector",
     "Flags Word and PDF documents built on a superseded QMS template before they reach review. 14 tests.",
     ["document", "footer regex", "master list", "verdict"], ["Python", "pdfplumber", "Streamlit"]),
    ("oracle", "vm_grabber.sh", "DEVOPS", ORANGE, "Oracle VM Grabber",
     "Keeps retrying Oracle Cloud Always Free Ampere VM launches until capacity frees up, so you don't have to.",
     ["launch", "no capacity", "retry", "VM up"], ["Shell"]),
]

PROOF = {
    "salvage": "11 RBI gates · 115 taxonomy rules · 10 bounded actions",
    "drowsiness": "3 alert levels · alarm + Twilio SMS emergency alert",
    "sysmon": "synthetic logic-trap data · saliency maps · Docker",
    "fnol": "11 test cases passing · Excel audit trail per claim",
    "template": "4 verdict types · 14 test cases · no AI in the decision",
    "oracle": "set-and-forget retry loop · runs unattended",
}
SHORT = {
    "salvage": "Payment-recovery agent. The LLM diagnoses; rules move the money.",
    "drowsiness": "Webcam system that catches a drowsy or fainting driver.",
    "sysmon": "Deep learning that spots attacks in Windows Sysmon logs.",
    "fnol": "Reads insurance claims with an LLM, routes them by rules.",
    "template": "Flags documents built on an outdated QMS template.",
    "oracle": "Retries Oracle Cloud free VM launches until one lands.",
}

def card(c):
    slug, wtitle, tag, tagc, name, desc, flow, stack = c
    W, H = 620, 410
    css = (".ants{stroke-dasharray:6 5;animation:ants .9s linear infinite}@keyframes ants{to{stroke-dashoffset:-11}}")
    b = [window(4, 4, W - 18, H - 18, wtitle, shadow=8)]
    x0, y0 = 32, 4 + 34
    tw = width(tag, "pix", 12) + 20
    tagtext = PAPER2 if tagc in (ORANGE, RUST, TEAL) else INK
    b.append(f'<rect x="{x0}" y="{y0+22}" width="{tw}" height="28" fill="{tagc}" stroke="{INK}" stroke-width="2"/>')
    b.append(T(x0 + 10, y0 + 42, tag, "pix", 12, tagtext))
    b.append(T(x0, y0 + 92, name, "head", 31, INK, ls=-0.5))
    for i, line in enumerate(wrap(desc, "body", 18, W - 18 - 64)):
        b.append(T(x0, y0 + 126 + i * 26, line, "body", 18, MUTED))
    # pipeline
    py = y0 + 196
    gap = 26
    ws = [width(s, "mono", 14) + 22 for s in flow]
    total = sum(ws) + gap * (len(ws) - 1)
    scale = min(1, (W - 18 - 64) / total)
    x = x0
    for i, (s, w) in enumerate(zip(flow, ws)):
        w *= scale
        last = i == len(flow) - 1
        fill = MUSTARD if last else PAPER2
        b.append(f'<rect x="{x}" y="{py}" width="{w}" height="36" fill="{fill}" stroke="{INK}" stroke-width="2.5"/>')
        b.append(T(x + w / 2, py + 23, s, "mono", 14 * scale if scale < 1 else 14, INK, anchor="middle"))
        if not last:
            ax = x + w
            b.append(f'<line class="ants" x1="{ax+3}" y1="{py+18}" x2="{ax+gap*scale-7}" y2="{py+18}" stroke="{INK}" stroke-width="2.5"/>')
            b.append(f'<path d="M{ax+gap*scale-8} {py+12} L{ax+gap*scale-2} {py+18} L{ax+gap*scale-8} {py+24} Z" fill="{INK}"/>')
        x += w + gap * scale
    # stack chips
    cy = y0 + 262
    x = x0
    for s in stack:
        cw = width(s, "mono", 14) + 20
        b.append(f'<rect x="{x}" y="{cy}" width="{cw}" height="28" fill="none" stroke="{INK}" stroke-width="2" stroke-dasharray="0"/>')
        b.append(T(x + 10, cy + 19, s, "mono", 14, INK))
        x += cw + 8
    pr = PROOF[slug]
    b.append(f'<rect x="5.5" y="{H-60}" width="{W-21}" height="44.5" fill="{INK}"/>')
    b.append(T(x0, H - 32, "PROOF", "pix", 12, MUSTARD))
    b.append(T(x0 + 82, H - 32, pr, "mono", 15, PAPER2))
    return slug, svg(W, H, "".join(b), ["pix", "head", "body", "mono"], css, f"{name}: {desc}")


# ---------------------------------------------------------------- internship log
def internship():
    W, H = 1280, 400
    css = ".cur{animation:blink 1.05s steps(1) infinite}@keyframes blink{50%{opacity:0}}"
    b = [window(4, 4, W - 18, H - 18, "internship.log  [read-only]")]
    x0 = 40
    b.append(T(x0, 84, "Dhee Coding Lab  ·  Prodhee Technologies  ·  Software Engineer Intern  ·  Jun - Aug 2026", "body", 20, INK))
    b.append(T(x0, 112, "Built the company's first AI integrations. Source is private company IP, so here's the changelog instead.", "body", 18, MUTED))
    rows = [("Text-to-SQL RAG", "plain-English questions -> validated SQL over placement data (Qdrant, sqlglot, Redis)"),
            ("Student-JD matching", "hybrid search that ranks students against job descriptions"),
            ("AI resume builder", "LLM rewrites, fact-checked against the student's own answers, PDF out"),
            ("Interview Q&A platform", "search and AI answers over real company interview questions")]
    y = 162
    for i, (k, v) in enumerate(rows):
        b.append(f'<rect x="{x0}" y="{y-22}" width="52" height="30" fill="{TEAL}"/>')
        b.append(T(x0 + 26, y - 1, "OK", "pix", 13, PAPER2, anchor="middle"))
        b.append(T(x0 + 70, y, k, "head", 21, INK))
        b.append(T(x0 + 360, y, v, "mono", 16, MUTED))
        y += 44
    b.append(T(x0, y + 6, "$ git log --private", "mono", 16, INK))
    b.append(f'<rect class="cur" x="{x0 + width("$ git log --private", "mono", 16) + 8}" y="{y-9}" width="10" height="20" fill="{ORANGE}"/>')
    return svg(W, H, "".join(b), ["pix", "head", "body", "mono"], css,
               "Internship at Dhee Coding Lab: Text-to-SQL RAG, student-JD matching, AI resume builder, interview Q&A platform")


# ---------------------------------------------------------------- achievements
PIX = {
    "chip":   [".X.X.X.X.", "XXXXXXXXX", ".X.....X.", "XX.XXX.XX", ".X.XXX.X.", "XX.XXX.XX", ".X.....X.", "XXXXXXXXX", ".X.X.X.X."],
    "trophy": ["..XXXXX..", "XXXXXXXXX", "X.XXXXX.X", "X.XXXXX.X", ".XXXXXXX.", "..XXXXX..", "...XXX...", "....X....", "..XXXXX.."],
    "star":   ["....X....", "...XXX...", "XXXXXXXXX", ".XXXXXXX.", "..XXXXX..", ".XXX.XXX.", "XX.....XX"],
    "scroll": ["XXXXXXXX.", "X......XX", "X.XXXX.X.", "X......X.", "X.XXXX.X.", "X......X.", "X.XXX..X.", "XXXXXXXX."],
    "heart":  [".XX...XX.", "XXXX.XXXX", "XXXXXXXXX", "XXXXXXXXX", ".XXXXXXX.", "..XXXXX..", "...XXX...", "....X...."],
    "flag":   ["XXXXXXX..", "XXXXXXXXX", "XXXXXXXXX", "XXXXXXX..", "X........", "X........", "X........", "X........"],
    "cap":    ["X.......X", "XXX...XXX", "X.XXXXX.X", "..XXXXX..", "..X.X.X..", "X.XXXXX.X", "XXX...XXX", "X.......X"],
}

def pixel(icon, x, y, s, color):
    out = []
    for r, row in enumerate(PIX[icon]):
        for c, ch in enumerate(row):
            if ch == "X":
                out.append(f'<rect x="{x+c*s}" y="{y+r*s}" width="{s}" height="{s}" fill="{color}"/>')
    return "".join(out)

def achievements():
    items = [("trophy", ORANGE, "PATENT FILED", "Driver drowsiness & faint detection"),
             ("chip", TEAL, "4 AI SYSTEMS SHIPPED", "The first AI integrations at Dhee Coding Lab"),
             ("star", MUSTARD, "CGPA 9.7 / 10", "B.Tech AI & ML, Jain University"),
             ("flag", RUST, "BUILDATHON 2026", "Razorpay AI Buildathon, Track 03"),
             ("scroll", TEAL, "TEAM LEAD", "FET Aavishkar 2026, Team Omnitrons"),
             ("heart", ORANGE, "DICE 0.93", "Cardiac segmentation, SE-ResUNet")]
    W, H = 1280, 470
    css = (".pop{animation:pop 6s steps(1) infinite}@keyframes pop{0%,92%{opacity:1}94%{opacity:0}96%{opacity:1}}"
           "@keyframes hop{0%,8%,100%{transform:translateY(0)}4%{transform:translateY(-8px)}}")
    b = []
    tw, th, gx, gy = 396, 196, 22, 26
    for i, (ic, col, title, sub) in enumerate(items):
        x = 4 + (i % 3) * (tw + gx); y = 4 + (i // 3) * (th + gy)
        b.append(f'<rect x="{x+8}" y="{y+8}" width="{tw}" height="{th}" fill="{INK}"/>')
        b.append(f'<rect x="{x}" y="{y}" width="{tw}" height="{th}" fill="{PAPER2}" stroke="{INK}" stroke-width="3"/>')
        b.append(f'<rect x="{x+20}" y="{y+22}" width="96" height="96" fill="{PAPER}" stroke="{INK}" stroke-width="2.5"/>')
        b.append(f'<rect x="{x+20}" y="{y+22}" width="96" height="96" fill="url(#dither)"/>')
        b.append(f'<g class="hop{i}">' + pixel(ic, x + 32, y + 36, 8, col) + '</g>')
        css += (f".hop{i}{{animation:hop 6s steps(2) {i*0.5}s infinite}}")
        b.append(T(x + 134, y + 48, "ACHIEVEMENT", "pix", 11, MUTED, extra='class="pop"'))
        b.append(T(x + 134, y + 66, "UNLOCKED", "pix", 11, MUTED, extra='class="pop"'))
        lines = wrap(title, "head", 24, tw - 150)
        for j, ln in enumerate(lines):
            b.append(T(x + 134, y + 100 + j * 28, ln, "head", 24, INK))
        for j, ln in enumerate(wrap(sub, "body", 17, tw - 40)):
            b.append(T(x + 20, y + 152 + j * 22, ln, "body", 17, MUTED))
    return svg(W, H, "".join(b), ["pix", "head", "body"], css,
               "Achievements: patent filed, IIT Hyderabad TiHAN program, CGPA 9.7, Razorpay Buildathon 2026, FET Aavishkar team lead, Dice 0.93 cardiac model")


# ---------------------------------------------------------------- footer
def footer():
    W, H = 1280, 200
    css = ".blink{animation:blink 1.2s steps(1) infinite}@keyframes blink{50%{opacity:0}}"
    b = [f'<rect width="{W}" height="{H}" fill="{PAPER}"/>', f'<rect width="{W}" height="{H}" fill="url(#dither)"/>']
    for i, c in enumerate([ORANGE, MUSTARD, TEAL, RUST]):
        b.append(f'<rect x="0" y="{H-40+i*10}" width="{W}" height="10" fill="{c}"/>')
    b.append(T(W / 2 - 30, 78, "Let's build something that holds up in production.", "head", 38, INK, anchor="middle", ls=-0.5))
    b.append(f'<g class="blink">' + T(W / 2 - 12, 132, "PRESS START TO CONNECT", "pix", 18, ORANGE, anchor="middle") +
             f'<path d="M{W/2 + width("PRESS START TO CONNECT", "pix", 18)/2 + 2} 114 l16 9 l-16 9 z" fill="{ORANGE}"/></g>')
    css += PANDA_CSS + (".armA{animation:armA .8s steps(1) infinite}.armB{animation:armB .8s steps(1) infinite}"
                        "@keyframes armA{50%{opacity:0}}@keyframes armB{0%{opacity:0}50%{opacity:1}}")
    b.append(panda(1166, 52, 5, "wave", bob=False))
    return svg(W, H, "".join(b), ["pix", "head"], css, "Let's build something that holds up in production. Press start to connect.")


if __name__ == "__main__":
    import sys
    if sys.argv[1:] == ["stats"]:
        open(os.path.join(OUT, "stats.svg"), "w").write(stats()); print("stats.svg")
        import mobile; mobile.main(only_stats=True); sys.exit()
    files = {"banner.svg": banner(), "stack.svg": stack(), "about.svg": about(), "stats.svg": stats(),
             "research.svg": research(), "btn-linkedin.svg": button("LinkedIn", "kamlesh-choudhary21", "linkedin", "#0A66C2"),
             "btn-x.svg": button("X / Twitter", "@Just_Kamlesh21", "x", INK),
             "internship.svg": internship(),
             "achievements.svg": achievements(), "footer.svg": footer()}
    for m in MENU:
        files[f"nav-{m.lower()}.svg"] = menubar(m)
    for c in CARDS:
        slug, s = card(c); files[f"card-{slug}.svg"] = s
    for n, s in files.items():
        open(os.path.join(OUT, n), "w").write(s)
        print(f"{n:24s} {len(s)/1024:6.1f} KB")
    import mobile
    mobile.main()
