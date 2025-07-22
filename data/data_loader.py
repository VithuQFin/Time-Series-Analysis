# data/data_loader.py

import yfinance as yf
import pandas as pd
import os

def fetch_multiple_tickers(tickers, period, raw_path="data/raw/"):
    os.makedirs(raw_path, exist_ok=True)
    all_data = []

    for ticker in tickers:
        try:
            print(f"🔄 Téléchargement de {ticker} pour {period}...")
            data = yf.download(ticker, period=period, auto_adjust=False)  # 🔧 correction ici

            if not data.empty:
                data.reset_index(inplace=True)
                data['Ticker'] = ticker

                # Vérifie que les colonnes nécessaires existent
                expected_cols = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Ticker']
                for col in ['Adj Close']:
                    if col not in data.columns:
                        data[col] = data['Close']  # fallback si Adj Close absent

                data = data[['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Ticker']]

                file_name = f"{ticker}_{period}.csv"
                file_path = os.path.join(raw_path, file_name)
                data.to_csv(file_path, index=False)

                print(f"✅ Données enregistrées : {file_path}")
                all_data.append(data)
            else:
                print(f"⚠️ Aucune donnée pour {ticker}")

        except Exception as e:
            print(f"❌ Erreur lors du téléchargement de {ticker} : {e}")

    return all_data

if __name__ == "__main__":
    tickers = ['AAPL', 'GOOGL', 'MSFT']
    period = '1y'
    fetch_multiple_tickers(tickers, period)