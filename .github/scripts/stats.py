"""Writes the activity card (dark and light) from the public contribution calendar.

Run by .github/workflows/profile.yml every day. Needs GITHUB_TOKEN and USER_LOGIN.
Fails loudly: a failed run shows on the Actions tab and the old card stays up.
"""
import json
import os
import pathlib
import sys
import urllib.request
from datetime import date

FONT = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Helvetica, Arial, sans-serif"
THEMES = {
    "dark": dict(bg="#161b22", border="#30363d", text="#e6edf3", muted="#8b949e", c1="#22d3ee", c2="#a78bfa"),
    "light": dict(bg="#ffffff", border="#d0d7de", text="#1f2328", muted="#59636e", c1="#0891b2", c2="#7c3aed"),
}

QUERY = """query($login: String!) { user(login: $login) { contributionsCollection {
  contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } } } } }"""


def calendar(login: str, token: str) -> dict:
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json", "User-Agent": "profile-stats"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if data.get("errors"):
        sys.exit(f"GitHub returned errors: {data['errors']}")
    return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def numbers(cal: dict) -> dict:
    days = [d for w in cal["weeks"] for d in w["contributionDays"]]
    counts = [d["contributionCount"] for d in days]
    longest = run = 0
    for c in counts:
        run = run + 1 if c else 0
        longest = max(longest, run)
    current = 0
    for i, c in enumerate(reversed(counts)):
        if c:
            current += 1
        elif i == 0:      # today may simply not have started yet
            continue
        else:
            break
    weekly = [sum(d["contributionCount"] for d in w["contributionDays"]) for w in cal["weeks"]]
    return dict(total=cal["totalContributions"], current=current, longest=longest, best=max(counts), weekly=weekly)


def card(n: dict, t: dict) -> str:
    W, H = 1200, 300
    metrics = [(f"{n['total']:,}", "contributions, last 12 months"), (f"{n['current']}", "day streak, running"),
               (f"{n['longest']}", "day longest streak"), (f"{n['best']:,}", "on the best day")]
    cols = ""
    for i, (big, label) in enumerate(metrics):
        x = 40 + i * 290
        cols += (f'<text x="{x}" y="128" font-family="{FONT}" font-size="58" font-weight="800" fill="url(#g)">{big}</text>'
                 f'<text x="{x + 2}" y="160" font-family="{FONT}" font-size="18" fill="{t["muted"]}">{label}</text>')
    wk = n["weekly"]
    top = max(wk) or 1
    x0, x1, base, hgt = 40, W - 40, 268, 74
    step = (x1 - x0) / max(1, len(wk) - 1)
    pts = [(x0 + i * step, base - v / top * hgt) for i, v in enumerate(wk)]
    line = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area = f"M{x0},{base} L" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f" L{x1},{base} Z"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t["c1"]}"/><stop offset="1" stop-color="{t["c2"]}"/></linearGradient>
<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["c2"]}" stop-opacity=".35"/><stop offset="1" stop-color="{t["c2"]}" stop-opacity="0"/></linearGradient>
<clipPath id="frame"><rect width="{W}" height="{H}" rx="16"/></clipPath>
<clipPath id="reveal"><rect x="0" y="0" width="0" height="{H}"><animate attributeName="width" from="0" to="{W}" dur="2.2s" fill="freeze"/></rect></clipPath></defs>
<g clip-path="url(#frame)"><rect width="{W}" height="{H}" fill="{t["bg"]}"/><rect width="{W}" height="4" fill="url(#g)"/></g>
<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="16" fill="none" stroke="{t["border"]}" stroke-width="1.5"/>
<text x="40" y="52" font-family="{FONT}" font-size="20" font-weight="700" fill="{t["text"]}">Activity</text>
<text x="{W - 40}" y="52" text-anchor="end" font-family="{FONT}" font-size="15" fill="{t["muted"]}">updated {date.today():%b} {date.today().day}, {date.today().year}</text>
{cols}
<g clip-path="url(#reveal)"><path d="{area}" fill="url(#fade)"/><polyline points="{line}" fill="none" stroke="url(#g)" stroke-width="3" stroke-linejoin="round"/></g>
</svg>'''


def main() -> None:
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "dist")
    out.mkdir(parents=True, exist_ok=True)
    n = numbers(calendar(os.environ["USER_LOGIN"], os.environ["GITHUB_TOKEN"]))
    if n["total"] <= 0:
        sys.exit("Calendar came back empty; keeping the old card.")
    for name, t in THEMES.items():
        (out / f"stats-{name}.svg").write_text(card(n, t), encoding="utf-8")
    print(json.dumps({k: v for k, v in n.items() if k != "weekly"}))


if __name__ == "__main__":
    main()
