#!/usr/bin/env python3
"""Module 3 lab: three agents write an investment memo.

Run:  python3 memo_pipeline.py

No API key. No installs. Pure standard-library Python.
Each "agent" is a function with one job. Each one writes its output to a file
and hands a small dict to the next agent. Watch the hand-offs in the terminal.

Data comes from company_facts.csv in this folder. The file ships with SAMPLE
numbers for a made-up company. Replace them with a real NSE company's numbers
from its published results or screener.in, then run again.
"""
import csv
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "output"

DISCLAIMER = (
    "This memo is a classroom exercise for the ISBMS course 'Agentic AI & "
    "Advanced Analytics in Finance'. It is built only from the numbers in "
    "company_facts.csv. It is not investment advice and not research under "
    "SEBI regulations."
)


def research_agent():
    """Job: collect the facts. Hand a clean fact sheet forward."""
    rows = list(csv.DictReader(open(HERE / "company_facts.csv")))
    rows.sort(key=lambda r: int(r["year"]))
    prev, latest = rows[-2], rows[-1]
    facts = {
        "company": latest["company"],
        "ticker": latest["ticker"],
        "year": latest["year"],
        "prev_year": prev["year"],
        "revenue": float(latest["revenue_cr"]),
        "revenue_prev": float(prev["revenue_cr"]),
        "profit": float(latest["net_profit_cr"]),
        "debt": float(latest["total_debt_cr"]),
        "equity": float(latest["equity_cr"]),
    }
    lines = [f"# Research notes — {facts['company']} ({facts['ticker']})", ""]
    lines.append(f"- Revenue FY{facts['year']}: Rs {facts['revenue']:,.0f} cr")
    lines.append(f"- Revenue FY{facts['prev_year']}: Rs {facts['revenue_prev']:,.0f} cr")
    lines.append(f"- Net profit FY{facts['year']}: Rs {facts['profit']:,.0f} cr")
    lines.append(f"- Total debt FY{facts['year']}: Rs {facts['debt']:,.0f} cr")
    lines.append(f"- Equity FY{facts['year']}: Rs {facts['equity']:,.0f} cr")
    lines.append("")
    lines.append("Source: company_facts.csv (filled by the student from published results).")
    (OUT / "1_research_notes.md").write_text("\n".join(lines))
    print(f"RESEARCH AGENT  done — {len(facts)} facts handed to the Analysis Agent")
    return facts


def analysis_agent(facts):
    """Job: read the numbers. Hand ratios and one-line readings forward."""
    growth = (facts["revenue"] / facts["revenue_prev"] - 1) * 100
    margin = facts["profit"] / facts["revenue"] * 100
    de = facts["debt"] / facts["equity"]
    analysis = {
        "growth_pct": round(growth, 1),
        "margin_pct": round(margin, 1),
        "debt_equity": round(de, 2),
    }
    readings = []
    readings.append(f"Revenue grew {analysis['growth_pct']}% over the year."
                    if growth >= 0 else
                    f"Revenue fell {abs(analysis['growth_pct'])}% over the year.")
    readings.append(f"The net margin is {analysis['margin_pct']}%. "
                    + ("That is a thin margin; small cost moves will swing profit."
                       if margin < 5 else "Profit has room to absorb a cost shock."))
    readings.append(f"Debt is {analysis['debt_equity']}x equity. "
                    + ("Leverage is high; check the interest cover next."
                       if de > 1 else "The balance sheet is lightly levered."))
    analysis["readings"] = readings
    lines = [f"# Analysis — {facts['company']}", ""]
    lines.append(f"- Revenue growth: {analysis['growth_pct']}%")
    lines.append(f"- Net margin: {analysis['margin_pct']}%")
    lines.append(f"- Debt to equity: {analysis['debt_equity']}x")
    lines.append("")
    for r in readings:
        lines.append(f"- {r}")
    (OUT / "2_analysis.md").write_text("\n".join(lines))
    print("ANALYSIS AGENT  done — 3 ratios and 3 readings handed to the Writing Agent")
    return analysis


def writing_agent(facts, analysis):
    """Job: draft the memo. One page, every number sourced."""
    m = []
    m.append(f"# Investment memo — {facts['company']} ({facts['ticker']})")
    m.append("")
    m.append("## The numbers")
    m.append(f"Revenue was Rs {facts['revenue']:,.0f} cr in FY{facts['year']}, "
             f"against Rs {facts['revenue_prev']:,.0f} cr the year before.")
    m.append(f"Net profit was Rs {facts['profit']:,.0f} cr, a margin of "
             f"{analysis['margin_pct']}%.")
    m.append(f"Debt stands at {analysis['debt_equity']}x equity.")
    m.append("")
    m.append("## The reading")
    for r in analysis["readings"]:
        m.append(f"- {r}")
    m.append("")
    m.append("## The view")
    m.append("Write your own view here in two sentences, then defend it in the "
             "peer review. The agents supply the numbers; the view is yours.")
    m.append("")
    m.append("## Sources")
    m.append("All figures come from company_facts.csv, filled from the company's "
             "published results.")
    m.append("")
    m.append(f"---\n{DISCLAIMER}")
    (OUT / "3_investment_memo.md").write_text("\n".join(m))
    print("WRITING AGENT   done — memo written to output/3_investment_memo.md")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    facts = research_agent()
    analysis = analysis_agent(facts)
    writing_agent(facts, analysis)
    print("\nPipeline finished. Read the three files in output/ in order —")
    print("that order IS the hand-off. Now you are the Reviewer: check every")
    print("number in the memo against company_facts.csv before you trust it.")
