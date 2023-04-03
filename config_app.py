import pandas as pd
import json


from scripts.Functions import *



##############################################################################
############################# DATA ###########################################
##############################################################################


data = pd.DataFrame()
Prices = pd.DataFrame()
gmt_hour_data = pd.DataFrame()
stablecoins = pd.DataFrame()
wallets = pd.DataFrame()

data_name_array = ['data', 'Prices', 'wallets', 'gmt_hour_data', 'stablecoins']

for name in data_name_array:
    (globals()[name]) = read_data_from_csv('data/' + str(name) + '.csv')

chains = ['Ethereum', 'Polygon', 'BNB Chain', 'Avalanche', 'Gnosis Chain', 'Optimism', 'Arbitrum', 'Fantom']

tokens = ['Ethereum (ETH)', 'Binance (BNB)', 'Polygon (MATIC)', 'Avalanche (AVAX)', 'Fantom (FTM)', 'Optimism (OP)', 'Arbitrum (ARB)']

##############################################################################
########################## Page configs ######################################
##############################################################################


config = {
    'displayModeBar': False
}

dropdown_style = {
    'display': 'inline-flex', 
    'align-items': 'center', 
    'justify-content': 'center'
}

file_chain = open('config/chains_config.json')
chains_config = json.load(file_chain)
file_chain.close()

dropdown_ico_size = 11

dropdown_options = [
    {
        "label": html.Span([
            html.Img(src = "assets/" + item.lower() + ".png", height = dropdown_ico_size),
            html.Span(item, className = "main-chains-selection"),
        ], style = dropdown_style
        ),
        "value": item,
    } for item in chains
]

dropdown_options_date_range = [
    {
        "label": html.Span([
            html.Span(('Last ' + dates + ' days'), className = "main-chains-selection")
        ], style = dropdown_style
        ),
        "value": dates,
    } for dates in ['30', '90', '180']
]

dropdown_options_date_range.append(
    {
        "label": html.Span([
            html.Span(('All'), className = "main-chains-selection")
        ], style = dropdown_style
        ),
        "value": 'All',
    }
)

dropdown_options_tokens = [
    {
        "label": html.Span([
            html.Span(token, className = "main-chains-selection"),
        ], style = dropdown_style
        ),
        "value": token,
    } for token in tokens
]