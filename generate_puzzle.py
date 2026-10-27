import html

W, H, OX, OY = 300, 200, 20, 84
CW, CH = OX * 2 + 3 * W, OY + 4 * H + 36
START = 3.0  # seconds before the puzzle starts solving

PIECES = [
    ("hello, world", "#cba6f7", ["Shraddha Pandey", "Software Dev Engineer", "MCA 2026 · Bengaluru", "OOP · DSA · Full-stack", "REST APIs · React"]),
    ("education / 01", "#89b4fa", ["BCA", "Surana College", "SGPA 8.42", "Completed"]),
    ("education / 02", "#94e2d5", ["MCA", "RV Institute of Tech & Mgmt", "2024 – 2026", "CGPA 8.9"]),
    ("experience / 2024", "#fab387", ["IoT Engineering Intern", "Hardware Technologies", "Vijayanagar · 2024", "C/C++ firmware on Arduino", "Real-time sensor streams"]),
    ("experience / 2026", "#f5c2e7", ["Junior Software Developer", "Edutainer · Jan – May 2026", "Reusable React components", "Client state + REST API sync"]),
    ("languages & core", "#a6e3a1", ["Python · JavaScript · TS", "SQL · Java · C", "DSA · OOP · REST design", "DB normalization", "Async programming"]),
    ("project / 01", "#f9e2af", ["Sentinel-Agent v2.0", "Async API monitor · FastAPI", "500+ events processed", "99.9% uptime via fallbacks", "~35% fewer false alerts"]),
    ("project / 02", "#89dceb", ["Job Portal", "Node · Express · React", "SQL + MongoDB dual-DB", "Cross-DB queries, 300+ records", "Indexed, optimized search"]),
    ("project / 03", "#f38ba8", ["Dark Pattern Detector", "Chrome ext · Manifest V3", "Flask REST API under 300 ms", "Async DOM parsing"]),
    ("project / 04", "#cba6f7", ["Sprucer", "Resume-to-JD fit scorer", "TF-IDF + cosine similarity", "100+ documents scored", "Python · Flask · scikit-learn"]),
    ("stack", "#89b4fa", ["Backend & Web", "Node · Express · FastAPI", "Flask · REST · CORS", "Frontend: React · TS · Vite", "Tailwind · Chrome Extensions", "SQL · MongoDB · Git · Linux"]),
    ("awards & certs", "#94e2d5", ["Winner – Ideacity", "Competition & Research Paper", "Presentation", "Finalist – Christ University", "Hackathon", "IBM Enterprise-Grade AI", "Power BI · Advanced Excel"]),
]

# piece i starts in slot PERM[i] (no piece starts in its own slot) with a small tilt
PERM = [5, 10, 7, 11, 0, 8, 2, 9, 4, 1, 6, 3]
TILT = [-9, 7, -6, 11, -12, 8, -7, 10, -8, 6, -10, 9]


def edge(x, y, dx, dy, L, kind):
    if kind == 0:
        return f"L{x + dx * L:.1f} {y + dy * L:.1f} "
    a, b = 0.5 - 24 / L, 0.5 + 24 / L
    sw = 1 if kind == 1 else 0
    return (f"L{x + dx * L * a:.1f} {y + dy * L * a:.1f} "
            f"A26 26 0 1 {sw} {x + dx * L * b:.1f} {y + dy * L * b:.1f} "
            f"L{x + dx * L:.1f} {y + dy * L:.1f} ")


def shape(c, r):
    top = -1 if r > 0 else 0
    right = 1 if c < 2 else 0
    bottom = 1 if r < 2 else 0
    left = -1 if c > 0 else 0
    d = "M0 0 "
    d += edge(0, 0, 1, 0, W, top)
    d += edge(W, 0, 0, 1, H, right)
    d += edge(W, H, -1, 0, W, bottom)
    d += edge(0, H, 0, -1, H, left)
    return d + "Z"


