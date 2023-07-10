from datetime import timedelta

from scripts.Functions import *

def distribution_bars_horizontal_addresses(data, current_data, x, y, last_date, first_date):

    fig_distribution = go.Figure()

    fig_distribution.add_trace(go.Bar(
        x = data[x], 
        y = data[y],
        orientation = 'h',
        marker_color = '#00C5FF',
        text = (data[x].div(1000)).map('{:,.1f}k'.format),
        textposition = 'inside',
        hovertemplate = '%{y}<extra></extra>',
        name = "Last month: " + str(last_date - timedelta(days = 30)).replace('00:00:00', '') + "-- " + str(last_date).replace('00:00:00', '')
    ))

    fig_distribution.add_trace(go.Bar(
        x = current_data[x], 
        y = current_data[y],
        orientation = 'h',
        marker_color = '#30F8F8',
        text = (current_data[x].div(1000)).map('{:,.1f}k'.format),
        textposition = 'inside',
        hovertemplate = '%{y}<extra></extra>',
        name = "Time range: " + str(first_date).replace('00:00:00', '') + "-- " + str(last_date).replace('00:00:00', '')
    ))
            
    fig_distribution.update_layout(
        xaxis_title = x, 
        yaxis_title = y,
        height = 500,
        plot_bgcolor = '#171730',
        paper_bgcolor = '#171730',
        font = dict(color = 'white'),
        legend = {
            'orientation': 'h',
            'xanchor': 'center',
            'yanchor': 'top',
            'x': 0.5,
            'y': -0.2
        }
    )

    return fig_distribution

def active_addresses(data, current_data):
    last_date = (max(data['Date(UTC)']))
    last_month_data = (data[data['Date(UTC)'].between((last_date - timedelta(days = 30)), last_date)])

    last_month_data_avg = average(last_month_data, 'Active addresses', 'CHAIN')
    last_month_current_data_avg = average(current_data, 'Active addresses', 'CHAIN')

    first_date = (min(current_data['Date(UTC)']))

    fig_data = distribution_bars_horizontal_addresses(last_month_data_avg, last_month_current_data_avg, 'Active addresses', 'CHAIN', last_date, first_date)

    return fig_data