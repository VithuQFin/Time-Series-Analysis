import pandas as pd
import numpy as np

def compute_annualized_return(df: pd.DataFrame, return_col: str = "Return", periods_per_year: int = 252) -> float:
    mean_return = df[return_col].mean()
    return (1 + mean_return)**periods_per_year - 1


def compute_annualized_volatility(df: pd.DataFrame, return_col: str = "Return", periods_per_year: int = 252) -> float:
    return df[return_col].std() * np.sqrt(periods_per_year)


def compute_sharpe_ratio(df: pd.DataFrame, return_col: str = "Return", risk_free_rate: float = 0.01, periods_per_year: int = 252) -> float:
    ann_return = compute_annualized_return(df, return_col, periods_per_year)
    ann_vol = compute_annualized_volatility(df, return_col, periods_per_year)
    excess_return = ann_return - risk_free_rate
    return excess_return / ann_vol if ann_vol != 0 else np.nan


def compute_sortino_ratio(df: pd.DataFrame, return_col: str = "Return", risk_free_rate: float = 0.01, periods_per_year: int = 252) -> float:
    downside_returns = df[df[return_col] < 0][return_col]
    downside_vol = downside_returns.std() * np.sqrt(periods_per_year)
    ann_return = compute_annualized_return(df, return_col, periods_per_year)
    excess_return = ann_return - risk_free_rate
    return excess_return / downside_vol if downside_vol != 0 else np.nan


def compute_cumulative_return(df: pd.DataFrame, return_col: str = "Return") -> float:
    cumulative = (1 + df[return_col]).prod() - 1
    return cumulative


def compute_max_drawdown(df: pd.DataFrame, return_col: str = "Return") -> float:
    cumulative = (1 + df[return_col]).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    return drawdown.min()


def compute_calmar_ratio(df: pd.DataFrame, return_col: str = "Return", periods_per_year: int = 252) -> float:
    ann_return = compute_annualized_return(df, return_col, periods_per_year)
    max_dd = abs(compute_max_drawdown(df, return_col))
    return ann_return / max_dd if max_dd != 0 else np.nan


def compute_rolling_volatility(df: pd.DataFrame, return_col: str = "Return", window: int = 20) -> pd.Series:
    return df[return_col].rolling(window=window).std()


def compute_value_at_risk(df: pd.DataFrame, return_col: str = "Return", confidence_level: float = 0.05) -> float:
    return np.percentile(df[return_col], 100 * confidence_level)


def compute_all_metrics(df: pd.DataFrame, return_col: str = "Return", periods_per_year: int = 252, risk_free_rate: float = 0.01) -> dict:
    return {
        "Cumulative Return": compute_cumulative_return(df, return_col),
        "Annualized Return": compute_annualized_return(df, return_col, periods_per_year),
        "Annualized Volatility": compute_annualized_volatility(df, return_col, periods_per_year),
        "Sharpe Ratio": compute_sharpe_ratio(df, return_col, risk_free_rate, periods_per_year),
        "Sortino Ratio": compute_sortino_ratio(df, return_col, risk_free_rate, periods_per_year),
        "Maximum Drawdown": compute_max_drawdown(df, return_col),
        "Calmar Ratio": compute_calmar_ratio(df, return_col, periods_per_year),
        "Value at Risk (5%)": compute_value_at_risk(df, return_col, confidence_level=0.05),
    }
