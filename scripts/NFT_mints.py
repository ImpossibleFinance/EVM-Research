import json
import plotly.graph_objs as go
from plotly.subplots import make_subplots



def nft_mints(data):

    f2 = open('chains_config.json')
    chains_config = json.load(f2)

    chains = data["CHAIN"].unique()

    data_sum = data.groupby('CHAIN').sum()
    data_sum['CHAIN'] = data_sum.index.get_level_values(0)
    data_sum['Color'] = [(list(filter(lambda x:x["chain_name"] == (y.split(" "))[0] ,chains_config)))[0]['colors'] for y in data_sum.index]

    data_sum = data_sum.reset_index(drop=True)

    fig = make_subplots(
        rows = 1, 
        cols = 2, 
        column_widths = [0.85, 0.15],
        specs=[[{'type':'xy'}, {'type':'domain'}]]
    )

    for chain in chains:
        data_chain = data[data["CHAIN"] == chain]
        fig.add_trace(go.Scatter(
            x = data_chain["Date(UTC)"], 
            y = data_chain["mints"],
            name = chain,
            marker_color = ((list(filter(lambda x:x["chain_name"] == (chain.split(" "))[0],chains_config)))[0]["colors"])
            ), 
            row = 1, col = 1)

    fig.add_trace(go.Pie(
        labels = data_sum['CHAIN'], 
        values = data_sum['mints'], 
        name = "Total Unique NFTs count", 
        marker_colors = data_sum['Color'], 
        showlegend=False, 
        marker_line = dict(color='#000000', width=2)
        ), row = 1, col = 2)

    fig.update_layout(
        title = "Daily New NFT<br><sup>Daily number of New NFTs (ERC-721 & ERC-1155) and total unique NFTs</sup>", 
        xaxis_title = "Date", 
        yaxis_title = "NFTs",
        height = 500,
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


    f2.close()

    return fig