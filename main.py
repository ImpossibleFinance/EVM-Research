from dash import Dash, html, dcc

from Transactions import *
from Active_addresses import *
from GMT_hour import *
from Avg_transactions import *
from Blocks import *

fig_txs, txs_histogram = transactions()

fig_addresses = active_addresses()

fig_gmt_distribution = gmt_hour()

avg_tx_by_chain = transactions_by_chain_by_time()

block_time, blocks_count = blocks()

app = Dash(__name__)

app.layout = html.Div(children=[
    html.Div(
        children = [
            #html.Img(src = 'assets/favicon.ico', className="header-img"),
            html.H1(children='EVM Blockchains Analysis', className="header-title"),
            html.P(
                children = "Analyze ....",
                className="header-description",
            ),
        ],
    ),

    dcc.Graph(
        id='transactions-over-time',
        figure=fig_txs
    ),
    dcc.Graph(
        id='transactions-gmt-distribution',
        figure=fig_gmt_distribution
    ),

    html.Div(children = dcc.Graph(
        id = 'txs-avg-txs-distribution',
        figure = avg_tx_by_chain,
        #  config={"displayModeBar": False},
        ),
        style={'width': '50%', 'display': 'inline-block'},
    ),
    html.Div(children = dcc.Graph(
        id = 'txs-histogram',
        figure = txs_histogram,
        #  config={"displayModeBar": False},
        ),
        style={'width': '50%', 'display': 'inline-block'},
    ),

    dcc.Graph(
        id='addresses-over-time',
        figure=fig_addresses
    ),

    dcc.Graph(
        id='block-time',
        figure=block_time
    ),
    dcc.Graph(
        id='blocks-count',
        figure=blocks_count
    ),
])

app.run_server(debug=True)