import json
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from Data_API import *


def gmt_hour():
    f = open('api_config.json')
    api_config = json.load(f)

    f2 = open('chains_config.json')
    chains_config = json.load(f2)

    data = data_by_url(((list(filter(lambda x:x["api_name"]=="GMT Hour",api_config)))[0]["chains_api"]))
    chains = data["Chain"].unique()

    fig = make_subplots(
        rows = 1, 
        cols = 2, 
        column_widths = [0.8, 0.2],
        specs=[[{'type':'xy'}, {'type':'xy'}]]
    )

    for chain in chains:
        data_chain = data[data["Chain"] == chain]
        fig.add_trace(go.Bar(
            x = data_chain["GMT hour"], 
            y = data_chain["Sum of transactions"],
            name = chain,
            marker_color = ((list(filter(lambda x:x["chain_name"]==chain,chains_config)))[0]["colors"])
            ), 
            row = 1, col = 1)

    fig.update_layout(
        title = "Distribution of EVM Transactions by GMT hour", 
        xaxis_title = "GMT Hour", 
        yaxis_title = "Transactions",
        height = 500,
        plot_bgcolor = '#171730',
        paper_bgcolor = '#171730',
        font = dict(color = 'white')
    )

    f.close()
    f2.close()

    return fig