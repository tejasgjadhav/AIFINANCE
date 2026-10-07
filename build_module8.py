#!/usr/bin/env python3
"""Build Module 8 deck: Fund Administration, NAV and Transfer Agency.
Nine slides: title, who does what, fund types, NAV, transfer agency and KYC, reconciliation, the accounting skill, live lab, practice."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
import copy

NAVY = RGBColor(0x0F, 0x21, 0x45)
NAVY2 = RGBColor(0x0B, 0x19, 0x36)
GOLD = RGBColor(0xC9, 0xA2, 0x27)
GOLDD = RGBColor(0x8F, 0x71, 0x13)
BLUE = RGBColor(0x3A, 0x5C, 0x9E)
INK = RGBColor(0x1B, 0x2A, 0x41)
BG = RGBColor(0xF7, 0xF8, 0xFA)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
MUTE = RGBColor(0x5D, 0x6B, 0x7E)
MUTEN = RGBColor(0x8F, 0xA1, 0xC4)  # muted on navy
SUBN = RGBColor(0xC9, 0xD6, 0xEE)   # subtitle on navy
TINT1 = RGBColor(0xE9, 0xEF, 0xF8)
TINT2 = RGBColor(0xD5, 0xE1, 0xF2)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]

FOOT_L = "ISBMS · PGDM 2025–27 · AGENTIC AI & ADVANCED ANALYTICS IN FINANCE"


def slide_bg(s, color):
    el = s.background.fill
    el.solid()
    el.fore_color.rgb = color


def box(s, x, y, w, h, fill=None):
    sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.line.fill.background()
    sh.shadow.inherit = False
    if fill is not None:
        sh.fill.solid()
        sh.fill.fore_color.rgb = fill
    else:
        sh.fill.background()
    return sh


def txt(s, x, y, w, h, paras, anchor=MSO_ANCHOR.TOP, align=PP_ALIGN.LEFT, wrap=True):
    """paras: list of paragraphs; each = (align_or_None, space_before_pt, [runs])
    run = (text, font_name_or_None, size_pt, bold, color)"""
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    for m in (tf.margin_left, ):
        pass
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    first = True
    for p_align, sp, runs in paras:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = p_align if p_align is not None else align
        if sp:
            p.space_before = Pt(sp)
        for text, fname, size, bold, color in runs:
            r = p.add_run()
            r.text = text
            r.font.size = Pt(size)
            r.font.bold = bold
            r.font.color.rgb = color
            if fname:
                r.font.name = fname
    return tb


def eyebrow(s, label):
    box(s, 0.6, 0.44, 0.13, 0.13, GOLD)
    txt(s, 0.86, 0.34, 11.83, 0.3, [(None, 0, [(label, None, 11, True, GOLD)])])


def title(s, text):
    txt(s, 0.6, 0.68, 12.13, 0.8, [(None, 0, [(text, "Georgia", 29, True, NAVY)])])


def footer(s, num, dark=False):
    c = MUTEN if dark else MUTE
    txt(s, 0.6, 7.08, 8.0, 0.25, [(None, 0, [(FOOT_L, None, 8, False, c)])])
    txt(s, 10.13, 7.08, 2.6, 0.25, [(PP_ALIGN.RIGHT, 0, [(f"MODULE 8  ·  {num:02d}", None, 8, False, c)])],
        align=PP_ALIGN.RIGHT)


def goal_band(s, lead, rest):
    box(s, 0.6, 6.3, 12.13, 0.66, NAVY)
    box(s, 0.6, 6.3, 0.07, 0.66, GOLD)
    txt(s, 0.9, 6.3, 11.53, 0.66,
        [(None, 0, [(lead + "  ", None, 12, True, GOLD), (rest, None, 12, False, WHITE)])],
        anchor=MSO_ANCHOR.MIDDLE)


def bullet(s, x, y, w, text, size=11):
    txt(s, x, y, w, 0.55, [(None, 0, [("▪  ", None, size, True, GOLD), (text, None, size, False, INK)])])


def new_slide():
    return prs.slides.add_slide(BLANK)


def minibox(s, x, y, label, w=0.62, h=0.34, fill=NAVY, tc=WHITE):
    box(s, x, y, w, h, fill)
    txt(s, x, y, w, h, [(PP_ALIGN.CENTER, 0, [(label, None, 8, True, tc)])],
        anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)


def arrow(s, x, y, ch="→", w=0.3):
    txt(s, x, y, w, 0.34, [(PP_ALIGN.CENTER, 0, [(ch, None, 13, True, GOLD)])],
        anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)


def three_cards(s, cards, top=1.72, h=4.2):
    """cards: list of (fill, kick, head, body, example, useline)"""
    xs = [0.6, 4.72, 8.84]
    for x, (fill, kick, head, body, ex, use) in zip(xs, cards):
        dark = fill == NAVY
        box(s, x, top, 3.95, h, fill)
        txt(s, x + 0.26, top + 0.2, 3.4, 0.3, [(None, 0, [(kick, None, 10, True, GOLD if dark else BLUE)])])
        txt(s, x + 0.26, top + 0.52, 3.4, 0.4, [(None, 0, [(head, "Georgia", 15, True, WHITE if dark else NAVY)])])
        txt(s, x + 0.26, top + 1.05, 3.4, 1.55, [(None, 0, [(body, None, 10, False, SUBN if dark else INK)])])
        box(s, x + 0.26, top + 2.62, 3.43, 1.0, WHITE)
        txt(s, x + 0.44, top + 2.72, 3.1, 0.85, [
            (None, 0, [("EXAMPLE", None, 8, True, BLUE)]),
            (None, 2, [(ex, None, 9.5, False, INK)]),
        ])
        txt(s, x + 0.26, top + 3.7, 3.4, 0.45, [(None, 0, [(use, None, 10, True, SUBN if dark else MUTE)])])

# ---------------------------------------------------------------- SIMPLE LAYOUT HELPER
def cards(s, items, cols, top=1.6, h=None, gap=0.17, dark_last=False):
    """items: (kicker, head, body). Equal cards in a grid between top and 6.15."""
    rows = (len(items) + cols - 1) // cols
    w = (12.13 - gap * (cols - 1)) / cols
    h = h or (6.15 - top - gap * (rows - 1)) / rows
    for i, (k, hd, b) in enumerate(items):
        x = 0.6 + (i % cols) * (w + gap)
        y = top + (i // cols) * (h + gap)
        dark = dark_last and i == len(items) - 1
        box(s, x, y, w, h, NAVY if dark else WHITE)
        box(s, x, y, w, 0.05, GOLD)
        paras = []
        if k:
            paras.append((None, 0, [(k, None, 10, True, GOLD if dark else BLUE)]))
        paras.append((None, 4 if k else 0, [(hd, "Georgia", 16, True, WHITE if dark else NAVY)]))
        paras.append((None, 6, [(b, None, 12, False, SUBN if dark else INK)]))
        txt(s, x + 0.28, y + 0.22, w - 0.56, h - 0.3, paras)


# ---------------------------------------------------------------- S1 TITLE
s = new_slide()
slide_bg(s, NAVY)
box(s, 0, 0, 13.333, 7.5, NAVY)
box(s, 10.23, 0, 3.1, 7.5, NAVY2)
box(s, 10.23, 0, 0.04, 7.5, GOLD)
txt(s, 0.6, 1.02, 9.0, 0.3, [(None, 0, [("ISBMS · PGDM 2025–27 · SEMESTER III · SESSION 8 OF 10", None, 12, True, GOLD)])])
txt(s, 0.6, 1.5, 9.4, 2.4, [
    (None, 0, [("Module 8", "Georgia", 58, True, WHITE)]),
    (None, 10, [("Fund Administration: NAV and Transfer Agency", "Georgia", 21, False, SUBN)]),
])
box(s, 0.6, 4.28, 4.4, 0.02, GOLD)
txt(s, 0.6, 4.52, 9.0, 1.2, [
    (None, 0, [("Faculty · Agentic AI & Advanced Analytics in Finance", None, 14, True, WHITE)]),
    (None, 4, [("PGDM-SEM3-SPEC-AIFINANCE", None, 12, False, MUTEN)]),
    (None, 3, [("tejasgjadhav.github.io/AIFINANCE", None, 12, True, GOLD)]),
])
txt(s, 10.55, 0.93, 2.4, 0.3, [(None, 0, [("TODAY", None, 10, True, GOLD)])])
txt(s, 10.55, 1.35, 2.5, 1.4, [
    (None, 0, [("Three questions", "Georgia", 15, True, WHITE)]),
    (None, 4, [("What is a fund's NAV?", None, 10, False, MUTEN)]),
    (None, 2, [("How do investors get in and out?", None, 10, False, MUTEN)]),
    (None, 2, [("Can AI check the books?", None, 10, False, MUTEN)]),
])
txt(s, 10.55, 3.25, 2.5, 1.2, [
    (None, 0, [("Live today", "Georgia", 15, True, WHITE)]),
    (None, 4, [("Claude's reconciliation", None, 10, False, MUTEN)]),
    (None, 2, [("skill checks a fund's", None, 10, False, MUTEN)]),
    (None, 2, [("books in front of you.", None, 10, False, MUTEN)]),
])
txt(s, 10.55, 4.85, 2.5, 1.6, [
    (None, 0, [("1", "Georgia", 44, True, GOLD)]),
    (None, 4, [("NAV REPORT, RECONCILED,", None, 9, False, MUTEN)]),
    (None, 2, [("BEFORE YOU LEAVE", None, 9, False, MUTEN)]),
])
footer(s, 1, dark=True)

# ---------------------------------------------------------------- S2 WHO DOES WHAT
s = new_slide()
slide_bg(s, BG)
eyebrow(s, "HOUR 1 · FUND ADMINISTRATION IN PLAIN WORDS")
title(s, "Who does what in a fund")
cards(s, [
    ("THE INVESTOR", "Puts money in", "Buys units of the fund and can sell them back later."),
    ("THE FUND MANAGER", "Decides what to buy", "The asset management company picks the shares the fund holds."),
    ("THE FUND ACCOUNTANT", "Keeps the books", "Records every trade and works out the NAV every day."),
    ("THE CUSTODIAN", "Holds the assets", "A bank that keeps the fund's shares and cash safe."),
    ("THE TRANSFER AGENT", "Keeps the investor list", "Records who owns how many units. In India: KFinTech and CAMS."),
    ("THE AUDITOR", "Checks it all", "Confirms once a year that the books are right."),
], cols=3, dark_last=True)
goal_band(s, "The key idea:", "the fund accountant's books, the custodian and the transfer agent must all agree before a NAV is published.")
footer(s, 2)

# ---------------------------------------------------------------- S3 FUND TYPES
s = new_slide()
slide_bg(s, BG)
eyebrow(s, "HOUR 1 · FUND TYPES AND THE BACK OFFICE")
title(s, "Four kinds of fund, one back office")
cards(s, [
    ("MUTUAL FUND", "NAV every day", "Open to anyone. The NAV is published every business day."),
    ("HEDGE FUND", "NAV every month", "For large investors. Uses complex trades such as short selling."),
    ("PRIVATE EQUITY AND VC", "Valued every quarter", "Buys whole companies or start-ups. Few deals, hard to price."),
    ("AIF", "India's category for large investors", "A SEBI category for funds sold to wealthy investors. The minimum is ₹1 crore."),
    ("WHO DOES THE WORK", "Fund administrators", "SS&C GlobeOp, Apex Group, HC Global and Opus Fund Services run this work for many funds."),
    ("WHERE AI HELPS", "The checking", "Price checks, finding breaks, reading corporate action notices and drafting reports."),
], cols=3, dark_last=True)
goal_band(s, "Today's case:", "Opus Fund Services and AI-powered fund automation, run from a GCC in Pune.")
footer(s, 3)

# ---------------------------------------------------------------- S4 NAV
s = new_slide()
slide_bg(s, BG)
eyebrow(s, "HOUR 1 · THE NAV IN SIX STEPS")
title(s, "NAV: what one unit of the fund is worth today")
box(s, 0.6, 1.6, 6.3, 4.55, WHITE)
box(s, 0.6, 1.6, 6.3, 0.05, GOLD)
txt(s, 0.88, 1.8, 5.8, 0.3, [(None, 0, [("THE DAILY STEPS", None, 10, True, BLUE)])])
steps = [("1", "Capture every trade done today."),
         ("2", "Price every holding at today's closing price."),
         ("3", "Book income and corporate actions, such as dividends and splits."),
         ("4", "Subtract expenses, such as the management fee."),
         ("5", "Divide what is left by the number of units."),
         ("6", "Reconcile with the custodian and the transfer agent, then publish.")]
y = 2.22
for n, t in steps:
    txt(s, 0.88, y, 0.4, 0.5, [(None, 0, [(n, "Georgia", 16, True, GOLD)])])
    txt(s, 1.35, y + 0.04, 5.4, 0.55, [(None, 0, [(t, None, 12, False, INK)])])
    y += 0.62
box(s, 7.1, 1.6, 5.63, 4.55, NAVY)
txt(s, 7.38, 1.8, 5.1, 0.3, [(None, 0, [("TODAY'S LAB FUND, BEFORE RECONCILIATION", None, 10, True, GOLD)])])
rows = [("10 holdings at market price", "₹43.37 crore"), ("Add cash", "₹2.60 crore"), ("Less expenses", "₹0.09 crore"),
        ("Net assets", "₹45.88 crore"), ("Units outstanding", "1 crore"), ("NAV per unit", "₹45.8800")]
y = 2.25
for a, b in rows:
    big = a in ("Net assets", "NAV per unit")
    txt(s, 7.38, y, 3.0, 0.45, [(None, 0, [(a, None, 12, big, WHITE if big else SUBN)])])
    txt(s, 10.2, y - 0.04, 2.3, 0.45, [(PP_ALIGN.RIGHT, 0, [(b, "Georgia", 15 if big else 13, True, GOLD if big else WHITE)])], align=PP_ALIGN.RIGHT)
    y += 0.6
goal_band(s, "The formula:", "NAV = (holdings at market price + cash − expenses) ÷ units. Indian mutual funds publish it on the AMFI website every day.")
footer(s, 4)

# ---------------------------------------------------------------- S5 TRANSFER AGENCY
s = new_slide()
slide_bg(s, BG)
eyebrow(s, "HOUR 2 · TRANSFER AGENCY AND KYC")
title(s, "How investors get in and out of a fund")
cards(s, [
    ("STEP 1 · KYC", "Know your customer", "The investor gives PAN and Aadhaar. Under SEBI rules KYC is done once and stored with a KYC registration agency."),
    ("WHERE AI HELPS", "Reading and matching", "OCR reads the PAN card. AI matches “R. Kumar” on PAN with “Rajesh Kumar” at the bank. A person approves."),
    ("STEP 2 · SUBSCRIPTION", "Money in, units out", "Units = amount ÷ NAV. Example: ₹50,000 ÷ ₹45.8920 = 1,089.515 units."),
    ("STEP 3 · REDEMPTION", "Units in, money out", "The investor sells units back. The fund pays units × NAV."),
    ("STEP 4 · DIVIDEND", "Income paid out", "When the fund pays income, the transfer agent sends each investor their share."),
    ("ROLE-PLAY", "Onboard an investor", "One student is the investor, one the transfer agent, one the compliance checker."),
], cols=3, dark_last=True)
goal_band(s, "STP in one line:", "straight-through processing means a transaction runs end to end with no manual step. When it breaks, someone reconciles.")
footer(s, 5)

# ---------------------------------------------------------------- S6 RECONCILIATION
s = new_slide()
slide_bg(s, BG)
eyebrow(s, "HOUR 2 · RECONCILIATION")
title(s, "Three records must agree before the NAV goes out")
cards(s, [
    ("RECORD 1", "The fund's books", "What the fund accountant has recorded."),
    ("RECORD 2", "The custodian", "The shares and cash the bank actually holds."),
    ("RECORD 3", "The transfer agent", "The units investors actually own."),
], cols=3, top=1.6, h=1.45)
cards(s, [
    ("BREAK 1 · IN OUR LAB", "A split not booked", "Stock H: 4,000 units in the books, 8,000 at the custodian. The value does not change."),
    ("BREAK 2 · IN OUR LAB", "A dividend not booked", "The custodian holds ₹1,20,000 more cash than the books."),
    ("BREAK 3 · IN OUR LAB", "A redemption not booked", "The transfer agent shows 20,000 fewer units than the books."),
], cols=3, top=3.25, h=2.9, dark_last=True)
goal_band(s, "Result:", "after the three fixes the NAV moves from ₹45.8800 to ₹45.8920. A small change, but every investor's money depends on it.")
footer(s, 6)

# ---------------------------------------------------------------- S7 THE ACCOUNTING SKILL
s = new_slide()
slide_bg(s, BG)
eyebrow(s, "HOUR 2 · THE ACCOUNTING SKILL DEMO")
title(s, "Claude's reconciliation skill does the checking")
cards(s, [
    ("WHAT A SKILL IS", "Saved instructions for one job", "A skill tells Claude how accountants do a task. The finance reconciliation skill knows how a reconciliation is done."),
    ("WHAT IT DOES · 1", "Compares two records", "It lines up the fund's books against the custodian and the transfer agent."),
    ("WHAT IT DOES · 2", "Sorts every difference", "Timing, error or missing entry. It says how old each break is."),
    ("WHAT IT DOES · 3", "Suggests the fix", "It proposes the correcting entry. The journal-entry skill drafts it."),
    ("RELATED SKILL", "Variance analysis", "Explains why the NAV moved from yesterday to today."),
    ("THE HUMAN", "Reviews and signs", "The skill never posts an entry. The fund accountant approves every fix."),
], cols=3, dark_last=True)
goal_band(s, "No subscription?", "the lab does the same steps with a free Python script and any free AI chat.")
footer(s, 7)

# ---------------------------------------------------------------- S8 THE LIVE LAB
s = new_slide()
slide_bg(s, BG)
eyebrow(s, "HOUR 3 · THE LIVE LAB")
title(s, "Build a NAV report, reconcile it, explain it")
cards(s, [
    ("PART A · 20 MIN", "Watch the skill", "The instructor runs Claude's reconciliation skill on the lab files and it finds the three breaks."),
    ("PART B · 30 MIN", "Run the NAV engine", "Run nav_engine.py in Codex, Colab or any Python. It prices the fund, finds the breaks and writes nav_report.csv."),
    ("PART C · 30 MIN", "Write the commentary", "Paste the printed prompt into any free AI chat. Check every number against nav_report.csv. Swap reports with the next desk."),
], cols=3, top=1.6, dark_last=True)
goal_band(s, "Free and keyless:", "built-in Python only, no API key and no installs. The fund is made up and the prices are illustrative.")
footer(s, 8)

# ---------------------------------------------------------------- S9 PRACTICE
s = new_slide()
slide_bg(s, BG)
eyebrow(s, "PRACTICE QUESTIONS")
title(s, "Simple questions before the exam")
qs = [
    ("Q1", "What is NAV, and how is it calculated?", "Net asset value per unit: holdings at market price plus cash minus expenses, divided by units."),
    ("Q2", "What does a custodian do, and what does a transfer agent do?", "The custodian holds the fund's shares and cash. The transfer agent keeps the list of investors and their units."),
    ("Q3", "Name two transfer agents for Indian mutual funds.", "KFinTech and CAMS."),
    ("Q4", "An investor puts in ₹10,000 at a NAV of ₹25. How many units does the investor get?", "₹10,000 ÷ ₹25 = 400 units."),
    ("Q5", "What is a reconciliation break? Give one example.", "A difference between two records. Example: a dividend the custodian received that the books did not record."),
    ("Q6", "What is STP?", "Straight-through processing: a transaction runs end to end with no manual step."),
    ("Q7", "What is a Claude skill, and which one helps a fund accountant?", "Saved instructions for one job. The reconciliation skill compares records and sorts the breaks."),
    ("Q8", "Where can AI help in KYC, and what must a person still do?", "AI reads documents and matches names. A person approves the investor."),
]
y = 1.5
for qn_, q, tip in qs:
    box(s, 0.6, y, 12.13, 0.6, WHITE)
    box(s, 0.6, y, 0.07, 0.6, BLUE)
    txt(s, 0.9, y + 0.12, 0.7, 0.4, [(None, 0, [(qn_, "Georgia", 13, True, BLUE)])])
    txt(s, 1.65, y + 0.06, 10.9, 0.55, [
        (None, 0, [(q, None, 11, True, INK)]),
        (None, 1, [("TIP  ", None, 9, True, GOLD), (tip, None, 9.5, False, MUTE)]),
    ])
    y += 0.67
footer(s, 9)

OUT = "slides/Module-08-Fund-Administration-NAV.pptx"
prs.save(OUT)
print("saved", OUT, len(prs.slides._sldIdLst), "slides")
