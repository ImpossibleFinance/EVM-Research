import json
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
from scripts.Data_API import *


def stablecoins_data():

    name_symbol = "Stablecoins by symbol"
    name_type = "Stablecoins by type"

    f = open('requests_config.json')
    api_config = json.load(f)


    data_symbol = data_by_url(
        ((list(filter(lambda x:x["api_name"] == name_symbol ,api_config)))[0]["zettablock_api"]),
        ((list(filter(lambda x:x["api_name"] == name_symbol ,api_config)))[0]["api_name"])
    )

    data_type = data_by_url(
        ((list(filter(lambda x:x["api_name"] == name_type ,api_config)))[0]["zettablock_api"]),
        ((list(filter(lambda x:x["api_name"] == name_type ,api_config)))[0]["api_name"])
    )

    f.close()

    return data_symbol, data_type


def stablecoins_charts(data_by_type):

    unique_types = data_by_type['stable'].unique()

    todays_data_by_type = data_by_type[data_by_type["Date(UTC)"] == data_by_type["Date(UTC)"][max(data_by_type.index)]]
    todays_data_by_type = todays_data_by_type.sort_values(by=['TVL_eth_by_type'])
    todays_data_by_type = todays_data_by_type.reset_index(drop=True)

    fig = make_subplots(
        rows = 1, 
        cols = 2, 
        column_widths = [0.80, 0.20],
        specs=[[{'type':'xy'}, {'type':'xy'}]]
    )

    for type in unique_types:
        data_chain = data_by_type[data_by_type["stable"] == type]
        fig.add_trace(go.Scatter(
            x = data_chain["Date(UTC)"], 
            y = data_chain["TVL_eth_by_type"],
            name = type,
            showlegend = False,
            ), row = 1, col = 1)

    fig.add_trace(go.Bar(
        x = todays_data_by_type['stable'],
        y = todays_data_by_type['TVL_eth_by_type'],
        name = '',
        marker_color = '#F05DF2',
        showlegend = False
    ), row = 1, col = 2)

    fig.update_layout(
        title = "Stablecoins supply by type<br><sup></sup>", 
        xaxis_title = "Date", 
        yaxis_title = "Supply (USD)",
        height = 600,
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


    return fig

def stablecoins_callback(data_by_tokens):
    unique_symbols = data_by_tokens['symbol'].unique()

    fig = go.Figure()

    for symbol in unique_symbols:
        data_token = data_by_tokens[data_by_tokens["symbol"] == symbol]
        fig.add_trace(go.Scatter(
            x = data_token["Date(UTC)"], 
            y = data_token["TVL_eth_by_symbol"],
            name = symbol,
            showlegend = False
            ))

    fig.update_layout(
        title = "Stablecoins supply by symbol<br><sup></sup>", 
        xaxis_title = "Date", 
        yaxis_title = "Supply (USD)",
        height = 600,
        plot_bgcolor = '#171730',
        paper_bgcolor = '#171730',
        font = dict(color = 'white')
    )

    return fig