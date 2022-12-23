import pandas as pd
import json
import numpy as np

from scripts.Data_API import *

def merge_data():
    data  = pd.DataFrame()

    f = open('requests_config.json')
    api_config = json.load(f)

    for x in api_config:
        if x['api_name'] == 'Main info':
            data = data_by_url(x['zettablock_api'], x['api_name'])
    data = data.sort_values(by=['Date(UTC)'])
    data = data.reset_index(drop=True)
    data = data.rename(columns = {"VALUE": "Value", "ADDRESSES": "Active addresses", "BLOCK_TIME": "Block time", "BLOCKS_COUNT": "Blocks count"})


    data = data.replace(np.nan, 0)
    return data
