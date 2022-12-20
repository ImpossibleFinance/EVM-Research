import json
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from scripts.Data_API import *
from scripts.Main_table import *

def active_addresses(data):

    f = open('chains_config.json')
    chains_config = json.load(f)

    chains = data["CHAIN"].unique()

    data_last_month_avg = last_month_addresses(data)[0]
    data_last_month_avg = data_last_month_avg.sort_values(by=['Active addresses'])

    fig = make_subplots(
        rows = 1, 
        cols = 2, 
        column_widths = [0.65, 0.35],
        specs=[[{'type':'xy'}, {'type':'xy'}]]
    )

    for chain in chains:
        data_chain = data[data["CHAIN"] == chain]
        fig.add_trace(go.Scatter(
            x = data_chain["Date(UTC)"], 
            y = data_chain["Active addresses"],
            name = chain,
            showlegend = False,
            marker_color = ((list(filter(lambda x:x["chain_name"]==chain,chains_config)))[0]["colors"])
            ), 
            row = 1, col = 1)

    fig.add_trace(go.Bar(
        x = data_last_month_avg['CHAIN'],
        y = data_last_month_avg['Active addresses'],
        name = '1M AVG',
        marker_color = '#FFD800',
        showlegend=False
    ), row = 1, col = 2)

    fig.update_layout(
        title = "EVM Active addresses over time<br><sup>Daily number of active addresses - i.e. unique senders of transactions</sup>", 
        xaxis_title = "Date", 
        yaxis_title = "Addresses",
        height = 500,
        plot_bgcolor = '#171730',
        paper_bgcolor = '#171730',
        font = dict(color = 'white')
    )

    fig.update_xaxes(
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
    fig.update_layout(xaxis=dict(rangeselector = dict(font = dict( color = "black"))))

    f.close()

    return fig