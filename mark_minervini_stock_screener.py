import pandas as pd

from client.yfinnace_data_client import get_stock_historical_price_data
from indicator.moving_average import MovingAverage
from indicator.relative_strength import RelativeStrength


class MarkMinerviniStockScreener:
    def __init__(self, date, stocks_df):
        self.date = date
        self.stocks_df = stocks_df
        self._index_relative_strength = self._calculate_index_relative_strength()
        self._applied_criteria_stocks_df = self._get_applied_criteria_stocks_df()

    def screen(self):
        return self._applied_criteria_stocks_df[self._applied_criteria_stocks_df['is_pass_all_conditions']]

    def _get_applied_criteria_stocks_df(self):
        stock_tickers = self.stocks_df['symbol'].tolist()
        result = []
        print(f'Total {len(stock_tickers)} stocks to screen...')
        for i, stock_ticker in enumerate(stock_tickers):
            try:
                print(f'Screening {stock_ticker}, [{i + 1}] out of [{len(stock_tickers)}]')
                stock_price_data_dict = self.gather_price_data(stock_ticker)
                is_pass_conditions_dict = self.calculate_is_pass_conditions_dict(stock_price_data_dict)
                combine_dict = stock_price_data_dict | is_pass_conditions_dict
                result.append(combine_dict)
            except Exception as e:
                print('Skip due to exception', e)
        return pd.DataFrame(result)

    def gather_price_data(self, stock_ticker):
        historical_price_data_df = get_stock_historical_price_data(date=self.date, stock_ticker=stock_ticker)
        ma = MovingAverage(historical_price_data_df)
        rs = RelativeStrength(historical_price_data_df)

        stock_price_data_dict = {
            'stock_ticker': stock_ticker,
            'price': round(historical_price_data_df["adjusted_close"][-1], 2),
            'sma_50': ma.sma_50,
            'sma_150': ma.sma_150,
            'sma_200': ma.sma_200,
            'sma_200_20_days_before': ma.get_sma_in_the_past(200, 20),
            'low_of_52_weeks': round(historical_price_data_df["adjusted_close"][-260:].min(), 2),
            'high_of_52_weeks': round(historical_price_data_df["adjusted_close"][-260:].max(), 2),
            'rs_rating': RelativeStrength.calculate_rs_rating(rs.relative_strength, self._index_relative_strength)
        }
        return stock_price_data_dict

    def is_pass_condition_1(self, stock_price_data):
        # Condition 1: Current Price > 150 SMA and > 200 SMA
        return (stock_price_data['price'] > stock_price_data['sma_150'] and
                stock_price_data['price'] > stock_price_data['sma_200'])

    def is_pass_condition_2(self, stock_price_data):
        # Condition 2: 150 SMA and > 200 SMA
        return stock_price_data['sma_150'] > stock_price_data['sma_200']

    def is_pass_condition_3(self, stock_price_data):
        # Condition 3: 200 SMA trending up for at least 1 month (ideally 4-5 months)
        # TODO add logic
        return stock_price_data['sma_200'] > stock_price_data['sma_200_20_days_before']

    def is_pass_condition_4(self, stock_price_data):
        # Condition 4: 50 SMA> 150 SMA and 50 SMA> 200 SMA
        return stock_price_data['sma_50'] > stock_price_data['sma_150'] > stock_price_data['sma_200']

    def is_pass_condition_5(self, stock_price_data):
        # Condition 5: Current Price > 50 SMA
        return stock_price_data['price'] > stock_price_data['sma_50']

    def is_pass_condition_6(self, stock_price_data):
        # Condition 6: Current Price is at least 30% above 52 week low (Many of the best are up 100-300% before coming out of consolidation)
        return stock_price_data['price'] >= (stock_price_data['low_of_52_weeks'] * 1.3)

    def is_pass_condition_7(self, stock_price_data):
        # Condition 7: Current Price is within 25% of 52 week high
        return stock_price_data['price'] >= (stock_price_data['high_of_52_weeks'] * 0.75)

    def is_pass_condition_8(self, stock_price_data):
        # Condiction 8: IBD RS_Rating greater than 70
        return stock_price_data['rs_rating'] > 70

    def is_pass_all_conditions(self, stock_price_data):
        return all(
            [self.is_pass_condition_1(stock_price_data),
             self.is_pass_condition_2(stock_price_data),
             self.is_pass_condition_3(stock_price_data),
             self.is_pass_condition_4(stock_price_data),
             self.is_pass_condition_5(stock_price_data),
             self.is_pass_condition_6(stock_price_data),
             self.is_pass_condition_7(stock_price_data),
             self.is_pass_condition_8(stock_price_data)]
        )

    def calculate_is_pass_conditions_dict(self, stock_price_data_dict):
        return {
            'is_pass_condition_1': self.is_pass_condition_1(stock_price_data_dict),
            'is_pass_condition_2': self.is_pass_condition_2(stock_price_data_dict),
            'is_pass_condition_3': self.is_pass_condition_3(stock_price_data_dict),
            'is_pass_condition_4': self.is_pass_condition_4(stock_price_data_dict),
            'is_pass_condition_5': self.is_pass_condition_5(stock_price_data_dict),
            'is_pass_condition_6': self.is_pass_condition_6(stock_price_data_dict),
            'is_pass_condition_7': self.is_pass_condition_7(stock_price_data_dict),
            'is_pass_condition_8': self.is_pass_condition_8(stock_price_data_dict),
            'is_pass_all_conditions': self.is_pass_all_conditions(stock_price_data_dict)
        }

    def _calculate_index_relative_strength(self):
        index_price_data = get_stock_historical_price_data(date=self.date, stock_ticker='VOO')
        index_rs = RelativeStrength(index_price_data)
        return index_rs.calculate_relative_strength()
