from dotenv import load_dotenv
import os
import json
import requests
import pandas as pd
import time
import datetime
import sys
from tqdm import tqdm

from dune_client.types import QueryParameter
from dune_client.client import DuneClient
from dune_client.query import Query


class Upload():
    def __init__(self, num_of_days, path):

        self.BASE_PATH = path

        load_dotenv()
        self.API_KEY_DUNE = os.getenv('DUNE_API_KEY')

        f = open(self.make_global_path('config/chains_config.json'))
        self.token_contracts = json.load(f)
        f.close()

        f2 = open(self.make_global_path('config/requests_config.json'))
        self.requests_config = json.load(f2)
        f2.close()


        self.end_date = datetime.datetime.today().strftime('%Y-%m-%d') + ' 00:00:00'
        self.start_date = (datetime.datetime.today() - datetime.timedelta(int(num_of_days))).strftime('%Y-%m-%d') + ' 00:00:00'
    
    
    def make_global_path(self,link):

        if self.BASE_PATH != '':
            return self.BASE_PATH + '/' + str(link)
        else:
            return link

    def get_price(self, token):
        url = 'https://api.coingecko.com/api/v3/coins/'+ token +'/market_chart'

        params = {
            'vs_currency': 'usd',
            'days': 'max',
            'interval': 'daily'
        }

        response = requests.get(url, params=params)

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

        print("-"*80)
        print("Prices are uploading:")
        print("-"*80)

        for item in tqdm(self.token_contracts):

            token = str(item['coingecko_tag'])

            file_path = self.make_global_path('data/Prices.csv') #'data/Prices.csv'

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

                data.to_csv(file_path, index = False)

                time.sleep(0.5)


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

    def data_by_url(self, internal_url, name): #### <=== Data #2-4

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

        #print("Results available at", query.url())

        dune = DuneClient(self.API_KEY_DUNE)
        results = dune.refresh(query)


        df = self.convert_Dune_to_DF(results)

        file_path = self.make_global_path('data') + '/'

        if name == 'data':
            df['DATE'] = (df['DATE'].str).replace(' 00:00:00.000 UTC','T00:00:00Z')
            df = df.rename(columns = {"DATE": "Date(UTC)", "VALUE": "Value", "ADDRESSES": "Active addresses", "BLOCK_TIME": "Block time", "BLOCKS_COUNT": "Blocks count"})
            df = df.sort_values(by = ['Date(UTC)'])
            df = df.reset_index(drop = True)


            first_date = (min(df['Date(UTC)']))

            try:
                if 'Date(UTC)' in df:
                    data_from_file = pd.read_csv(file_path + str(name) + '.csv')

                    result = pd.concat([data_from_file[data_from_file["Date(UTC)"] < first_date], df[df["Date(UTC)"] >= first_date]], ignore_index = True)
                    result.to_csv(file_path + str(name) + '.csv', index = False)

                    print("Rewriting CSV with new dates " + name)

                else:
                    df.to_csv(file_path + str(name) + '.csv', index = False)
                    print("Rewriting whole CSV: " + name)
            except:
                df.to_csv(file_path + str(name) + '.csv', index = False)
                print("Writing new CSV: " + name)
        else:
            df.to_csv(file_path + str(name) + '.csv', index = False)

    def upload_data(self, name):
        for item in self.requests_config:
            if item['api_name'] == 'Main info' and name == 'data':

                print("-"*80)
                print("Main data is uploading")
                print("-"*80)


                url = str(item['dune_id'])
                self.data_by_url(url, item['file_name'])
            elif item['api_name'] == 'GMT Hour' and name == 'gmt':

                print("-"*80)
                print("GMT Hour is uploading")
                print("-"*80)

                url = str(item['dune_id'])
                self.data_by_url(url, item['file_name'])

            elif item['api_name'] == 'Total Wallets' and name == 'wallets':

                print("-"*80)
                print("Wallets is uploading")
                print("-"*80)


                url = str(item['dune_id'])
                self.data_by_url(url, item['file_name'])

num_of_days = int(sys.argv[1])

set = str(sys.argv[2])

print("Number of days: ", num_of_days)

if set == 'dev':
    load_dotenv()
    path = os.getenv('GLOBAL_PATH')
else:
    path = ''

upload = Upload(num_of_days, path)

upload.upload_prices()

datas_array = ['data', 'gmt', 'wallets']

for datas in datas_array:
    upload.upload_data(datas)