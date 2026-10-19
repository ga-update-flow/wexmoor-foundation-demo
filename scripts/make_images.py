"""Generate all original artwork for the site as SVG (plus PNG/ICO favicons).

Run:  python3 scripts/make_images.py
Output: public/images/*.svg, public/favicon.svg, public/favicon.png, public/favicon.ico
"""
import os, random, math
from brand import *  # noqa: F401,F403

OUT = os.path.join(ROOT, "public", "images")
os.makedirs(OUT, exist_ok=True)

SKIN = ["#F2D0B5", "#E0AC88", "#C68863", "#A0673F", "#7A4B2A", "#5A3620"]
HAIR = ["#2B1D14", "#4A3020", "#151515", "#7A4A1E", "#B07A3C", "#3A2A1A"]
SHIRTS = [TERRA, GOLD, SAGE, SKY, "#3C5A93", "#E07B4F", "#7DB592", "#B85C8A", "#F0C468"]


def pts(p):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in p)


def w_mark(x, y, size, seed=7, clip_id="wclip", mono=None):
    s = size / 100
    poly = pts([(x + px * s, y + py * s) for px, py in W_POINTS])
    if mono:
        return f'<polygon points="{poly}" fill="{mono}"/>'
    tris = "".join(
        f'<polygon points="{pts([(x + a * s, y + b * s) for a, b in t])}" fill="{c}" stroke="{c}" stroke-width="0.4"/>'
        for t, c in facet_triangles(seed))
    return (f'<clipPath id="{clip_id}"><polygon points="{poly}"/></clipPath>'
            f'<g clip-path="url(#{clip_id})">{tris}</g>')


def write(name, w, h, body, title):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
           f'role="img" aria-label="{title}"><title>{title}</title>{body}</svg>')
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)


# ---------------------------------------------------------------- scene parts
def child(x, y, sc, rnd, arm_up=False, facing=0):
    skin, hair, shirt = rnd.choice(SKIN), rnd.choice(HAIR), rnd.choice(SHIRTS)
    g = []
    # body
    g.append(f'<rect x="{x - 26 * sc:.1f}" y="{y:.1f}" width="{52 * sc:.1f}" height="{70 * sc:.1f}" rx="{20 * sc:.1f}" fill="{shirt}"/>')
    # arms
    if arm_up:
        g.append(f'<rect x="{x + 14 * sc:.1f}" y="{y - 58 * sc:.1f}" width="{13 * sc:.1f}" height="{70 * sc:.1f}" rx="{6 * sc:.1f}" fill="{shirt}" transform="rotate(12 {x + 20 * sc:.1f} {y:.1f})"/>')
        g.append(f'<circle cx="{x + 30 * sc:.1f}" cy="{y - 60 * sc:.1f}" r="{8 * sc:.1f}" fill="{skin}"/>')
    # head
    g.append(f'<circle cx="{x:.1f}" cy="{y - 24 * sc:.1f}" r="{24 * sc:.1f}" fill="{skin}"/>')
    style = rnd.randint(0, 3)
    if style == 0:
        g.append(f'<path d="M{x - 25 * sc:.1f},{y - 26 * sc:.1f} a{25 * sc:.1f},{25 * sc:.1f} 0 0 1 {50 * sc:.1f},0 q{-25 * sc:.1f},{-8 * sc:.1f} {-50 * sc:.1f},0z" fill="{hair}"/>')
    elif style == 1:
        g.append(f'<circle cx="{x:.1f}" cy="{y - 34 * sc:.1f}" r="{21 * sc:.1f}" fill="{hair}"/><circle cx="{x - 22 * sc:.1f}" cy="{y - 40 * sc:.1f}" r="{9 * sc:.1f}" fill="{hair}"/><circle cx="{x + 22 * sc:.1f}" cy="{y - 40 * sc:.1f}" r="{9 * sc:.1f}" fill="{hair}"/>')
    elif style == 2:
        g.append(f'<path d="M{x - 26 * sc:.1f},{y - 20 * sc:.1f} a{26 * sc:.1f},{28 * sc:.1f} 0 0 1 {52 * sc:.1f},0 l0,{26 * sc:.1f} l{-8 * sc:.1f},0 l0,{-22 * sc:.1f} q{-18 * sc:.1f},{-12 * sc:.1f} {-36 * sc:.1f},0 l0,{22 * sc:.1f} l{-8 * sc:.1f},0z" fill="{hair}"/>')
    else:
        g.append(f'<ellipse cx="{x:.1f}" cy="{y - 40 * sc:.1f}" rx="{24 * sc:.1f}" ry="{12 * sc:.1f}" fill="{hair}"/>')
    if facing == 0:
        g.append(f'<circle cx="{x - 8 * sc:.1f}" cy="{y - 24 * sc:.1f}" r="{2.6 * sc:.1f}" fill="#2a2a2a"/><circle cx="{x + 8 * sc:.1f}" cy="{y - 24 * sc:.1f}" r="{2.6 * sc:.1f}" fill="#2a2a2a"/>')
        g.append(f'<path d="M{x - 7 * sc:.1f},{y - 14 * sc:.1f} q{7 * sc:.1f},{6 * sc:.1f} {14 * sc:.1f},0" stroke="#7a3b2a" stroke-width="{2 * sc:.1f}" fill="none" stroke-linecap="round"/>')
    return "".join(g)


