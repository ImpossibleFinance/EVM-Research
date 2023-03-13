import dash
from dash import html, Input, Output, dcc
from datetime import timedelta


from scripts.Functions import *
from config_app import *
from scripts.distribution_by_day_of_week import *
from scripts.gmt_distribution import *
from scripts.active_addresses_distribution import *


###########################################################################
############################# Page ########################################
###########################################################################


dash.register_page(
    __name__,
    path = '/',
    title = 'EVM Dashboard',
    name = 'EVM Dashboard'
)

layout = html.Div([
    html.Div([
        html.Img(src = "assets/DataLab.svg", alt = " ", className = "if-ico"),
    ],className = "header-title"),

    html.Div([
        html.Iframe(
            src = "assets/other_dashboards_list.html",
            className = "list-dash"
        )
    ], id = 'dashboard-list'),


    html.Div([
        html.H1([' EVM Blockchains Analysis'], 
                className = "main-header-title"),
        html.H2(["The comparison of activity on EVM blockchains: daily transactions, active addresses, as well as average block creation time and daily block count"],
                className = "description-main"),
    ]),

    html.Div([
        html.H1([
            html.Div([
                html.Div(className = "kpi_container", id = 'total-txs'),
                html.Div(className = "kpi_container", id = 'total-addresses')
            ], className = "left_container"),
            html.Div([
                html.H1('Transactions', className = 'left_container_h1'),
                dcc.Graph(
                    config = config, 
                    id = 'transactions-over-time', 
                ),
            ])
        ],className = "left"),
                
        html.Div([
            html.H2('Filter Criteria'),

            html.P('Blockchain'),

            dcc.Dropdown(
                options = dropdown_options,
                value = ['Ethereum', 'BNB Chain', 'Polygon'],
                multi = True,
                clearable = True,
                id = 'chain-selections',
                placeholder = "Select Chains",
                className = "dropdown-table-input"
            ),

            html.Br(),
            html.P('Date Range'),

            dcc.Dropdown(
                options = dropdown_options_date_range,
                value = '30',
                id = 'date-range-selections',
                className = "dropdown-table-input"
            ),

        ], className = "right_container"),
    ], className = "grid-container"),

    html.Div(className = "kpi_container", id = 'distribution-txs-active'),
    html.Div(className = "kpi_container", id = 'distribution-txs-passive'),

    dcc.Graph(
        config = config, 
        id = 'transactions-distribution-week'
    ),

    dcc.Graph(
        config = config, 
        id = 'transactions-distribution',
        style={'width': '60%', 'display': 'inline-block'}
    ),
    html.Div(
        className = "kpi_container", 
        id = 'distribution-time-zones',
        style = {'width': '30%', 'display': 'inline-block'}
    ),

    ############################## Addresses ##############################

    html.Div([
        html.H1('Addresses', className = 'left_container_h1'),
        dcc.Graph(
            config = config, 
            id = 'active-addresses-over-time', 
        ),
    ]),

    dcc.Graph(
        config = config, 
        id = 'addresses-distribution',
        style={'width': '55%', 'display': 'inline-block'}
    ),
    html.Div(
        className = "kpi_container", 
        id = 'ath-active-users',
        style = {'width': '35%', 'display': 'inline-block'}
    ),

    ############################## Blocks ##############################

    html.Div([
        html.H1('Blocks', className = 'left_container_h1'),
        dcc.Graph(
            config = config, 
            id = 'block-time-over-time', 
        ),
    ]),

    dcc.Graph(
        config = config, 
        id = 'blocks-count-over-time',
        style={'width': '60%', 'display': 'inline-block'}
    ),
    html.Div(
        className = "kpi_container", 
        id = 'total-blocks-count',
        style = {'width': '30%', 'display': 'inline-block'}
    ),
])

############################### Transactions ###############################
#callback for rendering by category

@dash.callback(
    Output('transactions-over-time', 'figure'),
    Input('date-range-selections', 'value'),
    Input('chain-selections', 'value')
)
def render_transactions(date_range, chain):
    if chain != []:
        current_data = (data.loc[data['CHAIN'].isin(chain)])
    else:
        return go.Figure()
    last_date = (max(current_data['Date(UTC)']))

    if date_range != 'All':
        current_data = (current_data[current_data['Date(UTC)'].between((last_date - timedelta(days = int(date_range))), last_date)])

    return fig_line_over_time(current_data, 'Date(UTC)', 'Value', 'CHAIN', chains_config, 'Overtime Transactions Breakdown', False)

