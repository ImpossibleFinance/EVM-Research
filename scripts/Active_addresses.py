import json
import plotly.graph_objs as go
from scripts.Data_API import *


def active_addresses(data):

    f = open('chains_config.json')
    chains_config = json.load(f)

    chains = data["Chain"].unique()

    fig = go.Figure()

    for chain in chains:
        data_chain = data[data["Chain"] == chain]
        fig.add_trace(go.Scatter(
            x = data_chain["Date(UTC)"], 
            y = data_chain["Active addresses"],
            name = chain,
            marker_color = ((list(filter(lambda x:x["chain_name"]==chain,chains_config)))[0]["colors"])
            ))

    fig.update_layout(
        title = "EVM Active addresses over time", 
        xaxis_title = "Date", 
        yaxis_title = "Addresses",
        height = 500,
        plot_bgcolor = '#171730',
        paper_bgcolor = '#171730',
        font = dict(color = 'white')
    )

    f.close()

    return fig