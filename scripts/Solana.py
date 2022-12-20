import json
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
from scripts.Data_API import *


def solana_upload():

    name = "Solana Metrics"

    f = open('requests_config.json')
    api_config = json.load(f)


    data = data_by_url(
        ((list(filter(lambda x:x["api_name"] == name ,api_config)))[0]["zettablock_api"]),
        ((list(filter(lambda x:x["api_name"] == name ,api_config)))[0]["api_name"])
    )

    f.close()

    return data

def non_evm_metrics(data_evm, data_non_evm):
    f = open('chains_config.json')
    chains_config = json.load(f)

    emv_chain = data_evm['CHAIN'].unique()[0]
    non_evm_chain = data_non_evm['CHAIN'].unique()[1]

    fig = go.Figure()
    fig2 = go.Figure()

    fig.add_trace(go.Scatter(
        x = data_evm["Date(UTC)"], 
        y = data_evm["Value"],
        name = emv_chain,
        showlegend = False,
        marker_color = ((list(filter(lambda x:x["chain_name"] == emv_chain,chains_config)))[0]["colors"])
        ))

    fig.add_trace(go.Scatter(
        x = data_non_evm["Date(UTC)"], 
        y = data_non_evm["VALUE"],
        name = non_evm_chain,
        showlegend = False,
        marker_color = ((list(filter(lambda x:x["chain_name"]== non_evm_chain,chains_config)))[0]["colors"])
        ))

    fig2.add_trace(go.Scatter(
        x = data_evm["Date(UTC)"], 
        y = data_evm["Active addresses"],
        name = emv_chain,
        showlegend = False,
        marker_color = ((list(filter(lambda x:x["chain_name"] == emv_chain,chains_config)))[0]["colors"])
        ))

    fig2.add_trace(go.Scatter(
        x = data_non_evm["Date(UTC)"], 
        y = data_non_evm["ADDRESSES"],
        name = non_evm_chain,
        showlegend = False,
        marker_color = ((list(filter(lambda x:x["chain_name"]== non_evm_chain,chains_config)))[0]["colors"])
        ))

    fig.update_layout(
        title = "EVM and Non-EVM Transactions over time", 
        xaxis_title = "Date", 
        yaxis_title = "Transactions",
        height = 500,
        plot_bgcolor = '#171730',
        paper_bgcolor = '#171730',
        font = dict(color = 'white')
    )

    fig2.update_layout(
        title = "EVM and Non-EVM Active Addresses over time", 
        xaxis_title = "Date", 
        yaxis_title = "Users",
        height = 500,
        plot_bgcolor = '#171730',
        paper_bgcolor = '#171730',
        font = dict(color = 'white')
    )

    fig.update_yaxes(type = "log")
    fig2.update_yaxes(type = "log")

    f.close()

    return fig, fig2

def non_evm_prices(price_data, data_non_evm):

    f = open('chains_config.json')
    tokens_config = json.load(f)

    emv_chain = price_data['TOKEN'].unique()[0]
    non_evm_chain = data_non_evm['TOKEN'].unique()[1]

    for item in tokens_config:
        if item['token'] == non_evm_chain:
            token_color = item['colors']
        if item['token'] == emv_chain:
            eth_color = item['colors']
    
    fig = make_subplots(specs = [[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            x = price_data['Date(UTC)'],
            y = price_data['PRICE'],
            name = str(emv_chain) + " price",
            marker_color = eth_color
        ),
        secondary_y = False,
    )

    fig.add_trace(
        go.Scatter(
            x = data_non_evm['Date(UTC)'],
            y = data_non_evm['PRICE'],
            name = str(non_evm_chain) + " price",
            marker_color = token_color
        ),
        secondary_y = True,
    )

    fig.update_layout(
        title = "EVM and Non-EVM native token prices<br><sup></sup>", 
        xaxis_title = "Date", 
        xaxis_tickangle = 30,
        #title = dict( x = 0.5),
        xaxis_tickfont = dict(size = 9),
        yaxis_tickfont = dict(size = 9),
        plot_bgcolor = '#171730',
        paper_bgcolor = '#171730',
        font = dict(color = 'white'),
        showlegend = False
    )

    f.close()

    return fig

def solana(non_evm_data, data, price_data):
    data_ethereum = data[data["CHAIN"] == "Ethereum"]
    data_price_ethereum = price_data[price_data["TOKEN"] == "Ethereum (ETH)"]
    data_ethereum = data_ethereum.reset_index(drop=True)
    data_price_ethereum = data_price_ethereum.reset_index(drop=True)

    fig_transactions, fig_addresses = non_evm_metrics(data_ethereum, non_evm_data)

    fig_non_evm_price = non_evm_prices(data_price_ethereum, non_evm_data)


    return fig_transactions, fig_addresses, fig_non_evm_price