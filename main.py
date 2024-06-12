import datetime

from client.nasdap_data_client import get_all_stocks
from screener.mark_minervini_stock_screener import MarkMinerviniStockScreener
from service.file_service import create_directory_if_not_exist

execution_date = datetime.datetime.now()

stocks_df = get_all_stocks()
valid_ticker_stocks_df = stocks_df[stocks_df['symbol'].str.fullmatch('[A-Z]+')]

screener = MarkMinerviniStockScreener(date=execution_date, stocks_df=valid_ticker_stocks_df)

screened_stocks_df = screener.screen()

pre_screened_stocks_df = screener._applied_criteria_stocks_df
pre_screened_filename = 'output/criteria/{}_pre_screened_stocks_for_{}_at_{}.csv'.format(
screener.get_screener_name(),
execution_date.strftime('%Y%m%d'),
execution_date.strftime('%Y%m%d%H%M%S')
)
create_directory_if_not_exist(pre_screened_filename)
pre_screened_stocks_df.to_csv(pre_screened_filename, index=False)

screened_stocks_filename = 'output/{}_screened_stocks_for_{}_at_{}.csv'.format(
screener.get_screener_name(),
execution_date.strftime('%Y%m%d'),
execution_date.strftime('%Y%m%d%H%M%S')
)
create_directory_if_not_exist(screened_stocks_filename)
screened_stocks_df.to_csv(screened_stocks_filename, index=False)
