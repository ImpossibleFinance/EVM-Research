import pandas as pd
import json


from Data_API import *

def merge_data():
    data  = pd.DataFrame()

    f = open('chains_config.json')
    chains_config = json.load(f)
    chains = []
    for x in chains_config:
        chains.append(x['chain_name'])


    for chain in chains:
        data = pd.concat([data, data_by_url((list(filter(lambda x:x["chain_name"] == chain, chains_config)))[0]["chains_api"])])

    data = data.reset_index(drop=True)
    
    data = data.rename(columns = {"DATE": "Date(UTC)", "VALUE": "Value", "CHAIN": "Chain", "ADDRESSES": "Active addresses", "BLOCK_TIME": "Block time", "BLOCKS_COUNT": "Blocks count"})

    return data
