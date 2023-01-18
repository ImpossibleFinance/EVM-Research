from dash import Dash, html, dcc, dash_table, callback_context
from dash.dependencies import Input, Output
import flask

from scripts.Transactions import *
from scripts.Active_addresses import *
from scripts.Blocks import *
from scripts.GMT_hour import *
from scripts.Main_table import *
from scripts.NFT_mints import *
from scripts.Prices import *
from scripts.Stablecoins import *


def read_data(name):
    df = pd.read_csv('csv_data/' + str(name) + '.csv')

    if 'DATE' in df:
        df['DATE'] = pd.to_datetime(pd.to_datetime(df['DATE']).dt.strftime('%Y-%m-%d'))
    
    if 'Date(UTC)' in df:
        df['Date(UTC)'] = pd.to_datetime(pd.to_datetime(df['Date(UTC)']).dt.strftime('%Y-%m-%d'))
    
    return df

data_name_array = ['data', 'price_data', 'gmt_hour_data', 'nfts_data', 'stablecoins']

for name in data_name_array:
    (globals()[name]) = read_data(str(name))

#### Load data

table_data, last_date = table_data(data)
fig_txs, txs_histogram, txs_total = transactions(data)
fig_addresses, fig_addresses_distribution = active_addresses(data)
block_time, blocks_count = blocks(data)

avg_tx_by_chain = transactions_by_chain_by_time(data)

fig_gmt_distribution = gmt_hour(gmt_hour_data)

nft_mint = nft_mints(nfts_data)

stablecoins_chart, stablecoins_stats, stablecoins_MA90_volume, stablecoins_MA90_share, stablecoins_Agg_transfers = stablecoins_charts(stablecoins)


####

last_date = (str(last_date).split(" "))[0]

fig_gmt_distribution.update_layout(clickmode = 'event+select')


server = flask.Flask(__name__)

app = Dash(__name__, server = server)


app.title = 'EVM Dashboard'


