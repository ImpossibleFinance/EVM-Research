from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import flask

from scripts.Transactions import *
from scripts.Active_addresses import *
from scripts.Blocks import *
from scripts.GMT_hour import *
from scripts.Prices import *
from scripts.Stablecoins import *

config = {
    'displayModeBar': False
}


def read_data(name):
    df = pd.read_csv('csv_data/' + str(name) + '.csv')

    if 'DATE' in df:
        df['DATE'] = pd.to_datetime(pd.to_datetime(df['DATE']).dt.strftime('%Y-%m-%d'))
    
    if 'Date(UTC)' in df:
        df['Date(UTC)'] = pd.to_datetime(pd.to_datetime(df['Date(UTC)']).dt.strftime('%Y-%m-%d'))
    
    return df

data_name_array = ['data', 'price_data', 'gmt_hour_data', 'stablecoins']

for name in data_name_array:
    (globals()[name]) = read_data(str(name))

#### Load data

last_date = (max(data['Date(UTC)']))
#fig_txs, txs_histogram = transactions(data)
#fig_addresses, fig_addresses_distribution = active_addresses(data)
#block_time, blocks_count = blocks(data)

#avg_tx_by_chain = transactions_by_chain_by_time(data)

fig_gmt_distribution = gmt_hour(gmt_hour_data)

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
                    ' EVM Blockchains Analysis (Open Beta V 0.3.2)', 
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
    html.H1('Before you begin, please select the chains you wish to review:', className = "h1-description"),
    #html.P('This choice will affect all of the charts in the 1st part except the Interactive table and Distribution by GMT Hour chart', className = "h1-description"),

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

    dcc.Tabs(id = 'category-tabs',
        value = 'transactions',
        children=[
            dcc.Tab(label='📧 Transactions 📈', value='transactions'),
            dcc.Tab(label='Addresses (WIP)', value='addresses'),
            dcc.Tab(label='Blocks & Block time (WIP)', value='blocks'),
        ], className = "category-input-main"
    ),

    html.Div(id = 'content-render'),

    html.Div(children = [
        html.H2('Stablecoins in EVM chains', className = "h1-description"),
        html.P('In the part below we will look at stablecoins statistic on EVM chains. In order not to clutter up the charts, we chose the top-3 fiat-collateral stablecoins, namely USDC, USDT and BUSD. One algorithmic - FRAX and one crypto-collateral stablecoin - DAI.', className = "stablecoin-description"),

        html.Div(children = dcc.Graph(
            id = 'stablecoins-by-type',
            figure = stablecoins_chart,
            config = config
            ),
            style={'width': '80%', 'display': 'inline-block'},
        ),
        html.Div(children = dcc.Graph(
            id = 'stablecoins-stats-today',
            figure = stablecoins_stats,
            config = config
            ),
            style={'width': '20%', 'display': 'inline-block'},
        ),


        html.Div(children = dcc.Graph(
            id = 'stablecoins-90ma-transfer-volume',
            figure = stablecoins_MA90_volume,
            config = config
            ),
            style={'width': '60%', 'display': 'inline-block'},
        ),

        html.Div(children = dcc.Graph(
            id = 'stablecoins-90ma-transfer-volume-share',
            figure = stablecoins_MA90_share,
            config = config
            ),
            style={'width': '40%', 'display': 'inline-block'},
        ),

        dcc.Graph(
            id = 'stablecoins-aggregated-transfers',
            figure = stablecoins_Agg_transfers,
            config = config
        ),

    ], className = "bridge-border"
    ),

    html.H2('EVM native tokens price', className = "h1-description"),
    html.P('Select token symbol here. The chart below shows Ethereum price and price of token you selected', className = "h1-description"),
    dcc.RadioItems(
        (price_data[price_data["TOKEN"] != "Ethereum (ETH)"])["TOKEN"].unique(),
        'Binance (BNB)',
        id = 'evm-prices-item',
        className = "price-input"
    ),
    dcc.Graph(
        id='evm-price-plot',
        config = config
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

#callback for rendering by category
@app.callback(
    Output('content-render', 'children'),
    Input('category-tabs', 'value'),
    Input('chain-selections', 'value')
)
def render_content(tab, chain):
    if tab == 'transactions':

        fig_txs, txs_histogram = transactions(data.loc[data['CHAIN'].isin(chain)])

        avg_tx_by_chain = transactions_by_chain_by_time(data.loc[data['CHAIN'].isin(chain)])

        fig_gmt_distribution = gmt_hour(gmt_hour_data.loc[gmt_hour_data['CHAIN'].isin(chain)])

        fig_indicators_sum = main_indicators(data.loc[data['CHAIN'].isin(chain)])

        return [

            html.H2('Total number of transactions since the launch', className = "h1-description"),

            dcc.Graph(
                id='transactions-sum-indicators',
                figure = fig_indicators_sum, 
                config = config
            ),

            dcc.Graph(
                id='transactions-over-time',
                figure = fig_txs,
                config = config
            ),

            html.Div(children = dcc.Graph(
                id = 'txs-avg-txs-distribution',
                figure = avg_tx_by_chain,
                config = config
                ),
                style={'width': '50%', 'display': 'inline-block'},
            ),
            html.Div(children = dcc.Graph(
                id = 'txs-histogram',
                figure = txs_histogram,
                config = config
                ),
                style={'width': '50%', 'display': 'inline-block'},
            ),

            html.Div(children = dcc.Graph(
                id = 'transactions-gmt-distribution',
                figure = fig_gmt_distribution,
                config = config
                )
            ),
        ]
    
    if tab == 'addresses':
        fig_addresses = active_addresses(data.loc[data['CHAIN'].isin(chain)])

        fig_addresses_distribution = average_addresses(data.loc[data['CHAIN'].isin(chain)])

        fig_trend, fig_trend_txt = trend_address(data.loc[data['CHAIN'].isin(chain)])

        return [
            dcc.Graph(
                id = 'addresses-over-time',
                figure = fig_addresses,
                config = config
            ),
            dcc.Graph(
                id = 'addresses-histogram',
                figure = fig_addresses_distribution,
                config = config
            ),


            html.Div(children = dcc.Graph(
                id = 'addresses-trend-chart',
                figure = fig_trend,
                config = config
                ),
                style={'width': '80%', 'display': 'inline-block'},
            ),
            html.Div(children = dcc.Graph(
                id = 'addresses-indicators-chart',
                figure = fig_trend_txt,
                config = config
                ),
                style={'width': '20%', 'display': 'inline-block'},
            ),
        ]

    if tab == 'blocks':

        block_time, blocks_count = blocks(data.loc[data['CHAIN'].isin(chain)])

        return [
            dcc.Graph(
                id='block-time',
                figure=block_time,
                config = config
            ),
            dcc.Graph(
                id='blocks-count',
                figure=blocks_count,
                config = config
            ),
        ]

    return tab


# callback for evm prices

@app.callback(
    Output('evm-price-plot', 'figure'),
    Input('evm-prices-item', 'value')
)
def price_evm(value):
    return evm_prices_chart(price_data, value)





if __name__ == '__main__':
    app.run_server(debug = True)