"""Phone-width versions of every panel (served via <picture> media queries in README.md).

Designed at 600 px wide (300 px for project cards) so text stays readable when a
phone shrinks them to ~290 px.
"""
import datetime as dt, json, os
import build as B
from build import (T, svg, window, width, wrap, floppy, panda, bamboo, bubble, pixel, logo, stamp,
                   PANDA_CSS, INK, PAPER, PAPER2, MUTED, ORANGE, MUSTARD, TEAL, RUST,
                   CARDS, PROOF, SHORT, STACK, HEAT, LANGC, ICONS, FULL, GCOL)

OUT = os.path.join(B.OUT, "m")
MW = 600
BLINK = ".cur{animation:blink 1.05s steps(1) infinite}@keyframes blink{50%{opacity:0}}"


def bg(w, h):
    return f'<rect width="{w}" height="{h}" fill="{PAPER}"/><rect width="{w}" height="{h}" fill="url(#dither)"/>'


def banner():
    H = 640
    css = BLINK + PANDA_CSS + (".f1{animation:bob 5s ease-in-out infinite}.f2{animation:bob 5s ease-in-out -1.6s infinite}"
                               ".f3{animation:bob 5s ease-in-out -3.2s infinite}@keyframes bob{50%{transform:translateY(-6px)}}")
    b = [bg(MW, H)]
    for i, c in enumerate([ORANGE, MUSTARD, TEAL, RUST]):
        b.append(f'<circle cx="{MW}" cy="{H}" r="{250 - i*30}" fill="none" stroke="{c}" stroke-width="24"/>')
    b.append(f'<circle cx="{MW}" cy="{H}" r="148" fill="{PAPER}"/>')
    b.append(window(22, 24, MW - 52, 360, "kamlesh.app"))
    px = 52
    b.append(T(px, 104, "HELLO, WORLD. I'M", "pix", 19, ORANGE))
    b.append(T(px - 3, 188, "Kamlesh", "head", 80, INK, ls=-2))
    b.append(T(px - 3, 264, "Choudhary", "head", 80, INK, ls=-2))
    b.append(T(px, 312, "AI/ML Engineer", "body", 27, MUTED))
    tag = "LLMs understand. Rules decide."
    tw = width(tag, "body", 27)
    b.append(f'<rect x="{px-5}" y="{330}" width="{tw+10}" height="38" fill="{MUSTARD}"/>')
    b.append(T(px, 358, tag, "body", 27, INK))
    b.append(f'<rect class="cur" x="{px + tw + 12}" y="333" width="14" height="32" fill="{INK}"/>')
    b.append(floppy(30, 418, 96, TEAL, "RAG", -9, "f1"))
    b.append(floppy(146, 410, 96, ORANGE, "AGENTS", 6, "f2"))
    b.append(floppy(88, 534, 84, MUSTARD, "VISION", -4, "f3"))
    s = 7
    b.append(panda(410, 476, s, "sit", extra=bamboo(-1.5 * s, 7 * s, s, 12)))
    bub, bcss, _ = bubble(272, 412, ["hi, I'm Momo!", "pip install bamboo", "hire my human :)"], 10.5, tail=452)
    b.append(bub)
    return svg(MW, H, "".join(b), ["pix", "head", "body"], css + bcss,
               "Kamlesh Choudhary - AI/ML Engineer. LLMs understand. Rules decide.")


NAV_SUB = {"About": "who's running this", "Stack": "loaded modules", "Projects": "things I've shipped",
           "Log": "research & wins", "Stats": "live from GitHub"}

