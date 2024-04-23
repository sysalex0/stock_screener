import requests
import pandas as pd

url = "https://api.nasdaq.com/api/screener/stocks?download=true"


def get_all_stocks():
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.7',
        'origin': 'https://www.nasdaq.com',
        'priority': 'u=1, i',
        'referer': 'https://www.nasdaq.com/',
        'sec-ch-ua': '"Chromium";v="124", "Brave";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }
    response = requests.request("GET", url, headers=headers)

    json_data = response.json()
    stocks = json_data['data']['rows']
    return pd.DataFrame.from_dict(stocks)