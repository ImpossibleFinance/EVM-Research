import dash
from dash import html, Input, Output, dcc
from datetime import timedelta


from scripts.Functions import *
from config_app import *
from scripts.distribution_by_day_of_week import *
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
        html.Img(src = "assets/IF.png", alt = " ", className = "if-ico"),
        html.Div([
            html.H1(['Impossible Finance'],className = "impossible-description"),
            html.H2(['DATA LAB'],className = "data-lab-description"),
        ])
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
        html.H2('Filter Criteria'),
        html.Br(),
        html.P('Blockchain'),

        dcc.Dropdown(
            options = dropdown_options,
            value = ['BNB Chain', 'Polygon'],
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

    html.Div([
        html.Div(className = "kpi_container", id = 'total-txs'),
        html.Div(className = "kpi_container", id = 'total-addresses'),


        html.H1('Transactions', className = 'left_container_h1'),
        dcc.Graph(
            config = config, 
            id = 'transactions-over-time', 
        ),

        html.Div(className = "kpi_container", id = 'distribution-txs-active'),
        html.Div(className = "kpi_container", id = 'distribution-txs-passive'),

        dcc.Graph(
            config = config, 
            id = 'transactions-distribution-week'
        )#,

        #dcc.Graph(
        #    config = config, 
        #    id = 'transactions-distribution'
        #)
    ], className = "left_container")

])


#callback for rendering by category

@dash.callback(
    Output('transactions-over-time', 'figure'),
    Input('date-range-selections', 'value'),
    Input('chain-selections', 'value')
)
def render_transactions(date_range, chain):
    current_data = (data.loc[data['CHAIN'].isin(chain)])
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
    result_data = total_transactions_sum(data.loc[data['CHAIN'].isin(chain)])

    return kpi(result_data['CHAIN'], result_data['Value'], 'Total & Trend Change', 'Month-over-Month'), kpi(result_data['CHAIN'], result_data['Active addresses'], 'Active Wallets', 'Month-over-Month')

@dash.callback(
    Output('transactions-distribution-week', 'figure'),
    Output('distribution-txs-active', 'children'),
    Output('distribution-txs-passive', 'children'),
    Input('date-range-selections', 'value'),
    Input('chain-selections', 'value')
)
def render_transactions_day_of_week(date_range, chain):
    current_data = (data.loc[data['CHAIN'].isin(chain)])
    last_date = (max(current_data['Date(UTC)']))

    if date_range != 'All':
        current_data = (current_data[current_data['Date(UTC)'].between((last_date - timedelta(days = int(date_range))), last_date)])
    
    return transactions_by_day_of_week(current_data, date_range, chains_config)

@dash.callback(
    Output('transactions-distribution', 'figure'),
    Input('chain-selections', 'value')
)
def render_transactions(chain):
    current_data = (gmt_hour_data.loc[gmt_hour_data['CHAIN'].isin(chain)])

    return distribution_bars(current_data, 'GMT_HOUR', 'AVG_TXS_COUNT', 'CHAIN', chains_config, 'Distribution of EVM transactions by GMT hour', False)
