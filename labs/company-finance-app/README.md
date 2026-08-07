# Company Finance Lookup — the Module 1 app

Type a company name. Get the latest market price and the last reported revenue from
Yahoo Finance. This is the app built in class, in one instruction, by an AI coding agent.

The instruction that produced it was this:

> Create an application where I enter the name of a company and it connects to yfinance
> to give me the revenue and the latest market price.

The agent then wrote `server.py`, `templates/index.html`, `static/app.js` and
`static/styles.css`, started the server, called its own API, found the port was not
answering, switched off the Flask debug reloader, restarted, and checked the page in a
browser. 702 lines, no line typed by a human.

---

## Run it

```bash
pip install -r requirements.txt
```

```bash
python3 server.py
```

Then open http://127.0.0.1:5055

Type a company name, or use the Apple / Reliance / Microsoft buttons. For Indian
companies use the NSE ticker if the name does not resolve, for example `RELIANCE.NS`.

---

## Your job is to break it

The app works. That does not mean the numbers are right. Two real results from the
same build:

| Query | Ticker | Price | Revenue reported |
|---|---|---|---|
| Reliance | RELIANCE.NS | INR 1,334.80 | INR 10.57T |
| Infosys | INFY.NS | INR 1,175.10 | INR 20.16B |

Reliance is correct. Infosys is not. Infosys reports roughly ₹1.6 lakh crore of annual
revenue, which is about ₹1.6T. The figure the app printed is the dollar number carrying
a rupee label.

Nothing crashed. No error appeared. A number that is wrong by a factor of about eighty
was displayed in a clean interface, and it would have gone into a report if nobody had
checked.

**Exercise.** Find where in `server.py` the revenue is read, work out why the currency
label is wrong, and fix it so the app prints the currency Yahoo actually reported the
statement in. Then run these four checks on every company you try:

1. Does the number match the company's own filing?
2. Is the currency and the unit stated?
3. Does the date match the period you asked for?
4. What does the app print when the data is missing?

---

## What this is not

yfinance reads Yahoo Finance. It is free, it is convenient, and it is not licensed
market data. It is fine for teaching, prototypes and backtests. Nothing you value for a
client should rest on it.
