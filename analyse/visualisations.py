# src/visualisations.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
import streamlit as st

def plot_price_series(df: pd.DataFrame, title: str = "Évolution du prix", ticker: str = ""):
    plt.figure(figsize=(12, 5))
    plt.plot(df["Date"], df["Close"], label=f"{ticker} - Prix de clôture")
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Prix")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_log_return_evolution(df: pd.DataFrame, return_col: str = "Log Return", ticker: str = ""):
    plt.figure(figsize=(12, 5))
    plt.plot(df["Date"], df[return_col], label=f"{ticker} - Rendement logarithmique")
    plt.title("Évolution du rendement logarithmique")
    plt.xlabel("Date")
    plt.ylabel("Rendement Logarithmique")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_return_evolution(df: pd.DataFrame, return_col: str = "Return", ticker: str = ""):
    plt.figure(figsize=(12, 5))
    plt.plot(df["Date"], df[return_col], label=f"{ticker} - Rendement")
    plt.title("Évolution du rendement")
    plt.xlabel("Date")
    plt.ylabel("Rendement")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_rolling_volatility(df: pd.DataFrame, window: int = 20, return_col: str = "Return", ticker: str = ""):
    rolling_vol = df[return_col].rolling(window).std()
    plt.figure(figsize=(12, 5))
    plt.plot(df["Date"], rolling_vol, label=f"{ticker} - Volatilité glissante ({window} jours)")
    plt.title(f"Volatilité glissante - Fenêtre {window} jours")
    plt.xlabel("Date")
    plt.ylabel("Volatilité")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_correlation_matrix(data_dict: dict):
    """
    Affiche la heatmap des corrélations entre plusieurs DataFrames.
    
    Parameters:
        data_dict (dict): Dictionnaire {ticker: DataFrame nettoyé}
    """
    returns = pd.DataFrame({
        ticker: df["Return"] for ticker, df in data_dict.items()
    })

    corr = returns.corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1, linewidths=0.5)
    plt.title("Matrice de corrélation des rendements")
    plt.tight_layout()
    plt.show()

def plot_corr_matrix_plotly(data_dict):
    returns = pd.DataFrame({
        ticker: df["Return"] for ticker, df in data_dict.items()
    })

    corr_matrix = returns.corr()

    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        title="Matrice de corrélation des rendements"
    )
    fig.update_layout(margin=dict(l=40, r=40, t=40, b=40))
    st.plotly_chart(fig, use_container_width=True)



def plot_return_distribution(df: pd.DataFrame, return_col: str = "Return", bins: int = 50, ticker: str = ""):
    plt.figure(figsize=(10, 5))
    sns.histplot(df[return_col], bins=bins, kde=True)
    plt.title(f"Distribution des rendements - {ticker}")
    plt.xlabel("Rendement")
    plt.ylabel("Fréquence")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_log_return_distribution(df: pd.DataFrame, return_col: str = "Log Return", bins: int = 50, ticker: str = ""):
    plt.figure(figsize=(10, 5))
    sns.histplot(df[return_col], bins=bins, kde=True)
    plt.title(f"Distribution des rendements logarithmiques - {ticker}")
    plt.xlabel("Rendement Logarithmique")
    plt.ylabel("Fréquence")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_drawdown(df: pd.DataFrame, return_col: str = "Return", ticker: str = ""):
    cumulative = (1 + df[return_col]).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak

    plt.figure(figsize=(12, 5))
    plt.plot(df["Date"], drawdown, color="red", label=f"Drawdown - {ticker}")
    plt.title("Drawdown cumulé")
    plt.xlabel("Date")
    plt.ylabel("Drawdown")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
