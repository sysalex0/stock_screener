class RelativeStrength:
    def __init__(self, stock_price_df):
        self._stock_price_df = stock_price_df
        self.relative_strength = self.calculate_relative_strength()

    @staticmethod
    def calculate_rs_rating(stock_rs_strange_value, index_rs_strange_value):
        return round(100 * (stock_rs_strange_value / index_rs_strange_value),2)

    def calculate_relative_strength(self):
        ## relative gain and losses
        self._stock_price_df['close_shift'] = self._stock_price_df['adjusted_close'].shift(1)

        ## Gains (true) and Losses (False)
        self._stock_price_df['gains'] = self._stock_price_df.apply(
            lambda x: x['adjusted_close'] if x['adjusted_close'] >= x['close_shift'] else 0, axis=1)
        self._stock_price_df['loss'] = self._stock_price_df.apply(
            lambda x: x['adjusted_close'] if x['adjusted_close'] <= x['close_shift'] else 0, axis=1)

        avg_gain = self._stock_price_df['gains'].mean()
        avg_losses = self._stock_price_df['loss'].mean()

        # remove intermediate column
        self._stock_price_df = self._stock_price_df.drop('close_shift', axis=1)
        self._stock_price_df = self._stock_price_df.drop('gains', axis=1)
        self._stock_price_df = self._stock_price_df.drop('loss', axis=1)

        return round(avg_gain / avg_losses, 2)
