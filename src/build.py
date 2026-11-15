"""Builds the static images for the profile README into assets/.

Run: py -3 src/build.py   (from the repo root). Live images (stats card, snake) are made by
.github/workflows/profile.yml and live on the `output` branch.
"""
import base64
import io
import pathlib
from xml.sax.saxutils import escape

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
OUT = ROOT / "assets"
OUT.mkdir(exist_ok=True)

FONT = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'Cascadia Code', 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

THEMES = {
    "dark": dict(bg="#0d1117", panel="#161b22", border="#30363d", text="#e6edf3", soft="#c9d1d9",
                 muted="#8b949e", c1="#22d3ee", c2="#a78bfa", chip="#21262d", glow=".32"),
    "light": dict(bg="#ffffff", panel="#ffffff", border="#d0d7de", text="#1f2328", soft="#31373d",
                  muted="#59636e", c1="#0891b2", c2="#7c3aed", chip="#f0f3f6", glow=".16"),
}


def png_data(path: pathlib.Path, size: tuple[int, int] | None = None, crop=None, fmt="PNG") -> str:
    im = Image.open(path).convert("RGB" if fmt == "JPEG" else "RGBA")
    if crop:
        im = im.crop(crop)
    if size:
        im = im.resize(size, Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, fmt, **({"quality": 82} if fmt == "JPEG" else {"optimize": True}))
    mime = "image/jpeg" if fmt == "JPEG" else "image/png"
    return f"data:{mime};base64," + base64.b64encode(buf.getvalue()).decode()


def grad(t: dict, gid: str = "g") -> str:
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0">'
            f'<stop offset="0" stop-color="{t["c1"]}"/><stop offset="1" stop-color="{t["c2"]}"/></linearGradient>')


# --------------------------------------------------------------------------- header

PHRASES = [
    "applyfirst: jobs the hour they go up",
    "Wavr: control Chrome with your hands",
    "Zephyr RTOS: fixing GPIO drivers in C",
]


