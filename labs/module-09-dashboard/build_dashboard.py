"""
Module 9 lab: a daily pre-market dashboard, built the way a capstone should be.

Run:  python3 build_dashboard.py
      python3 build_dashboard.py --break     (blanks one input to show the refusal)

Built-in Python only. No internet, no API key, no installs.
All figures are an illustrative morning snapshot for teaching, not live market data.

The design follows the faculty's daily market dashboard, with one change:
here Python computes every number (layers L1 and L3), and the AI only writes
the commentary from those numbers (layer L4).
"""
import csv, html, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- L1  INGEST
def load_snapshot():
    rows = {}
    with open(os.path.join(HERE, "market_snapshot.csv"), newline="") as f:
        for r in csv.DictReader(f):
            rows[r["item"]] = r
    return rows

snap = load_snapshot()
if "--break" in sys.argv:
    snap["gift_nifty"]["value"] = ""          # simulate a missing feed
missing = [k for k, r in snap.items() if r["value"].strip() == ""]
if missing:
    print("REFUSED: these inputs are missing, so no dashboard was written:", ", ".join(missing))
    print("A dashboard with a blank number is worse than no dashboard.")
    sys.exit(1)
v = {k: float(r["value"]) for k, r in snap.items()}
headlines = [h.strip() for h in open(os.path.join(HERE, "headlines.txt")) if h.strip()]
dcf = {r["item"]: r["value"] for r in csv.DictReader(open(os.path.join(HERE, "dcf_inputs.csv"), newline=""))}

# ---------------------------------------------------------------- L3  ENGINE
gap = v["gift_nifty"] - v["nifty_prev_close"]
gap_pct = gap / v["nifty_prev_close"] * 100
open_call = "gap-up" if gap > 20 else "gap-down" if gap < -20 else "flat"
inr_move = v["usdinr"] - v["usdinr_prev"]
brent_pct = (v["brent"] - v["brent_prev"]) / v["brent_prev"] * 100
vix_regime = "low" if v["india_vix"] < 15 else "normal" if v["india_vix"] < 20 else "high"
flows_net = v["fii_net_crore"] + v["dii_net_crore"]

# Sentiment: a simple word list. FinBERT does the same job far better (see the optional Colab cell on the lab page).
POS = {"strong", "rise", "rises", "growth", "stable", "eases", "higher", "hopes", "cut"}
NEG = {"warn", "slower", "weakens", "outflows", "pressure", "concerns", "lower"}
# Watch the crude oil headline: falling crude is good news for India, but the word "concerns" makes the list call it negative.
def score(text):
    words = set(text.lower().replace(",", "").split())
    s = len(words & POS) - len(words & NEG)
    return "positive" if s > 0 else "negative" if s < 0 else "neutral"
sentiment = [(h, score(h)) for h in headlines]
pos = sum(1 for _, s in sentiment if s == "positive"); neg = sum(1 for _, s in sentiment if s == "negative")

# DCF: five years of growth, then a terminal value, all discounted at WACC.
fcf, g, wacc, tg = float(dcf["fcf_last"]), float(dcf["growth_years_1_5"]), float(dcf["wacc"]), float(dcf["terminal_growth"])
pv, flows = 0.0, []
for year in range(1, 6):
    fcf *= 1 + g
    flows.append(fcf)
    pv += fcf / (1 + wacc) ** year
terminal = flows[-1] * (1 + tg) / (wacc - tg)
pv_terminal = terminal / (1 + wacc) ** 5
equity = pv + pv_terminal - float(dcf["net_debt"])
per_share = equity / float(dcf["shares_crore"])

print("ENGINE RESULTS")
print(f"  Expected open: {open_call}, {gap:+.0f} points ({gap_pct:+.2f}%)")
print(f"  USD/INR {inr_move:+.2f}   Brent {brent_pct:+.2f}%   India VIX {v['india_vix']:.2f} ({vix_regime})")
print(f"  FII {v['fii_net_crore']:+,.0f} cr, DII {v['dii_net_crore']:+,.0f} cr, net {flows_net:+,.0f} cr")
print(f"  Headlines: {pos} positive, {neg} negative, {len(headlines) - pos - neg} neutral")
print(f"  DCF {dcf['company']}: Rs {per_share:,.0f} a share (PV of 5 years Rs {pv:,.0f} cr + PV of terminal Rs {pv_terminal:,.0f} cr - net debt)")

