import json
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
from plotly import tools
from scripts.Data_API import *


def blocks(data):

    f = open('chains_config.json')
    chains_config = json.load(f)


    chains = data["Chain"].unique()

    todays_data = data[data["Date(UTC)"] == data["Date(UTC)"][max(data.index)]]
    todays_data = todays_data.reset_index(drop=True)

    fig = make_subplots(
        rows = 1, 
        cols = 2, 
        column_widths = [0.2, 0.8],
        specs=[[{'type':'xy'}, {'type':'xy'}]]
    )

    fig2 = go.Figure()

    for chain in chains:
        data_chain = data[data["Chain"] == chain]
        fig.add_trace(go.Scatter(
            x = data_chain["Date(UTC)"], 
            y = data_chain["Block time"],
            name = chain,
            marker_color = ((list(filter(lambda x:x["chain_name"]==chain,chains_config)))[0]["colors"])
            ), 
            row = 1, col = 2)

        fig2.add_trace(go.Scatter(
            x = data_chain["Date(UTC)"], 
            y = data_chain["Blocks count"],
            name = chain,
            marker_color = ((list(filter(lambda x:x["chain_name"]==chain,chains_config)))[0]["colors"])
            ))

    fig.add_trace(go.Bar(
        x = todays_data['Chain'],
        y = todays_data['Block time'],
        name = '',
        marker_color = '#0CFF00',
        showlegend=False
    ), row = 1, col = 1)

    fig.update_layout(
        title = "Average block time", 
        yaxis_title = "Time [s]",
        height = 500,
        plot_bgcolor = '#171730',
        paper_bgcolor = '#171730',
        font = dict(color = 'white')
    )

    fig2.update_layout(
        title = "Blocks count", 
        xaxis_title = "Date", 
        yaxis_title = "Blocks",
        height = 500,
        plot_bgcolor = '#171730',
        paper_bgcolor = '#171730',
        font = dict(color = 'white')
    )

    fig2.update_xaxes(
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
    fig2.update_layout(xaxis=dict(rangeselector = dict(font = dict( color = "black"))))
    

    f.close()

    return fig, fig2