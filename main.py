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

# === PARAMÈTRES GLOBAUX === #
TICKERS = ["AAPL"]
PERIOD = "5y"  # ex: "1y", "5y", "max"
RAW_PATH = "data/raw/"
CLEAN_PATH = "data/clean/"
PERIODS_PER_YEAR = 252
RISK_FREE_RATE = 0.02

# === ÉTAPE 1 : TÉLÉCHARGEMENT DES DONNÉES === #
print("📥 Étape 1 : Téléchargement des données...")
fetch_multiple_tickers(TICKERS, PERIOD, raw_path=RAW_PATH)

# === ÉTAPE 2 : NETTOYAGE DES DONNÉES === #
print("\n🧹 Étape 2 : Nettoyage des données...")
clean_data_files(raw_path=RAW_PATH, clean_path=CLEAN_PATH)

# === ÉTAPE 3 : CHARGEMENT DES FICHIERS NETTOYÉS === #
print("\n📂 Étape 3 : Chargement des fichiers nettoyés...")
cleaned_dfs = {}

for ticker in TICKERS:
    file_name = f"{ticker}_{PERIOD}.csv"
    file_path = os.path.join(CLEAN_PATH, file_name)

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df["Date"] = pd.to_datetime(df["Date"])
        cleaned_dfs[ticker] = df
    else:
        print(f"⚠️ Fichier nettoyé non trouvé pour {ticker} ({file_name})")

# === ÉTAPE 4 : CALCUL DES MÉTRIQUES === #
print("\n📊 Étape 4 : Calcul des métriques financières...\n")
for ticker, df in cleaned_dfs.items():
    print(f"📈 {ticker}")
    metrics = compute_all_metrics(df, return_col="Return", periods_per_year=PERIODS_PER_YEAR, risk_free_rate=RISK_FREE_RATE)
    for key, value in metrics.items():
        print(f"   {key:25s} : {value:.2%}" if isinstance(value, float) else f"   {key:25s} : {value}")
    print("")

# === ÉTAPE 5 : VISUALISATIONS === #
print("\n📉 Étape 5 : Visualisations...\n")
for ticker, df in cleaned_dfs.items():
    print(f"🔍 Visualisation de {ticker}...")
    plot_price_series(df, ticker=ticker)
    plot_log_return_evolution(df, ticker=ticker)
    plot_return_evolution(df, ticker=ticker)
    plot_rolling_volatility(df, window=20, ticker=ticker)
    plot_return_distribution(df, ticker=ticker)
    plot_log_return_distribution(df, ticker=ticker)
    plot_drawdown(df, ticker=ticker)

# === ÉTAPE 6 : MATRICE DE CORRÉLATION === #
if len(TICKERS) > 1:
    print("\n🔗 Étape 6 : Matrice de corrélation...")
    plot_correlation_matrix(cleaned_dfs)

print("\n✅ Pipeline terminé.")
