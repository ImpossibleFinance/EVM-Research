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

data_name_array = ['data', 'price_data', 'data_avg_txs', 'gmt_hour_data', 'nfts_data', 'data_bridges', 'stable_symbol', 'stable_type', 'solana_data']

for name in data_name_array:
    try:
        if max(pd.read_csv('csv_data/' + str(name) + '.csv').index) <= (max((globals()[name]).index)):
            print("Rewriting old CSV " + name)
            (globals()[name]).to_csv('csv_data/' + str(name) + '.csv', index = False)
        else:
            print("Someting wrong with " + name)
    except:
        (globals()[name]).to_csv('csv_data/' + str(name) + '.csv', index = False)
        print("Writing new CSV: " + name)