app.layout = html.Div(children=[
    html.Div(
        children = [
            html.Div([
                html.Img(src = "assets/IF.png", alt = " ", className = "if-ico"),
                html.H1(
                    ' EVM Blockchains Analysis (Open Beta V 0.3)', 
                ),
            ],
            className = "header-title"
            ),
            html.H2([
                html.Span("Built by"),
                html.Span(" Impossible Research ", className="header-description-if"),
                html.Span("team")
                ],
                className = "header-description"
                
            ),
            html.H2([
                html.Span("The analysis is a comparison of activity on EVM blockchains, including metrics such as daily transactions, active addresses, as well as average block creation time and daily block count."),
                html.Span(" Impossible Finance ", className="description-if-and-zb"),
                html.Span("team has collected the most interesting metrics for you using"),
                html.Span(" Dune API ", className="description-if-and-zb"),
                ],
                className = "description-main"
            ),
        ],
    ),

    html.Div( children = [
    html.H1('Before you begin, please select the chains you wish to review:', className = "price-description"),
    #html.P('This choice will affect all of the charts in the 1st part except the Interactive table and Distribution by GMT Hour chart', className = "price-description"),

    dcc.Dropdown(
        [
            {
                "label": html.Span(
                    [
                        html.Img(src = "assets/ethereum.png", height = 15),
                        html.Span("Ethereum", className = "main-chains-selection"),
                    ], style={'display': 'inline-flex', 'align-items': 'center', 'justify-content': 'center'}
                ),
                "value": "Ethereum",
            },

            {
                "label": html.Span(
                    [
                        html.Img(src = "assets/polygon.png", height = 15),
                        html.Span("Polygon", className = "main-chains-selection"),
                    ], style={'display': 'inline-flex', 'align-items': 'center', 'justify-content': 'center'}
                ),
                "value": "Polygon",
            },

            {
                "label": html.Span(
                    [
                        html.Img(src = "assets/bnb.png", height = 15),
                        html.Span("BNB Chain", className = "main-chains-selection"),
                    ], style={'display': 'inline-flex', 'align-items': 'center', 'justify-content': 'center'}
                ),
                "value": "BNB Chain",
            },

            {
                "label": html.Span(
                    [
                        html.Img(src = "assets/avalanche.png", height = 15),
                        html.Span("Avalanche", className = "main-chains-selection"),
                    ], style={'display': 'inline-flex', 'align-items': 'center', 'justify-content': 'center'}
                ),
                "value": "Avalanche",
            },

            {
                "label": html.Span(
                    [
                        html.Img(src = "assets/gnosis.png", height = 15),
                        html.Span("Gnosis Chain", className = "main-chains-selection"),
                    ], style={'display': 'inline-flex', 'align-items': 'center', 'justify-content': 'center'}
                ),
                "value": "Gnosis Chain",
            },
            
            {
                "label": html.Span(
                    [
                        html.Img(src = "assets/optimism.png", height = 15),
                        html.Span("Optimism", className = "main-chains-selection"),
                    ], style={'display': 'inline-flex', 'align-items': 'center', 'justify-content': 'center'}
                ),
                "value": "Optimism",
            },

            {
                "label": html.Span(
                    [
                        html.Img(src = "assets/arbitrum.png", height = 15),
                        html.Span("Arbitrum", className = "main-chains-selection"),
                    ], style={'display': 'inline-flex', 'align-items': 'center', 'justify-content': 'center'}
                ),
                "value": "Arbitrum",
            },

            {
                "label": html.Span(
                    [
                        html.Img(src = "assets/fantom.png", height = 15),
                        html.Span("Fantom", className = "main-chains-selection"),
                    ], style={'display': 'inline-flex', 'align-items': 'center', 'justify-content': 'center'}
                ),
                "value": "Fantom",
            },
        ], 
        value = ['Ethereum', 'BNB Chain', 'Polygon'],
        multi = True,
        id = 'chain-selections',
        className = "dropdown-table-input"
    ),
    ], className = "chains-input-main"
    ),

    html.H1('Total number of transactions since the launch', className = "price-description"),

    dcc.Graph(
        id='total-txs-indicators',
        figure = txs_total
    ),

    dcc.Graph(
        id='transactions-over-time',
        figure = fig_txs
    ),

    html.Div(children = dcc.Graph(
        id = 'txs-avg-txs-distribution',
        figure = avg_tx_by_chain,
        ),
        style={'width': '50%', 'display': 'inline-block'},
    ),
    html.Div(children = dcc.Graph(
        id = 'txs-histogram',
        figure = txs_histogram,
        ),
        style={'width': '50%', 'display': 'inline-block'},
    ),

    html.Div(children = dcc.Graph(
        id = 'transactions-gmt-distribution',
        figure = fig_gmt_distribution,
        )
    ),


    html.Div(children = dcc.Graph(
        id = 'addresses-over-time',
        figure = fig_addresses
        ),
        style={'width': '65%', 'display': 'inline-block'},
    ),
    html.Div(children = dcc.Graph(
        id = 'addresses-histogram',
        figure = fig_addresses_distribution,
        ),
        style={'width': '35%', 'display': 'inline-block'},
    ),

    dcc.Graph(
        id='block-time',
        figure=block_time
    ),
    dcc.Graph(
        id='blocks-count',
        figure=blocks_count
    ),
    dcc.Graph(
        id='nft-mint-count',
        figure=nft_mint
    ),

    html.Div(children = [
        html.H2('Stablecoins in EVM chains', className = "price-description"),
        html.P('In the part below we will look at stablecoins statistic on EVM chains. In order not to clutter up the charts, we chose the top-3 fiat-collateral stablecoins, namely USDC, USDT and BUSD. One algorithmic - FRAX and one crypto-collateral stablecoin - DAI.', className = "stablecoin-description"),

        html.Div(children = dcc.Graph(
            id = 'stablecoins-by-type',
            figure = stablecoins_chart,
            ),
            style={'width': '80%', 'display': 'inline-block'},
        ),
        html.Div(children = dcc.Graph(
            id = 'stablecoins-stats-today',
            figure = stablecoins_stats,
            ),
            style={'width': '20%', 'display': 'inline-block'},
        ),


        html.Div(children = dcc.Graph(
            id = 'stablecoins-90ma-transfer-volume',
            figure = stablecoins_MA90_volume,
            ),
            style={'width': '60%', 'display': 'inline-block'},
        ),

        html.Div(children = dcc.Graph(
            id = 'stablecoins-90ma-transfer-volume-share',
            figure = stablecoins_MA90_share,
            ),
            style={'width': '40%', 'display': 'inline-block'},
        ),

        dcc.Graph(
            id = 'stablecoins-aggregated-transfers',
            figure = stablecoins_Agg_transfers
        ),

    ], className = "bridge-border"
    ),

    html.H2('EVM native tokens price', className = "price-description"),
    html.P('Select token symbol here. The chart below shows Ethereum price and price of token you selected', className = "price-description"),
    dcc.RadioItems(
        (price_data[price_data["TOKEN"] != "Ethereum (ETH)"])["TOKEN"].unique(),
        'Binance (BNB)',
        id = 'evm-prices-item',
        className = "price-input"
    ),
    dcc.Graph(
        id='evm-price-plot'
    ),

    # The END

    html.H2([
            html.Span("The original of this dashboard is made on"),
            html.A(
                " Dune Analytics", 
                href='https://dune.com/KARTOD/blockchains-analysis', 
                target="_blank"
            )
        ],
        className = "description-main"
    ),
])

#callback for main checklist
@app.callback(
    Output('transactions-over-time', 'figure'),
    Output('txs-histogram', 'figure'),
    Output('addresses-over-time', 'figure'),
    Output('addresses-histogram', 'figure'),
    Output('block-time', 'figure'),
    Output('blocks-count', 'figure'),
    Output('txs-avg-txs-distribution', 'figure'),
    Output('total-txs-indicators', 'figure'),
    Output('transactions-gmt-distribution', 'figure'),
    Input('chain-selections', 'value')
)
def update_output(value):
    if value:
        fig_txs, txs_histogram, txs_total = transactions(data.loc[data['CHAIN'].isin(value)])

        fig_addresses, fig_addresses_distribution = active_addresses(data.loc[data['CHAIN'].isin(value)])

        block_time, blocks_count = blocks(data.loc[data['CHAIN'].isin(value)])

        avg_tx_by_chain = transactions_by_chain_by_time(data.loc[data['CHAIN'].isin(value)])

        fig_gmt_distribution = gmt_hour(gmt_hour_data.loc[gmt_hour_data['CHAIN'].isin(value)])
            
        return fig_txs, txs_histogram, fig_addresses, fig_addresses_distribution, block_time, blocks_count, avg_tx_by_chain, txs_total, fig_gmt_distribution

    else:
        fig = go.Figure()

        fig.update_layout(
            height = 400,
            plot_bgcolor = '#171730',
            paper_bgcolor = '#171730',
            font = dict(color = 'white')
        )

        return fig, fig, fig, fig, fig, fig, fig

# callback for evm prices

@app.callback(
    Output('evm-price-plot', 'figure'),
    Input('evm-prices-item', 'value')
)
def price_evm(value):
    return evm_prices_chart(price_data, value)

if __name__ == '__main__':
    app.run_server(debug = True)