def nav(active):
    H = 100
    idx = B.MENU.index(active) + 1
    b = [f'<rect x="3" y="3" width="{MW-12}" height="{H-14}" fill="{PAPER2}" stroke="{INK}" stroke-width="3"/>',
         f'<rect x="9" y="{H-11}" width="{MW-9}" height="8" fill="{INK}"/>',
         f'<rect x="{MW-9}" y="9" width="8" height="{H-14}" fill="{INK}"/>']
    for i, c in enumerate([ORANGE, MUSTARD, TEAL, RUST]):
        b.append(f'<rect x="{24 + (i%2)*16}" y="{28 + (i//2)*16}" width="15" height="15" fill="{c}"/>')
    b.append(T(76, 56, f"{idx:02d}/05", "pix", 15, ORANGE))
    nw = width(active, "pix", 22) + 28
    b.append(f'<rect x="166" y="20" width="{nw}" height="54" fill="{INK}"/>')
    b.append(T(180, 58, active, "pix", 22, PAPER2))
    sub = NAV_SUB[active]
    b.append(T(MW - 30, 56, sub, "mono", 19, MUTED, anchor="end"))
    return svg(MW, H, "".join(b), ["pix", "mono"], "", f"Section {idx}: {active} - {sub}")


def about():
    H = 940
    css = PANDA_CSS + BLINK + ".dot{animation:dot 1.6s steps(1) infinite}@keyframes dot{50%{opacity:.25}}"
    b = []
    dx, dy, dw, dh = 8, 112, MW - 30, 580
    b.append(window(dx, dy, dw, dh, "About This Human"))
    b.append(panda(dx + dw - 128, dy - 104, 5.5, "sit"))
    px = dx + 34
    b.append(T(px, dy + 104, "Kamlesh OS", "head", 54, INK, ls=-1.5))
    b.append(T(px, dy + 140, "version 9.7  (CGPA build)", "mono", 21, MUTED))
    b.append(f'<line x1="{px}" y1="{dy+164}" x2="{dx+dw-34}" y2="{dy+164}" stroke="{INK}" stroke-width="2.5" stroke-dasharray="4 5"/>')
    rows = [("BASED IN", "Bengaluru, India"), ("EDUCATION", "B.Tech AI & ML, semester 5"),
            ("LAST JOB", "SWE Intern, Dhee Coding Lab"), ("FOCUS", "LLM systems that hold up")]
    for i, (k, v) in enumerate(rows):
        y = dy + 204 + i * 76
        b.append(T(px, y, k, "pix", 14, MUTED))
        b.append(T(px, y + 32, v, "body", 26, INK))
    sy = dy + dh - 72
    st = "OPEN TO AI/ML INTERNSHIPS"
    sw = width(st, "pix", 15) + 62
    b.append(f'<rect x="{px}" y="{sy}" width="{sw}" height="46" fill="{TEAL}" stroke="{INK}" stroke-width="3"/>')
    b.append(f'<rect class="dot" x="{px+16}" y="{sy+16}" width="13" height="13" fill="{PAPER2}"/>')
    b.append(T(px + 42, sy + 30, st, "pix", 15, PAPER2))
    cy = dy + dh + 36
    b.append(window(dx, cy, dw, H - cy - 18, "about.py"))
    fs = 21; lx = px; ly = cy + 34 + 52
    segs = [[("def ", B.KW), ("rule", B.CLS), ("(self) -> ", INK), ("str", B.KW), (":", INK)],
            [("    return ", B.KW), ('"LLMs understand.', B.STR)],
            [('            Rules decide."', B.STR)]]
    for i, line in enumerate(segs):
        x = lx
        for txt, col in line:
            b.append(T(x, ly + i * 36, txt, "mono", fs, col, extra='xml:space="preserve"'))
            x += width(txt, "mono", fs)
    b.append(f'<rect class="cur" x="{x + 4}" y="{ly + 72 - 19}" width="11" height="24" fill="{ORANGE}"/>')
    return svg(MW, H, "".join(b), ["pix", "head", "body", "mono"], css,
               "About Kamlesh: AI/ML Engineer, B.Tech AI & ML, former SWE intern at Dhee Coding Lab, open to AI/ML internships")


