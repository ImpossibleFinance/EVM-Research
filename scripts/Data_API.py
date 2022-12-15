import pandas as pd
import requests
import json

import os
#from dotenv import load_dotenv


def query(url):

    path = 'scripts/graphql/' + str(url) + ".graphql"
    with open(path) as f:
        return (f.read())

def data_by_url(internal_url, api_name):

    #load_dotenv()
    #API_KEY = os.getenv('API_KEY_ZETTA_BLOCK')

    API_KEY = os.environ['API_KEY_ZETTA_BLOCK']

    _query = query(api_name)

    headers = {'X-API-KEY': API_KEY}

    data = {'query': _query}
    r = requests.post(internal_url, headers = headers, data = json.dumps(data)).text
    json_object = json.loads(r)
    df = pd.DataFrame.from_dict(json_object['data']['records'])

    if 'chain' in df:
        df = df.rename(columns = {"chain": "CHAIN"})

    if 'date' in df:
        df = df.rename(columns = {"date": "DATE"})
    if 'DATE' in df:
        df['DATE'] = pd.to_datetime(pd.to_datetime(df['DATE']).dt.strftime('%Y-%m-%d'))



    print(1) # calculate requests count
    return df