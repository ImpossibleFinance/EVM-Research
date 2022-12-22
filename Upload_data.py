import pandas as pd

from merge import *
from scripts.Prices import *
from scripts.Avg_transactions import *
from scripts.GMT_hour import *
from scripts.NFT_mints import *
from scripts.Bridges_activity import *

from scripts.Stablecoins import *

from scripts.Solana import *

data = merge_data()
price_data = evm_prices()
data_avg_txs = avg_transactions_data()
gmt_hour_data = gmt_data()
nfts_data = nfts_data_load()
data_bridges = bridges_data_load()

stable_symbol, stable_type = stablecoins_data()

solana_data = solana_upload()

try:
    if max(pd.read_csv('csv_data/data.csv').index) <= max(data.index):
        data.to_csv('csv_data/data.csv', index = False)
except:
    data.to_csv('csv_data/data.csv', index = False)


try:
    if max(pd.read_csv('csv_data/price_data.csv').index) <= max(price_data.index):
        price_data.to_csv('csv_data/price_data.csv', index = False)
except:
    price_data.to_csv('csv_data/price_data.csv', index = False)

try:
    if max(pd.read_csv('csv_data/data_avg_txs.csv').index) <= max(data_avg_txs.index):
        data_avg_txs.to_csv('csv_data/data_avg_txs.csv', index = False)
except:
    data_avg_txs.to_csv('csv_data/data_avg_txs.csv', index = False)

try:
    if max(pd.read_csv('csv_data/gmt_hour_data.csv').index) <= max(gmt_hour_data.index):
        gmt_hour_data.to_csv('csv_data/gmt_hour_data.csv', index = False)
except:
    gmt_hour_data.to_csv('csv_data/gmt_hour_data.csv', index = False)


try:
    if max(pd.read_csv('csv_data/nfts_data.csv').index) <= max(nfts_data.index):
        nfts_data.to_csv('csv_data/nfts_data.csv', index = False)
except:
    nfts_data.to_csv('csv_data/nfts_data.csv', index = False)

try:
    if max(pd.read_csv('csv_data/data_bridges.csv').index) <= max(data_bridges.index):
        data_bridges.to_csv('csv_data/data_bridges.csv', index = False)
except:
    data_bridges.to_csv('csv_data/data_bridges.csv', index = False)
    


try:
    if max(pd.read_csv('csv_data/stable_symbol.csv').index) <= max(stable_symbol.index):
        stable_symbol.to_csv('csv_data/stable_symbol.csv', index = False)
except:
    stable_symbol.to_csv('csv_data/stable_symbol.csv', index = False)

try:
    if max(pd.read_csv('csv_data/stable_type.csv').index) <= max(stable_type.index):
        stable_type.to_csv('csv_data/stable_type.csv', index = False)
except:
    stable_type.to_csv('csv_data/stable_type.csv', index = False)




try:
    if max(pd.read_csv('csv_data/solana_data.csv').index) <= max(solana_data.index):
        solana_data.to_csv('csv_data/solana_data.csv', index = False)
except:
    solana_data.to_csv('csv_data/solana_data.csv', index = False)