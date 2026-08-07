"""
MODULE 1 · STEP 1 — Read the numbers out of a filing, using plain Python.

WHAT THIS IS
    An annual report is text. A computer does not "see" a profit and loss
    statement; it sees characters. This script hunts for six labels and grabs
    the number printed next to each one.

WHAT YOU LEARN
    Rules work when the page looks the way you expected, and break the moment
    it does not. That is era one of AI in finance, and it is why the rest of
    this course exists.

HOW TO RUN
    python3 step1_read_the_numbers.py

    Nothing to install. No API key. No internet.
"""

import re
import pathlib

HERE = pathlib.Path(__file__).parent

# ---------------------------------------------------------------------------
# 1. The six lines we want, and the words a company might print for each one.
#    Indian companies do not use identical wording, so we list the variants.
# ---------------------------------------------------------------------------
FIELDS = {
    "revenue_from_operations": ["revenue from operations"],
    "other_income":            ["other income"],
    "total_expenses":          ["total expenses"],
    "profit_before_tax":       ["profit before tax"],
    "tax_expense":             ["total tax expense", "tax expense"],
    "profit_after_tax":        ["profit for the year", "profit after tax"],
}

# A number as printed in an Indian filing: 1,48,320 or 8,42,150 or 22505.
NUMBER = r"\(?\d[\d,]*\)?"


def find_number(text, labels):
    """Return the first number printed after any of these labels."""
    for label in labels:
        # Look for the label, then skip anything that is not a digit, then
        # take the first number on that line.
        pattern = re.escape(label) + r"[^\d\n]*(" + NUMBER + r")"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return to_number(match.group(1))
    return None                      # not found — say so, never guess


def to_number(printed):
    """'1,48,320' -> 148320.   '(425)' -> -425 (brackets mean negative)."""
    negative = printed.startswith("(")
    digits = printed.strip("()").replace(",", "")
    value = int(digits)
    return -value if negative else value


def find_unit(text):
    """Crore or lakh? Getting this wrong is a 100x error, so we read it."""
    lowered = text.lower()
    if "crore" in lowered:
        return "INR crore"
    if "lakh" in lowered:
        return "INR lakh"
    return "unit not stated"


# ---------------------------------------------------------------------------
# 2. Two checks. These are ordinary accounting identities — the same ones you
#    would use on paper. They are also the cheapest lie detector in this course.
# ---------------------------------------------------------------------------
def run_checks(items):
    results = []

    revenue = items["revenue_from_operations"]
    other = items["other_income"]
    expenses = items["total_expenses"]
    pbt = items["profit_before_tax"]
    tax = items["tax_expense"]
    pat = items["profit_after_tax"]

    if None not in (revenue, other, expenses, pbt):
        expected = revenue + other - expenses
        results.append(("Revenue + other income - expenses = PBT",
                        expected == pbt,
                        f"{expected:,} vs {pbt:,} printed"))

    if None not in (pbt, tax, pat):
        expected = pbt - tax
        results.append(("PBT - tax = PAT",
                        expected == pat,
                        f"{expected:,} vs {pat:,} printed"))

    return results


# ---------------------------------------------------------------------------
# 3. Run it on all three excerpts and print what we found.
# ---------------------------------------------------------------------------
def read_one(path):
    text = path.read_text()
    items = {field: find_number(text, labels) for field, labels in FIELDS.items()}

    print("=" * 68)
    print(f"FILE   {path.name}")
    print(f"UNIT   {find_unit(text)}")
    print("-" * 68)
    for field, value in items.items():
        shown = f"{value:,}" if value is not None else "not found"
        print(f"  {field:<28} {shown:>18}")

    print("-" * 68)
    checks = run_checks(items)
    if not checks:
        print("  Could not run the checks — some fields are missing.")
    for name, passed, detail in checks:
        print(f"  [{'PASS' if passed else 'FAIL'}] {name:<42} {detail}")
    print()


if __name__ == "__main__":
    for path in sorted((HERE / "excerpts").glob("*.txt")):
        read_one(path)

    print("=" * 68)
    print("NOW LOOK AT WHAT HAPPENED")
    print("""
  company_a  works. The page looked the way the rules expected.

  company_b  works too, but read the unit. It is LAKH, not crore. Revenue of
             8,42,150 lakh is ₹8,421 crore — put it next to company_a's crore
             figures without converting and you are wrong by 100x. No check
             failed. That is exactly what makes it dangerous.

  company_c  breaks. Two reasons, both worth remembering:
               1. There are two columns, FY2025 and FY2024. The rules grab
                  whichever number comes first and never mention the second.
               2. The first check FAILS honestly: this company adds share of
                  profit of associates between total expenses and PBT, so
                  revenue + other income - expenses does not reach PBT.
                  The number is right; the rule was too simple.

  Fixing this by writing more rules is possible, and it never ends: every new
  company prints something you did not plan for. That is the problem an AI
  model solves — and STEP 2 is where you point one at company_c.
""")
