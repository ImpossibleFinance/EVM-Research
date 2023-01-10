import json
import plotly.graph_objs as go
from scripts.Data_API import *


def gmt_data_load():

    f = open('requests_config.json')
    api_config = json.load(f)

    name = "GMT Hour"

    data = data_by_url(
        ((list(filter(lambda x:x["api_name"] == name ,api_config)))[0]["zettablock_api"]),
        ((list(filter(lambda x:x["api_name"] == name ,api_config)))[0]["api_name"])
    )

    f.close()

    return data

def gmt_hour(data):

    f2 = open('chains_config.json')
    chains_config = json.load(f2)

    chains = data["CHAIN"].unique()

    fig = go.Figure()

    for chain in chains:
        data_chain = data[data["CHAIN"] == chain]
        fig.add_trace(go.Bar(
            x = data_chain["GMT_HOUR"], 
            y = data_chain["AVG_TXS_COUNT"],
            name = chain,
            marker_color = ((list(filter(lambda x:x["chain_name"]==chain,chains_config)))[0]["colors"])
            ))

    fig.update_layout(
        title = "Distribution of EVM Transactions by GMT hour (Last 1 month)<br><sup>Distribution of the average number of transactions each GMT hour, to get a separate graph hover your mouse over the desired chain</sup>", 
        xaxis_title = "GMT Hour", 
        yaxis_title = "Average # of Transactions",
        height = 500,
        plot_bgcolor = '#171730',
        paper_bgcolor = '#171730',
        font = dict(color = 'white'),
        showlegend = False
    )

    f2.close()

    return fig, data