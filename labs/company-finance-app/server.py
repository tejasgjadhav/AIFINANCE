from __future__ import annotations

from datetime import datetime
from typing import Any

import pandas as pd
import yfinance as yf
from flask import Flask, jsonify, render_template, request


app = Flask(__name__)


COMMON_TICKERS = {
    "apple": "AAPL",
    "microsoft": "MSFT",
    "google": "GOOGL",
    "alphabet": "GOOGL",
    "amazon": "AMZN",
    "tesla": "TSLA",
    "meta": "META",
    "facebook": "META",
    "nvidia": "NVDA",
    "netflix": "NFLX",
    "tata consultancy services": "TCS.NS",
    "tcs": "TCS.NS",
    "reliance": "RELIANCE.NS",
    "infosys": "INFY.NS",
    "hdfc bank": "HDFCBANK.NS",
    "icici bank": "ICICIBANK.NS",
}


def compact_number(value: Any) -> str | None:
    if value is None or pd.isna(value):
        return None

    number = float(value)
    abs_number = abs(number)
    units = [
        (1_000_000_000_000, "T"),
        (1_000_000_000, "B"),
        (1_000_000, "M"),
        (1_000, "K"),
    ]

    for divisor, suffix in units:
        if abs_number >= divisor:
            return f"{number / divisor:,.2f}{suffix}"
    return f"{number:,.2f}"


def resolve_symbol(query: str) -> dict[str, str]:
    normalized = query.strip().lower()
    if normalized in COMMON_TICKERS:
        symbol = COMMON_TICKERS[normalized]
        return {"symbol": symbol, "name": query.strip(), "exchange": "Matched locally"}

    if query.isupper() and len(query) <= 12:
        return {"symbol": query, "name": query, "exchange": "Ticker entered"}

    try:
        search = yf.Search(query, max_results=5)
        quotes = getattr(search, "quotes", []) or []
        for quote in quotes:
            symbol = quote.get("symbol")
            quote_type = quote.get("quoteType", "")
            if symbol and quote_type in {"EQUITY", "ETF"}:
                return {
                    "symbol": symbol,
                    "name": quote.get("shortname") or quote.get("longname") or symbol,
                    "exchange": quote.get("exchDisp") or quote.get("exchange") or "Yahoo Finance",
                }
    except Exception:
        pass

    return {"symbol": query.strip().upper(), "name": query.strip(), "exchange": "Fallback ticker"}


def latest_price(ticker: yf.Ticker, info: dict[str, Any]) -> tuple[float | None, str | None]:
    price_fields = ("regularMarketPrice", "currentPrice", "previousClose")
    for field in price_fields:
        value = info.get(field)
        if value is not None:
            return float(value), field

    try:
        fast_price = ticker.fast_info.get("last_price")
        if fast_price is not None:
            return float(fast_price), "fast_info.last_price"
    except Exception:
        pass

    history = ticker.history(period="1d", interval="1m")
    if not history.empty:
        return float(history["Close"].dropna().iloc[-1]), "intraday close"

    return None, None


def latest_revenue(ticker: yf.Ticker, info: dict[str, Any]) -> tuple[float | None, str | None, str | None]:
    statements = [
        ("annual financials", ticker.financials),
        ("quarterly financials", ticker.quarterly_financials),
    ]

    for label, frame in statements:
        if frame is not None and not frame.empty and "Total Revenue" in frame.index:
            series = frame.loc["Total Revenue"].dropna()
            if not series.empty:
                period = series.index[0]
                if hasattr(period, "date"):
                    period_label = period.date().isoformat()
                else:
                    period_label = str(period)
                return float(series.iloc[0]), label, period_label

    value = info.get("totalRevenue") or info.get("revenue")
    if value is not None:
        return float(value), "profile totalRevenue", "Trailing twelve months"

    return None, None, None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/company")
def company():
    query = request.args.get("name", "").strip()
    if not query:
        return jsonify({"error": "Enter a company name or ticker."}), 400

    resolved = resolve_symbol(query)
    ticker = yf.Ticker(resolved["symbol"])

    try:
        info = ticker.get_info() or {}
        price, price_source = latest_price(ticker, info)
        revenue, revenue_source, revenue_period = latest_revenue(ticker, info)
    except Exception as exc:
        return jsonify({"error": f"Could not load Yahoo Finance data: {exc}"}), 502

    currency = info.get("currency") or info.get("financialCurrency") or ""
    market_cap = info.get("marketCap")

    return jsonify(
        {
            "query": query,
            "symbol": resolved["symbol"],
            "companyName": info.get("longName") or info.get("shortName") or resolved["name"],
            "exchange": info.get("exchange") or resolved["exchange"],
            "currency": currency,
            "latestPrice": price,
            "latestPriceFormatted": f"{currency} {price:,.2f}".strip() if price is not None else None,
            "priceSource": price_source,
            "revenue": revenue,
            "revenueFormatted": f"{currency} {compact_number(revenue)}".strip() if revenue is not None else None,
            "revenueSource": revenue_source,
            "revenuePeriod": revenue_period,
            "marketCapFormatted": f"{currency} {compact_number(market_cap)}".strip()
            if market_cap is not None
            else None,
            "website": info.get("website"),
            "updatedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5055, debug=False)
