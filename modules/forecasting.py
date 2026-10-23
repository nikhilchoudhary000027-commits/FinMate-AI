"""Monthly expense forecasting: moving-average baseline vs Linear Regression."""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

MIN_MONTHS_FOR_BASELINE = 3
MIN_MONTHS_FOR_MODEL = 12


def make_features(series):
    """series: pandas Series indexed by 'YYYY-MM' strings with monthly totals."""
    df = pd.DataFrame({"y": series.values}, index=series.index)
    for k in (1, 2, 3):
        df[f"lag_{k}"] = df["y"].shift(k)
    df["month_num"] = [int(m[5:7]) for m in df.index]
    return df.dropna()


def baseline_predictions(df):
    """Moving average of the previous three months."""
    return df[["lag_1", "lag_2", "lag_3"]].mean(axis=1)


def evaluate(series, test_fraction=0.2):
    """Chronological split. Returns metrics dict, or None if too little data."""
    if len(series) < MIN_MONTHS_FOR_MODEL:
        return None
    df = make_features(series)
    split = int(len(df) * (1 - test_fraction))
    train, test = df.iloc[:split], df.iloc[split:]
    cols = ["lag_1", "lag_2", "lag_3", "month_num"]

    model = LinearRegression().fit(train[cols], train["y"])
    pred = model.predict(test[cols])
    base = baseline_predictions(test)

    def rmse(a, b):
        return float(np.sqrt(mean_squared_error(a, b)))

    return {
        "train_months": len(train), "test_months": len(test),
        "baseline_mae": mean_absolute_error(test["y"], base),
        "baseline_rmse": rmse(test["y"], base),
        "model_mae": mean_absolute_error(test["y"], pred),
        "model_rmse": rmse(test["y"], pred),
        "test_index": list(test.index),
        "actual": list(test["y"]), "baseline_pred": list(base),
        "model_pred": list(pred), "model": model,
    }


def forecast_next(series):
    """Forecast next month. Returns (value, method) or (None, reason)."""
    n = len(series)
    if n < MIN_MONTHS_FOR_BASELINE:
        return None, "Not enough history (need at least 3 months)."
    if n < MIN_MONTHS_FOR_MODEL:
        return float(series.iloc[-3:].mean()), "preliminary moving average"
    df = make_features(series)
    cols = ["lag_1", "lag_2", "lag_3", "month_num"]
    model = LinearRegression().fit(df[cols], df["y"])
    last = series.iloc[-3:].values
    next_month = (int(series.index[-1][5:7]) % 12) + 1
    x = pd.DataFrame([[last[2], last[1], last[0], next_month]], columns=cols)
    return float(model.predict(x)[0]), "linear regression"