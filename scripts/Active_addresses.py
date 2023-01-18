import json
import plotly.graph_objs as go

from scripts.Main_table import *

def active_addresses(data):

    f = open('chains_config.json')
    chains_config = json.load(f)

    chains = data["CHAIN"].unique()

    data_last_month_avg = last_month_addresses(data)[0]
    data_last_month_avg = data_last_month_avg.sort_values(by=['Active addresses'])

    fig_addresses = go.Figure()

    for chain in chains:
        data_chain = data[data["CHAIN"] == chain]
        fig_addresses.add_trace(go.Scatter(
            x = data_chain["Date(UTC)"], 
            y = data_chain["Active addresses"],
            name = chain,
            showlegend = False,
            marker_color = ((list(filter(lambda x:x["chain_name"]==chain,chains_config)))[0]["colors"])
            ))

    fig_addresses.update_layout(
        title = "EVM Active addresses over time<br><sup>Daily number of active addresses - i.e. unique senders of transactions</sup>", 
        xaxis_title = "Date", 
        yaxis_title = "Addresses",
        height = 500,
        plot_bgcolor = '#171730',
        paper_bgcolor = '#171730',
        hovermode = "x unified",
        font = dict(color = 'white')
    )

    fig_addresses.update_xaxes(
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
    fig_addresses.update_layout(xaxis=dict(rangeselector = dict(font = dict( color = "black"))))

    max_of_avg_addresses = ((data_last_month_avg.loc[data_last_month_avg['Active addresses'].idxmax()])['Active addresses'])

    fig_avg = go.Figure(
        go.Bar(
            x = [max_of_avg_addresses + 0.35*max_of_avg_addresses]*(max(data_last_month_avg.index) + 1),
            y = data_last_month_avg['CHAIN'],
            text = (data_last_month_avg["Active addresses"].div(1000)).map('{:,.1f}k'.format),
            textposition = "inside",
            textfont = dict(color="white"),
            orientation = "h",
            marker_color = "grey",
            hovertemplate = 'Addresses: %{text}<extra></extra>',
        )
    )

    fig_avg.add_trace(
        go.Bar(
            x = data_last_month_avg['Active addresses'],
            y = data_last_month_avg['CHAIN'],
            orientation = "h",
            hovertemplate = '%{y}<extra></extra>'
        )
    )
    fig_avg.update_layout(
        title = "Average number of addresses<br><sup>Average number of acitive addresses for last 1 Month</sup>",
        barmode = "overlay", 
        showlegend = False, 
        template = "presentation",
        height = 500,
        plot_bgcolor = '#171730',
        paper_bgcolor = '#171730',
        font = dict(color = 'white')
    )

    fig_avg.update_yaxes(
        tickmode = "array",
        categoryorder = "total ascending",
        tickvals = data_last_month_avg['CHAIN'],
        ticktext = data_last_month_avg['CHAIN'],
        ticklabelposition = "inside",
        tickfont = dict(color = "white"),
    )

    fig_avg.update_xaxes(range=[0, max_of_avg_addresses + 0.35*max_of_avg_addresses], visible = False)

    f.close()

    return fig_addresses, fig_avg