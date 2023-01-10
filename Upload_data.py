import pandas as pd

from merge import *
from scripts.Prices import *
from scripts.GMT_hour import *
from scripts.NFT_mints import *

from scripts.Stablecoins import *

data = merge_data()
price_data = evm_prices_load()
gmt_hour_data = gmt_data_load()
nfts_data = nfts_data_load()

stable_symbol, stable_type = stablecoins_data_load()

data_name_array = ['data', 'price_data', 'gmt_hour_data', 'nfts_data', 'stable_symbol', 'stable_type']


for name in data_name_array:
    df = (globals()[name])
    try:
        if 'Date(UTC)' in df:
            data_from_file = pd.read_csv('csv_data/' + str(name) + '.csv')

            first_date = (min(df['Date(UTC)']))

            result = pd.concat([data_from_file[data_from_file["Date(UTC)"] <= first_date], df[df["Date(UTC)"] > first_date]], ignore_index=True)
            result.to_csv('csv_data/' + str(name) + '.csv', index = False)

            print("Rewriting CSV with new dates " + name)

        else:
            df.to_csv('csv_data/' + str(name) + '.csv', index = False)
            print("Rewriting whole CSV: " + name)
    except:
        df.to_csv('csv_data/' + str(name) + '.csv', index = False)
        print("Writing new CSV: " + name)