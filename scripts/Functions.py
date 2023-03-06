from math import log, floor
import pandas as pd


from dash import html
import plotly.graph_objs as go
import plotly.express as px

kpi_style = {
    'display': 'flex', 
    'align-items': 'center', 
    'justify-content': 'left',
    'margin-top': '10px'
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

def total_transactions_sum(data):
    data_sum = data.groupby('CHAIN').sum()
    data_sum['CHAIN'] = data_sum.index.get_level_values(0)
    data_sum = data_sum.sort_values(by=['Value'], ascending = False)
    data_sum = data_sum.reset_index(drop=True)

    return data_sum

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
                html.Img(src = "assets/" + (chains[j]).lower() + ".png", height = 12),
                html.Span(chains[j], className = "chains_list_kpi"),
                html.Span(number_format(float(values[j])), className = "values_list_kpi"),
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
            #legendgroup = d.name,
            hoverinfo = 'skip',
            showlegend = False,
            #name = d.name + ':<br>' + number_format(d.y[-1])
        )
    if log_scale == True:
        fig_line.update_yaxes(type = "log")
            
    return fig_line