# ---------------------------------------------------------------- L5  OUTPUT
def tile(label, value, sub):
    return f'<div class="t"><div class="l">{html.escape(label)}</div><div class="v">{html.escape(value)}</div><div class="s">{html.escape(sub)}</div></div>'
tiles = "".join([
    tile("Expected open", open_call.upper(), f"GIFT Nifty {v['gift_nifty']:,.0f} vs close {v['nifty_prev_close']:,.0f} ({gap:+.0f})"),
    tile("USD/INR", f"{v['usdinr']:.2f}", f"{inr_move:+.2f} since yesterday"),
    tile("Brent crude", f"${v['brent']:.2f}", f"{brent_pct:+.2f}%"),
    tile("India VIX", f"{v['india_vix']:.2f}", f"{vix_regime} volatility"),
    tile("Institutional flows", f"{flows_net:+,.0f} cr", f"FII {v['fii_net_crore']:+,.0f} / DII {v['dii_net_crore']:+,.0f}"),
    tile("News mood", f"{pos} up / {neg} down", f"{len(headlines)} headlines scored"),
])
news = "".join(f'<li><span class="{s}">{s}</span> {html.escape(h)}</li>' for h, s in sentiment)
page = f"""<!doctype html><html><head><meta charset="utf-8"><title>Pre-market dashboard</title>
<style>body{{font-family:Helvetica,Arial,sans-serif;background:#0f2145;color:#eef2f8;margin:0;padding:24px}}
h1{{font-size:22px;margin:0 0 4px}}.sub{{color:#9fb0cc;margin-bottom:18px}}
.g{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}.t{{background:#16305e;border-top:3px solid #c9a227;border-radius:8px;padding:12px}}
.l{{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#c9a227}}.v{{font-size:24px;font-weight:bold;margin:4px 0}}.s{{font-size:12px;color:#9fb0cc}}
h2{{font-size:16px;margin:22px 0 8px;color:#c9a227}}li{{margin:6px 0}}.positive{{color:#4ade80}}.negative{{color:#f87171}}.neutral{{color:#9fb0cc}}
li span{{display:inline-block;width:70px;font-size:11px;text-transform:uppercase}}.box{{background:#16305e;border-radius:8px;padding:12px;font-size:14px}}</style></head><body>
<h1>Pre-market dashboard</h1><div class="sub">Illustrative snapshot for teaching. Every number below was computed in Python.</div>
<div class="g">{tiles}</div>
<h2>Headlines and their mood</h2><ul>{news}</ul>
<h2>Valuation: {html.escape(dcf['company'])}</h2><div class="box">DCF value Rs {per_share:,.0f} a share.
Five years of free cash flow growing {g:.0%}, WACC {wacc:.0%}, terminal growth {tg:.0%}, less net debt Rs {float(dcf['net_debt']):,.0f} crore.</div>
<h2>Morning brief</h2><div class="box">Paste the AI's brief here after you have checked every number.</div>
</body></html>"""
open(os.path.join(HERE, "dashboard.html"), "w").write(page)
print("\nWrote dashboard.html. Open it in a browser.")

# ---------------------------------------------------------------- L4  COMMENTARY PROMPT
print("\nPASTE THIS INTO ANY FREE AI CHAT FOR THE MORNING BRIEF")
print("-" * 70)
print("Write a five-sentence pre-market brief for Indian equities. Use only these numbers.")
print("Do not add any number, name or event that is not listed. Do not give buy or sell advice.")
print(f"Expected open: {open_call}, GIFT Nifty {gap:+.0f} points versus yesterday's Nifty close.")
print(f"USD/INR {v['usdinr']:.2f} ({inr_move:+.2f}). Brent ${v['brent']:.2f} ({brent_pct:+.2f}%). India VIX {v['india_vix']:.2f}, {vix_regime}.")
print(f"FII net {v['fii_net_crore']:+,.0f} crore, DII net {v['dii_net_crore']:+,.0f} crore.")
print(f"Headline mood: {pos} positive, {neg} negative out of {len(headlines)}.")
print("-" * 70)
print("Then check every number in the brief against the ENGINE RESULTS above.")