def stack():
    TS, GAP, x0 = 100, 12, 26
    items, labels = [], []
    y = 112
    for gname, its in STACK:
        labels.append((gname, x0, y))
        y += 22
        for j, (slug, name, desc) in enumerate(its):
            items.append((slug, name, desc, x0 + j * (TS + GAP), y))
        y += TS + 46
    cap_y = y - 10
    H = cap_y + 150 + 120
    N = len(items); D = 1.6; TT = N * D
    css = [PANDA_CSS, BLINK,
           ".legA{animation:legA .5s steps(1) infinite}.legB{animation:legB .5s steps(1) infinite}"
           "@keyframes legA{50%{opacity:0}}@keyframes legB{0%{opacity:0}50%{opacity:1}}"
           f".walk{{animation:walk 12s linear infinite}}@keyframes walk{{from{{transform:translateX(-110px)}}to{{transform:translateX({MW+20}px)}}}}"]
    sel = []
    for k, it in enumerate(items):
        a, b2 = k / N * 100, (k + 1) / N * 100
        sel.append(f"{a:.3f}%,{b2-0.001:.3f}%{{transform:translate({it[3]-7}px,{it[4]-7}px)}}")
    css.append(f"@keyframes sel{{{''.join(sel)}}}.sel{{animation:sel {TT}s infinite}}")

    def slot(nm, k, on, off):
        a, b2 = k / N * 100, (k + 1) / N * 100
        kf = (f"0%,{b2-0.01:.3f}%{{{on}}}{b2:.3f}%,100%{{{off}}}" if k == 0 else
              f"0%,{a-0.01:.3f}%{{{off}}}{a:.3f}%,{b2-0.01:.3f}%{{{on}}}{b2:.3f}%,100%{{{off}}}")
        css.append(f"@keyframes {nm}{k}{{{kf}}}.{nm}{k}{{animation:{nm}{k} {TT}s infinite}}")

    b = [window(4, 4, MW - 14, H - 14, "modules.sys")]
    b.append(T(x0, 80, "INVENTORY", "pix", 20, INK))
    b.append(T(x0 + width("INVENTORY", "pix", 20) + 14, 80, f"{N} modules", "mono", 20, MUTED))
    gcol = GCOL
    for gname, x, y in labels:
        b.append(f'<rect x="{x}" y="{y-12}" width="12" height="12" fill="{gcol[gname]}"/>')
        b.append(T(x + 20, y, gname, "pix", 14, INK))
    for k, (slug, name, desc, x, y) in enumerate(items):
        slot("lift", k, "transform:translateY(-6px)", "transform:translateY(0)")
        b.append(f'<rect x="{x+5}" y="{y+5}" width="{TS}" height="{TS}" fill="{INK}"/>')
        b.append(f'<g class="lift{k}"><rect x="{x}" y="{y}" width="{TS}" height="{TS}" fill="{PAPER2}" stroke="{INK}" stroke-width="2.5"/>'
                 + logo(slug, x + TS / 2, y + 40, 44) + T(x + TS / 2, y + 88, name, "mono", 14, INK, anchor="middle") + "</g>")
    b.append(f'<g class="sel"><rect x="0" y="0" width="{TS+14}" height="{TS+14}" fill="none" stroke="{ORANGE}" stroke-width="4" stroke-dasharray="20 9"/></g>')
    b.append(f'<rect x="{x0}" y="{cap_y}" width="{MW-14-x0-22}" height="130" fill="{PAPER2}" stroke="{INK}" stroke-width="2.5"/>')
    b.append(f'<rect x="{x0}" y="{cap_y}" width="150" height="40" fill="{INK}"/>')
    b.append(T(x0 + 75, cap_y + 27, "SELECTED", "pix", 15, PAPER2, anchor="middle"))
    for k, (slug, name, desc, x, y) in enumerate(items):
        slot("cap", k, "opacity:1", "opacity:0")
        parts = [T(x0 + 20, cap_y + 78, FULL.get(slug, name), "head", 30, INK)]
        for j, ln in enumerate(wrap(desc, "body", 22, MW - 100)[:2]):
            parts.append(T(x0 + 20, cap_y + 108 + j * 26, ln, "body", 22, MUTED))
        b.append(f'<g class="cap{k}"' + ("" if k == 0 else ' opacity="0"') + ">" + "".join(parts) + "</g>")
    fy = H - 24
    b.append(f'<defs><clipPath id="lane"><rect x="7" y="{fy-110}" width="{MW-20}" height="110"/></clipPath></defs>')
    b.append(f'<line x1="{x0}" y1="{fy-3}" x2="{MW-40}" y2="{fy-3}" stroke="{INK}" stroke-width="2" stroke-dasharray="4 6" opacity=".4"/>')
    b.append(f'<g clip-path="url(#lane)"><g class="walk">{panda(0, fy - 98, 5, "walk")}</g></g>')
    return svg(MW, H, "".join(b), ["pix", "head", "body", "mono"], "".join(css),
               "Tech stack: " + ", ".join(i[1] for i in items))