@dash.callback(
    Output('total-txs', 'children'),
    Output('total-addresses', 'children'),
    Input('chain-selections', 'value')
)
def render_total_stats(chain):
    if chain != []:
        result_data = total_sum(data.loc[data['CHAIN'].isin(chain)], 'Value', 'CHAIN')
    else:
        return kpi([], [], 'Total & Trend Change', 'Month-over-Month'), kpi([], [], 'Active Wallets', 'Month-over-Month')

    return kpi(result_data['CHAIN'], result_data['Value'], 'Total & Trend Change', 'Month-over-Month'), kpi(result_data['CHAIN'], result_data['Active addresses'], 'Active Wallets', 'Month-over-Month')

@dash.callback(
    Output('transactions-distribution-week', 'figure'),
    Output('distribution-txs-active', 'children'),
    Output('distribution-txs-passive', 'children'),
    Input('date-range-selections', 'value'),
    Input('chain-selections', 'value')
)
def render_transactions_day_of_week(date_range, chain):
    if chain != []:
        current_data = (data.loc[data['CHAIN'].isin(chain)])
    else:
        return go.Figure(), kpi([], [], 'Most Active day', ''), kpi([], [], 'Most Passive day', '')
    last_date = (max(current_data['Date(UTC)']))

    if date_range != 'All':
        current_data = (current_data[current_data['Date(UTC)'].between((last_date - timedelta(days = int(date_range))), last_date)])
    
    return transactions_by_day_of_week(current_data, date_range, chains_config)

@dash.callback(
    Output('transactions-distribution', 'figure'),
    Output('distribution-time-zones', 'children'),
    Input('chain-selections', 'value')
)
def render_transactions_by_gmt(chain):
    if chain != []:
        current_data = (gmt_hour_data.loc[gmt_hour_data['CHAIN'].isin(chain)])
    else:
        return go.Figure(), kpi([], [], 'Active Time Zones', '')

    return distribution_by_gmt(current_data, chains_config)


############################### Addresses ###############################

@dash.callback(
    Output('active-addresses-over-time', 'figure'),
    Output('ath-active-users', 'children'),
    Output('addresses-distribution', 'figure'),
    Input('date-range-selections', 'value'),
    Input('chain-selections', 'value')
)
def render_transactions(date_range, chain):
    if chain != []:
        current_data = (data.loc[data['CHAIN'].isin(chain)])
    else:
        return go.Figure(), kpi([], [], 'ATH of Daily Active Wallets', ''), go.Figure()
    
    last_date = (max(current_data['Date(UTC)']))

    if date_range != 'All':
        current_data = (current_data[current_data['Date(UTC)'].between((last_date - timedelta(days = int(date_range))), last_date)])

    active_address_over_time = fig_line_over_time(current_data, 'Date(UTC)', 'Active addresses', 'CHAIN', chains_config, 'Active Addresses over time', False)
    ath = find_ath(current_data, 'CHAIN', 'Active addresses', 'Date(UTC)')
    active_address_distribution = active_addresses((data.loc[data['CHAIN'].isin(chain)]), current_data)

    return active_address_over_time, ath, active_address_distribution



############################### Blocks ###############################

@dash.callback(
    Output('block-time-over-time', 'figure'),
    Output('blocks-count-over-time', 'figure'),
    Output('total-blocks-count', 'children'),
    Input('date-range-selections', 'value'),
    Input('chain-selections', 'value')
)
def render_transactions(date_range, chain):
    if chain != []:
        current_data = (data.loc[data['CHAIN'].isin(chain)])
    else:
        return go.Figure()
    
    last_date = (max(current_data['Date(UTC)']))

    if date_range != 'All':
        current_data = (current_data[current_data['Date(UTC)'].between((last_date - timedelta(days = int(date_range))), last_date)])

    block_time_over_time = fig_line_over_time(current_data, 'Date(UTC)', 'Block time', 'CHAIN', chains_config, 'Block time', True)
    blocks_over_time = fig_line_over_time(current_data, 'Date(UTC)', 'Blocks count', 'CHAIN', chains_config, 'Blocks Count', True)
    
    arr_blocks = total_sum(data.loc[data['CHAIN'].isin(chain)], 'Value', 'CHAIN')
    total_blocks_count = kpi(arr_blocks['CHAIN'], arr_blocks['Blocks count'], 'Total Blocks made on blockchains', '')

    return block_time_over_time, blocks_over_time, total_blocks_count