import pandas as pd

from indicator.trend import Trend


class MovingAverage:
    ma_values = [50, 150, 200]

    def __init__(self, stock_price_df):
        self._stock_price_df = stock_price_df
        self._sma_df = self._calculate_sma()
        self.sma_50 = self._sma_df["50"][-1]
        self.sma_150 = self._sma_df["150"][-1]
        self.sma_200 = self._sma_df["200"][-1]

    def _calculate_sma(self):
        sma_dict = {}
        for x in self.ma_values:
            sma_dict[str(x)] = round(self._stock_price_df['adjusted_close'].rolling(window=x).mean(), 2)
        return pd.DataFrame.from_dict(sma_dict)

    def get_sma_in_the_past(self, sma_day_x, n_days_before):
        try:
            sma_x_on_n_days_before = self._sma_df[str(sma_day_x)][-n_days_before]
        except Exception:
            sma_x_on_n_days_before = 0
        return sma_x_on_n_days_before

    def get_sma_df(self, sma_day):
        return self._sma_df[str(sma_day)]