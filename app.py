from dash import Dash, html, dcc, dash_table, callback_context
from dash.dependencies import Input, Output
from merge import *
import flask

from scripts.Transactions import *
from scripts.Active_addresses import *
from scripts.Blocks import *
from scripts.GMT_hour import *
from scripts.Main_table import *
from scripts.NFT_mints import *
from scripts.Prices import *
from scripts.Stablecoins import *

from scripts.Solana import *


def read_data(name):
    df = pd.read_csv('csv_data/' + str(name) + '.csv')

    if 'DATE' in df:
        df['DATE'] = pd.to_datetime(pd.to_datetime(df['DATE']).dt.strftime('%Y-%m-%d'))
    
    if 'Date(UTC)' in df:
        df['Date(UTC)'] = pd.to_datetime(pd.to_datetime(df['Date(UTC)']).dt.strftime('%Y-%m-%d'))
    
    return df

data_name_array = ['data', 'price_data', 'gmt_hour_data', 'nfts_data', 'stable_symbol', 'stable_type', 'solana_data']

for name in data_name_array:
    (globals()[name]) = read_data(str(name))

#### Load data

table_data, last_date = table_data(data)
fig_txs, txs_histogram = transactions(data)
fig_addresses = active_addresses(data)
block_time, blocks_count = blocks(data)

avg_tx_by_chain = transactions_by_chain_by_time(data)

fig_gmt_distribution, data_gmt = gmt_hour(gmt_hour_data)

nft_mint = nft_mints(nfts_data)

stablecoins_by_type = stablecoins_charts(stable_type)


## Part II

