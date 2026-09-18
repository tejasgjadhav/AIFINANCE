#!/usr/bin/env python3
"""Build Module 5 deck: Risk Modelling - PD Models & Monte Carlo VaR.
8 slides, plain English, ends on practice questions."""
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
    txt(s, 10.13, 7.08, 2.6, 0.25, [(PP_ALIGN.RIGHT, 0, [(f"MODULE 5  ·  {num:02d}", None, 8, False, c)])],
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



# ---------------------------------------------------------------- S1 TITLE
s = new_slide()
slide_bg(s, NAVY)
box(s, 0, 0, 13.333, 7.5, NAVY)
box(s, 10.23, 0, 3.1, 7.5, NAVY2)
box(s, 10.23, 0, 0.04, 7.5, GOLD)
txt(s, 0.6, 1.02, 9.0, 0.3, [(None, 0, [("ISBMS · PGDM 2025–27 · SEMESTER III · SESSION 5 OF 10", None, 12, True, GOLD)])])
txt(s, 0.6, 1.5, 9.4, 2.4, [
    (None, 0, [("Module 5", "Georgia", 58, True, WHITE)]),
    (None, 10, [("Risk Modelling — PD Models & Monte Carlo VaR", "Georgia", 21, False, SUBN)]),
])
box(s, 0.6, 4.28, 4.4, 0.02, GOLD)
txt(s, 0.6, 4.52, 9.0, 1.2, [
    (None, 0, [("Tejas Jadhav, CFA, FRM", None, 17, True, WHITE)]),
    (None, 4, [("Faculty · Agentic AI & Advanced Analytics in Finance (PGDM-SEM3-SPEC-AIFINANCE)", None, 12, False, MUTEN)]),
    (None, 3, [("tejasgjadhav.github.io/AIFINANCE", None, 12, True, GOLD)]),
])
txt(s, 10.55, 0.93, 2.4, 0.3, [(None, 0, [("TODAY", None, 10, True, GOLD)])])
txt(s, 10.55, 1.35, 2.5, 1.1, [
    (None, 0, [("Two questions", "Georgia", 15, True, WHITE)]),
    (None, 4, [("Will this borrower pay?", None, 10, False, MUTEN)]),
    (None, 2, [("How much can this book lose?", None, 10, False, MUTEN)]),
])
txt(s, 10.55, 3.05, 2.5, 1.2, [
    (None, 0, [("No heavy maths", "Georgia", 15, True, WHITE)]),
    (None, 4, [("Every number today comes", None, 10, False, MUTEN)]),
    (None, 2, [("from one multiplication or", None, 10, False, MUTEN)]),
    (None, 2, [("one sorted list.", None, 10, False, MUTEN)]),
])
txt(s, 10.55, 4.85, 2.5, 1.6, [
    (None, 0, [("1", "Georgia", 44, True, GOLD)]),
    (None, 4, [("VaR ENGINE, BUILT AND", None, 9, False, MUTEN)]),
    (None, 2, [("READ, BEFORE YOU LEAVE", None, 9, False, MUTEN)]),
])
footer(s, 1, dark=True)

# ---------------------------------------------------------------- S2 THE PLAN
s = new_slide()
slide_bg(s, BG)
eyebrow(s, "THE PLAN")
title(s, "What we do in these three hours")
cards = [
    (0.6, "HOUR 1 · 60 MIN", "Will they pay?", [
        "PD, LGD and EAD, and the one line that joins them",
        "Basel II and where the bank is allowed to use its own model",
        "Building a PD model: logistic regression, trees, XGBoost",
        "Reading the score: Gini, KS, AUC-ROC, and SHAP",
    ]),
    (4.72, "HOUR 2 · 60 MIN", "How much can we lose?", [
        "Three ways to compute VaR, and why they disagree",
        "10,000 simulated days on a multi-asset portfolio",
        "CVaR: the question VaR refuses to answer",
        "Basel III thresholds at 95% and 99%",
    ]),
    (8.84, "HOUR 3 · 60 MIN", "Build it", [
        "A Monte Carlo VaR engine on five NSE stocks",
        "10,000 paths, then 95% and 99% VaR and CVaR",
        "An AI-written risk note, checked against the numbers",
        "One PDF report you can hand to somebody",
    ]),
]
for x, kick, head, items in cards:
    box(s, x, 1.72, 3.95, 3.5, WHITE)
    box(s, x, 1.72, 3.95, 0.06, GOLD)
    txt(s, x + 0.28, 2.02, 3.4, 0.3, [(None, 0, [(kick, None, 9.5, True, BLUE)])])
    txt(s, x + 0.28, 2.38, 3.4, 0.45, [(None, 0, [(head, "Georgia", 17, True, NAVY)])])
    for i, t in enumerate(items):
        txt(s, x + 0.28, 3.0 + i * 0.52, 3.4, 0.5,
            [(None, 0, [("▪  ", None, 10, True, GOLD), (t, None, 10, False, INK)])])
box(s, 0.6, 5.42, 12.13, 0.66, TINT1)
box(s, 0.6, 5.42, 0.07, 0.66, BLUE)
txt(s, 0.95, 5.42, 11.5, 0.66, [(None, 0, [
    ("THE GRADED ASSIGNMENT IS INTRODUCED TODAY.  ", None, 11, True, BLUE),
    ("You will build a risk report on a portfolio of your own and defend the numbers in it.", None, 11, False, INK)])],
    anchor=MSO_ANCHOR.MIDDLE)
goal_band(s, "The whole module in one line:",
          "two questions, two numbers, and the honesty to say how wrong each number could be.")
footer(s, 2)

# ---------------------------------------------------------------- S3 EXPECTED LOSS
s = new_slide()
slide_bg(s, BG)
eyebrow(s, "HOUR 1 · CREDIT RISK")
title(s, "Three numbers, one multiplication")
defs = [
    ("PD", "Probability of Default", "How likely is it that this borrower stops paying in the next year?", "4%"),
    ("LGD", "Loss Given Default", "If they do stop, how much of the money do we never get back?", "45%"),
    ("EAD", "Exposure at Default", "How much will actually be outstanding on the day they stop?", "₹8,00,000"),
]
for i, (abbr, full, q, val) in enumerate(defs):
    x = 0.6 + i * 4.12
    box(s, x, 1.72, 3.95, 2.0, WHITE)
    txt(s, x + 0.28, 1.94, 1.5, 0.5, [(None, 0, [(abbr, "Georgia", 26, True, NAVY)])])
    txt(s, x + 0.28, 2.5, 3.4, 0.3, [(None, 0, [(full, None, 10, True, BLUE)])])
    txt(s, x + 0.28, 2.84, 3.4, 0.6, [(None, 0, [(q, None, 10.5, False, INK)])])
    box(s, x + 2.5, 1.9, 1.2, 0.5, TINT1)
    txt(s, x + 2.5, 1.9, 1.2, 0.5, [(PP_ALIGN.CENTER, 0, [(val, None, 13, True, BLUE)])],
        anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
box(s, 0.6, 3.92, 12.13, 0.86, NAVY)
box(s, 0.6, 3.92, 0.07, 0.86, GOLD)
txt(s, 0.95, 3.92, 11.5, 0.86, [(None, 0, [
    ("EXPECTED LOSS  =  PD  ×  LGD  ×  EAD      ", "Georgia", 17, True, GOLD),
    ("4%  ×  45%  ×  ₹8,00,000  =  ₹14,400 per loan", "Georgia", 17, True, WHITE)])],
    anchor=MSO_ANCHOR.MIDDLE)
txt(s, 0.6, 5.0, 6.0, 1.2, [
    (None, 0, [("Say it in words", "Georgia", 15, True, NAVY)]),
    (None, 6, [("Out of a hundred loans like this one, four go bad. When one goes bad we lose "
                "45 paise in the rupee on the ₹8 lakh still outstanding. So we price ₹14,400 "
                "into every loan, whether it goes bad or not.", None, 11.5, False, INK)]),
])
txt(s, 6.9, 5.0, 5.83, 1.2, [
    (None, 0, [("The part students miss", "Georgia", 15, True, NAVY)]),
    (None, 6, [("Expected loss is a cost, not a surprise. It is budgeted and priced in. "
                "Capital is held for the UNEXPECTED loss, which is the year four loans "
                "becomes eleven.", None, 11.5, False, INK)]),
])
goal_band(s, "Basel II, in one sentence:",
          "a bank that can prove its own PD, LGD and EAD models work is allowed to use them to set its own capital.")
footer(s, 3)

# ---------------------------------------------------------------- S4 BASEL II
s = new_slide()
slide_bg(s, BG)
eyebrow(s, "HOUR 1 · BASEL II")
title(s, "Who is allowed to use their own model?")
txt(s, 0.6, 1.58, 12.13, 0.32, [(None, 0, [
    ("Every bank must hold capital against its loans. Basel II gave banks two ways to work out how much.",
     None, 12, False, MUTE)])])
two = [
    (0.6, WHITE, "THE STANDARDISED APPROACH", "The regulator gives you the numbers.", [
        "A loan gets a risk weight from a published table.",
        "The weight comes off the borrower's external rating.",
        "The bank models nothing and estimates nothing.",
        "Simple to run, and it usually demands more capital.",
    ]),
    (6.73, NAVY, "THE IRB APPROACH", "The bank estimates its own numbers.", [
        "Foundation IRB: the bank estimates PD. The regulator still sets LGD and EAD.",
        "Advanced IRB: the bank estimates PD, LGD and EAD itself.",
        "This is where every model in this module actually gets used.",
        "Permission is granted by the supervisor, and it can be taken away.",
    ]),
]
for x, fill, kick, head, items in two:
    dark = fill == NAVY
    box(s, x, 2.0, 6.0, 2.6, fill)
    txt(s, x + 0.28, 2.2, 5.4, 0.3, [(None, 0, [(kick, None, 9.5, True, GOLD if dark else BLUE)])])
    txt(s, x + 0.28, 2.54, 5.4, 0.36, [(None, 0, [(head, "Georgia", 15, True, WHITE if dark else NAVY)])])
    for k, t in enumerate(items):
        txt(s, x + 0.28, 3.0 + k * 0.4, 5.4, 0.38,
            [(None, 0, [("▪  ", None, 9.5, True, GOLD), (t, None, 9.5, False, SUBN if dark else INK)])])
box(s, 0.6, 4.78, 12.13, 1.16, TINT1)
box(s, 0.6, 4.78, 0.07, 1.16, BLUE)
txt(s, 0.95, 4.94, 11.5, 0.9, [
    (None, 0, [("WHY A BANK WANTS ITS OWN MODEL, IN ONE SUM", None, 9.5, True, BLUE)]),
    (None, 4, [("Take a ₹100 crore corporate book. On the standardised weight of 100% the bank "
                "holds 8% of ₹100 crore, which is ₹8 crore. Suppose its own model justifies an "
                "effective weight of 60%. Now it holds 8% of ₹60 crore, which is ₹4.8 crore. "
                "The same book has freed ₹3.2 crore of capital to lend again.",
                None, 11, False, INK)]),
])
goal_band(s, "Basel II is a bargain, not a gift:",
          "prove your model works and you may set your own capital. Fail to prove it and you go back to the regulator's table.")
footer(s, 4)

# ---------------------------------------------------------------- S5 BUILDING PD
s = new_slide()
slide_bg(s, BG)
eyebrow(s, "HOUR 1 · BUILDING THE MODEL")
title(s, "From five ratios to one probability")
txt(s, 0.6, 1.58, 12.13, 0.32, [(None, 0, [
    ("Here is one borrower. These are numbers you already know how to compute from a balance sheet.",
     None, 12, False, MUTE)])])
ratios = [("Current ratio", "1.4"), ("Debt to equity", "2.1"), ("Interest cover", "2.3"),
          ("Sales growth", "−4%"), ("Times paid late", "3")]
for k, (lab, val) in enumerate(ratios):
    x = 0.6 + k * 2.45
    box(s, x, 1.98, 2.3, 0.86, WHITE)
    txt(s, x + 0.18, 2.1, 1.95, 0.3, [(None, 0, [(lab, None, 9, True, BLUE)])])
    txt(s, x + 0.18, 2.4, 1.95, 0.38, [(None, 0, [(val, "Georgia", 17, True, NAVY)])])
box(s, 0.6, 3.02, 12.13, 0.72, NAVY)
box(s, 0.6, 3.02, 0.07, 0.72, GOLD)
txt(s, 0.95, 3.02, 11.5, 0.72, [(None, 0, [
    ("SCORE  =  −3.2  +  (0.8 × debt to equity)  −  (0.5 × interest cover)  +  (0.4 × times late)      ",
     "Georgia", 13, True, WHITE),
    ("→  PD = 4%", "Georgia", 14, True, GOLD)])], anchor=MSO_ANCHOR.MIDDLE)
txt(s, 0.6, 3.94, 6.0, 1.7, [
    (None, 0, [("Say what just happened", "Georgia", 15, True, NAVY)]),
    (None, 6, [("Every ratio gets a weight. Multiply each ratio by its weight and add them up. "
                "That total is the score. A curve then squeezes the score into a number between "
                "0 and 1, and that number is the probability of default. There is nothing else "
                "inside a logistic regression.", None, 11, False, INK)]),
])
txt(s, 6.9, 3.94, 5.83, 1.7, [
    (None, 0, [("Why banks still start here", "Georgia", 15, True, NAVY)]),
    (None, 6, [("You can print this model on one line. You can point at the weight that hurt "
                "this borrower. A supervisor can recompute it by hand. For a regulated lending "
                "decision, that matters more than the last two points of accuracy.",
                None, 11, False, INK)]),
])
goal_band(s, "Do it live:",
          "change interest cover from 2.3 to 1.1 in front of the class, recompute the score, and watch the PD move.")
footer(s, 5)

# ---------------------------------------------------------------- S6 LR vs XGBOOST
s = new_slide()
slide_bg(s, BG)
eyebrow(s, "HOUR 1 · THE CHOICE EVERY TEAM ARGUES ABOUT")
title(s, "The older model, or the one that predicts better?")
three = [
    (0.6, 3.95, WHITE, "LOGISTIC REGRESSION", "One weight per ratio, added up.",
     "You can print it, explain one decline, and defend it line by line.",
     "It assumes each ratio pushes in a straight line, which is not always true."),
    (4.72, 3.95, WHITE, "DECISION TREE", "A flowchart of yes and no questions.",
     "Anyone can read it. Interest cover below 1.5? Then debt to equity above 3?",
     "Change the data slightly and the tree redraws itself completely."),
    (8.84, 3.89, NAVY, "XGBOOST", "Hundreds of small trees, voting.",
     "Each tree fixes the mistakes of the one before it. Usually the most accurate.",
     "There is no single weight to point at, so a decline is hard to explain."),
]
for x, w, fill, kick, head, pro, con in three:
    dark = fill == NAVY
    box(s, x, 1.68, w, 3.0, fill)
    txt(s, x + 0.28, 1.9, w - 0.56, 0.3, [(None, 0, [(kick, None, 9.5, True, GOLD if dark else BLUE)])])
    txt(s, x + 0.28, 2.24, w - 0.56, 0.6, [(None, 0, [(head, "Georgia", 15, True, WHITE if dark else NAVY)])])
    txt(s, x + 0.28, 2.96, w - 0.56, 0.74,
        [(None, 0, [("+  ", None, 10, True, GOLD), (pro, None, 10, False, SUBN if dark else INK)])])
    txt(s, x + 0.28, 3.82, w - 0.56, 0.74,
        [(None, 0, [("−  ", None, 10, True, GOLD), (con, None, 10, False, SUBN if dark else MUTE)])])
box(s, 0.6, 4.86, 12.13, 1.1, TINT1)
box(s, 0.6, 4.86, 0.07, 1.1, BLUE)
txt(s, 0.95, 5.0, 11.5, 0.9, [
    (None, 0, [("WHAT YOU ACTUALLY GAIN AND LOSE", None, 9.5, True, BLUE)]),
    (None, 4, [("On the same data XGBoost usually buys you a few points of accuracy. That is real, "
                "and it is smaller than people expect. What it costs you is the sentence you give "
                "the customer who was declined. Most banks build both, use the sharper one to "
                "challenge the simpler one, and ship the one they can explain.",
                None, 11, False, INK)]),
])
goal_band(s, "The rule of thumb:",
          "the newer the model, the better it predicts and the harder it is to defend to the person you just declined.")
footer(s, 6)

# ---------------------------------------------------------------- S7 READING IT
s = new_slide()
slide_bg(s, BG)
eyebrow(s, "HOUR 1 · DOES IT WORK, AND CAN YOU EXPLAIN IT?")
title(s, "Three checks on the model, one check on the decision")
txt(s, 0.6, 1.56, 12.13, 0.32, [(None, 0, [
    ("Take 1,000 borrowers. Fifty of them defaulted. Here is how you find out whether the model saw them coming.",
     None, 12, False, MUTE)])])
checks = [
    ("AUC-ROC", "0.78", "Pick one borrower who defaulted and one who did not, at random. AUC is "
     "how often the model gave the defaulter the higher risk score. Half is a coin flip. A real "
     "working model sits near 0.78."),
    ("GINI", "0.56", "The same fact on the scale banks prefer: Gini = 2 × AUC − 1. An AUC of 0.78 "
     "is a Gini of 0.56. If somebody quotes you one, you can compute the other."),
    ("KS STATISTIC", "0.41", "Sort all 1,000 by score, riskiest first. Walk down the list and "
     "track how many defaulters and how many good borrowers you have picked up. KS is the widest "
     "gap between the two, and it shows you where the cut-off earns its keep."),
]
for k, (head, val, body) in enumerate(checks):
    x = 0.6 + k * 4.12
    w = 3.95 if k < 2 else 3.89
    box(s, x, 1.96, w, 2.2, WHITE)
    box(s, x, 1.96, w, 0.05, GOLD)
    txt(s, x + 0.28, 2.2, 2.2, 0.32, [(None, 0, [(head, None, 10, True, BLUE)])])
    txt(s, x + w - 1.3, 2.12, 1.05, 0.44, [(PP_ALIGN.RIGHT, 0, [(val, "Georgia", 20, True, NAVY)])],
        align=PP_ALIGN.RIGHT)
    txt(s, x + 0.28, 2.66, w - 0.56, 1.3, [(None, 0, [(body, None, 10, False, INK)])])
box(s, 0.6, 4.3, 12.13, 1.64, NAVY)
box(s, 0.6, 4.3, 0.07, 1.64, GOLD)
txt(s, 0.95, 4.48, 11.5, 1.3, [
    (None, 0, [("SHAP  ·  THE ONE THAT EXPLAINS A PERSON, NOT A MODEL", None, 10, True, GOLD)]),
    (None, 5, [("The three numbers above judge the whole model. They tell you it ranks borrowers "
                "well. They cannot tell one rejected applicant why.", None, 11, False, SUBN)]),
    (None, 5, [("SHAP takes a single decision apart. For this borrower: the interest cover of 2.3 "
                "pushed the PD up by 1.8 points, the three late payments pushed it up 0.9 more, "
                "and the current ratio pulled it back down 0.3. That is the sentence you give the "
                "customer, and it is the one the regulator asks to see.", None, 11, False, WHITE)]),
])
goal_band(s, "Do it live:",
          "train both models on a public credit file, print the AUC of each, then SHAP one rejected applicant and read the reason out loud.")
footer(s, 7)

# ---------------------------------------------------------------- S6 VaR
s = new_slide()
slide_bg(s, BG)
eyebrow(s, "HOUR 2 · MARKET RISK")
title(s, "VaR is one sentence. The rest is how you compute it.")
box(s, 0.6, 1.6, 12.13, 0.76, NAVY)
box(s, 0.6, 1.6, 0.07, 0.76, GOLD)
txt(s, 0.95, 1.6, 11.5, 0.76, [(None, 0, [
    ("A 99% one-day VaR of ₹6,60,000 means this:  ", None, 12, True, GOLD),
    ("on 99 days out of 100, we should lose less than ₹6,60,000. It says nothing about the hundredth day.",
     None, 12, False, WHITE)])], anchor=MSO_ANCHOR.MIDDLE)
ways = [
    ("HISTORICAL SIMULATION", "Replay the last 500 days that actually happened.",
     "Assumes nothing about the shape of returns.",
     "You only ever see what already occurred."),
    ("PARAMETRIC", "Assume a normal curve and use one volatility number.",
     "Fast, and you can do it in a spreadsheet.",
     "Real markets have fatter tails than normal."),
    ("MONTE CARLO", "Invent 10,000 tomorrows from volatility and correlation.",
     "Handles many assets and odd payoffs.",
     "Only as good as the assumptions you fed it."),
]
for i, (head, what, pro, con) in enumerate(ways):
    x = 0.6 + i * 4.12
    dark = i == 2
    box(s, x, 2.56, 3.95, 2.42, NAVY if dark else WHITE)
    txt(s, x + 0.28, 2.78, 3.4, 0.3, [(None, 0, [(head, None, 10, True, GOLD if dark else BLUE)])])
    txt(s, x + 0.28, 3.14, 3.4, 0.62, [(None, 0, [(what, None, 11, True, WHITE if dark else NAVY)])])
    txt(s, x + 0.28, 3.86, 3.4, 0.5, [(None, 0, [("+  ", None, 10, True, GOLD), (pro, None, 10, False, SUBN if dark else INK)])])
    txt(s, x + 0.28, 4.4, 3.4, 0.5, [(None, 0, [("−  ", None, 10, True, GOLD), (con, None, 10, False, SUBN if dark else MUTE)])])
txt(s, 0.6, 5.16, 6.0, 1.1, [
    (None, 0, [("CVaR, the question VaR ducks", "Georgia", 15, True, NAVY)]),
    (None, 6, [("VaR tells you the edge of the bad 1%. CVaR tells you the average loss once you "
                "are inside it. VaR says ₹6.6 lakh; CVaR might say ₹9.4 lakh.", None, 11, False, INK)]),
])
txt(s, 6.9, 5.16, 5.83, 1.1, [
    (None, 0, [("Basel III asks for both levels", "Georgia", 15, True, NAVY)]),
    (None, 6, [("95% and 99% are the thresholds you report. Run all three methods on the same "
                "portfolio and you get three different answers. That gap is the lesson.", None, 11, False, INK)]),
])
footer(s, 8)

# ---------------------------------------------------------------- S7 THE LAB
s = new_slide()
slide_bg(s, BG)
eyebrow(s, "HOUR 3 · THE LAB")
title(s, "Build it, compare it, then test it")
box(s, 0.6, 1.58, 12.13, 0.68, NAVY2)
box(s, 0.6, 1.58, 0.07, 0.68, GOLD)
txt(s, 0.95, 1.58, 11.5, 0.68, [
    (None, 0, [("THE SENTENCE WE TYPE", None, 8.5, True, GOLD)]),
    (None, 2, [("\u201cBuild a Monte Carlo VaR engine for five NSE stocks, run 10,000 paths, and "
                "give me 95% and 99% VaR and CVaR.\u201d", "Georgia", 13, True, WHITE)]),
], anchor=MSO_ANCHOR.MIDDLE)
parts = [
    (0.6, 3.95, WHITE, "PART A  ·  35 MIN", "Build it", [
        "Five NSE stocks, two years of daily returns",
        "Each stock's volatility, and how the five move together",
        "Ten thousand simulated tomorrows",
        "Sort them: the 100th worst is your 99% VaR, and the tail past it is CVaR",
    ]),
    (4.72, 3.95, WHITE, "PART B  ·  10 MIN", "Compare it", [
        "Run the same portfolio through historical and parametric",
        "Three methods, three different answers",
        "Which one do you report, and why that one?",
        "The gap between them is your uncertainty, made visible",
    ]),
    (8.84, 3.89, NAVY, "PART C  ·  15 MIN", "Test it", [
        "Count the breaches over 250 real trading days",
        "At 99% you expect two or three, not nine",
        "Basel zones: 0-4 green, 5-9 yellow, 10 or more red",
        "A red zone means rebuild it, not explain it away",
    ]),
]
for x, w, fill, kick, head, items in parts:
    dark = fill == NAVY
    box(s, x, 2.42, w, 3.34, fill)
    txt(s, x + 0.28, 2.64, w - 0.56, 0.3, [(None, 0, [(kick, None, 9.5, True, GOLD if dark else BLUE)])])
    txt(s, x + 0.28, 2.98, w - 0.56, 0.44, [(None, 0, [(head, "Georgia", 17, True, WHITE if dark else NAVY)])])
    for j2, t in enumerate(items):
        txt(s, x + 0.28, 3.56 + j2 * 0.56, w - 0.56, 0.54,
            [(None, 0, [("\u25aa  ", None, 10, True, GOLD), (t, None, 10, False, SUBN if dark else INK)])])
goal_band(s, "Why Part C matters most:",
          "building a VaR takes 35 minutes. Finding out it breached nine times when it should have breached three takes 15.")
footer(s, 9)

# ---------------------------------------------------------------- S8 PRACTICE
s = new_slide()
slide_bg(s, BG)
eyebrow(s, "PRACTICE QUESTIONS")
title(s, "Six questions before the exam")
qs = [
    ("Q1", "A loan has PD 3%, LGD 40% and EAD ₹5,00,000. What is the expected loss, and who pays it?",
     "₹6,000. The borrower pays it, priced into the interest rate, whether or not this loan goes bad."),
    ("Q2", "Explain the difference between expected loss and unexpected loss, and what each is funded by.",
     "Expected loss is budgeted and priced in. Unexpected loss is the bad year, and capital is held against it."),
    ("Q3", "A PD model scores AUC 0.78. Say what that means without using the word AUC.",
     "Take a defaulter and a non-defaulter at random; 78 times in 100 the model scores the defaulter as riskier."),
    ("Q4", "Your XGBoost model beats the logistic regression. Give one reason you might still ship the regression.",
     "You can print it, explain a single decline, and defend it to a regulator. Accuracy is not the only test."),
    ("Q5", "Historical, parametric and Monte Carlo give three different VaRs on one portfolio. Why, and which do you report?",
     "Each assumes something different about returns. Report the method your policy names, and disclose the other two."),
    ("Q6", "Your 99% one-day VaR is ₹6.6 lakh. In 250 trading days you breach it nine times. What does that tell you?",
     "You expected about 2 or 3. Nine says the model understates risk, and it must be rebuilt, not explained away."),
]
y = 1.58
for qn_, q, tip in qs:
    box(s, 0.6, y, 12.13, 0.74, WHITE)
    box(s, 0.6, y, 0.07, 0.74, BLUE)
    txt(s, 0.9, y + 0.07, 0.7, 0.4, [(None, 0, [(qn_, "Georgia", 14, True, BLUE)])])
    txt(s, 1.7, y + 0.06, 10.8, 0.64, [
        (None, 0, [(q, None, 10.5, True, INK)]),
        (None, 2, [("TIP  ", None, 9, True, GOLD), (tip, None, 9, False, MUTE)]),
    ])
    y += 0.8
box(s, 0.6, 6.42, 12.13, 0.56, NAVY)
box(s, 0.6, 6.42, 0.07, 0.56, GOLD)
txt(s, 0.9, 6.42, 11.5, 0.56, [(None, 0, [
    ("Before Session 6:  ", None, 11, True, GOLD),
    ("pick five listed stocks, and write down the one thing that would make all five fall together.", None, 11, False, WHITE)])],
    anchor=MSO_ANCHOR.MIDDLE)
txt(s, 0.6, 7.08, 9.0, 0.25, [(None, 0, [("The tip is the shape of the answer, not the whole answer. Two or three sentences each in the exam.", None, 8, False, MUTE)])])
txt(s, 10.13, 7.08, 2.6, 0.25, [(PP_ALIGN.RIGHT, 0, [("MODULE 5  ·  10", None, 8, False, MUTE)])], align=PP_ALIGN.RIGHT)

OUT = "slides/Module-05-Risk-Modelling.pptx"
prs.save(OUT)
print("saved", OUT, len(prs.slides._sldIdLst), "slides")
