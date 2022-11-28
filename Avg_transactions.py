import json
import plotly.graph_objs as go
from Data_API import *


def transactions_by_chain_by_time():
    f = open('api_config.json')
    api_config = json.load(f)

    data = data_by_url(((list(filter(lambda x:x["api_name"]=="Txs by time and chain",api_config)))[0]["chains_api"]))

    fig = go.Figure()
    _columns = ['1M Value', '3M Value', '6M Value', '1Y Value']
    _color = ['#FF0000', '#F7FF00', '#08FF00', '#00AAFF']

    for x in range (len(_columns)):
        fig.add_trace(go.Bar(
            x = data[_columns[x]],
            y = data['Chain'],
            orientation='h',
            name = 'Last ' + _columns[x][:3],
            marker_color = _color[x],
            text = ['Last ' + _columns[x][:3] + ' : ' + "%.2f" %(v/1e6) + 'M' for v in data[_columns[x]]],
            textposition = 'inside'
        ))

    fig.update_layout(
        title = "Average daily transactions", 
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