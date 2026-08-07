# Module 1 Lab — Read a filing, and check what you were told

**Everything here runs free.** No Claude subscription, no API key, no paid account,
no `pip install`. Plain Python 3 and the standard library. It works in a free Codex
session, in Google Colab, in Replit, or on your own laptop.

You will do in 60 minutes what a first-year analyst does on a Monday morning: pull six
numbers out of an annual report, and prove they are right.

---

## Before you start (5 minutes)

1. Download this folder, or open it in your free coding sandbox.
2. Check Python works:

```bash
python3 --version
```

Anything from 3.8 upwards is fine. That is the whole setup.

---

## What is in the folder

| File | What it is |
|---|---|
| `excerpts/company_a.txt` | A clean profit and loss statement, in ₹ crore |
| `excerpts/company_b.txt` | The same thing, but in ₹ **lakh**, with a footnote |
| `excerpts/company_c.txt` | Two years side by side, with a line most rules miss |
| `step1_read_the_numbers.py` | Pulls the numbers out with ordinary Python rules |
| `prompt.txt` | The prompt you paste into any free AI chat |
| `step2_check_ai_output.py` | Checks the AI's answer — four tests |
| `step3_agent_loop.py` | A working Observe → Plan → Act → Reflect loop |
| `ai_output.sample.json` | What a good AI answer looks like |
| `optional_claude_api.py` | Instructor demo only. You do not need it. |

---

## Step 1 — Do it with rules (15 minutes)

```bash
python3 step1_read_the_numbers.py
```

The script hunts for six labels and grabs the number next to each: revenue from
operations, other income, total expenses, profit before tax, tax expense, profit
after tax. Then it runs two ordinary accounting checks:

- revenue + other income − total expenses = profit before tax
- profit before tax − tax = profit after tax

**Read the output carefully.** Company A works. Company B works but is printed in
**lakh** — 8,42,150 lakh is ₹8,421 crore, so putting it beside Company A's crore
figures without converting is a 100× error, and no check catches it. Company C breaks
the rules outright.

That is the point of Step 1. Rules work until the page changes. Every listed company
prints its P&L slightly differently, so the rules never stop needing patches.

**Answer before moving on:** which of the three failures would still have been wrong if
nobody read the output?

---

## Step 2 — Do it with AI, then refuse to trust it (25 minutes)

1. Open `prompt.txt` and copy all of it.
2. Open any free AI chat you already use — ChatGPT, Claude.ai, Gemini, Copilot, or the
   sandbox we use in class.
3. Paste the prompt. Where it says *paste the contents of one file*, paste
   `excerpts/company_c.txt` — the one the rules could not read.
4. Copy the JSON it gives back into a new file called `ai_output.json` in this folder.
5. Run the checker:

```bash
python3 step2_check_ai_output.py excerpts/company_c.txt
```

Four checks run, in the order a real desk applies them:

1. **Does it parse?** If the model wrapped the JSON in a sentence, this fails.
2. **Is the shape right?** All six fields, for every period.
3. **Does it add up?** The two accounting identities again.
4. **Is every number actually printed in the filing?** This is the one that catches an
   invented figure. The checker searches the source text for each number, with and
   without Indian comma grouping.

When something fails, change the **prompt**, not the numbers, and run it again. Write
down what failed and what you changed — that note is the deliverable.

> Company C fails check 3 honestly, and you should be able to say why in one sentence.
> The company adds *share of profit of associates* between total expenses and profit
> before tax. The model is right; the identity was too simple. Knowing the difference
> between a model error and a rule that is too crude is the whole skill.

---

## Step 3 — See an agent actually work (10 minutes)

```bash
python3 step3_agent_loop.py
```

A fund's NAV does not match the custodian's. The script observes the gap, plans its own
checks, calls three "tools", and reflects after each one until the difference is fully
explained — then drafts a note for a human to sign.

There is no AI in that file. It is 60 lines of Python you can read end to end, which is
exactly why it is worth reading: the loop, the step budget, the tool boundary and the
human sign-off are the parts that matter, and they do not change when a model is dropped
into the middle.

Then do what the last line of the output tells you: mark the corporate action as already
processed and run it again. Watch it escalate instead of inventing an answer.

---

## What to hand in

Make a folder or a GitHub repository called `module1-extraction` containing:

- `prompt.txt` — your final version, not the first one
- `ai_output.json` — the answer you got back
- `NOTES.md` — a short table: which excerpt, did it parse, did the arithmetic tie, how
  many of the six fields were found, and one line on what went wrong and what you changed

Three lines of notes. Anyone can get one good answer out of an AI. What a desk pays for
is somebody who can say, in writing, how often it was right and where it broke.

---

## Why the lab is built this way

You are learning to be the person who checks the machine, not the person who is impressed
by it. Every module in this course ends with something that runs, and this is the first
one. By Session 10 you will have ten.
