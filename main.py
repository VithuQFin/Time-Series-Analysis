# main.py

import os
import pandas as pd
from data.data_loader import fetch_multiple_tickers
from data.data_cleaning import clean_data_files
from analyse.metrics import compute_all_metrics
from analyse.visualisations import (
    plot_price_series,
    plot_log_return_evolution,
    plot_return_evolution,
    plot_rolling_volatility,
    plot_return_distribution,
    plot_log_return_distribution,
    plot_drawdown,
    plot_correlation_matrix
)

# === GLOBAL PARAMETERS === #
TICKERS = ["AAPL"]
PERIOD = "5y"  # e.g., "1y", "5y", "max"
RAW_PATH = "data/raw/"
CLEAN_PATH = "data/clean/"
PERIODS_PER_YEAR = 252
RISK_FREE_RATE = 0.02

# === STEP 1: DOWNLOAD DATA === #
print("📥 Step 1: Downloading data...")
fetch_multiple_tickers(TICKERS, PERIOD, raw_path=RAW_PATH)

# === STEP 2: CLEAN DATA === #
print("\n🧹 Step 2: Cleaning data...")
clean_data_files(raw_path=RAW_PATH, clean_path=CLEAN_PATH)

# === STEP 3: LOAD CLEANED FILES === #
print("\n📂 Step 3: Loading cleaned files...")
cleaned_dfs = {}

for ticker in TICKERS:
    file_name = f"{ticker}_{PERIOD}.csv"
    file_path = os.path.join(CLEAN_PATH, file_name)

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df["Date"] = pd.to_datetime(df["Date"])
        cleaned_dfs[ticker] = df
    else:
        print(f"⚠️ Cleaned file not found for {ticker} ({file_name})")

# === STEP 4: COMPUTE METRICS === #
print("\n📊 Step 4: Computing financial metrics...\n")
for ticker, df in cleaned_dfs.items():
    print(f"📈 {ticker}")
    metrics = compute_all_metrics(df, return_col="Return", periods_per_year=PERIODS_PER_YEAR, risk_free_rate=RISK_FREE_RATE)
    for key, value in metrics.items():
        print(f"   {key:25s} : {value:.2%}" if isinstance(value, float) else f"   {key:25s} : {value}")
    print("")

# === STEP 5: VISUALIZATIONS === #
print("\n📉 Step 5: Generating visualizations...\n")
for ticker, df in cleaned_dfs.items():
    print(f"🔍 Visualizing {ticker}...")
    plot_price_series(df, ticker=ticker)
    plot_log_return_evolution(df, ticker=ticker)
    plot_return_evolution(df, ticker=ticker)
    plot_rolling_volatility(df, window=20, ticker=ticker)
    plot_return_distribution(df, ticker=ticker)
    plot_log_return_distribution(df, ticker=ticker)
    plot_drawdown(df, ticker=ticker)

# === STEP 6: CORRELATION MATRIX === #
if len(TICKERS) > 1:
    print("\n🔗 Step 6: Computing correlation matrix...")
    plot_correlation_matrix(cleaned_dfs)

print("\n✅ Pipeline completed.")