def adult(x, y, sc, rnd):
    skin, hair, shirt = rnd.choice(SKIN), rnd.choice(HAIR), rnd.choice([INDIGO, SAGE, TERRA, "#3C5A93"])
    return (f'<rect x="{x - 32 * sc:.1f}" y="{y:.1f}" width="{64 * sc:.1f}" height="{150 * sc:.1f}" rx="{24 * sc:.1f}" fill="{shirt}"/>'
            f'<circle cx="{x:.1f}" cy="{y - 28 * sc:.1f}" r="{27 * sc:.1f}" fill="{skin}"/>'
            f'<path d="M{x - 29 * sc:.1f},{y - 26 * sc:.1f} a{29 * sc:.1f},{30 * sc:.1f} 0 0 1 {58 * sc:.1f},0 l0,{30 * sc:.1f} l{-9 * sc:.1f},0 l0,{-26 * sc:.1f} q{-20 * sc:.1f},{-14 * sc:.1f} {-40 * sc:.1f},0 l0,{26 * sc:.1f} l{-9 * sc:.1f},0z" fill="{hair}"/>'
            f'<circle cx="{x - 9 * sc:.1f}" cy="{y - 28 * sc:.1f}" r="{2.8 * sc:.1f}" fill="#2a2a2a"/><circle cx="{x + 9 * sc:.1f}" cy="{y - 28 * sc:.1f}" r="{2.8 * sc:.1f}" fill="#2a2a2a"/>'
            f'<path d="M{x - 8 * sc:.1f},{y - 16 * sc:.1f} q{8 * sc:.1f},{6 * sc:.1f} {16 * sc:.1f},0" stroke="#7a3b2a" stroke-width="{2.2 * sc:.1f}" fill="none" stroke-linecap="round"/>')


def book(x, y, w, h, color, rot=0):
    return (f'<g transform="rotate({rot} {x + w / 2:.1f} {y + h / 2:.1f})"><rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="3" fill="{color}"/>'
            f'<rect x="{x + w * 0.1:.1f}" y="{y + h * 0.15:.1f}" width="{w * 0.8:.1f}" height="{h * 0.08:.1f}" fill="#fff" opacity=".55"/></g>')


def shelf(x, y, w, rnd):
    g = [f'<rect x="{x}" y="{y + 90}" width="{w}" height="10" fill="#8a6a4a"/>']
    cx = x + 6
    while cx < x + w - 20:
        bw = rnd.randint(12, 22); bh = rnd.randint(55, 85)
        g.append(f'<rect x="{cx}" y="{y + 90 - bh}" width="{bw}" height="{bh}" rx="2" fill="{rnd.choice(SHIRTS)}"/>')
        cx += bw + 2
    return "".join(g)


