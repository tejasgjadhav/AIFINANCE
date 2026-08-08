# Module 1 Project — from one company to any company

Two steps. The first is Python that works for Swiggy. The second is the same idea working
for every listed company, built by an AI coding agent in under six minutes.

---

## Step 1 — Python gets the numbers  (`swiggy_data.py`)

This is the file ChatGPT wrote from one sentence of plain English:

> Write a Python script that gets Swiggy's latest share price, its revenue, and its profit
> and loss lines from Yahoo Finance. Comment every line.

Run it:

```bash
pip install yfinance
```

```bash
python3 swiggy_data.py
```

Real output, from the run in class:

```
SWIGGY LIMITED  (SWIGGY.NS)
Share price        : INR 280.75
Revenue            : INR 228,280,000,000
                     (about INR 22,828 crore)
Year ending        : 2026-03-31

PROFIT AND LOSS  (figures in crore)
                                2026-03-31      2025-03-31      2024-03-31
Total Revenue                       22,828          15,046          11,073
Cost Of Revenue                     10,666           6,438           4,948
Gross Profit                        12,162           8,608           6,125
Operating Expense                   16,576          12,000           8,726
Operating Income                    -4,414          -3,392          -2,601
Net Income                          -4,154          -3,117          -2,350
```

Thirty lines of Python, and you have three years of a listed company's P&L on your screen.
Revenue doubled in two years. The operating loss widened every year. That is a real reading
of a real company, and it took one sentence to ask for.

### But look at what it cannot do

- **It only does Swiggy.** The ticker `SWIGGY.NS` is typed into line 20. Another company
  means editing the file.
- **You have to know the ticker.** `SWIGGY.NS`, not "Swiggy". Nobody on a business desk
  knows that, and Yahoo's symbol for a company is not always guessable.
- **Only you can run it.** Anyone who wants a number has to install Python, open a terminal
  and edit a file. On a real desk that means they just ask you instead, and you become the
  bottleneck.

---

## Step 2 — Codex scales it to any company  (`codex_app/`)

This is everything that was typed into Codex:

> Create an application where I enter the name of a company and it connects to yfinance to
> give me the revenue and the latest market price.

What came back, unprompted:

| | |
|---|---|
| Files written | 5 — `server.py`, `index.html`, `app.js`, `styles.css`, `README.md` |
| Lines of code | 702 |
| Time | 5 minutes 29 seconds |
| Lines typed by a human | 0 |

It also started the server, called its own API, found the port was not answering, worked
out that Flask's debug reloader was killing the process, switched it off, restarted, then
opened the page in a browser and checked the result card rendered at desktop width.

Run it:

```bash
cd codex_app && pip install -r requirements.txt
```

```bash
python3 server.py
```

Then open http://127.0.0.1:5055 and type **Swiggy**. Or Reliance, or Infosys, or Apple.

### What actually changed between Step 1 and Step 2

| | Step 1 · the script | Step 2 · the app |
|---|---|---|
| Companies it handles | one, hardcoded | any listed company |
| What you type | a Yahoo ticker | a company name |
| Who can use it | you, in a terminal | anyone, in a browser |
| Where the name becomes a ticker | in your head | Yahoo's search, called by the code |
| Effort to add a company | edit the file | type it in the box |

The step that does the scaling is small and easy to miss: the app takes the name you typed,
asks Yahoo's search endpoint for matching symbols, prefers the NSE listing, and only then
fetches the data. That one lookup is the difference between a script for Swiggy and a tool
for the whole market.

You did not write it. You described the job in one sentence and checked the result.

---

## What did not change

Codex could not tell that a number was wrong. Point the app at Infosys and it returns
revenue of 20.16B labelled INR. Infosys reports about ₹1.6 lakh crore, which is ₹1.6T.
Yahoo files Infosys statements in dollars, and the app printed the dollar figure with a
rupee label. Nothing crashed. No warning appeared.

`swiggy_data.py` catches it, because ChatGPT was told to compare the two currency fields
and print a warning when they disagree. The agent that wrote the app was not told that, so
it did not.

**That is the whole lesson of Module 1.** The machine builds fast and it builds what you
asked for. The four checks are still yours:

1. Does the number match the company's own filing?
2. Is the currency and the unit stated?
3. Does the period match the year you wanted?
4. What does it print when the data is missing?

---

## What to submit

Run both. Then write four lines: one company you looked up, one number you verified against
its annual report, one number that looked wrong, and the check that caught it.

`yfinance` reads Yahoo Finance. It is free and it is fine for teaching, prototypes and
backtests. It is not licensed market data, so nothing you value for a client rests on it.
