def get_sector(yf_ticker):
    print('info: ', yf_ticker.info)
    return yf_ticker.info['sector']


def get_industry(yf_ticker):
    return yf_ticker.info['industry']
