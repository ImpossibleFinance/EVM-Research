import pandas as pd

from merge import *
from scripts.Prices import *
from scripts.Avg_transactions import *
from scripts.GMT_hour import *
from scripts.NFT_mints import *
from scripts.Bridges_activity import *


data = merge_data()
price_data = evm_prices()
data_avg_txs = avg_transactions_data()
gmt_hour_data = gmt_data()
nfts_data = nfts_data_load()
data_bridges = bridges_data_load()


if max(pd.read_csv('csv_data/data.csv').index) <= max(data.index):
    data.to_csv('csv_data/data.csv', index = False)

if max(pd.read_csv('csv_data/price_data.csv').index) <= max(price_data.index):
    price_data.to_csv('csv_data/price_data.csv', index = False)

if max(pd.read_csv('csv_data/data_avg_txs.csv').index) <= max(data_avg_txs.index):
    data_avg_txs.to_csv('csv_data/data_avg_txs.csv', index = False)

if max(pd.read_csv('csv_data/gmt_hour_data.csv').index) <= max(gmt_hour_data.index):
    gmt_hour_data.to_csv('csv_data/gmt_hour_data.csv', index = False)

if max(pd.read_csv('csv_data/nfts_data.csv').index) <= max(nfts_data.index):
    nfts_data.to_csv('csv_data/nfts_data.csv', index = False)

if max(pd.read_csv('csv_data/data_bridges.csv').index) <= max(data_bridges.index):
    data_bridges.to_csv('csv_data/data_bridges.csv', index = False)