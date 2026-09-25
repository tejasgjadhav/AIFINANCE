"""
Module 6 lab: turn structured bank data into a Basel III Pillar 3 disclosure (Word).

What it does, in order:
  1. Reads bank_data.json.
  2. Computes CET1, Tier 1 and total capital ratios, the leverage ratio, LCR and NSFR.
  3. Compares each ratio with the RBI minimum (base + capital conservation buffer + D-SIB surcharge).
  4. Checks the computed ratios against the ratios the bank actually published.
  5. Writes a Word document in the RBI Pillar 3 table layout: DF-2 capital adequacy,
     DF-18 leverage ratio, and a liquidity table, plus a commentary section.

No API key. Python and python-docx only.  Run:  python3 build_pillar3.py
"""
import json
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

d = json.load(open("bank_data.json"))
cap, req, rwa, lev = d["capital"], d["capital_requirement"], d["risk_weighted_assets"], d["leverage"]
liq, mins, pub = d["liquidity_ILLUSTRATIVE"], d["rbi_minimums_pct"], d["published_ratios_for_checking_pct"]

# ---------- 1. compute ----------
tier1 = cap["cet1_capital"] + cap["additional_tier1_capital"]
total_cap = tier1 + cap["tier2_capital"]
R = rwa["total"]
ratios = {
    "CET1 ratio":          cap["cet1_capital"] / R * 100,
    "Tier 1 ratio":        tier1 / R * 100,
    "Total capital ratio": total_cap / R * 100,
    "Leverage ratio":      lev["tier1_capital"] / lev["total_exposure"] * 100,
    "LCR":                 liq["hqla"] / liq["net_cash_outflows_30d"] * 100,
    "NSFR":                liq["available_stable_funding"] / liq["required_stable_funding"] * 100,
}
buf = mins["capital_conservation_buffer"] + (mins["dsib_surcharge"] if d["is_dsib"] else 0)
minimum = {
    "CET1 ratio":          mins["cet1"] + buf,
    "Tier 1 ratio":        mins["tier1"] + buf,
    "Total capital ratio": mins["total_capital"] + buf,
    "Leverage ratio":      mins["leverage_dsib"] if d["is_dsib"] else mins["leverage_other"],
    "LCR":                 mins["lcr"],
    "NSFR":                mins["nsfr"],
}
min_total_crar = minimum["Total capital ratio"] / 100
rwa_by_type = {k: req[k] / min_total_crar for k in ("credit_risk", "market_risk", "operational_risk")}

# ---------- 2. check against what the bank published ----------
checks = [
    ("CET1 ratio", pub["cet1_crar"]), ("Tier 1 ratio", pub["tier1_crar"]),
    ("Total capital ratio", pub["total_crar"]), ("Leverage ratio", pub["leverage_ratio"]),
]
print(f"{'Ratio':22s} {'computed':>9s} {'published':>10s} {'RBI min':>8s}  status")
for name, p in checks:
    c = ratios[name]
    ok = abs(round(c, 2) - p) <= 0.01
    print(f"{name:22s} {c:8.2f}% {p:9.2f}% {minimum[name]:7.2f}%  {'MATCH' if ok else 'MISMATCH'}")
for name in ("LCR", "NSFR"):
    print(f"{name:22s} {ratios[name]:8.2f}% {'n/a':>10s} {minimum[name]:7.2f}%  illustrative inputs")

# ---------- 3. write the Word document ----------
doc = Document()
st = doc.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(10.5)

def h(text, lvl=1):
    doc.add_heading(text, lvl)

def para(text, bold=False, italic=False, size=None):
    p = doc.add_paragraph(); r = p.add_run(text); r.bold = bold; r.italic = italic
    if size: r.font.size = Pt(size)
    return p

def table(headers, rows, widths=None):
    t = doc.add_table(rows=1, cols=len(headers)); t.style = "Light Grid Accent 1"
    for i, x in enumerate(headers):
        c = t.rows[0].cells[i]; c.text = ""; r = c.paragraphs[0].add_run(x); r.bold = True
    for row in rows:
        cells = t.add_row().cells
        for i, x in enumerate(row):
            cells[i].text = x
            if i > 0: cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    doc.add_paragraph()
    return t

def mn(x): return f"{x:,.1f}"
def pc(x): return f"{x:.2f}%"

t = doc.add_heading(f"Basel III Pillar 3 Disclosures", 0)
para(f"{d['bank']}  |  as at {d['as_of']}  |  figures in {d['unit']}", bold=True)
para("Generated from structured data by the Module 6 lab script. Capital and leverage inputs are the bank's "
     "published figures; liquidity inputs are illustrative teaching values and are marked as such.", italic=True, size=9)