def board(x, y, w, h, text):
    return (f'<rect x="{x - 8}" y="{y - 8}" width="{w + 16}" height="{h + 16}" rx="6" fill="#8a6a4a"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="#2F4A44"/>'
            f'<text x="{x + w / 2}" y="{y + h / 2 + 18}" font-family="Georgia, serif" font-size="{min(54, h * 0.45):.0f}" fill="#F5EFE6" text-anchor="middle" opacity=".9">{text}</text>')


def window(x, y, w, h):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#BFDCE6" stroke="#fff" stroke-width="8"/>'
            f'<line x1="{x + w / 2}" y1="{y}" x2="{x + w / 2}" y2="{y + h}" stroke="#fff" stroke-width="6"/>'
            f'<line x1="{x}" y1="{y + h / 2}" x2="{x + w}" y2="{y + h / 2}" stroke="#fff" stroke-width="6"/>'
            f'<circle cx="{x + w * 0.75}" cy="{y + h * 0.28}" r="{h * 0.12}" fill="{GOLD}" opacity=".85"/>')


def bunting(x1, x2, y, rnd):
    g = [f'<path d="M{x1},{y} Q{(x1 + x2) / 2},{y + 30} {x2},{y}" stroke="#7a6a5a" stroke-width="2" fill="none"/>']
    n = int((x2 - x1) / 46)
    for i in range(n):
        t = (i + 0.5) / n
        px = x1 + (x2 - x1) * t
        py = y + 30 * 4 * t * (1 - t) * 0.5 + 1
        g.append(f'<polygon points="{px - 15:.1f},{py:.1f} {px + 15:.1f},{py:.1f} {px:.1f},{py + 30:.1f}" fill="{rnd.choice(SHIRTS)}"/>')
    return "".join(g)


def scene(w, h, seed, kind="class", text="A b C"):
    rnd = random.Random(seed)
    wall = rnd.choice(["#F3E9DA", "#EAF0EE", "#F1E6E0", "#E9ECF3"])
    floor_y = h * 0.78
    g = [f'<rect width="{w}" height="{h}" fill="{wall}"/>',
         f'<rect y="{floor_y:.1f}" width="{w}" height="{h - floor_y:.1f}" fill="{rnd.choice(["#D9C3A5", "#C9B79B", "#BFCFC4"])}"/>']
    # rug of facets
    for i in range(0, w, 80):
        g.append(f'<polygon points="{i},{h} {i + 80},{h} {i + 40},{floor_y + 20:.1f}" fill="{rnd.choice(FACETS)}" opacity=".35"/>')
    if kind in ("class", "reading"):
        g.append(board(w * 0.08, h * 0.12, w * 0.30, h * 0.36, text))
        g.append(window(w * 0.70, h * 0.10, w * 0.18, h * 0.40))
        g.append(bunting(w * 0.40, w * 0.68, h * 0.08, rnd))
        g.append(shelf(int(w * 0.42), int(h * 0.30), int(w * 0.22), rnd))
    elif kind == "outdoor":
        g[0] = f'<rect width="{w}" height="{h}" fill="#CFE5EC"/>'
        g.append(f'<circle cx="{w * 0.82}" cy="{h * 0.22}" r="{h * 0.11}" fill="{GOLD}"/>')
        for i in range(5):
            tx = w * (0.08 + i * 0.22)
            g.append(f'<rect x="{tx - 8:.0f}" y="{h * 0.45:.0f}" width="16" height="{h * 0.35:.0f}" fill="#7a5a3a"/><circle cx="{tx:.0f}" cy="{h * 0.42:.0f}" r="{h * 0.14:.0f}" fill="{rnd.choice([SAGE, "#7DB592", "#4E8A68"])}"/>')
        g[1] = f'<rect y="{floor_y:.1f}" width="{w}" height="{h - floor_y:.1f}" fill="#9CC48A"/>'
    elif kind == "office":
        g.append(window(w * 0.06, h * 0.10, w * 0.22, h * 0.45))
        g.append(shelf(int(w * 0.62), int(h * 0.12), int(w * 0.30), rnd))
        g.append(shelf(int(w * 0.62), int(h * 0.36), int(w * 0.30), rnd))
    # people
    count = max(2, int(w / (230 if w / h > 2.5 else 170)))
    base_sc = h / 420 * (1.55 if w / h > 2.5 else 1)
    positions = sorted(rnd.uniform(0.05, 0.95) for _ in range(count))
    if kind != "office" and rnd.random() < 0.7:
        g.append(adult(w * rnd.uniform(0.15, 0.85), floor_y - 150 * base_sc * 1.15, base_sc * 1.15, rnd))
    for p in positions:
        sc = base_sc * rnd.uniform(0.85, 1.15)
        g.append(child(w * p, floor_y - 40 * sc, sc, rnd, arm_up=(kind == "class" and rnd.random() < 0.45)))
    if kind == "reading":
        for p in positions:
            g.append(book(w * p - 30 * base_sc, floor_y - 30 * base_sc, 60 * base_sc, 40 * base_sc, rnd.choice(SHIRTS), rnd.randint(-12, 12)))
    # tables in front for classroom scenes
    if kind == "class":
        for i in range(0, w, int(w / 3)):
            g.append(f'<rect x="{i + 30}" y="{floor_y + 4:.0f}" width="{w / 3 - 60:.0f}" height="{h * 0.07:.0f}" rx="6" fill="#A9825C"/>')
    if kind == "office":
        g.append(f'<rect x="{w * 0.15:.0f}" y="{floor_y - 10:.0f}" width="{w * 0.7:.0f}" height="{h * 0.08:.0f}" rx="8" fill="#8a6a4a"/>')
    return "".join(g)


