import pandas as pd
import requests
import json

import os
from dotenv import load_dotenv


def query(url):
    if url == "Transactions":
        return """
            {
                records {
                    date,
                    chain,
                    VALUE
                }
            }
        """

    if url == "Addresses":
        return """
            {
                records {
                    date,
                    chain,
                    ADDRESSES
                }
            }
        """

    if url == "Blocks":
        return """
            {
                records {
                    date,
                    chain,
                    BLOCK_TIME,
                    BLOCKS_COUNT
                }
            }
        """

    if url == "GMT Hour":
        return """
            {
                records {
                    GMT_HOUR,
                    Chain,
                    AVG_TXS_COUNT
                }
            }
        """
    if url == "Distribution by time and chain":
        return """
            {
                records {
                    Chain,
                    Value_1M,
                    Value_3M,
                    Value_6M,
                    Value_1Y
                }
            }
        """


def data_by_url(internal_url, api_name):

    load_dotenv()
    API_KEY = os.getenv('API_KEY_ZETTA_BLOCK')
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