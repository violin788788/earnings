import os
import time
import csv
import requests
from dataclasses import dataclass
from datetime import datetime, time as dtime, timedelta
from typing import Dict, List

import pandas as pd
from sec_edgar_downloader import Downloader

# ======================
# CONFIG
# ======================

API_KEY = os.getenv("POLYGON_API_KEY", "PUT_YOUR_KEY_HERE")
SEC_FOLDER = "sec-edgar-filings"
PRICE_FOLDER = "price_history"

BEGIN_DATE = "2023-01-01"
END_DATE = "2026-01-01"

MARKET_OPEN = dtime(9, 30)
MARKET_CLOSE = dtime(16, 0)

# ======================
# DATA MODELS
# ======================

@dataclass
class EarningsEvent:
    stock: str
    filing_date: str
    release_type: str  # BMO / AMC
    gap: float
    move_up: float
    move_down: float
    move_close: float
    vp_before: int
    vp_after: int


# ======================
# UTILITIES
# ======================

def percent_change(a: float, b: float) -> float:
    return round((b / a - 1) * 100, 2)


def load_price_history(stock: str) -> pd.DataFrame:
    path = os.path.join(PRICE_FOLDER, f"{stock}_polygon_daily.csv")
    df = pd.read_csv(path, parse_dates=["date"])
    df.set_index("date", inplace=True)
    return df


# ======================
# SEC DOWNLOAD
# ======================

def download_sec_filings(stocks: List[str]) -> None:
    dl = Downloader("ResearchProject", "email@example.com")

    for stock in stocks:
        stock_path = os.path.join(SEC_FOLDER, stock)
        if os.path.exists(stock_path):
            continue

        print(f"Downloading SEC filings for {stock}")
        dl.get("10-Q", stock, after=BEGIN_DATE, before=END_DATE)
        dl.get("10-K", stock, after=BEGIN_DATE, before=END_DATE)


def truncate_filings(stock: str, limit: int = 1000) -> None:
    base = os.path.join(SEC_FOLDER, stock)
    for root, _, files in os.walk(base):
        for file in files:
            if file == "full-submission.txt":
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content[:limit])


# ======================
# PRICE HISTORY
# ======================

def download_price_history(stock: str) -> None:
    out = os.path.join(PRICE_FOLDER, f"{stock}_polygon_daily.csv")
    if os.path.exists(out):
        return

    url = f"https://api.polygon.io/v2/aggs/ticker/{stock}/range/1/day/{BEGIN_DATE}/{END_DATE}"
    params = {
        "adjusted": "true",
        "sort": "asc",
        "limit": 50000,
        "apiKey": API_KEY
    }

    bars = []
    while url:
        r = requests.get(url, params=params)
        if r.status_code == 429:
            time.sleep(60)
            continue
        r.raise_for_status()
        data = r.json()
        bars.extend(data.get("results", []))
        url = data.get("next_url")
        if url:
            url += f"&apiKey={API_KEY}"
            time.sleep(15)

    df = pd.DataFrame(bars)
    df["date"] = pd.to_datetime(df["t"], unit="ms")
    df = df.rename(columns={"o": "open", "h": "high", "l": "low", "c": "close", "v": "volume"})
    df.set_index("date", inplace=True)
    df.to_csv(out)


# ======================
# EARNINGS PARSER
# ======================

def parse_acceptance_datetime(text: str) -> datetime:
    tag = "<ACCEPTANCE-DATETIME>"
    start = text.find(tag)
    if start == -1:
        raise ValueError("No acceptance datetime found")

    raw = text[start:].split(">")[1][:14]
    return datetime.strptime(raw, "%Y%m%d%H%M%S")


def classify_release(ts: datetime):
    if ts.time() >= MARKET_CLOSE:
        return "AMC", ts.date(), ts.date() + timedelta(days=1)
    if ts.time() < MARKET_OPEN:
        return "BMO", ts.date() - timedelta(days=1), ts.date()
    return None, None, None


# ======================
# CORE ANALYSIS
# ======================

def analyze_stock(stock: str) -> List[EarningsEvent]:
    df = load_price_history(stock)
    events = []

    base = os.path.join(SEC_FOLDER, stock)

    for root, _, files in os.walk(base):
        if "full-submission.txt" not in files:
            continue

        path = os.path.join(root, "full-submission.txt")
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        try:
            ts = parse_acceptance_datetime(text)
            release, before_day, after_day = classify_release(ts)
            if not release:
                continue

            before = df.loc[str(before_day)]
            after = df.loc[str(after_day)]

            vp_before = int(before["close"] * before["volume"])
            vp_after = int(after["open"] * after["volume"])

            if vp_after < vp_before:
                continue

            event = EarningsEvent(
                stock=stock,
                filing_date=str(ts.date()),
                release_type=release,
                gap=percent_change(before["close"], after["open"]),
                move_up=percent_change(after["open"], after["high"]),
                move_down=percent_change(after["open"], after["low"]),
                move_close=percent_change(after["open"], after["close"]),
                vp_before=vp_before,
                vp_after=vp_after,
            )

            events.append(event)

        except Exception as e:
            print(stock, "skipped:", e)

    return events


# ======================
# ENTRY POINT
# ======================

def load_stock_list(csv_file: str) -> List[str]:
    with open(csv_file, newline="", encoding="utf-8") as f:
        return [row[0] for row in csv.reader(f) if row and row[0] != "Symbol"]


def main():
    stocks = load_stock_list("500.csv")[:100]

    os.makedirs(PRICE_FOLDER, exist_ok=True)

    download_sec_filings(stocks)

    for stock in stocks:
        truncate_filings(stock)
        download_price_history(stock)

    all_events = []
    for stock in stocks:
        all_events.extend(analyze_stock(stock))

    df = pd.DataFrame([e.__dict__ for e in all_events])
    df.to_csv("earnings_events.csv", index=False)
    print(df.head())


if __name__ == "__main__":
    main()
