import datetime

from client.nasdap_data_client import get_all_stocks
from mark_minervini_stock_screener import MarkMinerviniStockScreener

execution_date = datetime.datetime.now()

stocks_df = get_all_stocks()
valid_ticker_stocks_df = stocks_df[stocks_df['symbol'].str.fullmatch('[A-Z]+')]
# screener = MarkMinerviniStockScreener(date=execution_date, stocks_df=stocks_df.head(1))
screener = MarkMinerviniStockScreener(date=execution_date, stocks_df=stocks_df)
pre_screened_stocks_df = screener._applied_criteria_stocks_df
screened_stocks_df = screener.screen()

pre_screened_filename = 'pre_screened_stocks_for_{}_at_{}.csv'.format(
    execution_date.strftime('%Y%m%d'),
    execution_date.strftime('%Y%m%d%H%M%S')
)
pre_screened_stocks_df.to_csv(pre_screened_filename)

filename = 'screened_stocks_for_{}_at_{}.csv'.format(
    execution_date.strftime('%Y%m%d'),
    execution_date.strftime('%Y%m%d%H%M%S')
)
screened_stocks_df.to_csv(filename)