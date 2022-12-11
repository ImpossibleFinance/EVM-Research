import json
import plotly.graph_objs as go
from scripts.Data_API import *
import numpy as np


def bridges_activity():
    name = "Bridges Activity"

    f = open('requests_config.json')
    api_config = json.load(f)

    data = data_by_url(
        ((list(filter(lambda x:x["api_name"] == name ,api_config)))[0]["zettablock_api"]),
        ((list(filter(lambda x:x["api_name"] == name ,api_config)))[0]["api_name"])
    )

    data_avg_by_bridge = data.groupby('name').mean()
    data_avg_by_bridge['name'] = data_avg_by_bridge.index.get_level_values(0)
    data_avg_by_bridge = data_avg_by_bridge.reset_index(drop=True)

    data = data.sort_values(by=['name'])
    data_avg_by_bridge = data_avg_by_bridge.sort_values(by=['name'])

    bridges = data["name"].unique()
    bridges = np.append(['Ethereum'], bridges)

    fig = go.Figure()

    fig.add_trace(go.Sankey(
        valueformat = ".0f",
        valuesuffix = " Transfers",
        node = {
            "label": bridges,
            "pad": 10
        },
        link = dict(
            source = [0 for i in range(len(bridges)-1)],
            target = [i for i in range(1,len(bridges))],
            value = [k for k in data_avg_by_bridge['TRANSFERS']],
            customdata = ["{:,.2f}".format(round(j, 1)) for j in data_avg_by_bridge['USD_VALUE']],

            hovertemplate = 'This way has average transfers:  %{value}'+
            '<br /> and average USD value %{customdata}<extra></extra>',
        )
    ))

    fig.update_layout(
        title = "ERC-20 token transfers to different bridges<br><sup>Average transfers was calculated for all ERC-20 transfers for last 90 days .But USD Value only for stablecoins (such as USDC, USDT, BUSD, DAI and etc.)</sup>", 
        height = 800,
        plot_bgcolor = '#171730',
        paper_bgcolor = '#171730',
        font = dict(color = 'white'),
        showlegend = False
    )

    return fig, data, data_avg_by_bridge['name']