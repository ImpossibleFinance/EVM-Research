from math import log, floor
import pandas as pd

from dash import html
import plotly.graph_objs as go

kpi_style = {
    'display': 'flex', 
    'align-items': 'center', 
    'justify-content': 'left',
    'margin-top': '16px'
}

def number_format(number):
    units = ['', 'K', 'M', 'B', 'T', 'P']
    k = 1000.0
    magnitude = int(floor(log(number, k)))
    return '%.2f%s' % (number / k**magnitude, units[magnitude])

def read_data_from_csv(path):
    df = pd.read_csv(path)

    if 'Date(UTC)' in df:
        df['Date(UTC)'] = pd.to_datetime(pd.to_datetime(df['Date(UTC)']).dt.strftime('%Y-%m-%d'))
    
    return df

def total_sum(data, value, group_by):
    data_sum = data.groupby(group_by).sum()
    data_sum[group_by] = data_sum.index.get_level_values(0)
    data_sum = data_sum.sort_values(by = [value], ascending = False)
    data_sum = data_sum.reset_index(drop=True)

    return data_sum

def average(data, value, group_by):

    data_average  = data.groupby([group_by]).mean()
    data_average[group_by] = data_average.index.get_level_values(0)
    data_average = data_average.sort_values(by = [value], ascending = False)
    data_average = data_average.reset_index(drop=True)

    return data_average

def find_ath(data, group_by, max_index, max_over_index):

    groups = data[group_by].unique()
    
    ath = []
    chains = []

    for group in groups:
        data_group = data[data[group_by] == group]

        idmax = data_group[max_index].idxmax()

        ath_stat = number_format(float(data_group[max_index][idmax])) + ' - ' + (str(data_group[max_over_index][idmax])).replace('00:00:00', '')
        ath.append(ath_stat)
        chains.append(group)

    return kpi(chains, ath, 'ATH of Daily Active Wallets', '')


#######################################################
##################  Charts  ###########################
#######################################################




def kpi(chains, values, title, subtitle):

    if len(chains) != len(values):
        print("errorrrrr")
        return None

    div_output = []

    for j in range(len(chains)):
        div_output.append(
            html.Span([
                html.Img(src = "assets/" + (chains[j]).lower() + ".png", height = 22),
                html.Span(chains[j], className = "chains_list_kpi"),
                html.Span(number_format(float(values[j])), className = "values_list_kpi") if type(values[j]) != str else html.Span(values[j], className = "values_list_kpi"),
            ], style = kpi_style
            ),
        )

    counter = html.Div([
        html.H1(children = title),
        html.H3(children = subtitle),
        html.Div(children = div_output)
    ], className = "card_container"),

    return counter


def fig_line_over_time(data, x, y, group_by, config, title, log_scale):
    fig_line = go.Figure()

    groups = data[group_by].unique()

    if config != False:
        for group in groups:
            data_group = data[data[group_by] == group]
            fig_line.add_trace(go.Scatter(
                x = data_group[x], 
                y = data_group[y],
                name = group,
                showlegend = False,
                marker_color = ((list(filter(lambda xx:xx["chain_name"] == group, config)))[0]["colors"])
                ))
    else:
        for group in groups:
            data_group = data[data[group_by] == group]
            fig_line.add_trace(go.Scatter(
                x = data_group[x], 
                y = data_group[y],
                name = group,
                showlegend = False,
                ))
            
    fig_line.update_layout(
        title = title, 
        xaxis_title = x, 
        yaxis_title = y,
        height = 500,
        hovermode = "x unified",
        plot_bgcolor = '#171730',
        paper_bgcolor = '#171730',
        font = dict(color = 'white'),
    )

    for i, d in enumerate(fig_line.data):
        fig_line.add_scatter(
            x = [d.x[-1]], 
            y = [d.y[-1]],
            mode = 'markers',
            marker = dict(color = d.marker.color, size = 10),
            hoverinfo = 'skip',
            showlegend = False,
        )
    if log_scale == True:
        fig_line.update_yaxes(type = "log")
            
    return fig_line



def distribution_bars(data, x, y, group_by, config, title, log_scale):

    groups = data[group_by].unique()

    fig_distribution = go.Figure()

    if config != False:
        for group in groups:
            data_group = data[data[group_by] == group]
            fig_distribution.add_trace(go.Bar(
                x = data_group[x], 
                y = data_group[y],
                name = group,
                marker_color = ((list(filter(lambda xx:xx["chain_name"] == group, config)))[0]["colors"])
                ))
            
    else:
        for group in groups:
            data_group = data[data[group_by] == group]
            fig_distribution.add_trace(go.Bar(
                x = data_group[x], 
                y = data_group[y],
                name = group,
                ))
            
    fig_distribution.update_layout(
        title = title, 
        xaxis_title = x, 
        yaxis_title = y,
        height = 500,
        hovermode = "x unified",
        plot_bgcolor = '#171730',
        paper_bgcolor = '#171730',
        font = dict(color = 'white'),
        showlegend = False
    )

    return fig_distribution