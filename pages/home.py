import dash
from dash import html, Input, Output, dcc
from datetime import timedelta


from scripts.Functions import *
from config import *
from scripts.distribution_by_day_of_week import *
from scripts.gmt_distribution import *
from scripts.active_addresses_distribution import *


def find_ath(data, group_by, max_index, max_over_index, title):

    groups = data[group_by].unique()
    
    ath = []
    chains = []

    for group in groups:
        data_group = data[data[group_by] == group]

        idmax = data_group[max_index].idxmax()

        ath_stat = number_format(data_group[max_index][idmax]) + ' - ' + (str(data_group[max_over_index][idmax])).replace('00:00:00', '')
        ath.append(ath_stat)
        chains.append(group)

    return create_ez_kpi(chains, ath, title, '', True)

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

            ############################## Transactions ##############################
            html.H1('Transactions', className = 'left_container_h1'),
            html.Div([
                html.P(["Overtime Transactions Breakdown"],className = "title_small"),
                dcc.Graph(
                    config = config, 
                    id = 'transactions-over-time', 
                ),
            ], className = "single_column"),
            html.Div([
                html.P(["Distribution by day of week"],className = "title_small"),
                dcc.Graph(
                    config = config, 
                    id = 'transactions-distribution-week'
                ),
                html.Div(className = "kpi_container", id = 'distribution-txs-active'),
                html.Div(className = "kpi_container", id = 'distribution-txs-passive'),
            ], className = "single_column"),

            html.Div([
                html.Div([
                    html.P(["Distribution of EVM transactions by GMT hour"],className = "title_small"),
                    dcc.Graph(
                        config = config, 
                        id = 'transactions-distribution',
                        style={'width': '100%', 'display': 'inline-block'}
                    ),
                    ], className = "two_column big_colune"),
                    html.Div([
                        html.P(["Active Time Zones"],className = "title_small"),
                        html.Div(
                            className = "kpi_container", 
                            id = 'distribution-time-zones',
                            style = {'width': '100%', 'display': 'inline-block'}
                        ),
                    ], className = "two_column small_colune")
            ], className = "two_column_box"),

            


            ############################## Addresses ##############################
            html.H1('Addresses', className = 'left_container_h1'),
            html.Div([
                html.P(["Active Addresses Over Time"],className = "title_small"),
                dcc.Graph(
                    config = config, 
                    id = 'active-addresses-over-time', 
                ),
            ], className = "single_column"),

            html.Div([
                html.Div([
                    html.P(["Active Addresses Average Comparison"],className = "title_small"),
                    dcc.Graph(
                        config = config, 
                        id = 'addresses-distribution',
                        style={'width': '100%', 'display': 'inline-block'}
                    ),
                    ], className = "two_column big_colune"),
                html.Div([
                    html.P(["ATH Of Daily Active Wallets"],className = "title_small"),
                    html.Div(
                        className = "kpi_container", 
                        id = 'ath-active-users',
                        style = {'width': '100%', 'display': 'inline-block'}
                    ),
                    ], className = "two_column small_colune")
            ], className = "two_column_box"),

            ############################## Blocks ##############################
            html.H1('Blocks', className = 'left_container_h1'),
            html.Div([
                html.P(["Block Time"],className = "title_small"),
                        dcc.Graph(
                    config = config, 
                    id = 'block-time-over-time', 
                ),
            ], className = "single_column"),
            html.Div([
                html.Div([
                    html.P(["Block Count"],className = "title_small"),
                    dcc.Graph(
                        config = config, 
                        id = 'blocks-count-over-time',
                        style={'width': '100%', 'display': 'inline-block'}
                    ),
                    ], className = "two_column big_colune"),
                html.Div([
                    html.P(["Total Blocks made on blockchains"],className = "title_small"),
                    html.Div(
                        className = "kpi_container", 
                        id = 'total-blocks-count',
                        style = {'width': '100%', 'display': 'inline-block'}
                    ),
                    ], className = "two_column small_colune")
            ], className = "two_column_box"),

            ############################## Prices ##############################
            html.H1('EVM Native tokens price', className = 'left_container_h1'),
            
            html.Div([
                html.P(["Exchange rates to UDS"],className = "title_small"),
                dcc.Dropdown(
                    options = dropdown_options_tokens,
                    value = 'Binance (BNB)',
                    id = 'tokens-selections',
                    placeholder = "Select Tokens",
                    className = "prices-dropdown-table-input"
                ),
                dcc.Graph(
                    config = config, 
                    id = 'evm-tokens-price', 
                ),
            ], className = "single_column"),

            ############################## Template ##############################

            

            #----------------------- Section Title -----------------------#
            #html.H1('Section Title', className = 'left_container_h1'),

            #--------------------- Single Column -----------------------#
            #html.Div([
            #    html.P(["Chart title"],className = "title_small"),
            #    html.Div(["you can put chart here."], className = "note"),
            #], className = "single_column"),

            #----------------------- Two Column -----------------------#
            #html.Div([
            #    html.Div([
            #        html.P(["Chart title"],className = "title_small"),
            #        html.Div(["you can put chart here."], className = "note"),
            #        ], className = "two_column big_colune"),
            #    html.Div([
            #        html.P(["Chart title"],className = "title_small"),
            #        html.Div(["you can put chart here."], className = "note"),
            #        ], className = "two_column small_colune")
            #], className = "two_column_box"),

            

            
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


])

############################### Transactions ###############################