def card(c):
    slug, wtitle, tag, tagc, name, desc, flow, stack = c
    W, H = 300, 500
    b = [window(3, 3, W - 12, H - 12, wtitle, shadow=6, bar=30)]
    x0 = 22
    tagtext = PAPER2 if tagc in (ORANGE, RUST, TEAL) else INK
    tw = width(tag, "pix", 14) + 20
    b.append(f'<rect x="{x0}" y="56" width="{tw}" height="32" fill="{tagc}" stroke="{INK}" stroke-width="2"/>')
    b.append(T(x0 + 10, 79, tag, "pix", 14, tagtext))
    y = 132
    for ln in wrap(name, "head", 31, W - 50):
        b.append(T(x0, y, ln, "head", 31, INK, ls=-0.5)); y += 34
    y += 8
    for ln in wrap(SHORT[slug], "body", 22, W - 46):
        b.append(T(x0, y, ln, "body", 22, MUTED)); y += 27
    b.append(f'<rect x="4.5" y="{H-120}" width="{W-15}" height="111.5" fill="{INK}"/>')
    b.append(T(x0, H - 90, "PROOF", "pix", 13, MUSTARD))
    for j, ln in enumerate(wrap(PROOF[slug], "mono", 17, W - 46)[:3]):
        b.append(T(x0, H - 60 + j * 23, ln, "mono", 17, PAPER2))
    return slug, svg(W, H, "".join(b), ["pix", "head", "body", "mono"], "", f"{name}: {SHORT[slug]}")


def internship():
    rows = [("Text-to-SQL RAG", "plain-English questions turned into validated SQL"),
            ("Student-JD matching", "hybrid search that ranks students against job descriptions"),
            ("AI resume builder", "LLM rewrites, fact-checked against the student's own answers"),
            ("Interview Q&A platform", "search and AI answers over real interview questions")]
    H = 840
    b = [window(4, 4, MW - 14, H - 14, "internship.log")]
    x0 = 32
    b.append(T(x0, 90, "Dhee Coding Lab", "head", 32, INK))
    b.append(T(x0, 124, "Software Engineer Intern · Jun - Aug 2026", "body", 21, MUTED))
    y = 168
    for ln in wrap("Built the company's first AI integrations. The code is private, so here's the changelog.", "body", 22, MW - 80):
        b.append(T(x0, y, ln, "body", 22, INK)); y += 28
    y += 30
    for k, v in rows:
        b.append(f'<rect x="{x0}" y="{y-26}" width="58" height="34" fill="{TEAL}"/>')
        b.append(T(x0 + 29, y - 2, "OK", "pix", 15, PAPER2, anchor="middle"))
        b.append(T(x0 + 76, y, k, "head", 26, INK))
        yy = y + 34
        for ln in wrap(v, "mono", 18, MW - 76 - x0 - 30):
            b.append(T(x0 + 76, yy, ln, "mono", 18, MUTED)); yy += 25
        y = yy + 34
    b.append(T(x0, y, "$ git log --private", "mono", 19, INK))
    b.append(f'<rect class="cur" x="{x0 + width("$ git log --private", "mono", 19) + 8}" y="{y-17}" width="11" height="22" fill="{ORANGE}"/>')
    return svg(MW, H, "".join(b), ["pix", "head", "body", "mono"], BLINK,
               "Internship at Dhee Coding Lab: Text-to-SQL RAG, student-JD matching, AI resume builder, interview Q&A platform")


ACH = [("trophy", ORANGE, "PATENT FILED", "Driver drowsiness & faint detection"),
       ("chip", TEAL, "4 AI SYSTEMS SHIPPED", "First AI integrations at Dhee Coding Lab"),
       ("star", MUSTARD, "CGPA 9.7 / 10", "B.Tech AI & ML, Jain University"),
       ("flag", RUST, "BUILDATHON 2026", "Razorpay AI Buildathon, Track 03"),
       ("scroll", TEAL, "TEAM LEAD", "FET Aavishkar 2026, Team Omnitrons"),
       ("heart", ORANGE, "DICE 0.93", "Cardiac segmentation, SE-ResUNet")]

