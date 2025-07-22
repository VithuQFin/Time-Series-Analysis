# 📈 Financial Time Series Analysis

This repository provides a complete pipeline for downloading, cleaning, analyzing, and visualizing financial time series data (e.g., stock prices). It supports multiple assets and includes both a CLI interface (`main.py`).

---

## 🔧 Features

- ✅ Download historical price data from Yahoo Finance
- 🧹 Clean and preprocess the data (missing values, formatting, returns)
- 📊 Compute key financial metrics (Sharpe Ratio, Sortino, Max Drawdown, Volatility, CAGR, etc.)
- 📉 Generate plots: price evolution, drawdowns, return distributions, rolling volatility, etc.
- 🔗 Correlation matrix across multiple assets

---

## 🗂️ Project Structure

.
├── analyse/
│ ├── metrics.py # Financial metrics computation
│ └── visualisations.py # Static visualizations
├── data/
│ ├── raw/ # Raw downloaded data
│ ├── clean/ # Cleaned data after preprocessing
│ ├── data_loader.py # Yahoo Finance data fetcher
│ └── data_cleaning.py # Data preprocessing pipeline
├── main.py # Main CLI-based pipeline
├── requirements.txt # Python dependencies
├── .gitignore # Git ignored files
└── README.md # Project documentation