non_evm_txs, non_evm_users, non_evm_price = solana(solana_data, data, price_data)


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
                className = "description-main"
            ),
        ],
    ),

    html.Div( children = [
    html.H1('Before you begin, please select the chains you wish to review:', className = "price-description"),
    html.P('This choice will affect all of the charts in the 1st part except the Interactive table and Distribution by GMT Hour chart', className = "price-description"),

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
                        html.Img(src = "assets/arbitrum.png", height = 15),
                        html.Span("Arbitrum", className = "main-chains-selection"),
                    ], style={'display': 'inline-flex', 'align-items': 'center', 'justify-content': 'center'}
                ),
                "value": "Arbitrum",
            },
        ], 
        value = ['Ethereum', 'Polygon'],
        multi = True,
        id = 'chain-selections',
        className = "dropdown-table-input"
    ),
    ], className = "chains-input-main"
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
        columns = [{"name": i, "id": i} 
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
        figure = fig_txs
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
        html.H2('Stablecoins in EVM chains', className = "price-description"),
        html.Div(children = dcc.Graph(
            id = 'stablecoins-by-type',
            figure = stablecoins_by_type,
            ),
        ),
        html.P('Select stablecoins here. So you can choose the stablecoins you want to compare in terms of supply.', className = "price-description"),

        dcc.Dropdown(
        [
            {
                "label": html.Span(
                    [
                        html.Img(src = "assets/usdc.png", height = 15),
                        html.Span("USDC", className = "main-chains-selection"),
                    ], style={'display': 'inline-flex', 'align-items': 'center', 'justify-content': 'center'}
                ),
                "value": "USDC",
            },

            {
                "label": html.Span(
                    [
                        html.Img(src = "assets/usdt.png", height = 15),
                        html.Span("USDT", className = "main-chains-selection"),
                    ], style={'display': 'inline-flex', 'align-items': 'center', 'justify-content': 'center'}
                ),
                "value": "USDT",
            },

            {
                "label": html.Span(
                    [
                        html.Img(src = "assets/busd.png", height = 15),
                        html.Span("BUSD", className = "main-chains-selection"),
                    ], style={'display': 'inline-flex', 'align-items': 'center', 'justify-content': 'center'}
                ),
                "value": "BUSD",
            },

            {
                "label": html.Span(
                    [
                        html.Img(src = "assets/dai.png", height = 15),
                        html.Span("DAI", className = "main-chains-selection"),
                    ], style={'display': 'inline-flex', 'align-items': 'center', 'justify-content': 'center'}
                ),
                "value": "DAI",
            },

            {
                "label": html.Span(
                    [
                        html.Img(src = "assets/pax.png", height = 15),
                        html.Span("PAX", className = "main-chains-selection"),
                    ], style={'display': 'inline-flex', 'align-items': 'center', 'justify-content': 'center'}
                ),
                "value": "PAX",
            },

            {
                "label": html.Span(
                    [
                        html.Img(src = "assets/lusd.png", height = 15),
                        html.Span("LUSD", className = "main-chains-selection"),
                    ], style={'display': 'inline-flex', 'align-items': 'center', 'justify-content': 'center'}
                ),
                "value": "LUSD",
            },

            {
                "label": html.Span(
                    [
                        html.Img(src = "assets/mim.png", height = 15),
                        html.Span("MIM", className = "main-chains-selection"),
                    ], style={'display': 'inline-flex', 'align-items': 'center', 'justify-content': 'center'}
                ),
                "value": "MIM",
            },

            {
                "label": html.Span(
                    [
                        html.Img(src = "assets/fei.png", height = 15),
                        html.Span("FEI", className = "main-chains-selection"),
                    ], style={'display': 'inline-flex', 'align-items': 'center', 'justify-content': 'center'}
                ),
                "value": "FEI",
            },

            {
                "label": html.Span(
                    [
                        html.Img(src = "assets/susd.png", height = 15),
                        html.Span("sUSD", className = "main-chains-selection"),
                    ], style={'display': 'inline-flex', 'align-items': 'center', 'justify-content': 'center'}
                ),
                "value": "sUSD",
            },

            {
                "label": html.Span(
                    [
                        html.Img(src = "assets/ust.png", height = 15),
                        html.Span("UST", className = "main-chains-selection"),
                    ], style={'display': 'inline-flex', 'align-items': 'center', 'justify-content': 'center'}
                ),
                "value": "UST",
            },

            {
                "label": html.Span(
                    [
                        html.Img(src = "assets/frax.png", height = 15),
                        html.Span("FRAX", className = "main-chains-selection"),
                    ], style={'display': 'inline-flex', 'align-items': 'center', 'justify-content': 'center'}
                ),
                "value": "FRAX",
            },

            {
                "label": html.Span(
                    [
                        html.Img(src = "assets/alchemix.png", height = 15),
                        html.Span("Alchemix", className = "main-chains-selection"),
                    ], style={'display': 'inline-flex', 'align-items': 'center', 'justify-content': 'center'}
                ),
                "value": "ALUSD",
            },
            
        ], 
        value = ['USDC', 'USDT', 'BUSD', 'DAI'],
        multi = True,
        id = 'stablecoins-selections',
        className = "dropdown-table-input"
    ),

        html.Div(children = dcc.Graph(
            id = 'stablecoins-by-symbol',
            ),
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

    # Part II

    html.Div([
        html.Img(src = "assets/ethereum.png", alt = " ", className = "evm-ico"),
        html.H1(
            ' EVM VS Non-EVM Blockchains ', 
        ),
        html.Img(src = "assets/solana.png", alt = " ", className = "nonevm-ico"),
    ],
    className = "header-title"
    ),

    html.Div(children = dcc.Graph(
        id = 'evm-vs-non-evm-txs',
        figure = non_evm_txs,
        ),
        style={'width': '50%', 'display': 'inline-block'},
    ),
    html.Div(children = dcc.Graph(
        id = 'evm-vs-non-evm-users',
        figure = non_evm_users,
        ),
        style={'width': '50%', 'display': 'inline-block'},
    ),

    dcc.Graph(
        id = 'non-evm-price',
        figure = non_evm_price
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
    Output('block-time', 'figure'),
    Output('blocks-count', 'figure'),
    Output('txs-avg-txs-distribution', 'figure'),
    Output('nft-mint-count', 'figure'),
    Input('chain-selections', 'value')
)
def update_output(value):
    if value:
        fig_txs, txs_histogram = transactions(data.loc[data['CHAIN'].isin(value)])

        fig_addresses = active_addresses(data.loc[data['CHAIN'].isin(value)])

        block_time, blocks_count = blocks(data.loc[data['CHAIN'].isin(value)])

        avg_tx_by_chain = transactions_by_chain_by_time(data.loc[data['CHAIN'].isin(value)])

        nfts_value = []

        for x in value:
            nfts_value.append(x + " ERC-721")
            nfts_value.append(x + " ERC-1155")

        nft_mint = nft_mints(nfts_data.loc[nfts_data['CHAIN'].isin(nfts_value)])
            
        return fig_txs, txs_histogram, fig_addresses, block_time, blocks_count, avg_tx_by_chain, nft_mint

    else:
        fig = go.Figure()

        fig.update_layout(
            height = 400,
            plot_bgcolor = '#171730',
            paper_bgcolor = '#171730',
            font = dict(color = 'white')
        )

        return fig, fig, fig, fig, fig, fig, fig


# callback for table
@app.callback(
    Output('table_out_p1', 'children'), 
    Input('table', 'active_cell'))
def update_graphs(active_cell):
    if active_cell and active_cell['column_id'] != 'CHAIN':
        return_data = str(table_data.iloc[active_cell['row']]['CHAIN']) + " " + str(active_cell['column_id']) + ":"
        return return_data
    return " "

@app.callback(
    Output('table_out_p2', 'children'), 
    Input('table', 'active_cell'))
def update_graphs(active_cell):
    if active_cell and active_cell['column_id'] != 'CHAIN':
        cell_data = table_data.iloc[active_cell['row']][active_cell['column_id']]
        return_data = "On " + str(last_date) + " : " + str(cell_data)
        return return_data
    return "Click the table"

@app.callback(
    Output('table_out_p3', 'children'), 
    Input('table', 'active_cell'))
def update_graphs(active_cell):
    if active_cell and active_cell['column_id'] != 'CHAIN':
        return_data = " Average value for last 1M:"

        if str(active_cell['column_id']) == '# of Transactions':
            return_data = return_data + " " + str("{:,.1f}".format(round(table_data.iloc[active_cell['row']]['Value'], 0)))
        if str(active_cell['column_id']) == '# of Active addresses':
            return_data = return_data + " " + str("{:,.1f}".format(round(table_data.iloc[active_cell['row']]['Active addresses'], 0)))
        if str(active_cell['column_id']) == 'Block time [s]':
            return_data = return_data + " " + str("{:,.2f}".format(round(table_data.iloc[active_cell['row']]['Block time'], 2)))
        if str(active_cell['column_id']) == '# of Blocks':
            return_data = return_data + " " + str("{:,.1f}".format(round(table_data.iloc[active_cell['row']]['Blocks count'], 0)))
        return return_data
    return "Percentage in brackets is the difference between current value & average value for last 1 month"





# callback for gmt distribution

@app.callback(
    Output('transactions-gmt-distribution-specific-chain', 'figure'),
    Input('transactions-gmt-distribution', 'hoverData')
)
def specific_chain_gmt(hoverData):
    if hoverData:
        _chain_list = ((data_gmt[data_gmt.index == hoverData['points'][0]['curveNumber']]['CHAIN']).to_string()).split(" ")
        if _chain_list[len(_chain_list)-2] != '':
            chain = _chain_list[len(_chain_list)-2] + ' ' + _chain_list[len(_chain_list)-1]
        else:
            chain = _chain_list[len(_chain_list)-1]    

        data_chain = data_gmt[data_gmt["CHAIN"] == chain]

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

        fig.update_xaxes(type = "log")

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


#callback for stablecoins
@app.callback(
    Output('stablecoins-by-symbol', 'figure'),
    Input('stablecoins-selections', 'value')
)
def update_stablecoins(value):
    if value:
        fig = stablecoins_callback(stable_symbol.loc[stable_symbol['symbol'].isin(value)])

        return fig

    else:
        fig = go.Figure()

        fig.update_layout(
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
def price_evm(value):
    return evm_prices_chart(price_data, value)

if __name__ == '__main__':
    app.run_server(debug = True)