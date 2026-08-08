"""
STEP 1 — Get Swiggy's numbers with Python.

This is the file ChatGPT wrote when it was asked, in plain English:

    "Write a Python script that gets Swiggy's latest share price, its revenue,
     and its profit and loss lines from Yahoo Finance. Comment every line."

Run it:
    pip install yfinance
    python3 swiggy_data.py

Nothing else. No API key, no data subscription.
"""

import yfinance as yf

# Swiggy is listed on the NSE. Yahoo writes NSE tickers with a .NS suffix.
TICKER = "SWIGGY.NS"

stock = yf.Ticker(TICKER)
info = stock.info
pnl = stock.financials          # the profit and loss statement, one column per year


# --- 1. the share price right now ------------------------------------------
price = info.get("regularMarketPrice")
price_currency = info.get("currency")

print("=" * 62)
print(f"SWIGGY LIMITED  ({TICKER})")
print("=" * 62)
print(f"Share price        : {price_currency} {price:,.2f}")


# --- 2. revenue, and the currency the statements are filed in --------------
statement_currency = info.get("financialCurrency")
latest_year = pnl.columns[0]                    # most recent financial year
revenue = float(pnl.loc["Total Revenue", latest_year])

print(f"Revenue            : {statement_currency} {revenue:,.0f}")
print(f"                     (about {statement_currency} {revenue/1e7:,.0f} crore)")
print(f"Year ending        : {str(latest_year)[:10]}")


# --- 3. always compare the two currency fields -----------------------------
# The price can come back in rupees while the statements are filed in dollars.
# Infosys does exactly that. Check it every single time.
if price_currency != statement_currency:
    print()
    print("WARNING: price is in", price_currency, "but the statements are in",
          statement_currency, "- do not put these two numbers in the same table.")


# --- 4. the profit and loss, three years side by side ----------------------
LINES = ["Total Revenue", "Cost Of Revenue", "Gross Profit",
         "Operating Expense", "Operating Income", "Net Income"]

print()
print("PROFIT AND LOSS  (figures in crore)")
years = list(pnl.columns[:3])
print(f"{'':<26}" + "".join(f"{str(y)[:10]:>16}" for y in years))

for line in LINES:
    if line not in pnl.index:
        continue                                 # not every company reports every line
    row = ""
    for y in years:
        value = pnl.loc[line, y]
        row += f"{value/1e7:>16,.0f}" if value == value else f"{'-':>16}"  # NaN check
    print(f"{line:<26}{row}")

print()
print("Now check one number against Swiggy's own annual report before you use it.")
