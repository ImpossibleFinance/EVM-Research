import json
import plotly.graph_objs as go
import pandas as pd


def stablecoins_charts(data):

    f = open('stablecoins_config.json')
    chains_config = json.load(f)

    data['total_tvl'] = data.sort_values(by=['Date(UTC)'], ascending=True).groupby(['stable'])['tvl'].cumsum()
    data['ma90'] = data.sort_values(by=['Date(UTC)'], ascending=True)\
                    .groupby('stable')['send_amount']\
                    .rolling(90, min_periods = 1).mean()\
                    .reset_index(drop=True, level=0)
    data['year'] = pd.DatetimeIndex(data['Date(UTC)']).year
    data['agg_transfer_volume'] = data.sort_values(by=['Date(UTC)'], ascending=True)\
                       .groupby(by = ['year', 'stable'])['send_amount']\
                       .cumsum()

    todays_data_by_type = data[data["Date(UTC)"] == data["Date(UTC)"][max(data.index)]]
    todays_data_by_type = todays_data_by_type.sort_values(by=['total_tvl'])
    todays_data_by_type = todays_data_by_type.reset_index(drop=True)

    fig = go.Figure()

    for type in todays_data_by_type['stable']:
        data_chain = data[data["stable"] == type]
        fig.add_trace(go.Scatter(
            x = data_chain["Date(UTC)"], 
            y = data_chain["total_tvl"],
            name = type,
            showlegend = False,
            fill = 'tonexty',
            stackgroup = 'one',
            marker_color = ((list(filter(lambda x:x["token"] == type,chains_config)))[0]["colors"])
            ))

    fig.update_layout(
        title = "Stablecoins supply<br><sup></sup>", 
        xaxis_title = "Date", 
        yaxis_title = "Supply (USD)",
        height = 650,
        hovermode = "x unified",
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


    fig2 = go.Figure()

    k = 0

    for index in todays_data_by_type['stable']:
        temp = todays_data_by_type[todays_data_by_type["stable"] == index]
        reference = float(temp['total_tvl'])-float(temp['tvl'])
        
        
        fig2.add_trace(go.Indicator(
            mode = "number+delta",
            value = float(temp['total_tvl']),
            delta = {'reference': reference, 'relative': False},
            domain = {'row': k, 'column': 1},
            title = dict(
                text = index
            ),
            ))

        k += 1

    fig2.update_layout(
        title = "Stablecoins supply on last day", 
        height = 700,
        plot_bgcolor = '#171730',
        paper_bgcolor = '#171730',
        font = dict(color = 'white'),
        grid = {'rows': k, 'columns': 1, 'pattern': "independent"},
    )


    # Transfer Volume

    fig_ma = go.Figure()
    fig_ma_share = go.Figure()
    fig_agg = go.Figure()

    for type in todays_data_by_type['stable']:
        data_chain = data[data["stable"] == type]
        fig_ma.add_trace(go.Scatter(
            x = data_chain["Date(UTC)"], 
            y = data_chain["ma90"],
            name = type,
            showlegend = False,
            marker_color = ((list(filter(lambda x:x["token"] == type,chains_config)))[0]["colors"])
            ))

        fig_agg.add_trace(go.Scatter(
            x = data_chain["Date(UTC)"], 
            y = data_chain["agg_transfer_volume"],
            name = type,
            showlegend = False,
            mode = 'lines',
            stackgroup = 'one',
            marker_color = ((list(filter(lambda x:x["token"] == type,chains_config)))[0]["colors"])
            ))

        fig_ma_share.add_trace(go.Scatter(
            x = data_chain["Date(UTC)"], 
            y = data_chain["ma90"],
            name = type,
            showlegend = False,
            stackgroup = 'one',
            groupnorm = 'percent',
            marker_color = ((list(filter(lambda x:x["token"] == type,chains_config)))[0]["colors"])
            ))

    fig_ma.update_layout(
        title = "Daily On-Chain Transfer Volume (90MA)<br><sup>90-day moving average on-chain volume and it's market share</sup>", 
        xaxis_title = "Date", 
        yaxis_title = "Volume (90MA) (USD)",
        height = 600,
        hovermode = "x unified",
        plot_bgcolor = '#171730',
        paper_bgcolor = '#171730',
        font = dict(color = 'white')
    )

    fig_agg.update_layout(
        title = "Stablecoins Aggregated Transactions Volume<br><sup></sup>", 
        xaxis_title = "Date", 
        yaxis_title = "Volume transfered (USD)",
        height = 600,
        hovermode = "x unified",
        plot_bgcolor = '#171730',
        paper_bgcolor = '#171730',
        font = dict(color = 'white')
    )

    fig_ma_share.update_layout(
        xaxis_title = "Date", 
        yaxis_title = "Volume share (%)",
        height = 600,
        hovermode = "x unified",
        plot_bgcolor = '#171730',
        paper_bgcolor = '#171730',
        font = dict(color = 'white'),
        yaxis = dict(
            type = 'linear',
            range = [1, 100],
            ticksuffix = '%'
        )
    )

    f.close()

    return fig, fig2, fig_ma, fig_ma_share, fig_agg