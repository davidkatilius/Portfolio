import pandas as pd
import os
import json
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from time import time, sleep

def api_runner():
    global df
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
      'start':'1',
      'limit':'50',
      'convert':'USD'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': 'bb5fc193-7d23-4a9b-8a42-d26b4a881b92',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        #print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
        
    df = pd.json_normalize(data['data'])
    df['timestamp'] = pd.to_datetime('now',utc=True)
    
    if not os.path.isfile(r'..\CoinMarketCap_API.csv'):
        df.to_csv(r'C:\Users\katil\Documents\Python\CoinMarketCapAPI\raw_data.csv',header='column_names')
    else:
        df.to_csv(r'C:\Users\katil\Documents\Python\CoinMarketCapAPI\raw_data.csv',mode='a',header=False)

api_runner()
