import datetime
from pathlib import Path

from client.nasdap_data_client import get_all_stocks
from screener.mark_minervini_stock_screener import MarkMinerviniStockScreener

execution_date = datetime.datetime.now()

stocks_df = get_all_stocks()
valid_ticker_stocks_df = stocks_df[stocks_df['symbol'].str.fullmatch('[A-Z]+')]

screeners = [
    MarkMinerviniStockScreener(date=execution_date, stocks_df=valid_ticker_stocks_df)
]

for screener in screeners:
    pre_screened_stocks_df = screener._applied_criteria_stocks_df
    screened_stocks_df = screener.screen()

    directory = "output"
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)

    pre_screened_filename = 'output/{}_pre_screened_stocks_for_{}_at_{}.csv'.format(
        screener.get_screener_name(),
        execution_date.strftime('%Y%m%d'),
        execution_date.strftime('%Y%m%d%H%M%S')
    )
    pre_screened_stocks_df.to_csv(pre_screened_filename)

    filename = 'output/{}_screened_stocks_for_{}_at_{}.csv'.format(
        screener.get_screener_name(),
        execution_date.strftime('%Y%m%d'),
        execution_date.strftime('%Y%m%d%H%M%S')
    )
    screened_stocks_df.to_csv(filename)