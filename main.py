from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from merge import *


from Transactions import *
from Active_addresses import *
from Blocks import *
from Avg_transactions import *
from GMT_hour import *

data = merge_data()

fig_txs, txs_histogram = transactions(data)
fig_addresses = active_addresses(data)
block_time, blocks_count = blocks(data)
avg_tx_by_chain = transactions_by_chain_by_time()
fig_gmt_distribution, data_gmt = gmt_hour()


fig_gmt_distribution.update_layout(clickmode = 'event+select')


app = Dash(__name__)
app.title = 'EVM Dashboard'
app.layout = html.Div(children=[
    html.Div(
        children = [
            html.Div([
                html.Img(src = "assets/fivicon.ico"),
                html.H1(
                    children='EVM Blockchains Analysis', 
                ),
            ],
            className = "header-title"
            ),
            html.H2([
                html.Span(children = "Built by"),
                html.Span(children = " Impossible Research ", className="header-description-if"),
                html.Span(children = "team")
                ],
                className = "header-description"
                
            ),
            html.H2(
                children = "Analyze ....The live Impossible Finance price today is $0,070130 USD with a 24-hour trading volume of $260,85 USD. We update our IF to USD price in real-time. Impossible Finance is down 2,11% in the last 24 hours. The current CoinMarketCap ranking is #1635, with a live market cap of $420 828 USD. It has a circulating supply of 6 000 661 IF coins and a max. supply of 21 000 000 IF coins.",
                className="description-main"
            ),
        ],
    ),

    dcc.Graph(
        id='transactions-over-time',
        figure=fig_txs
    ),

    html.Div(children = dcc.Graph(
        id = 'transactions-gmt-distribution',
        figure = fig_gmt_distribution,
        ),
        style={'width': '70%', 'display': 'inline-block'},
    ),

    html.Div(children = dcc.Graph(
        id = 'transactions-gmt-distribution-specific-chain'
        ),
        style={'width': '30%', 'display': 'inline-block'},
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

@app.callback(
    Output('transactions-gmt-distribution-specific-chain', 'figure'),
    Input('transactions-gmt-distribution', 'hoverData')
)
def specific_chain_gmt(hoverData):
    if hoverData:
        _chain_list = ((data_gmt[data_gmt.index == hoverData['points'][0]['curveNumber']]['Chain']).to_string()).split(" ")
        if _chain_list[len(_chain_list)-2] != '':
            chain = _chain_list[len(_chain_list)-2] + ' ' + _chain_list[len(_chain_list)-1]
        else:
            chain = _chain_list[len(_chain_list)-1]    

        data_chain = data_gmt[data_gmt["Chain"] == chain]

        f2 = open('chains_config.json')
        chains_config = json.load(f2)

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x = data_chain['Sum of transactions'],
            y = data_chain['GMT hour'],
            orientation = 'h',
            marker_color = ((list(filter(lambda x:x["chain_name"]==chain,chains_config)))[0]["colors"])
        ))

        fig.update_layout(
            title = "Distribution for " + chain + ":", 
            xaxis_title = "Transactions", 
            yaxis_title = "GMT Hour",
            height = 500,
            plot_bgcolor = '#171730',
            paper_bgcolor = '#171730',
            font = dict(color = 'white')
        )

        f2.close()

        return fig
    else:
        fig = go.Figure()

        fig.update_layout(
            xaxis_title = "Transactions", 
            yaxis_title = "GMT Hour",
            height = 500,
            plot_bgcolor = '#171730',
            paper_bgcolor = '#171730',
            font = dict(color = 'white')
        )

        return fig

if __name__ == '__main__':
    app.run_server(debug=True)