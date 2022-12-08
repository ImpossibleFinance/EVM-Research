from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output
from merge import *


from scripts.Transactions import *
from scripts.Active_addresses import *
from scripts.Blocks import *
from scripts.Avg_transactions import *
from scripts.GMT_hour import *
from scripts.Main_table import *

data = merge_data()

table_data, last_date = table_data(data)
fig_txs, txs_histogram = transactions(data)
fig_addresses = active_addresses(data)
block_time, blocks_count = blocks(data)
avg_tx_by_chain = transactions_by_chain_by_time()
fig_gmt_distribution, data_gmt = gmt_hour()
last_date = (str(last_date).split(" "))[0]

fig_gmt_distribution.update_layout(clickmode = 'event+select')


app = Dash(__name__)
app.title = 'EVM Dashboard'
app.layout = html.Div(children=[
    html.Div(
        children = [
            html.Div([
                html.Img(src = "assets/favicon.ico", alt = " ", className = "if-ico"),
                html.H1(
                    ' EVM Blockchains Analysis', 
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
            html.H2(
                "Analyze....",
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
])


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
            return_data = return_data + " " + str(round(table_data.iloc[active_cell['row']]['Value'], 0))
        if str(active_cell['column_id']) == '# of Active addresses':
            return_data = return_data + " " + str(round(table_data.iloc[active_cell['row']]['Active addresses'], 0))
        if str(active_cell['column_id']) == 'Block time [s]':
            return_data = return_data + " " + str(round(table_data.iloc[active_cell['row']]['Block time'], 0))
        if str(active_cell['column_id']) == '# of Blocks':
            return_data = return_data + " " + str(round(table_data.iloc[active_cell['row']]['Blocks count'], 0))
        return return_data
    return "Percentage in brackets is the difference between current value & average value for last 1 month"




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

if __name__ == '__main__':
    app.run_server(debug = True)