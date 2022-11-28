import json
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
from plotly import tools
from Data_API import *


def blocks():
    f = open('api_config.json')
    api_config = json.load(f)

    f2 = open('chains_config.json')
    chains_config = json.load(f2)

    data = data_by_url(((list(filter(lambda x:x["api_name"]=="Blocks",api_config)))[0]["chains_api"]))

    chains = data["Chain"].unique()

    fig = go.Figure()
    fig2 = go.Figure()

    for chain in chains:
        data_chain = data[data["Chain"] == chain]
        fig.add_trace(go.Scatter(
            x = data_chain["Date(UTC)"], 
            y = data_chain["Block time"],
            name = chain,
            marker_color = ((list(filter(lambda x:x["chain_name"]==chain,chains_config)))[0]["colors"])
            ))

        fig2.add_trace(go.Scatter(
            x = data_chain["Date(UTC)"], 
            y = data_chain["Blocks count"],
            name = chain,
            marker_color = ((list(filter(lambda x:x["chain_name"]==chain,chains_config)))[0]["colors"])
            ))

    fig.update_layout(
        title = "Average block time", 
        xaxis_title = "Date", 
        yaxis_title = "Time [s]",
        height = 500,
        plot_bgcolor = '#171730',
        paper_bgcolor = '#171730',
        font = dict(color = 'white')
        #template = 'plotly_dark'
    )

    fig2.update_layout(
        title = "Blocks count", 
        xaxis_title = "Date", 
        yaxis_title = "Blocks",
        height = 500,
        plot_bgcolor = '#171730',
        paper_bgcolor = '#171730',
        font = dict(color = 'white')
        #template = 'plotly_dark'
    )

    fig.update_xaxes(
        #rangeslider_visible=True,
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
    
    fig2.update_xaxes(
        #rangeslider_visible=True,
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
    f2.close()

    return fig, fig2