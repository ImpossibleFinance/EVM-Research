
import json
import requests
import pandas as pd
import os
import time

def get_price(token):
    url = 'https://api.coingecko.com/api/v3/coins/'+ token +'/market_chart'
    params = {
        'vs_currency': 'usd',
        'days': 'max',
        'interval': 'daily'
    }

    response = requests.get(url, params=params)
    print(token)
    data = response.json()
    data = pd.DataFrame(data['prices'], columns=['Uni_time', 'PRICE'])

    data['Date(UTC)'] = pd.to_datetime(data['Uni_time']/1000, unit = 's')
    data = data.sort_values(by = ['Date(UTC)'], ascending = True)

    data = data.drop(['Uni_time'], axis = 1)

    if (str(data['Date(UTC)'][data['Date(UTC)'].idxmax()])).split(' ')[1] != '00:00:00':
        data = data[:-1]

    data['Date(UTC)'] = (data['Date(UTC)']).replace(' 00:00:00','')

    return data

def upload_prices():
    f = open('config/chains_config.json')
    token_contracts = json.load(f)

    k = 0
    for item in token_contracts:

        print(str(k) + '/' + str(len(token_contracts)))

        token = str(item['coingecko_tag'])

        file_path = 'data/Prices.csv'

        if os.stat(file_path).st_size == 0 or os.stat(file_path).st_size == 1:
            csv_data = pd.DataFrame()
            existing_tokens = []
        else:
            csv_data = pd.read_csv(file_path)
            existing_tokens = csv_data['TOKEN'].unique()


        if token not in existing_tokens and token != '-':
            price_data = get_price(token)
            price_data['TOKEN'] = str(item['token'])
            data = pd.concat([csv_data, price_data])

            data.to_csv('data/Prices.csv', index = False)

            time.sleep(0.5)


        k += 1

upload_prices()