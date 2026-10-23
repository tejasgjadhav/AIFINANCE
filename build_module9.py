#!/usr/bin/env python3
"""Build Module 9 deck: Market Commentary and Valuation Dashboards.
Ten simple slides; the case is the faculty's daily market dashboard, shown by design only."""
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
    num = len(prs.slides._sldIdLst)  # number slides by position, so inserts never break the sequence
    c = MUTEN if dark else MUTE
    txt(s, 0.6, 7.08, 8.0, 0.25, [(None, 0, [(FOOT_L, None, 8, False, c)])])
    txt(s, 10.13, 7.08, 2.6, 0.25, [(PP_ALIGN.RIGHT, 0, [(f"MODULE 9  ·  {num:02d}", None, 8, False, c)])],
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
txt(s, 0.6, 1.02, 9.0, 0.3, [(None, 0, [("ISBMS · PGDM 2025–27 · SEMESTER III · SESSION 9 OF 10", None, 12, True, GOLD)])])
txt(s, 0.6, 1.5, 9.4, 2.4, [
    (None, 0, [("Module 9", "Georgia", 58, True, WHITE)]),
    (None, 10, [("Market Commentary and Valuation Dashboards", "Georgia", 21, False, SUBN)]),
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
    (None, 4, [("Is the news good or bad?", None, 10, False, MUTEN)]),
    (None, 2, [("What is a company worth?", None, 10, False, MUTEN)]),
    (None, 2, [("Can a dashboard run itself?", None, 10, False, MUTEN)]),
])
txt(s, 10.55, 3.45, 2.5, 1.2, [
    (None, 0, [("Live today", "Georgia", 15, True, WHITE)]),
    (None, 4, [("Our daily market dashboard,", None, 10, False, MUTEN)]),
    (None, 2, [("then you build your own.", None, 10, False, MUTEN)]),
])
txt(s, 10.55, 4.95, 2.5, 1.6, [
    (None, 0, [("1", "Georgia", 44, True, GOLD)]),
    (None, 4, [("PRE-MARKET DASHBOARD,", None, 9, False, MUTEN)]),
    (None, 2, [("BUILT BEFORE YOU LEAVE", None, 9, False, MUTEN)]),
])
footer(s, 0, dark=True)

# ---------------------------------------------------------------- S2 SENTIMENT
s = new_slide()
slide_bg(s, BG)
eyebrow(s, "HOUR 1 · FINANCIAL NLP")
title(s, "Sentiment analysis: is this news good or bad?")
cards(s, [
    ("WHAT IT IS", "Scoring the mood of text", "A model reads a headline or a transcript and labels it positive, negative or neutral."),
    ("FINBERT", "A model trained on finance text", "A version of BERT trained on financial news and reports. It is free to download."),
    ("WHY NOT A WORD LIST?", "Words mislead", "\u201cCrude oil falls as supply concerns ease\u201d is good news for India. A word list sees \u201cconcerns\u201d and calls it negative."),
    ("STEP 1", "Collect", "Gather NSE announcements and news headlines each morning."),
    ("STEP 2", "Clean and score", "Remove noise, then score each item with FinBERT."),
    ("STEP 3", "Write the commentary", "AI writes a short note from the scores, and a person checks it."),
], cols=3, dark_last=True)
goal_band(s, "Remember:", "sentiment is a signal, not a decision. It tells you the mood, not what to buy.")
footer(s, 0)

# ---------------------------------------------------------------- S3 EARNINGS CALLS
s = new_slide()
slide_bg(s, BG)
eyebrow(s, "HOUR 1 · EARNINGS CALLS AND EVENTS")
title(s, "Reading earnings calls at scale")
cards(s, [
    ("KEY PHRASES", "What management stresses", "Phrases like \u201cguidance raised\u201d or \u201cmargin pressure\u201d are pulled out of a long transcript."),
    ("EVENT SIGNALS", "News that moves prices", "A results date, a rating change or a big order is tagged as an event."),
    ("THE CASE", "AI earnings summaries", "Bloomberg Intelligence uses AI to summarise earnings calls, so an analyst reads one page, not fifty."),
    ("THE RULE", "Check against the source", "Every number in an AI summary must match the transcript or the filing."),
], cols=2, dark_last=True)
goal_band(s, "Live demo:", "FinBERT scores the lines of an NSE earnings call transcript, one by one.")
footer(s, 0)

# ---------------------------------------------------------------- S4 DCF
s = new_slide()
slide_bg(s, BG)
eyebrow(s, "HOUR 2 · VALUATION WITH AI")
title(s, "DCF: what a company is worth today")
cards(s, [
    ("STEP 1", "Project cash flows", "Grow last year's free cash flow for five years. In our lab: \u20b91,000 crore growing 12% a year."),
    ("STEP 2", "Discount them", "Divide each year's cash by (1 + WACC) to the power of the year. Our WACC is 11%."),
    ("STEP 3", "Add a terminal value", "Value every year after year 5 in one number, growing 5% a year, then discount it."),
    ("STEP 4", "Per share", "Subtract net debt of \u20b91,500 crore and divide by 50 crore shares. Result: about \u20b9439 a share."),
    ("WHERE AI HELPS", "Assumptions and explanation", "AI can draft the assumptions and explain the result. It never does the arithmetic."),
    ("WHERE PYTHON HELPS", "The calculation", "Python does every multiplication and division, so the answer can be checked."),
], cols=3, dark_last=True)
goal_band(s, "Sensitivity:", "most of the value sits in the terminal value, so a small change in WACC moves the answer a lot.")
footer(s, 0)

# ---------------------------------------------------------------- S5 COMPARABLES
s = new_slide()
slide_bg(s, BG)
eyebrow(s, "HOUR 2 · COMPARABLE COMPANIES")
title(s, "Comparables: is it cheap or dear against its peers?")
cards(s, [
    ("P/E", "Price to earnings", "Share price \u00f7 earnings per share. A price of \u20b9440 and EPS of \u20b922 gives a P/E of 20."),
    ("EV/EBITDA", "Whole business value to operating profit", "Enterprise value \u00f7 EBITDA. It ignores how the company is financed."),
    ("P/BV", "Price to book value", "Share price \u00f7 book value per share. Common for banks."),
    ("HOW TO USE THEM", "Compare with peers", "If peers trade at a P/E of 25 and our company at 20, ask why before calling it cheap."),
    ("DATA", "Damodaran and ESG", "Professor Damodaran publishes free industry multiples. ESG scores can adjust the risk view."),
    ("WHERE AI HELPS", "Collecting the multiples", "AI pulls the multiples out of filings. Python lines them up and checks them."),
], cols=3, dark_last=True)
goal_band(s, "Remember:", "a multiple is a quick check. A DCF explains why the value is what it is.")
footer(s, 0)

# ---------------------------------------------------------------- S6 THE DASHBOARD
s = new_slide()
slide_bg(s, BG)
eyebrow(s, "THE CASE · OUR DAILY MARKET DASHBOARD")
title(s, "A dashboard that is ready before the market opens")
cards(s, [
    ("TOP STRIP", "The markets at a glance", "Nifty 50, Sensex, Brent crude, USD/INR and India VIX, with their last change."),
    ("OVERNIGHT CUES", "What happened while we slept", "GIFT Nifty, US markets and currency moves, pointing to the likely open."),
    ("SUMMARY", "A short morning brief", "A paragraph that ties the overnight cues and the news together."),
    ("NEWS FEED", "Five to eight headlines", "The day's main stories, each with its source."),
    ("WHEN", "Every weekday, 8:30 AM", "It refreshes itself 45 minutes before the 9:15 AM open."),
    ("WHO TOUCHES IT", "Nobody", "No one opens a laptop. The page is simply there each morning."),
], cols=3, dark_last=True)
goal_band(s, "Today:", "you see it live, then you build a smaller version of it in Hour 3.")
footer(s, 0)

# ---------------------------------------------------------------- S7 HOW IT IS BUILT
s = new_slide()
slide_bg(s, BG)
eyebrow(s, "THE CASE · HOW IT IS BUILT")
title(s, "Five steps, run by a schedule")
flow = [("1", "Schedule", "GitHub Actions starts the job every weekday morning."),
        ("2", "Python script", "Sends Claude a fixed prompt template and today's page."),
        ("3", "Claude API", "Runs ten or more web searches and writes the updated page."),
        ("4", "Safety check", "The script checks the new page is complete before saving it."),
        ("5", "Publish", "The page is saved to GitHub and goes live on GitHub Pages.")]
w, gap = 2.25, 0.22
for i, (n, h, b) in enumerate(flow):
    x = 0.6 + i * (w + gap)
    dark = i == 2
    box(s, x, 1.65, w, 2.3, NAVY if dark else WHITE)
    box(s, x, 1.65, w, 0.05, GOLD)
    txt(s, x + 0.2, 1.82, w - 0.4, 2.05, [
        (None, 0, [(n, "Georgia", 20, True, GOLD)]),
        (None, 2, [(h, "Georgia", 15, True, WHITE if dark else NAVY)]),
        (None, 5, [(b, None, 11, False, SUBN if dark else INK)]),
    ])
    if i < 4:
        txt(s, x + w - 0.02, 2.6, gap + 0.04, 0.4, [(PP_ALIGN.CENTER, 0, [("\u2192", None, 14, True, GOLD)])], align=PP_ALIGN.CENTER)
cards(s, [
    ("WHAT WORKS WELL", "It runs itself, reliably", "A schedule, a fixed prompt, a safety check and free hosting."),
    ("WHAT WE WOULD IMPROVE", "Numbers in Python, words in AI", "Today Claude finds and works out the numbers. A bank would fetch them in Python and let AI only write."),
], cols=2, top=4.15, h=2.0, dark_last=True)
goal_band(s, "Governance:", "the API key sits in GitHub's secret store, and the job stops if the key is missing.")
footer(s, 0)

# ---------------------------------------------------------------- S8 THE LIVE LAB
s = new_slide()
slide_bg(s, BG)
eyebrow(s, "HOUR 3 · THE LIVE LAB")
title(s, "Build your own pre-market dashboard")
cards(s, [
    ("PART A · 20 MIN", "Watch it live", "The instructor opens the daily market dashboard and runs its job by hand."),
    ("PART B · 40 MIN", "Build your version", "Run build_dashboard.py. Python computes the gap, flows, VIX, news mood and a DCF, then writes dashboard.html."),
    ("PART C · 30 MIN", "Write and check the brief", "Paste the printed prompt into any free AI chat. Check every number. Swap with the next desk."),
], cols=3, dark_last=True)
goal_band(s, "Free and keyless:", "built-in Python only. The snapshot is illustrative. Run it with --break to watch it refuse a missing number.")
footer(s, 0)

# ---------------------------------------------------------------- S9 ASSIGNMENT
s = new_slide()
slide_bg(s, BG)
eyebrow(s, "CLASS ASSIGNMENT")
title(s, "Ten questions, ten marks, five minutes")
cards(s, [
    ("WHERE", "On the course website", "Open \u201cClass assignments (A and B)\u201d from the Module 9 or Module 10 card."),
    ("PASSWORD", "Given in class", "Class A and Class B each have their own tab and their own password."),
    ("FORMAT", "True or false", "Ten questions on Modules 1 to 8, one at a time, 30 seconds each."),
    ("RULES", "Stay on the page", "Leaving the tab loses the question on screen. You cannot go back."),
    ("MARKING", "Automatic", "Your score appears as soon as you finish."),
    ("LEADERBOARD", "First attempt only", "Each class has its own leaderboard. Only your first attempt counts."),
], cols=3, dark_last=True)
goal_band(s, "Before you start:", "enter your full name and your roll number. Use one device and a steady connection.")
footer(s, 0)

# ---------------------------------------------------------------- S10 PRACTICE
s = new_slide()
slide_bg(s, BG)
eyebrow(s, "PRACTICE QUESTIONS")
title(s, "Simple questions before the exam")
qs = [
    ("Q1", "What is sentiment analysis?", "Scoring text as positive, negative or neutral."),
    ("Q2", "What is FinBERT?", "A BERT language model trained on financial text to score sentiment."),
    ("Q3", "Why can a word list get sentiment wrong?", "It ignores context. Falling crude is good for India, but the word list may call it negative."),
    ("Q4", "What are the four steps of a DCF?", "Project cash flows, discount them, add a terminal value, convert to per-share value."),
    ("Q5", "What does P/E tell you?", "How many rupees investors pay for one rupee of earnings."),
    ("Q6", "Why should Python, not AI, do the arithmetic?", "Python gives the same checkable answer every time. A number an AI produced is hard to defend."),
    ("Q7", "How does the daily market dashboard update itself?", "A schedule runs a script, Claude searches and writes the page, a check runs, and the page is published."),
    ("Q8", "What should the dashboard do if a number is missing?", "Refuse to publish and say which input is missing."),
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
footer(s, 0)

OUT = "slides/Module-09-Market-Commentary-and-Dashboards.pptx"
prs.save(OUT)
print("saved", OUT, len(prs.slides._sldIdLst), "slides")
