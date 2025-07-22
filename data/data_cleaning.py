# data/data_cleaning.py

import pandas as pd
import os
import numpy as np

def clean_data_files(raw_path="data/raw/", clean_path="data/clean/"):
    os.makedirs(clean_path, exist_ok=True)

    raw_files = [f for f in os.listdir(raw_path) if f.endswith('.csv')]
    if not raw_files:
        print("⚠️ Aucun fichier brut trouvé.")
        return

    for file in raw_files:
        file_path = os.path.join(raw_path, file)
        print(f"🔧 Nettoyage de {file}...")

        try:
            df = pd.read_csv(file_path)

            # Supprimer les lignes avec Date vide
            df = df[df['Date'].notna()]

            # Conversion date
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df.dropna(subset=['Date'], inplace=True)

            # Colonnes numériques à convertir
            num_cols = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
            for col in num_cols:
                df[col] = pd.to_numeric(df[col], errors='coerce')

            # Supprimer les lignes où une colonne essentielle est manquante ou le volume est nul
            df.dropna(subset=num_cols, inplace=True)
            df = df[df['Volume'] > 0]

            # Nettoyage général
            df.drop_duplicates(inplace=True)
            df.sort_values(by='Date', inplace=True)
            df.reset_index(drop=True, inplace=True)

            # Calcul du rendement
            df['Return'] = df['Close'].pct_change().fillna(0)
            df['Log Return'] = np.log(df['Close'] / df['Close'].shift(1)).fillna(0)
            # Sauvegarde
            clean_file_path = os.path.join(clean_path, file)
            df.to_csv(clean_file_path, index=False)
            print(f"✅ Fichier nettoyé sauvegardé : {clean_file_path}")

        except Exception as e:
            print(f"❌ Erreur lors du traitement de {file} : {e}")

if __name__ == "__main__":
    clean_data_files()