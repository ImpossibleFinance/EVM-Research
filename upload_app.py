from dotenv import load_dotenv
import os
import json
import requests
import pandas as pd
import time
import datetime

from dune_client.types import QueryParameter
from dune_client.client import DuneClient
from dune_client.query import Query


class Upload():
    def __init__(self):

        load_dotenv()
        self.API_KEY_DUNE = os.getenv('DUNE_API_KEY')

        f = open('config/chains_config.json')
        self.token_contracts = json.load(f)
        f.close()

        f2 = open('config/requests_config.json')
        self.requests_config = json.load(f2)
        f2.close()


        self.end_date = datetime.datetime.today().strftime('%Y-%m-%d') + ' 00:00:00'
        self.start_date = (datetime.datetime.today() - datetime.timedelta(14)).strftime('%Y-%m-%d') + ' 00:00:00'

    def get_price(self, token):
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
    
    def upload_prices(self): #### <=== Data #1

        k = 0
        for item in self.token_contracts:

            print(str(k) + '/' + str(len(self.token_contracts)))

            token = str(item['coingecko_tag'])

            file_path = 'data/Prices.csv'

            if os.stat(file_path).st_size == 0 or os.stat(file_path).st_size == 1:
                csv_data = pd.DataFrame()
                existing_tokens = []
            else:
                csv_data = pd.read_csv(file_path)
                existing_tokens = csv_data['TOKEN'].unique()


            if token not in existing_tokens and token != '-':
                price_data = self.get_price(token)
                price_data['TOKEN'] = str(item['token'])
                data = pd.concat([csv_data, price_data])

                data.to_csv('data/Prices.csv', index = False)

                time.sleep(0.5)


            k += 1


    def convert_Dune_to_DF(self, results):
        str_results = str(results).replace('ResultsResponse(', '')
        str_results = str_results[str_results.find('result=ExecutionResult(rows='):].replace('result=ExecutionResult(rows=[', '')
        str_remove_results = str_results[str_results.find('], metadata=ResultMetadata(column_names='):]
        str_results = str_results.replace(str_remove_results, '')
        
        string_value = "[" + str_results + "]"
        
        string_value = string_value.replace("'", "\"")
        
        json_data = json.loads(string_value)
        
        df = pd.DataFrame(json_data)
        
        print('Here is new data:')
        print(df)
        return df

    def data_by_url(self, internal_url, name):

        if name == 'data':
            data_params = [    
                QueryParameter.date_type(name = "Start Date", value = self.start_date),
                QueryParameter.date_type(name = "End Date", value = self.end_date),
            ]
        else:
            data_params = []


        query = Query(
            name = "Sample Query",
            query_id = int(internal_url),
            params = data_params
        )

        print("Results available at", query.url())

        dune = DuneClient(self.API_KEY_DUNE)
        results = dune.refresh(query)


        df = self.convert_Dune_to_DF(results)

        if name == 'data':
            df['DATE'] = (df['DATE'].str).replace(' 00:00:00.000 UTC','T00:00:00Z')
            df = df.rename(columns = {"DATE": "Date(UTC)", "VALUE": "Value", "ADDRESSES": "Active addresses", "BLOCK_TIME": "Block time", "BLOCKS_COUNT": "Blocks count"})
            df = df.sort_values(by = ['Date(UTC)'])
            df = df.reset_index(drop = True)


            first_date = (min(df['Date(UTC)']))

            try:
                if 'Date(UTC)' in df:
                    data_from_file = pd.read_csv('data/' + str(name) + '.csv')

                    result = pd.concat([data_from_file[data_from_file["Date(UTC)"] < first_date], df[df["Date(UTC)"] >= first_date]], ignore_index = True)
                    result.to_csv('data/' + str(name) + '.csv', index = False)

                    print("Rewriting CSV with new dates " + name)

                else:
                    df.to_csv('data/' + str(name) + '.csv', index = False)
                    print("Rewriting whole CSV: " + name)
            except:
                df.to_csv('data/' + str(name) + '.csv', index = False)
                print("Writing new CSV: " + name)
        else:
            df.to_csv('data/' + str(name) + '.csv', index = False)

    def upload_data(self, name):
        for item in self.requests_config:
            if item['api_name'] == 'Main info' and name == 'data':
                url = str(item['dune_id'])
                self.data_by_url(url, item['file_name'])
            elif item['api_name'] == 'GMT Hour' and name == 'gmt':
                url = str(item['dune_id'])
                self.data_by_url(url, item['file_name'])

            elif item['api_name'] == 'Total Wallets' and name == 'wallets':
                url = str(item['dune_id'])
                self.data_by_url(url, item['file_name'])


upload = Upload()


upload.upload_prices()
upload.upload_data()