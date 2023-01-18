import json
import plotly.graph_objs as go

def gmt_hour(data):

    f2 = open('chains_config.json')
    chains_config = json.load(f2)

    chains = data["CHAIN"].unique()

    fig_distribution = go.Figure()

    for chain in chains:
        data_chain = data[data["CHAIN"] == chain]
        fig_distribution.add_trace(go.Bar(
            x = data_chain["GMT_HOUR"], 
            y = data_chain["AVG_TXS_COUNT"],
            name = chain,
            marker_color = ((list(filter(lambda x:x["chain_name"]==chain,chains_config)))[0]["colors"])
            ))

    fig_distribution.update_layout(
        title = "Distribution of EVM Transactions by GMT hour (Last 1 month)<br><sup>Distribution of the average number of transactions each GMT hour, to get a separate graph hover your mouse over the desired chain</sup>", 
        xaxis_title = "GMT Hour", 
        yaxis_title = "Average # of Transactions",
        height = 500,
        hovermode = "x unified",
        plot_bgcolor = '#171730',
        paper_bgcolor = '#171730',
        font = dict(color = 'white'),
        showlegend = False
    )

    f2.close()

    return fig_distribution