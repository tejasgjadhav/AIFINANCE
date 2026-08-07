"""
MODULE 1 · STEP 2 — Make an AI do the reading, then check its homework.

WHAT YOU DO FIRST (no API key, no subscription)
    1. Open prompt.txt. Copy all of it.
    2. Open any free AI chat you already have — ChatGPT, Claude.ai, Gemini,
       Copilot, or the coding sandbox we are using in class.
    3. Paste the prompt, then paste one file from excerpts/ where the prompt
       says to. Send it.
    4. Copy the JSON it replies with into ai_output.json in this folder.
    5. Run:   python3 step2_check_ai_output.py excerpts/company_c.txt

WHAT THIS SCRIPT DOES
    It refuses to trust the model. Four checks, in the order a desk would
    apply them. Any FAIL means you fix the prompt and run it again — that
    loop is the actual skill this module teaches.

    Nothing to install. No API key. No internet.
"""

import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).parent
FIELDS = ["revenue_from_operations", "other_income", "total_expenses",
          "profit_before_tax", "tax_expense", "profit_after_tax"]


def check_1_does_it_parse(raw):
    """The model must return JSON, not a friendly sentence around JSON."""
    try:
        return True, json.loads(raw), "clean JSON"
    except json.JSONDecodeError as e:
        return False, None, f"json.loads failed: {e}"


def check_2_shape(data):
    """Every field we asked for must be present, even if the value is null."""
    if "periods" not in data or not data["periods"]:
        return False, "no 'periods' list in the answer"
    missing = []
    for p in data["periods"]:
        for f in FIELDS:
            if f not in p:
                missing.append(f"{p.get('period', '?')}.{f}")
    if missing:
        return False, "missing fields: " + ", ".join(missing)
    return True, f"{len(data['periods'])} period(s), all six fields present"


def check_3_arithmetic(period):
    """
    Two identities from ordinary accounting:
        revenue + other income - total expenses = profit before tax
        profit before tax - tax = profit after tax

    The model was told NOT to calculate. So if these tie, the numbers it
    copied are internally consistent. If they do not tie, either the model
    made one up, or the company has an extra line (share of associates,
    exceptional items) sitting between the two totals. Both are worth knowing.
    """
    out = []
    g = period.get
    if None not in (g("revenue_from_operations"), g("other_income"),
                    g("total_expenses"), g("profit_before_tax")):
        expected = g("revenue_from_operations") + g("other_income") - g("total_expenses")
        out.append((expected == g("profit_before_tax"),
                    f"revenue + other income - expenses = PBT   "
                    f"({expected:,} vs {g('profit_before_tax'):,})"))
    if None not in (g("profit_before_tax"), g("tax_expense"), g("profit_after_tax")):
        expected = g("profit_before_tax") - g("tax_expense")
        out.append((expected == g("profit_after_tax"),
                    f"PBT - tax = PAT                           "
                    f"({expected:,} vs {g('profit_after_tax'):,})"))
    return out


def check_4_every_number_is_printed(period, source_text):
    """
    The strictest check, and the one that catches invented numbers.
    Every figure in the answer must literally appear in the filing text,
    with or without Indian comma grouping.
    """
    invented = []
    for f in FIELDS:
        value = period.get(f)
        if value is None:
            continue
        plain = str(abs(value))
        grouped = indian_format(abs(value))
        if plain not in source_text.replace(",", "") and grouped not in source_text:
            invented.append(f"{f}={value}")
    return (not invented), (", ".join(invented) if invented else "all figures found in the text")


def indian_format(n):
    """148320 -> '1,48,320'  (last three digits, then pairs)."""
    s = str(n)
    if len(s) <= 3:
        return s
    head, tail = s[:-3], s[-3:]
    parts = []
    while len(head) > 2:
        parts.insert(0, head[-2:])
        head = head[:-2]
    if head:
        parts.insert(0, head)
    return ",".join(parts) + "," + tail


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("Usage: python3 step2_check_ai_output.py excerpts/company_c.txt")
        return

    source = pathlib.Path(sys.argv[1])
    answer_file = HERE / "ai_output.json"

    if not answer_file.exists():
        print("ai_output.json not found.")
        print("Paste the AI's answer into that file first — see the top of this script.")
        return

    raw = answer_file.read_text().strip()
    source_text = source.read_text()

    print("=" * 68)
    print(f"SOURCE  {source.name}")
    print("=" * 68)

    ok, data, detail = check_1_does_it_parse(raw)
    print(f"[{'PASS' if ok else 'FAIL'}] 1 · Does it parse?            {detail}")
    if not ok:
        print("\n  Fix: your prompt must say 'no text before or after the JSON'.")
        print("  Delete anything around the braces in ai_output.json and run again.")
        return

    ok, detail = check_2_shape(data)
    print(f"[{'PASS' if ok else 'FAIL'}] 2 · Is the shape right?       {detail}")
    if not ok:
        print("\n  Fix: paste the JSON schema into the prompt again, exactly.")
        return

    print(f"      Unit reported: {data.get('unit', 'MISSING')}"
          f"   (check this against the filing — lakh and crore differ by 100x)")

    for period in data["periods"]:
        print("-" * 68)
        print(f"  PERIOD {period.get('period', '?')}")
        for passed, line in check_3_arithmetic(period):
            print(f"  [{'PASS' if passed else 'FAIL'}] 3 · {line}")
        passed, detail = check_4_every_number_is_printed(period, source_text)
        print(f"  [{'PASS' if passed else 'FAIL'}] 4 · Every number printed in the source? {detail}")

    print("-" * 68)
    print("""
WHAT TO DO WITH A FAIL

  Check 3 fails  ->  first read the filing. If there is an extra line between
                     total expenses and profit before tax (share of associates,
                     exceptional items), the model is right and the identity is
                     too simple. If there is no such line, the model invented
                     a number. Add to your prompt: 'never compute a figure'.

  Check 4 fails  ->  the model produced a figure that is nowhere in the text.
                     This is a hallucination. Add a rule: 'if a line item is
                     not printed, return null', and ask it to quote the source
                     line for each number.

  Record what failed and what you changed. That note is the deliverable —
  more than the JSON is.
""")


if __name__ == "__main__":
    main()
