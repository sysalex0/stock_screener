import numpy as np
from sklearn.linear_model import LinearRegression

class Trend:
    def __init__(self, time_price_df):
        self._time_metric_series = time_price_df.dropna()

    def is_up(self, days):
        time = self._time_metric_series.index.values
        price = self._time_metric_series.values

        time = time.reshape(len(time), 1)

        x = time[-days:]
        y = price[-days:]
        model = LinearRegression()
        model.fit(x, y)

        slope = model.coef_[0] if model.coef_ else 0
        return slope > 0