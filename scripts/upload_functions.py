
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

def upload_prices(): #### <===
    f = open('config/chains_config.json')
    token_contracts = json.load(f)
    f.close()

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

def data_by_url(internal_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
    }


    url = 'https://node-api.flipsidecrypto.com/api/v2/queries/' + internal_url
    r = requests.get(url, headers=headers).text
    json_object = json.loads(r)
    df = pd.DataFrame.from_dict(json_object)

    if 'Date(UTC)' in df:
        df['Date(UTC)'] = pd.to_datetime(df["Date(UTC)"])

    return df

def upload_data(): ## <====

    f = open('config/requests_config.json')
    requests_config = json.load(f)
    f.close()

    for item in requests_config:
        if item['api_name'] == 'Main info':
            url = str(item['flipside_api'])

    df = data_by_url(url)
    df = df.rename(columns = {"DATE": "Date(UTC)", "VALUE": "Value", "ADDRESSES": "Active addresses", "BLOCK_TIME": "Block time", "BLOCKS_COUNT": "Blocks count"})
    df = df.sort_values(by=['Date(UTC)'])
    df = df.reset_index(drop = True)

    df['Date(UTC)'] = (df['Date(UTC)'].str).replace(' 00:00:00.000','T00:00:00Z')
    first_date = (min(df['Date(UTC)']))
    name = 'data'

    print(df)

    try:
        if 'Date(UTC)' in df:
            data_from_file = pd.read_csv('data/' + str(name) + '.csv')

            #first_date = (min(df['Date(UTC)']))

            result = pd.concat([data_from_file[data_from_file["Date(UTC)"] < first_date], df[df["Date(UTC)"] >= first_date]], ignore_index = True)
            result.to_csv('data/' + str(name) + '.csv', index = False)

            print("Rewriting CSV with new dates " + name)

        else:
            df.to_csv('data/' + str(name) + '.csv', index = False)
            print("Rewriting whole CSV: " + name)
    except:
        df.to_csv('data/' + str(name) + '.csv', index = False)
        print("Writing new CSV: " + name)



def upload_gmt_data(): ## <====

    f = open('config/requests_config.json')
    requests_config = json.load(f)
    f.close()

    for item in requests_config:
        if item['api_name'] == 'GMT Hour':
            url = str(item['flipside_api'])

    df = data_by_url(url)
    df = df.sort_values(by=['RANGE'])
    df = df.reset_index(drop = True)

    print(df)
    
    df.to_csv('data/gmt_hour_data.csv', index = False)
    

def upload_wallets_count(): ## <====

    f = open('config/requests_config.json')
    requests_config = json.load(f)
    f.close()

    for item in requests_config:
        if item['api_name'] == 'Total Wallets':
            url = str(item['flipside_api'])

    df = data_by_url(url)

    print(df)
    
    df.to_csv('data/wallets.csv', index = False)