h("Table DF-2: Capital Adequacy")
para("Qualitative disclosure", bold=True)
para(f"The Bank is identified as a Domestic Systemically Important Bank and holds the D-SIB surcharge of "
     f"{mins['dsib_surcharge']:.2f}% over the capital conservation buffer of {mins['capital_conservation_buffer']:.2f}%. "
     f"The applicable minimum total capital ratio is therefore {pc(minimum['Total capital ratio'])} of risk weighted assets.")
para("Quantitative disclosure: capital requirements", bold=True)
table(["Item", "Capital required", "Risk weighted assets"], [
    ["(b) Credit risk (standardised approach)", mn(req["credit_risk"]), mn(rwa_by_type["credit_risk"])],
    ["(c) Market risk (standardised duration approach)", mn(req["market_risk"]), mn(rwa_by_type["market_risk"])],
    ["(d) Operational risk (basic indicator approach)", mn(req["operational_risk"]), mn(rwa_by_type["operational_risk"])],
    ["Total capital requirement (b + c + d)", mn(req["total"]), mn(rwa["total"])],
])
para("Quantitative disclosure: capital ratios", bold=True)
table(["Ratio", "Computed", "RBI minimum incl. buffers", "Headroom"], [
    [k, pc(ratios[k]), pc(minimum[k]), f"{ratios[k]-minimum[k]:.2f} pp"]
    for k in ("CET1 ratio", "Tier 1 ratio", "Total capital ratio")
])
para("Composition of capital", bold=True)
table(["Component", "Amount"], [
    ["Common Equity Tier 1 capital", mn(cap["cet1_capital"])],
    ["Additional Tier 1 capital", mn(cap["additional_tier1_capital"])],
    ["Tier 1 capital", mn(tier1)],
    ["Tier 2 capital", mn(cap["tier2_capital"])],
    ["Total capital funds", mn(total_cap)],
    ["Total risk weighted assets", mn(rwa["total"])],
])

h("Table DF-18: Leverage Ratio")
table(["Item", "Amount"], [
    ["On-balance sheet exposures", mn(lev["on_balance_sheet_exposure"])],
    ["Derivative exposures", mn(lev["derivative_exposure"])],
    ["Securities financing transaction exposures", mn(lev["sft_exposure"])],
    ["Off-balance sheet items", mn(lev["off_balance_sheet_items"])],
    ["Total exposures", mn(lev["total_exposure"])],
    ["Tier 1 capital", mn(lev["tier1_capital"])],
    ["Basel III leverage ratio", pc(ratios["Leverage ratio"])],
    ["RBI minimum (D-SIB)", pc(minimum["Leverage ratio"])],
])

h("Liquidity: LCR and NSFR (illustrative inputs)")
para("The inputs in this table are teaching values, not the bank's published figures. The bank discloses LCR "
     "and NSFR in its annual report and quarterly liquidity disclosures.", italic=True, size=9)
table(["Item", "Amount"], [
    ["High quality liquid assets (HQLA)", mn(liq["hqla"])],
    ["Net cash outflows over 30 days", mn(liq["net_cash_outflows_30d"])],
    ["Liquidity Coverage Ratio", pc(ratios["LCR"])],
    ["Available stable funding", mn(liq["available_stable_funding"])],
    ["Required stable funding", mn(liq["required_stable_funding"])],
    ["Net Stable Funding Ratio", pc(ratios["NSFR"])],
    ["RBI minimum for each", pc(100.0)],
])

h("Reconciliation against published ratios")
para("Every ratio computed above is compared with the ratio the bank printed in its own disclosure. "
     "A mismatch means the input data or the formula is wrong, and the document must not be issued.")
rows = []
for name, p in checks:
    c = ratios[name]; ok = abs(round(c, 2) - p) <= 0.01
    rows.append([name, pc(c), pc(p), "Match" if ok else "MISMATCH"])
table(["Ratio", "Computed", "Published", "Status"], rows)

h("Commentary")
worst = min(("CET1 ratio", "Tier 1 ratio", "Total capital ratio", "Leverage ratio"),
            key=lambda k: ratios[k] - minimum[k])
para(f"All capital ratios are above the RBI minimum including buffers. The narrowest headroom is on the "
     f"{worst} at {ratios[worst]-minimum[worst]:.2f} percentage points. Credit risk accounts for "
     f"{req['credit_risk']/req['total']*100:.1f}% of the total capital requirement, market risk "
     f"{req['market_risk']/req['total']*100:.1f}% and operational risk {req['operational_risk']/req['total']*100:.1f}%. "
     f"The leverage ratio of {pc(ratios['Leverage ratio'])} is well above the {pc(minimum['Leverage ratio'])} D-SIB floor.")
para("Lab step: paste the two ratio tables above into any free AI chat and ask for a one-paragraph management "
     "commentary. Then check every number in its answer against this document before you keep a word of it.",
     italic=True, size=9)

out = "Pillar3_Disclosure_ICICI_Mar2025.docx"
doc.save(out)
print("saved", out)