def achievements():
    tw, th, gx, gy = 281, 300, 20, 24
    H = 3 * th + 2 * gy + 16
    css = "@keyframes hop{0%,8%,100%{transform:translateY(0)}4%{transform:translateY(-8px)}}"
    b = []
    for i, (ic, col, title, sub) in enumerate(ACH):
        x = 4 + (i % 2) * (tw + gx); y = 4 + (i // 2) * (th + gy)
        b.append(f'<rect x="{x+8}" y="{y+8}" width="{tw}" height="{th}" fill="{INK}"/>')
        b.append(f'<rect x="{x}" y="{y}" width="{tw}" height="{th}" fill="{PAPER2}" stroke="{INK}" stroke-width="3"/>')
        b.append(f'<rect x="{x+20}" y="{y+20}" width="100" height="100" fill="{PAPER}" stroke="{INK}" stroke-width="2.5"/>')
        b.append(f'<g class="hop{i}">' + pixel(ic, x + 34, y + 34, 8, col) + "</g>")
        css += f".hop{i}{{animation:hop 6s steps(2) {i*0.5}s infinite}}"
        b.append(T(x + 136, y + 56, "ACHIEVEMENT", "pix", 12, MUTED))
        b.append(T(x + 136, y + 76, "UNLOCKED", "pix", 12, MUTED))
        yy = y + 166
        for ln in wrap(title, "head", 28, tw - 40):
            b.append(T(x + 20, yy, ln, "head", 28, INK)); yy += 32
        yy += 6
        for ln in wrap(sub, "body", 21, tw - 40):
            b.append(T(x + 20, yy, ln, "body", 21, MUTED)); yy += 26
    return svg(MW, H, "".join(b), ["pix", "head", "body"], css, "Achievements: " + ", ".join(a[2] for a in ACH))


def research():
    H = 1120
    css = "@keyframes wig{0%,90%,100%{transform:rotate(0)}93%{transform:rotate(-2deg)}96%{transform:rotate(2deg)}}"
    b = [bg(MW, H)]
    mx, my, mw, mh = 30, 30, 530, 380
    b.append(f'<g transform="rotate(-1.5 {mx+mw/2} {my+mh/2})">')
    b.append(f'<rect x="{mx+8}" y="{my+8}" width="{mw}" height="{mh}" fill="{INK}"/>')
    b.append(f'<path d="M{mx} {my} H{mx+mw-50} L{mx+mw} {my+50} V{my+mh} H{mx} Z" fill="{B.FUR}" stroke="{INK}" stroke-width="3"/>')
    b.append(f'<path d="M{mx+mw-50} {my} V{my+50} H{mx+mw}" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>')
    lab = "MANUSCRIPT · IN PROGRESS"
    b.append(f'<rect x="{mx+30}" y="{my+34}" width="{width(lab,"pix",13)+22}" height="32" fill="{MUSTARD}" stroke="{INK}" stroke-width="2"/>')
    b.append(T(mx + 41, my + 56, lab, "pix", 13, INK))
    b.append(T(mx + 30, my + 118, "VLP-FusionNet", "head", 42, INK, ls=-1))
    yy = my + 158
    for ln in ["Deep-learning cardiac risk", "prediction from ECG signals", "(PTB-XL dataset)"]:
        b.append(T(mx + 30, yy, ln, "body", 25, INK)); yy += 31
    b.append(T(mx + 30, yy + 18, "Co-author · IEEE-style conference paper", "mono", 17, MUTED))
    for j, ww in enumerate([440, 400, 460]):
        b.append(f'<rect x="{mx+30}" y="{yy+44+j*16}" width="{ww}" height="7" fill="{INK}" opacity=".12"/>')
    b.append("</g>")
    sy0 = 470
    b.append(T(30, sy0, "CERTIFICATIONS", "pix", 20, INK))
    certs = [("IIT Hyderabad (TiHAN)", "6-month AI & ML program", TEAL, "cap"),
             ("Google Cloud", "", ORANGE, "googlecloud"), ("Meta", "", RUST, "meta"), ("Oracle", "", TEAL, "star"),
             ("Wolfram Research", "", MUSTARD, "wolfram"), ("University of Illinois", "", ORANGE, "scroll"),
             ("HackerRank", "", RUST, "hackerrank")]
    pos = [(30, sy0 + 30, 530, 170)]
    for k in range(6):
        pos.append((30 + (k % 3) * 182, sy0 + 236 + (k // 3) * 196, 164, 170))
    rots = [-1, 2, -2.5, 1.5, -1, 2.5, -2]
    for i, ((t, s_, c, lg), (x, y, w, h)) in enumerate(zip(certs, pos)):
        css += f".st{i}{{animation:wig 7s ease-in-out {i*0.8:.1f}s infinite;transform-box:fill-box;transform-origin:center}}"
        b.append(stamp(x, y, w, h, t, s_, c, rots[i], f"st{i}", lg))
    return svg(MW, H, "".join(b), ["pix", "head", "body", "mono"], css,
               "Research: VLP-FusionNet paper in progress. Certifications: IIT Hyderabad (TiHAN), Google Cloud, Meta, Oracle, Wolfram Research, University of Illinois, HackerRank")


def stats():
    d = json.load(open(os.path.join(B.ROOT, "data", "stats.json")))
    cal = d["calendar"]; counts = [c for _, c in cal]
    active = sum(1 for c in counts if c)
    best = max(cal, key=lambda x: x[1])
    streak = cur = 0
    for _, c in cal:
        cur = cur + 1 if c else 0; streak = max(streak, cur)
    H = 900
    css = BLINK
    b = [window(4, 4, MW - 14, H - 14, "player_stats.exe")]
    x0 = 30
    b.append(f'<g class="cur">' + T(x0, 88, "1UP", "pix", 19, ORANGE) + "</g>")
    b.append(T(x0 + 78, 88, d["login"].upper(), "pix", 19, INK))
    scores = [("CONTRIBUTIONS", str(d["total"])), ("ACTIVE DAYS", str(active)),
              ("LONGEST STREAK", f"{streak}d"), ("BEST DAY", str(best[1])), ("PUBLIC REPOS", str(d["repos"]))]
    lw = MW - 14 - x0 - 30
    for i, (k, v) in enumerate(scores):
        y = 150 + i * 56
        kw = width(k, "pix", 17); vw = width(v, "head", 34)
        b.append(T(x0, y, k, "pix", 17, INK))
        b.append(f'<line x1="{x0+kw+12}" y1="{y-3}" x2="{x0+lw-vw-14}" y2="{y-3}" stroke="{INK}" stroke-width="3.5" stroke-dasharray="3 7" opacity=".45"/>')
        b.append(T(x0 + lw, y + 5, v, "head", 34, ORANGE if i == 0 else INK, anchor="end"))
    # last 26 weeks
    weeks = 26
    start = dt.date.fromisoformat(cal[-1][0]) - dt.timedelta(days=weeks * 7 - 1)
    start -= dt.timedelta(days=(start.weekday() + 1) % 7)
    cmap = dict(cal)
    hx, hy, cs, gp = x0, 470, 17.5, 3.4
    b.append(T(x0, hy - 46, "LAST 6 MONTHS", "pix", 15, INK))
    lastm = None
    day = start; i = 0
    end = dt.date.fromisoformat(cal[-1][0])
    while day <= end:
        wk, dw = divmod(i, 7)
        c = cmap.get(day.isoformat(), 0)
        lv = 0 if c == 0 else 1 if c <= 2 else 2 if c <= 5 else 3 if c <= 9 else 4
        x = hx + wk * (cs + gp); y = hy + dw * (cs + gp)
        b.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cs}" height="{cs}" fill="{HEAT[lv]}"' + (f' stroke="{INK}" stroke-width="1.5"' if c else "") + "/>")
        if day.month != lastm and dw == 0:
            b.append(T(x, hy - 12, day.strftime("%b").lower(), "mono", 16, MUTED)); lastm = day.month
        day += dt.timedelta(1); i += 1
    hw = weeks * (cs + gp)
    css += f".scan{{animation:scan 7s steps({weeks}) infinite}}@keyframes scan{{from{{transform:translateX(0)}}to{{transform:translateX({hw:.1f}px)}}}}"
    b.append(f'<rect class="scan" x="{hx-3}" y="{hy-4}" width="{cs+6}" height="{7*(cs+gp)+4}" fill="none" stroke="{ORANGE}" stroke-width="3"/>')
    ly = hy + 7 * (cs + gp) + 80
    langs = sorted(d["langs"].items(), key=lambda x: -x[1]); tot = sum(v for _, v in langs)
    top = langs[:3]; rest = tot - sum(v for _, v in top)
    segs = top + ([("Other", rest)] if rest else [])
    b.append(T(x0, ly - 18, "LANGUAGES", "pix", 15, INK))
    bw = MW - 14 - x0 - 30; x = x0
    for j, (nm, v) in enumerate(segs):
        w = max(5, bw * v / tot)
        b.append(f'<rect x="{x:.1f}" y="{ly}" width="{w:.1f}" height="32" fill="{LANGC[j]}" stroke="{INK}" stroke-width="2.5"/>'); x += w
    for j, (nm, v) in enumerate(segs):
        lx = x0 + (j % 2) * 270; yy = ly + 70 + (j // 2) * 34
        b.append(f'<rect x="{lx}" y="{yy-15}" width="16" height="16" fill="{LANGC[j]}" stroke="{INK}" stroke-width="1.5"/>')
        b.append(T(lx + 26, yy, f"{nm} {v/tot*100:.1f}%", "mono", 19, INK))
    upd = dt.date.fromisoformat(d["updated"]).strftime("%d %b %Y").lower()
    b.append(T(x0, H - 40, f"synced daily · last sync {upd}", "mono", 17, MUTED))
    return svg(MW, H, "".join(b), ["pix", "head", "mono"], css,
               f"GitHub stats: {d['total']} contributions in the last year, {active} active days, {d['repos']} public repos")


def footer():
    H = 320
    css = PANDA_CSS + (".blink{animation:blink 1.2s steps(1) infinite}@keyframes blink{50%{opacity:0}}"
                       ".armA{animation:armA .8s steps(1) infinite}.armB{animation:armB .8s steps(1) infinite}"
                       "@keyframes armA{50%{opacity:0}}@keyframes armB{0%{opacity:0}50%{opacity:1}}")
    b = [bg(MW, H)]
    for i, c in enumerate([ORANGE, MUSTARD, TEAL, RUST]):
        b.append(f'<rect x="0" y="{H-48+i*12}" width="{MW}" height="12" fill="{c}"/>')
    b.append(T(32, 84, "Let's build something", "head", 40, INK, ls=-0.5))
    b.append(T(32, 132, "that holds up in production.", "head", 40, INK, ls=-0.5))
    b.append(f'<g class="blink">' + T(32, 210, "PRESS START", "pix", 22, ORANGE) +
             f'<path d="M{32 + width("PRESS START", "pix", 22) + 12} 190 l18 10 l-18 10 z" fill="{ORANGE}"/></g>')
    b.append(panda(452, 150, 6, "wave", bob=False))
    return svg(MW, H, "".join(b), ["pix", "head"], css, "Let's build something that holds up in production. Press start to connect.")


def main(only_stats=False):
    os.makedirs(OUT, exist_ok=True)
    files = {"stats.svg": stats()}
    if not only_stats:
        files.update({"banner.svg": banner(), "about.svg": about(), "stack.svg": stack(),
                      "internship.svg": internship(), "achievements.svg": achievements(),
                      "research.svg": research(), "footer.svg": footer()})
        for m in B.MENU:
            files[f"nav-{m.lower()}.svg"] = nav(m)
        for c in CARDS:
            slug, s = card(c); files[f"card-{slug}.svg"] = s
    for n, s in files.items():
        open(os.path.join(OUT, n), "w").write(s)
    print(f"mobile: {len(files)} files")


if __name__ == "__main__":
    main()
