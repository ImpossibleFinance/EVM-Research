import json
import plotly.graph_objs as go
from datetime import timedelta

from scripts.Functions import *

def active_addresses(data):

    f = open('chains_config.json')
    chains_config = json.load(f)

    chains = data["CHAIN"].unique()

    fig_addresses = go.Figure()

    for chain in chains:
        data_chain = data[data["CHAIN"] == chain]
        fig_addresses.add_trace(go.Scatter(
            x = data_chain["Date(UTC)"], 
            y = data_chain["Active addresses"],
            name = chain,
            showlegend = False,
            marker_color = ((list(filter(lambda x:x["chain_name"]==chain,chains_config)))[0]["colors"])
            ))

    fig_addresses.update_layout(
        title = "EVM Active addresses over time<br><sup>Daily number of active addresses - i.e. unique senders of transactions</sup>", 
        xaxis_title = "Date", 
        yaxis_title = "Addresses",
        height = 700,
        plot_bgcolor = '#171730',
        paper_bgcolor = '#171730',
        hovermode = "x unified",
        font = dict(color = 'white')
    )

    fig_addresses.update_xaxes(
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="month", stepmode="backward"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(count=5, label="5y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    fig_addresses.update_layout(xaxis=dict(rangeselector = dict(font = dict( color = "black"))))

    for i, d in enumerate(fig_addresses.data):
        fig_addresses.add_scatter(
            x = [d.x[-1]], 
            y = [d.y[-1]],
            mode = 'markers',
            marker = dict(color = d.marker.color, size = 10),
            legendgroup = d.name,
            hoverinfo = 'skip',
            name = d.name + ':<br>' + number_format(d.y[-1])
        )

    fig_addresses.update_layout(
        legend_title = "Last value:",
    )
    fig_addresses.update_xaxes(range = [min(data['Date(UTC)']), max(data['Date(UTC)'] + timedelta(days = 14))])

    f.close()

    return fig_addresses


def average_addresses(data):

    data = data.sort_values(by=['CHAIN'])

    last_date = (max(data['Date(UTC)']))

    ath_text = []
    ath_addresses = []
    ath_chain = data["CHAIN"].unique()

    for chain in ath_chain:
        id_max = data[data["CHAIN"] == chain]['Active addresses'].idxmax()

        ath_addresses.append(data['Active addresses'][id_max])

        text_temp = chain + '. ATH of daily active wallets was ' + str(number_format(data['Active addresses'][id_max])) + ' ( ' + str(data['Date(UTC)'][id_max]).split(" ")[0] + ' ) '
        ath_text.append(text_temp)

    _columns = ['Value_1M', 'Value_6M', 'Value_1Y']
    _days = [30, 180, 365]

    # Average addresses

    fig_avg = go.Figure()


    for i in range (len(_columns)):
        (globals()[_columns[i]]) = (data[data['Date(UTC)'].between((last_date - timedelta(days = _days[i])), last_date)]).groupby('CHAIN').mean()
        (globals()[_columns[i]])['CHAIN'] = (globals()[_columns[i]]).index.get_level_values(0)
        (globals()[_columns[i]]) = (globals()[_columns[i]]).reset_index(drop=True)


        fig_avg.add_trace(
            go.Bar(
                x = (globals()[_columns[i]])['Active addresses'],
                y = (globals()[_columns[i]])['CHAIN'],
                text = ((globals()[_columns[i]])["Active addresses"].div(1000)).map('{:,.1f}k'.format),
                orientation = "h",
                hovertemplate = 'Last ' + _columns[i][-2:] + ': %{text}<extra></extra>'
            )
        )

    fig_avg.add_trace(
        go.Bar(
            x = ath_addresses,
            y = ath_chain,
            text = ath_text,
            textposition = "inside",
            textfont = dict(
                color="white"
            ),
            orientation = "h",
            marker_color = "grey",
            hoverinfo = 'skip',
            insidetextanchor = "middle"
        )
    )

    fig_avg.update_layout(
        title = "Average number of addresses<br><sup>Average number of daily active wallets for different time ranges</sup>",
        barmode = "group", 
        showlegend = False, 
        template = "presentation",
        height = 900,
        plot_bgcolor = '#171730',
        paper_bgcolor = '#171730',
        font = dict(color = 'white')
    )

    fig_avg.update_yaxes(
        tickmode = "array",
        categoryorder = "total ascending",
        showticklabels = False,
        tickfont = dict(color = "white"),
    )

    fig_avg.update_xaxes(
        showticklabels = False,
        type = "log"
    )

    return fig_avg


def trend_address(data):

    f = open('chains_config.json')
    chains_config = json.load(f)

    fig_trend = go.Figure()

    chains = data["CHAIN"].unique()

    for chain in chains:
        data_chain = data[data["CHAIN"] == chain]
        fig_trend.add_trace(go.Scatter(
                x = data_chain["Date(UTC)"], 
                y = get_trend(data_chain['Active addresses'], 3),
                name = chain,
                showlegend = False,
                marker_color = ((list(filter(lambda x:x["chain_name"]==chain,chains_config)))[0]["colors"])
                ))

    fig_trend.update_layout(
        title = "EVM Active daily addresses trend<br><sup>For right part of this chart - green color is an up trend for daily active wallets and red is down trend.</sup>", 
        xaxis_title = "Date", 
        yaxis_title = "Addresses",
        height = 700,
        plot_bgcolor = '#171730',
        paper_bgcolor = '#171730',
        hovermode = "x unified",
        font = dict(color = 'white')
    )


    fig_trend_txt = go.Figure()

    k = 0

    for chain in chains:
        data_chain = data[data["CHAIN"] == chain]

        y_trend = get_trend(data_chain['Active addresses'], 3)
        
        fig_trend_txt.add_trace(go.Indicator(
            mode = "delta",
            value = y_trend.iloc[-1],
            delta = {'reference': y_trend.iloc[-30], 'relative': False},
            domain = {'row': k, 'column': 1},
            title = dict(
                text = chain
            ),
            ))

        k += 1

    fig_trend_txt.update_layout(
        title = "Trend now<br><sup>Value is a delta for last one month</sup>", 
        height = 700,
        plot_bgcolor = '#171730',
        paper_bgcolor = '#171730',
        font = dict(color = 'white'),
        grid = {'rows': k, 'columns': 1, 'pattern': "independent"}
    )

    f.close()

    return fig_trend, fig_trend_txt