@dash.callback(
    Output('transactions-over-time', 'figure'),

    Output('total-txs', 'children'),
    Output('total-addresses', 'children'),

    Input('date-range-selections', 'value'),
    Input('chain-selections', 'value')
)
def render_transactions(date_range, chain):
    if chain != []:
        current_data = (data.loc[data['CHAIN'].isin(chain)])
        wallets_current = (wallets.loc[wallets['CHAIN'].isin(chain)])
        result_data = total_sum(data.loc[data['CHAIN'].isin(chain)], 'Value', 'CHAIN')
    else:
        return creal_graph(), create_ez_kpi([], [], 'Total & Trend Change', 'Month-over-Month', True), create_ez_kpi([], [], 'Active Wallets', 'Month-over-Month', True)
    
    last_date = (max(current_data['Date(UTC)']))

    if date_range != 'All':
        current_data = (current_data[current_data['Date(UTC)'].between((last_date - timedelta(days = int(date_range))), last_date)])

    wallets_current = wallets_current.reset_index(drop = True)

    line_over_time = create_ez_line(
            current_data, 
            'Date(UTC)', 
            'Value', 
            None,
            'CHAIN', 
            chains_config,
            False,
            []
        )
    total_txs = create_ez_kpi(result_data['CHAIN'], result_data['Value'], 'Total & Trend Change', 'Month-over-Month', True)
    total_addresses = create_ez_kpi(wallets_current['CHAIN'], wallets_current['TOTAL_NEW'].astype(float), 'Total Active Wallets', 'Month-over-Month', True)

    return line_over_time, total_txs, total_addresses

@dash.callback(
    Output('transactions-distribution-week', 'figure'),
    Output('distribution-txs-active', 'children'),
    Output('distribution-txs-passive', 'children'),

    Input('date-range-selections', 'value'),
    Input('chain-selections', 'value')
)
def render_transactions(date_range, chain):
    if chain != []:
        current_data = (data.loc[data['CHAIN'].isin(chain)])
    else:
        return creal_graph(), create_ez_kpi([], [], 'Most Active day', '', True), create_ez_kpi([], [], 'Most Passive day', '', True)
    
    last_date = (max(current_data['Date(UTC)']))

    if date_range != 'All':
        current_data = (current_data[current_data['Date(UTC)'].between((last_date - timedelta(days = int(date_range))), last_date)])

    return transactions_by_day_of_week(current_data, date_range, chains_config)

@dash.callback(
    Output('transactions-distribution', 'figure'),
    Output('distribution-time-zones', 'children'),

    Input('date-range-selections', 'value'),
    Input('chain-selections', 'value')
)
def render_transactions_by_gmt(date_range, chain):
    if chain != []:
        current_data = (gmt_hour_data.loc[gmt_hour_data['CHAIN'].isin(chain)])
    else:
        return creal_graph(), create_ez_kpi([], [], 'Active Time Zones', '', True)

    if date_range != 'All':
        current_data = (current_data[current_data['RANGE'] == int(date_range)])

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
        return creal_graph(), create_ez_kpi([], [], '', '', True), creal_graph()
    
    last_date = (max(current_data['Date(UTC)']))

    if date_range != 'All':
        current_data = (current_data[current_data['Date(UTC)'].between((last_date - timedelta(days = int(date_range))), last_date)])

    active_address_over_time = create_ez_line(
            current_data, 
            'Date(UTC)', 
            'Active addresses', 
            None,
            'CHAIN', 
            chains_config, 
            False,
            []
        )
    ath = find_ath(current_data, 'CHAIN', 'Active addresses', 'Date(UTC)', '')
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
        return creal_graph(), creal_graph(), create_ez_kpi([], [], '', '', True)
    
    last_date = (max(current_data['Date(UTC)']))

    if date_range != 'All':
        current_data = (current_data[current_data['Date(UTC)'].between((last_date - timedelta(days = int(date_range))), last_date)])

    block_time_over_time = create_ez_line(
            current_data, 
            'Date(UTC)', 
            'Block time', 
            None,
            'CHAIN', 
            chains_config, 
            True,
            []
        )
    blocks_over_time = create_ez_line(
            current_data, 
            'Date(UTC)', 
            'Blocks count', 
            None,
            'CHAIN', 
            chains_config, 
            True,
            []
        )
    
    arr_blocks = total_sum(data.loc[data['CHAIN'].isin(chain)], 'Value', 'CHAIN')
    total_blocks_count = create_ez_kpi(arr_blocks['CHAIN'], arr_blocks['Blocks count'], '', '', True)

    return block_time_over_time, blocks_over_time, total_blocks_count


############################### EVM Prices ###############################

@dash.callback(
    Output('evm-tokens-price', 'figure'),

    Input('date-range-selections', 'value'),
    Input('tokens-selections', 'value')
)
def render_prices(date_range, token):
    
    tokens = [token, 'Ethereum (ETH)']

    if tokens != []:
        current_data = (Prices.loc[Prices['TOKEN'].isin(tokens)])
    else:
        return creal_graph()
    
    last_date = (max(current_data['Date(UTC)']))

    if date_range != 'All':
        current_data = (current_data[current_data['Date(UTC)'].between((last_date - timedelta(days = int(date_range))), last_date)])

    current_data = current_data.sort_values(by=['Date(UTC)'])
    current_data = current_data.reset_index(drop = True)

    tokens_data = current_data[current_data['TOKEN'] == 'Ethereum (ETH)'].merge(current_data[current_data['TOKEN'] == token], on = ['Date(UTC)'], how = 'left', indicator = False)

    tokens_data = tokens_data.rename(columns = {
        "PRICE_x": "Ethereum Price", 
        "PRICE_y": "Token Price"
    })

    chart = create_ez_line(
        tokens_data, 
        'Date(UTC)', 
        'Ethereum Price', 
        'Token Price',
        None,
        None, 
        False,
        [((list(filter(lambda xx:xx["chain_name"] == 'Ethereum', chains_config)))[0]["colors"]),((list(filter(lambda xx:xx["token"] == token, chains_config)))[0]["colors"])]
    )
    return chart