css = """
text{font-family:'JetBrains Mono','SFMono-Regular',Consolas,'Liberation Mono',monospace}
.pc{transform-box:fill-box;transform-origin:center}
@keyframes fi{from{opacity:0}to{opacity:1}}
@keyframes fo{from{opacity:1}to{opacity:0}}
@keyframes bar{from{transform:scaleX(0)}to{transform:scaleX(1)}}
.bar{transform-box:fill-box;transform-origin:left center;animation:bar %ss linear both}
.s1{animation:fo .4s ease %ss both}
.s2{opacity:0;animation:fi .5s ease %ss both}
""" % (START, START + 0.9, START + 1.2)

body = []
for i, (title, col, lines) in enumerate(PIECES):
    c, r = i % 3, i // 3
    x0, y0 = OX + c * W, OY + r * H
    sc, sr = PERM[i] % 3, PERM[i] // 3
    dx, dy = (sc - c) * W, (sr - r) * H
    delay = START + i * 0.1
    css += (f"@keyframes mv{i}{{from{{transform:translate({dx}px,{dy}px) rotate({TILT[i]}deg)}}"
            f"to{{transform:translate(0,0) rotate(0)}}}}\n"
            f".p{i}{{animation:mv{i} 1.1s cubic-bezier(.2,.9,.25,1.08) {delay:.1f}s both}}\n"
            f".c{i}{{opacity:0;animation:fi .6s ease {delay + 0.9:.1f}s both}}\n"
            f".f{i}{{animation:fo .35s ease {delay + 0.5:.1f}s both}}\n")
    t = [f'<text x="48" y="54" font-size="11" letter-spacing="1.5" fill="{col}">{html.escape(title.upper())}</text>']
    for j, ln in enumerate(lines):
        y = 80 + j * (20 if len(lines) <= 6 else 18)
        if j == 0:
            t.append(f'<text x="48" y="{y}" font-size="14" font-weight="700" fill="#cdd6f4">{html.escape(ln)}</text>')
        else:
            t.append(f'<text x="48" y="{y}" font-size="12" fill="#a6adc8">{html.escape(ln)}</text>')
    body.append(
        f'<g transform="translate({x0} {y0})"><g class="pc p{i}">'
        f'<path d="{shape(c, r)}" fill="{col}" fill-opacity=".10" stroke="{col}" stroke-width="2" stroke-linejoin="round"/>'
        f'<g class="f{i}"><text x="150" y="118" font-size="64" font-weight="700" text-anchor="middle" fill="{col}" fill-opacity=".55">?</text>'
        f'<text x="150" y="150" font-size="11" text-anchor="middle" fill="{col}" fill-opacity=".7">piece {i + 1:02d}</text></g>'
        f'<g class="c{i}">{"".join(t)}</g></g></g>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CW} {CH}" width="{CW}" height="{CH}" role="img" aria-label="Resume puzzle of Shraddha Pandey: education, internships, skills and projects">
<style>{css}</style>
<rect width="{CW}" height="{CH}" rx="18" fill="#1e1e2e"/>
<rect x=".5" y=".5" width="{CW - 1}" height="{CH - 1}" rx="18" fill="none" stroke="#45475a"/>
<circle cx="34" cy="34" r="6" fill="#f38ba8"/><circle cx="54" cy="34" r="6" fill="#f9e2af"/><circle cx="74" cy="34" r="6" fill="#a6e3a1"/>
<text x="96" y="39" font-size="13" fill="#7f849c">shraddha-pandey / resume.puzzle</text>
<text class="s1" x="{CW - 30}" y="39" font-size="13" text-anchor="end" fill="#fab387">shuffled · solving in 3s…</text>
<text class="s2" x="{CW - 30}" y="39" font-size="13" text-anchor="end" fill="#a6e3a1">solved ✓ every piece in place</text>
<rect x="{OX}" y="56" width="{3 * W}" height="3" rx="1.5" fill="#313244"/>
<rect class="bar" x="{OX}" y="56" width="{3 * W}" height="3" rx="1.5" fill="#cba6f7"/>
{"".join(body)}
</svg>'''

open("/mnt/user-data/outputs/puzzle-resume.svg", "w").write(svg)
print(len(svg), "bytes")