def banner(name, seed, kind, text, title):
    w, h = 1600, 400
    write(name, w, h, scene(w, h, seed, kind, text), title)


# ---------------------------------------------------------------- brand assets
def logo_files():
    # full horizontal logo
    body = (w_mark(0, 4, 92, clip_id="lw") +
            '<text x="108" y="38" font-family="Mulish, Arial, sans-serif" font-weight="800" font-size="30" letter-spacing="1.5" fill="#263B6A">WEXMOOR</text>'
            '<text x="108" y="70" font-family="Mulish, Arial, sans-serif" font-weight="300" font-size="30" letter-spacing="1.5" fill="#263B6A">FOUNDATION</text>'
            '<text x="109" y="95" font-family="Cormorant Garamond, Georgia, serif" font-style="italic" font-size="19" fill="#CC5F3A">Read. Teach. Lead.</text>')
    write("logo.svg", 330, 100, body, "The Wexmoor Foundation")
    write("logo-icon-white.svg", 100, 100, w_mark(0, 0, 100, mono="#ffffff"), "Wexmoor Foundation mark")
    fav = f'<rect width="100" height="100" rx="18" fill="{CREAM}"/>' + w_mark(8, 8, 84, clip_id="fw")
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">{fav}</svg>'
    with open(os.path.join(ROOT, "public", "favicon.svg"), "w") as f:
        f.write(svg)
    # raster favicon via PIL
    from PIL import Image, ImageDraw
    S = 256
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, S - 1, S - 1], radius=46, fill=CREAM)
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).polygon([(20 + x * 2.16, 20 + y * 2.16) for x, y in W_POINTS], fill=255)
    layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    for t, c in facet_triangles(7):
        ld.polygon([(20 + x * 2.16, 20 + y * 2.16) for x, y in t], fill=c)
    im.paste(layer, (0, 0), mask)
    im.save(os.path.join(ROOT, "public", "favicon.png"))
    im.save(os.path.join(ROOT, "public", "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
    im.resize((180, 180)).save(os.path.join(ROOT, "public", "apple-touch-icon.png"))


def footer_pattern():
    rnd = random.Random(11)
    w, h = 1600, 260
    g = []
    cols, rows = 16, 4
    P = {(i, j): (i * w / cols + (rnd.uniform(-40, 40) if 0 < i < cols else 0),
                  j * h / rows + (rnd.uniform(-25, 25) if 0 < j < rows else 0)) for i in range(cols + 1) for j in range(rows + 1)}
    pal = [INDIGO, "#2F4B80", "#3C5A93", "#33507F", TERRA, "#B9532F", SAGE, "#4E8A68", GOLD]
    for i in range(cols):
        for j in range(rows):
            a, b, c, d = P[i, j], P[i + 1, j], P[i + 1, j + 1], P[i, j + 1]
            base = pal[(i // 3 + j) % 4] if rnd.random() < 0.8 else rnd.choice(pal)
            g.append(f'<polygon points="{pts([a, b, c])}" fill="{base}"/>')
            g.append(f'<polygon points="{pts([a, c, d])}" fill="{rnd.choice(pal)}" opacity=".92"/>')
    write("footer-facets.svg", w, h, "".join(g), "Decorative faceted pattern")


def portrait(name, seed, title, w=400, h=600):
    rnd = random.Random(seed)
    bg = rnd.choice([SAND, "#DCE6EA", "#EADBD2", "#DDE8DF"])
    body = f'<rect width="{w}" height="{h}" fill="{bg}"/>'
    body += "".join(f'<polygon points="{pts(t2)}" fill="{c}" opacity=".18"/>' for t, c in facet_triangles(seed, 4)
                    for t2 in [[(x * w / 100, y * h / 100) for x, y in t]])
    body += adult(w / 2, h * 0.52, w / 170, rnd)
    write(name, w, h, body, title)


def chart(name):
    w, h = 600, 464
    bars = [("Low-poverty schools", 41, SAGE), ("High-poverty schools", 24, TERRA)]
    g = [f'<rect width="{w}" height="{h}" fill="#fff"/>',
         f'<text x="30" y="40" font-family="Mulish, Arial" font-size="19" font-weight="700" fill="{INDIGO}">Students taught by a teacher who exceeded</text>',
         f'<text x="30" y="64" font-family="Mulish, Arial" font-size="19" font-weight="700" fill="{INDIGO}">expected growth the prior year (BCS, illustrative)</text>',
         f'<line x1="60" y1="400" x2="560" y2="400" stroke="#999"/>']
    for i, (lab, v, c) in enumerate(bars):
        x = 120 + i * 220
        bh = v * 6.5
        g.append(f'<rect x="{x}" y="{400 - bh}" width="140" height="{bh}" fill="{c}"/>')
        g.append(f'<text x="{x + 70}" y="{392 - bh}" font-family="Mulish, Arial" font-size="24" font-weight="700" text-anchor="middle" fill="{INK}">{v}%</text>')
        g.append(f'<text x="{x + 70}" y="428" font-family="Mulish, Arial" font-size="15" text-anchor="middle" fill="{INK}">{lab}</text>')
    write(name, w, h, "".join(g), "Bar chart: 41% of students in low-poverty schools versus 24% in high-poverty schools were taught by a teacher who exceeded expected growth")


def beyond_graphic(name):
    w, h = 900, 380
    items = [("GRANTMAKING", "Multi-year support for proven partners", INDIGO),
             ("CONVENING", "Bringing educators, funders and leaders together", TERRA),
             ("RESEARCH", "Sponsoring studies that inform practice", SAGE),
             ("ADVOCACY", "Elevating evidence-based policy", GOLD)]
    g = [f'<rect width="{w}" height="{h}" fill="{CREAM}"/>',
         f'<text x="{w / 2}" y="52" font-family="Mulish, Arial" font-size="26" font-weight="800" text-anchor="middle" fill="{INDIGO}" letter-spacing="2">GRANTMAKING AND BEYOND</text>']
    for i, (t, s, c) in enumerate(items):
        x = 40 + i * 210
        g.append(f'<polygon points="{x + 95},{90} {x + 185},{150} {x + 185},{250} {x + 95},{310} {x + 5},{250} {x + 5},{150}" fill="{c}"/>')
        g.append(f'<text x="{x + 95}" y="205" font-family="Mulish, Arial" font-size="17" font-weight="800" text-anchor="middle" fill="#fff">{t}</text>')
        words, line, lines = s.split(), "", []
        for wd in words:
            if len(line + wd) > 22:
                lines.append(line); line = ""
            line += wd + " "
        lines.append(line)
        for k, ln in enumerate(lines):
            g.append(f'<text x="{x + 95}" y="{336 + k * 18}" font-family="Mulish, Arial" font-size="13" text-anchor="middle" fill="{INK}">{ln.strip()}</text>')
    write(name, w, h, "".join(g), "Grantmaking and beyond: grantmaking, convening, research and advocacy")


if __name__ == "__main__":
    logo_files()
    footer_pattern()
    write("hero-home.svg", 1600, 1000, scene(1600, 1000, 3, "class", "A b C"), "Students raising hands in a classroom")
    banners = [
        ("banner-about.svg", 21, "class", "Learn", "Classroom with students raising hands"),
        ("banner-board-chair.svg", 22, "office", "", "Foundation office"),
        ("banner-history.svg", 23, "outdoor", "", "Students outside under trees"),
        ("banner-approach.svg", 24, "class", "1 + 2", "Teacher leading a math lesson"),
        ("banner-people.svg", 25, "office", "", "Foundation team"),
        ("banner-financials.svg", 26, "office", "", "Foundation office"),
        ("banner-annual-reports.svg", 27, "class", "Read!", "Students raising hands"),
        ("banner-careers.svg", 28, "office", "", "Foundation office"),
        ("banner-news.svg", 29, "reading", "News", "Students reading"),
        ("banner-equity.svg", 30, "outdoor", "", "Students together outside"),
        ("banner-what-we-fund.svg", 31, "outdoor", "", "Young students outdoors with a teacher"),
        ("banner-mission.svg", 32, "reading", "ABC", "Teacher reading with young students"),
        ("banner-early-grades.svg", 33, "outdoor", "", "Smiling student on a playground"),
        ("banner-educators.svg", 34, "class", "Plan", "Teachers and students in a classroom"),
        ("banner-grantees.svg", 35, "class", "Hello", "Students in a classroom"),
        ("banner-spring.svg", 36, "outdoor", "", "Spring schoolyard"),
        ("banner-fall.svg", 37, "outdoor", "", "Fall schoolyard"),
        ("banner-partner.svg", 38, "reading", "a e i", "Young students with books"),
        ("banner-process.svg", 39, "class", "Cat Hat", "Students working together at tables"),
        ("banner-faqs.svg", 40, "reading", "?", "Students reading"),
        ("banner-contact.svg", 41, "office", "", "Foundation office"),
        ("banner-search.svg", 42, "reading", "Find", "Students reading"),
    ]
    for b in banners:
        banner(*b)
    write("process-side.svg", 475, 580, scene(475, 580, 51, "class", "b d p"), "Teacher working with students")
    write("faqs-side.svg", 435, 535, scene(435, 535, 52, "outdoor"), "Students on a playground")
    write("partner-side.svg", 475, 247, scene(475, 247, 53, "reading", "Read"), "Teacher reading with students")
    write("strategic-reading.svg", 600, 400, scene(600, 400, 54, "reading", "sh ch th"), "Two students reading picture books")
    write("grow-pipeline.svg", 600, 400, scene(600, 400, 55, "class", "Plan"), "Student teacher with a mentor teacher")
    write("multiply-reach.svg", 600, 400, scene(600, 400, 56, "class", "Team"), "Teacher leading a small team")
    write("educators-issue.svg", 600, 338, scene(600, 338, 57, "class", "Grow"), "Teacher at the board with students")
    write("board-group.svg", 600, 400, scene(600, 400, 58, "office"), "Illustration of the Board of Directors")
    write("news-read-brannock.svg", 825, 510, scene(825, 510, 61, "reading", "10 yrs"), "Read Brannock celebration")
    write("news-coaching.svg", 825, 510, scene(825, 510, 62, "class", "Coach"), "Literacy coach in a classroom")
    write("news-callahan.svg", 825, 510, scene(825, 510, 63, "office"), "Foundation office")
    portrait("chair-portrait.svg", 71, "Portrait illustration of Board Chair Margaret Wexmoor Ellison", 475, 600)
    portrait("staff-callahan.svg", 72, "Portrait illustration of Dr. Renee Callahan")
    portrait("staff-osei.svg", 73, "Portrait illustration of Martin Osei")
    portrait("staff-moreno.svg", 74, "Portrait illustration of Leah Moreno")
    chart("data-chart.svg")
    beyond_graphic("grantmaking-and-beyond.svg")
    print("images written to", OUT)
