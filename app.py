from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output
from merge import *
import flask

from scripts.Transactions import *
from scripts.Active_addresses import *
from scripts.Blocks import *
from scripts.Avg_transactions import *
from scripts.GMT_hour import *
from scripts.Main_table import *
from scripts.NFT_mints import *
from scripts.Bridges_activity import *
from scripts.Prices import *


data = merge_data()
price_data = evm_prices()

table_data, last_date = table_data(data)
fig_txs, txs_histogram = transactions(data)
fig_addresses = active_addresses(data)
block_time, blocks_count = blocks(data)


avg_tx_by_chain = transactions_by_chain_by_time()
fig_gmt_distribution, data_gmt = gmt_hour()
nft_mint = nft_mints()
bridges_chart, bridges_data, bridges_names = bridges_activity()

last_date = (str(last_date).split(" "))[0]

fig_gmt_distribution.update_layout(clickmode = 'event+select')
bridges_chart.update_layout(clickmode = 'event+select')


server = flask.Flask(__name__)

app = Dash(__name__, server = server)


app.title = 'EVM Dashboard'


app.layout = html.Div(children=[
    html.Div(
        children = [
            html.Div([
                html.Img(src = "assets/IF.png", alt = " ", className = "if-ico"),
                html.H1(
                    ' EVM Blockchains Analysis (Open Beta)', 
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
                html.Span(" ZettaBlock API ", className="description-if-and-zb"),
                ],
                className="description-main"
            ),
        ],
    ),
    html.Div( children = [
    html.H2('Interactive Data table', className = "table-name"),
    html.Div(children = [
        html.P(id = 'table_out_p1'),
        html.P(id = 'table_out_p2'),
        html.P(id = 'table_out_p3'),
    ], className = "table-output"
    ),

    dash_table.DataTable(
        id = 'table',
        columns=[{"name": i, "id": i} 
                 for i in table_data.columns],
        data = table_data.to_dict('records'),
        style_cell = dict(textAlign = 'left'),
        style_header = dict(backgroundColor = "paleturquoise"),
        style_data = dict(backgroundColor = "lavender"),
        style_data_conditional = [
        {
            'if': {
                'filter_query': '{Pct txs} > 0',
                'column_id': '# of Transactions'
            },
            'color': 'green',
            'fontWeight': 'bold'
        },
        {
            'if': {
                'filter_query': '{Pct txs} < 0',
                'column_id': '# of Transactions'
            },
            'color': 'red',
            'fontWeight': 'bold'
        },

        {
            'if': {
                'filter_query': '{Pct addresses} > 0',
                'column_id': '# of Active addresses'
            },
            'color': 'green',
            'fontWeight': 'bold'
        },
        {
            'if': {
                'filter_query': '{Pct addresses} < 0',
                'column_id': '# of Active addresses'
            },
            'color': 'red',
            'fontWeight': 'bold'
        },

        {
            'if': {
                'filter_query': '{Pct time} > 0',
                'column_id': 'Block time [s]'
            },
            'color': 'green',
            'fontWeight': 'bold'
        },
        {
            'if': {
                'filter_query': '{Pct time} < 0',
                'column_id': 'Block time [s]'
            },
            'color': 'red',
            'fontWeight': 'bold'
        },

        {
            'if': {
                'filter_query': '{Pct blocks} > 0',
                'column_id': '# of Blocks'
            },
            'color': 'green',
            'fontWeight': 'bold'
        },
        {
            'if': {
                'filter_query': '{Pct blocks} < 0',
                'column_id': '# of Blocks'
            },
            'color': 'red',
            'fontWeight': 'bold'
        },
        ],
        style_cell_conditional = [
            {
            'if': {'column_id': c},
            'display': 'none'
            } for c in ['Pct txs', 'Pct addresses', 'Pct time', 'Pct blocks', 'Value', 'Active addresses', 'Block time', 'Blocks count']
        ],
    ), 
    ], className = "table"
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
    dcc.Graph(
        id='nft-mint-count',
        figure=nft_mint
    ),

    html.Div(children = [
        html.Div(children = dcc.Graph(
            id = 'bridges-activity-sankey-diagram',
            figure = bridges_chart,
            ),
        ),

        html.Div(children = dcc.Graph(
            id = 'bridges-transfers-daily'
            ),
            style={'width': '50%', 'display': 'inline-block'},
        ),
        html.Div(children = dcc.Graph(
            id = 'bridges-usd-value-daily'
            ),
            style={'width': '50%', 'display': 'inline-block'},
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

    html.H2([
            html.Span("The original of this dashboard is made on"),
            html.A(
                " Dune Analytics", 
                href='https://dune.com/KARTOD/blockchains-analysis', 
                target="_blank"
            )
        ],
        className="description-main"
    ),
])


# callback for table
@app.callback(
    Output('table_out_p1', 'children'), 
    Input('table', 'active_cell'))
def update_graphs(active_cell):
    if active_cell and active_cell['column_id'] != 'Chain':
        return_data = str(table_data.iloc[active_cell['row']]['Chain']) + " " + str(active_cell['column_id']) + ":"
        return return_data
    return " "

@app.callback(
    Output('table_out_p2', 'children'), 
    Input('table', 'active_cell'))
def update_graphs(active_cell):
    if active_cell and active_cell['column_id'] != 'Chain':
        cell_data = table_data.iloc[active_cell['row']][active_cell['column_id']]
        return_data = "On " + str(last_date) + " : " + str(cell_data)
        return return_data
    return "Click the table"

@app.callback(
    Output('table_out_p3', 'children'), 
    Input('table', 'active_cell'))
def update_graphs(active_cell):
    if active_cell and active_cell['column_id'] != 'Chain':
        return_data = " Average value for last 1M:"

        if str(active_cell['column_id']) == '# of Transactions':
            return_data = return_data + " " + str("{:,.2f}".format(round(table_data.iloc[active_cell['row']]['Value'], 0)))
        if str(active_cell['column_id']) == '# of Active addresses':
            return_data = return_data + " " + str("{:,.2f}".format(round(table_data.iloc[active_cell['row']]['Active addresses'], 0)))
        if str(active_cell['column_id']) == 'Block time [s]':
            return_data = return_data + " " + str("{:,.2f}".format(round(table_data.iloc[active_cell['row']]['Block time'], 0)))
        if str(active_cell['column_id']) == '# of Blocks':
            return_data = return_data + " " + str("{:,.2f}".format(round(table_data.iloc[active_cell['row']]['Blocks count'], 0)))
        return return_data
    return "Percentage in brackets is the difference between current value & average value for last 1 month"





# callback for gmt distribution

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
            x = data_chain['AVG_TXS_COUNT'],
            y = data_chain['GMT_HOUR'],
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


# callback for bridges

@app.callback(
    Output('bridges-transfers-daily', 'figure'),
    Input('bridges-activity-sankey-diagram', 'clickData')
)
def specific_chain_gmt(clickData):
    if clickData:
        _temp_data = bridges_data[bridges_data["name"] == bridges_names[int(clickData['points'][0]['pointNumber'])]]

        fig = go.Figure()


        fig.add_trace(go.Bar(
            x = _temp_data['DATE'],
            y = _temp_data['TRANSFERS'],
        ))

        fig.update_layout(
            title = "ERC-20 transfers for " + bridges_names[int(clickData['points'][0]['pointNumber'])] + " :", 
            xaxis_title = "Date", 
            yaxis_title = "ERC-20 transfers",
            height = 400,
            plot_bgcolor = '#171730',
            paper_bgcolor = '#171730',
            font = dict(color = 'white')
        )

        return fig
    else:
        fig = go.Figure()

        fig.update_layout(
            xaxis_title = "ERC-20 transfers", 
            yaxis_title = "Transfers",
            height = 400,
            plot_bgcolor = '#171730',
            paper_bgcolor = '#171730',
            font = dict(color = 'white')
        )

        return fig

@app.callback(
    Output('bridges-usd-value-daily', 'figure'),
    Input('bridges-activity-sankey-diagram', 'clickData')
)
def specific_chain_gmt(clickData):
    if clickData:
        _temp_data = bridges_data[bridges_data["name"] == bridges_names[int(clickData['points'][0]['pointNumber'])]]

        fig = go.Figure()

        
        fig.add_trace(go.Bar(
            x = _temp_data['DATE'],
            y = _temp_data['USD_VALUE'],
        ))

        fig.update_layout(
            title = "Stablecoins transfers for " + bridges_names[int(clickData['points'][0]['pointNumber'])] + " in USD equivalent :", 
            xaxis_title = "Date", 
            yaxis_title = "USD Value",
            height = 400,
            plot_bgcolor = '#171730',
            paper_bgcolor = '#171730',
            font = dict(color = 'white')
        )

        return fig
    else:
        fig = go.Figure()

        fig.update_layout(
            xaxis_title = "Date", 
            yaxis_title = "USD Value",
            height = 400,
            plot_bgcolor = '#171730',
            paper_bgcolor = '#171730',
            font = dict(color = 'white')
        )

        return fig



# callback for evm prices

@app.callback(
    Output('evm-price-plot', 'figure'),
    Input('evm-prices-item', 'value')
)
def specific_chain_gmt(value):
    return evm_prices_chart(price_data, value)

if __name__ == '__main__':
    app.run_server(debug = True)