def typing(t: dict, x: int, y: int) -> str:
    slot, total = 4.6, 4.6 * len(PHRASES)
    out = [f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="25" fill="{t["c1"]}" font-weight="700">&gt;</text>']
    for i, phrase in enumerate(PHRASES):
        start, end = slot * i, slot * i + 4.1
        spans = []
        for j, ch in enumerate(phrase):
            on = (start + 0.25 + 0.055 * j) / total
            off = end / total
            spans.append(
                f'<tspan fill-opacity="0">{escape(ch)}<animate attributeName="fill-opacity" values="0;1;0" '
                f'keyTimes="0;{on:.4f};{off:.4f}" calcMode="discrete" dur="{total}s" repeatCount="indefinite"/></tspan>')
        out.append(f'<text x="{x + 30}" y="{y}" font-family="{MONO}" font-size="25" fill="{t["soft"]}" '
                   f'xml:space="preserve">{"".join(spans)}</text>')
    return "".join(out)


def header(t: dict) -> str:
    W, H = 1200, 300
    ring = lambda r, c, dur, rev=False: (
        f'<g><circle cx="1010" cy="150" r="{r}" fill="none" stroke="{t["border"]}" stroke-width="1.5"/>'
        f'<circle cx="{1010 + r}" cy="150" r="7" fill="{c}"/>'
        f'<animateTransform attributeName="transform" type="rotate" from="{"360" if rev else "0"} 1010 150" '
        f'to="{"0" if rev else "360"} 1010 150" dur="{dur}s" repeatCount="indefinite"/></g>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>{grad(t)}
<radialGradient id="g1"><stop offset="0" stop-color="{t["c1"]}" stop-opacity="{t["glow"]}"/><stop offset="1" stop-color="{t["c1"]}" stop-opacity="0"/></radialGradient>
<radialGradient id="g2"><stop offset="0" stop-color="{t["c2"]}" stop-opacity="{t["glow"]}"/><stop offset="1" stop-color="{t["c2"]}" stop-opacity="0"/></radialGradient>
<pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.3" fill="{t["muted"]}" fill-opacity=".28"/></pattern>
<clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#frame)">
<rect width="{W}" height="{H}" fill="{t["bg"]}"/>
<rect width="{W}" height="{H}" fill="url(#dots)"/>
<circle cx="160" cy="30" r="330" fill="url(#g1)"><animate attributeName="cx" values="160;330;160" dur="16s" repeatCount="indefinite"/></circle>
<circle cx="1060" cy="290" r="380" fill="url(#g2)"><animate attributeName="cy" values="290;190;290" dur="18s" repeatCount="indefinite"/></circle>
{ring(64, t["c1"], 9)}{ring(102, t["c2"], 15, True)}{ring(140, t["c1"], 24)}
<circle cx="1010" cy="150" r="26" fill="url(#g)"/>
<circle cx="1010" cy="150" r="26" fill="none" stroke="url(#g)" stroke-width="2"><animate attributeName="r" values="26;46;26" dur="3.2s" repeatCount="indefinite"/><animate attributeName="stroke-opacity" values=".9;0;.9" dur="3.2s" repeatCount="indefinite"/></circle>
</g>
<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="18" fill="none" stroke="{t["border"]}" stroke-width="1.5"/>
<text x="70" y="136" font-family="{FONT}" font-size="92" font-weight="800" letter-spacing="-2.5" fill="url(#g)">Jamin Xu</text>
<text x="74" y="188" font-family="{FONT}" font-size="29" fill="{t["text"]}">I build AI agents and tools that do real work.</text>
{typing(t, 74, 248)}
</svg>'''


# --------------------------------------------------------------------------- project cards

def chips(t: dict, items: list[str], x: int, y: int) -> str:
    out, cx = [], x
    for it in items:
        w = int(len(it) * 8.6 + 26)
        out.append(f'<rect x="{cx}" y="{y}" width="{w}" height="30" rx="15" fill="{t["chip"]}" stroke="{t["border"]}"/>'
                   f'<text x="{cx + w / 2}" y="{y + 20}" text-anchor="middle" font-family="{FONT}" font-size="15" '
                   f'fill="{t["soft"]}">{escape(it)}</text>')
        cx += w + 8
    return "".join(out)


def icon_box(t: dict, inner: str) -> str:
    return (f'<rect x="28" y="30" width="60" height="60" rx="15" fill="url(#g)" fill-opacity=".14" stroke="url(#g)" stroke-width="1.5"/>'
            f'<g transform="translate(28 30)">{inner}</g>')


ICONS = {
    "applyfirst": lambda t: '<path d="M34 9 L17 34 H29 L25 51 L43 25 H31 Z" fill="url(#g)"/>',
    "zephyr": lambda t: ('<rect x="18" y="18" width="24" height="24" rx="4" fill="none" stroke="url(#g)" stroke-width="3"/>'
                         + "".join(f'<path d="M{p} 10 V18 M{p} 42 V50 M10 {p} H18 M42 {p} H50" stroke="url(#g)" stroke-width="3" stroke-linecap="round"/>' for p in (24, 30, 36))),
    "decision": lambda t: ('<path d="M30 16 L16 42 M30 16 L44 42 M30 16 V42" stroke="url(#g)" stroke-width="3" fill="none"/>'
                           '<circle cx="30" cy="14" r="6" fill="url(#g)"/><circle cx="16" cy="44" r="5" fill="url(#g)"/>'
                           '<circle cx="30" cy="44" r="5" fill="url(#g)"/><circle cx="44" cy="44" r="5" fill="url(#g)"/>'),
}

HAND = {  # MediaPipe's 21 hand landmarks, open palm, in a 150x140 box
    0: (78, 136), 1: (52, 124), 2: (34, 106), 3: (22, 90), 4: (12, 76),
    5: (56, 80), 6: (51, 56), 7: (48, 40), 8: (45, 26),
    9: (78, 76), 10: (78, 49), 11: (78, 32), 12: (78, 16),
    13: (98, 80), 14: (103, 55), 15: (106, 40), 16: (109, 27),
    17: (116, 89), 18: (126, 70), 19: (132, 58), 20: (137, 47),
}
HAND_LINKS = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 5), (5, 6), (6, 7), (7, 8), (5, 9), (9, 10), (10, 11), (11, 12),
              (9, 13), (13, 14), (14, 15), (15, 16), (13, 17), (17, 18), (18, 19), (19, 20), (0, 17)]


def visual(t: dict, key: str) -> str:
    x, y, w, h = 372, 26, 202, 124
    frame = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{t["bg"]}" stroke="{t["border"]}"/>'
    if key == "applyfirst":
        img = png_data(SRC / "applyfirst-jobs.png", (404, 248), crop=(0, 0, 1280, 786 if False else 760), fmt="JPEG")
        return (f'<clipPath id="shot"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12"/></clipPath>'
                f'<image href="{img}" x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMinYMin slice" clip-path="url(#shot)"/>'
                f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="none" stroke="{t["border"]}" stroke-width="1.5"/>')
    if key == "wavr":
        ox, oy = x + 26, y - 14
        lines = "".join(f'<line x1="{ox + HAND[a][0] * .78}" y1="{oy + HAND[a][1] * .78 + 20}" x2="{ox + HAND[b][0] * .78}" '
                        f'y2="{oy + HAND[b][1] * .78 + 20}" stroke="url(#g)" stroke-width="2.5" stroke-linecap="round"/>' for a, b in HAND_LINKS)
        dots = ""
        for k, (px, py) in HAND.items():
            cx, cy = ox + px * .78, oy + py * .78 + 20
            tip = k in (4, 8, 12, 16, 20)
            anim = (f'<animate attributeName="r" values="3.5;6;3.5" dur="1.8s" begin="{k * .09:.2f}s" repeatCount="indefinite"/>' if tip else "")
            dots += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{3.5 if tip else 3}" fill="{t["c1"] if tip else t["c2"]}">{anim}</circle>'
        return frame + lines + dots
    if key == "zephyr":
        cx, cy = x + 62, y + 62
        pins = "".join(f'<path d="M{cx - 28 + i * 14} {cy - 40} V{cy - 30} M{cx - 28 + i * 14} {cy + 30} V{cy + 40}" stroke="{t["muted"]}" stroke-width="3"/>' for i in range(5))
        chip = (f'<rect x="{cx - 34}" y="{cy - 30}" width="68" height="60" rx="8" fill="{t["chip"]}" stroke="url(#g)" stroke-width="2"/>'
                f'<text x="{cx}" y="{cy + 7}" text-anchor="middle" font-family="{MONO}" font-size="17" font-weight="700" fill="{t["text"]}">GPIO</text>')
        wave_x = x + 108
        wave = (f'<path d="M{wave_x} {cy + 14} h12 v-28 h14 v28 h14 v-28 h14 v28 h12" fill="none" stroke="url(#g)" stroke-width="3" '
                f'stroke-dasharray="160" stroke-dashoffset="160"><animate attributeName="stroke-dashoffset" values="160;0;0" '
                f'keyTimes="0;.6;1" dur="2.6s" repeatCount="indefinite"/></path>')
        return frame + pins + chip + wave
    if key == "decision":
        bx = [(x + 14, "Known"), (x + 76, "Assumed"), (x + 146, "Missing")]
        root = (f'<rect x="{x + 56}" y="{y + 14}" width="90" height="30" rx="8" fill="url(#g)" fill-opacity=".9"/>'
                f'<text x="{x + 101}" y="{y + 35}" text-anchor="middle" font-family="{FONT}" font-size="15" font-weight="700" fill="{t["bg"]}">Decision</text>')
        kids = ""
        for i, (bxx, label) in enumerate(bx):
            wbox = 50 if i != 1 else 62
            kids += (f'<path d="M{x + 101} {y + 44} C{x + 101} {y + 64} {bxx + wbox / 2} {y + 64} {bxx + wbox / 2} {y + 82}" fill="none" stroke="{t["muted"]}" stroke-width="2"/>'
                     f'<rect x="{bxx}" y="{y + 82}" width="{wbox}" height="28" rx="7" fill="{t["chip"]}" stroke="url(#g)" stroke-width="1.5">'
                     f'<animate attributeName="stroke-opacity" values=".3;1;.3" dur="2.4s" begin="{i * .5}s" repeatCount="indefinite"/></rect>'
                     f'<text x="{bxx + wbox / 2}" y="{y + 101}" text-anchor="middle" font-family="{FONT}" font-size="12.5" fill="{t["soft"]}">{label}</text>')
        return frame + root + kids
    return frame


CARDS = {
    "applyfirst": dict(title="applyfirst", tag="Open-source AI job agent",
                       pitch=["Finds postings the hour they go up on",
                              "thousands of company career sites, applies",
                              "with Claude, and shows what gets interviews."],
                       stat="Runs on Windows, macOS and Linux",
                       chips=["Python", "FastAPI", "SQLite", "Claude Code"]),
    "wavr": dict(title="Wavr", tag="Chrome extension · live",
                 pitch=["Control the browser with hand gestures,",
                        "tracked from the webcam with MediaPipe.",
                        "All inference runs on-device."],
                 stat="★ 5.0 rating · passed Google review",
                 chips=["JavaScript", "MediaPipe", "Computer vision"]),
    "zephyr": dict(title="Zephyr RTOS", tag="Open-source contribution",
                   pitch=["Fixing the Stellaris GPIO driver in the",
                          "Linux Foundation's real-time OS: port masks,",
                          "interrupt setup and output levels."],
                   stat="Pull request #123502",
                   chips=["C", "Embedded", "Device drivers"]),
    "decision": dict(title="Decision Engine", tag="AI reasoning, measured",
                     pitch=["AI that fills a structured decision record",
                            "instead of a confident guess, separating",
                            "what is known from what is assumed."],
                     stat="Benchmarked against a plain AI answer",
                     chips=["LLMs", "Evaluation", "Python"]),
}


def card(t: dict, key: str) -> str:
    c = CARDS[key]
    W, H = 600, 330
    icon = (f'<image href="{png_data(SRC / "wavr-icon.png", (44, 44))}" x="36" y="38" width="44" height="44"/>'
            if key == "wavr" else "")
    box = icon_box(t, "" if key == "wavr" else ICONS[key](t))
    pitch = "".join(f'<text x="30" y="{196 + i * 28}" font-family="{FONT}" font-size="19.5" fill="{t["soft"]}">{escape(l)}</text>'
                    for i, l in enumerate(c["pitch"]))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>{grad(t)}<clipPath id="frame"><rect width="{W}" height="{H}" rx="16"/></clipPath></defs>
<g clip-path="url(#frame)"><rect width="{W}" height="{H}" fill="{t["panel"]}"/><rect width="{W}" height="4" fill="url(#g)"/></g>
<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="16" fill="none" stroke="{t["border"]}" stroke-width="1.5"/>
{box}{icon}
<text x="104" y="66" font-family="{FONT}" font-size="28" font-weight="800" fill="{t["text"]}">{escape(c["title"])}</text>
<text x="104" y="92" font-family="{FONT}" font-size="16" fill="{t["muted"]}">{escape(c["tag"])}</text>
<text x="30" y="150" font-family="{FONT}" font-size="17" font-weight="700" fill="url(#g)">{escape(c["stat"])}</text>
{visual(t, key)}
{pitch}
{chips(t, c["chips"], 30, 284)}
</svg>'''


# --------------------------------------------------------------------------- also shipped

SHIPPED = [
    ("AI Cultural Translator", "Guides newcomers through Canada's civic systems.", "100+ users · 949 commits · Next.js"),
    ("3D Storefront", "Headless Shopify with Three.js and an AI fit flow.", "Next.js · React Three Fiber · AI SDK"),
    ("Shin", "A price-verdict engine: a clear verdict or a clear refusal.", "TypeScript · Node.js · SQLite"),
    ("Spatial Mapping System", "3D scanner on a TI MSP432 with a time-of-flight sensor.", "Embedded C · UART · Python"),
]


def shipped(t: dict) -> str:
    W, H = 1200, 400
    tiles = ""
    for i, (name, line, hl) in enumerate(SHIPPED):
        x, y = 24 + (i % 2) * 588, 70 + (i // 2) * 160
        tiles += (f'<rect x="{x}" y="{y}" width="564" height="144" rx="14" fill="{t["panel"]}" stroke="{t["border"]}" stroke-width="1.5"/>'
                  f'<rect x="{x}" y="{y + 22}" width="4" height="100" rx="2" fill="url(#g)"/>'
                  f'<text x="{x + 28}" y="{y + 46}" font-family="{FONT}" font-size="25" font-weight="800" fill="{t["text"]}">{escape(name)}</text>'
                  f'<text x="{x + 28}" y="{y + 82}" font-family="{FONT}" font-size="19" fill="{t["soft"]}">{escape(line)}</text>'
                  f'<text x="{x + 28}" y="{y + 118}" font-family="{FONT}" font-size="17" font-weight="700" fill="url(#g)">{escape(hl)}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>{grad(t)}</defs>
<text x="26" y="40" font-family="{FONT}" font-size="26" font-weight="800" fill="{t["text"]}">Also shipped</text>
<text x="200" y="40" font-family="{FONT}" font-size="18" fill="{t["muted"]}">private code, happy to walk through it</text>
{tiles}
</svg>'''


def main() -> None:
    for name, t in THEMES.items():
        (OUT / f"header-{name}.svg").write_text(header(t), encoding="utf-8")
        (OUT / f"shipped-{name}.svg").write_text(shipped(t), encoding="utf-8")
        for key in CARDS:
            (OUT / f"card-{key}-{name}.svg").write_text(card(t, key), encoding="utf-8")
    for p in sorted(OUT.glob("*.svg")):
        print(f"{p.name:32} {p.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
