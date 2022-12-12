import json
import plotly.graph_objs as go
from scripts.Data_API import *


def transactions_by_chain_by_time():
    f = open('requests_config.json')
    api_config = json.load(f)

    name = "Distribution by time and chain"

    data = data_by_url(
        ((list(filter(lambda x:x["api_name"] == name ,api_config)))[0]["zettablock_api"]),
        ((list(filter(lambda x:x["api_name"] == name ,api_config)))[0]["api_name"])
    )

    fig = go.Figure()
    _columns = ['Value_1M', 'Value_3M', 'Value_6M', 'Value_1Y']
    _color = ['#FF0000', '#F7FF00', '#08FF00', '#00AAFF']

    for x in range (len(_columns)):
        fig.add_trace(go.Bar(
            x = data[_columns[x]],
            y = data['Chain'],
            orientation='h',
            name = 'Last ' + _columns[x][-2:],
            marker_color = _color[x],
            text = ['Last ' + _columns[x][-2:] + ' : ' + "%.2f" %(v/1e6) + 'M' for v in data[_columns[x]]],
            textposition = 'inside'
        ))

    fig.update_layout(
        title = "Average daily transactions<br><sup>Comparison of the average number of transactions in different periods</sup>", 
        xaxis_title = "Average daily txs", 
        yaxis_title = "Chain",
        height = 700,
        plot_bgcolor = '#171730',
        paper_bgcolor = '#171730',
        font = dict(color = 'white'),
        barmode='group'
        #template = 'plotly_dark'
    )

    f.close()

    return fig