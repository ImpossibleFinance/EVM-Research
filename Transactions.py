import json
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
from Data_API import *

def txs_distribution(data):

    A = (data.groupby(by = [data["Date(UTC)"].dt.day_name(), data["Chain"]])['Value'].sum()).to_frame()
    A['Day of Week'] = A.index.get_level_values(0)
    A['Chain'] = A.index.get_level_values(1)

    sorter = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    sorterIndex = dict(zip(sorter,range(len(sorter))))
    A['Day_id'] = A['Day of Week']
    A['Day_id'] = A['Day_id'].map(sorterIndex)
    A.sort_values('Day_id', inplace=True)

    A = A.reset_index(drop=True)
    return A

def transactions(data):

    f = open('chains_config.json')
    chains_config = json.load(f)

    chains = data['Chain'].unique()

    res_distribution = (txs_distribution(data))

    data_sum = data.groupby('Chain').sum()
    data_sum['Chain'] = data_sum.index.get_level_values(0)
    data_sum['Color'] = [(list(filter(lambda x:x["chain_name"]==y,chains_config)))[0]['colors'] for y in data_sum.index]

    data_sum = data_sum.reset_index(drop=True)


    res_distribution['Color'] = [(list(filter(lambda x:x["chain_name"]==y, chains_config)))[0]['colors'] for y in res_distribution['Chain']]

    result = res_distribution.merge(data_sum, on='Chain', how='inner', suffixes=('_1', '_2'))
    result['Percentage'] = round(result['Value_1']/result['Value_2']*100, 2)

    result = result.drop(columns=['Day_id', 'Color_2'])
    res_distribution = res_distribution.drop(columns=['Day_id'])

    # Plots

    fig = make_subplots(
        rows = 1, 
        cols = 2, 
        column_widths = [0.8, 0.2],
        specs=[[{'type':'xy'}, {'type':'domain'}]]
    )

    for chain in chains:
        data_chain = data[data["Chain"] == chain]
        fig.add_trace(go.Scatter(
            x = data_chain["Date(UTC)"], 
            y = data_chain["Value"],
            name = chain,
            marker_color = ((list(filter(lambda x:x["chain_name"]==chain,chains_config)))[0]["colors"])
            ), 
            row = 1, col = 1)

    fig.add_trace(go.Pie(
        labels = data_sum['Chain'], 
        values = data_sum['Value'], 
        name = "Total transactions count", 
        marker_colors = data_sum['Color'], 
        showlegend=False, 
        marker_line = dict(color='#000000', width=2)
        ), row = 1, col = 2)
    fig.update_layout(
        title = "EVM Transactions over time", 
        xaxis_title = "Date", 
        yaxis_title = "Transactions",
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

    fig2 = px.scatter(
        result,
        x = 'Day of Week',
        y = 'Chain',
        size = 'Percentage',
        color = 'Percentage',
        height = 700,
        color_continuous_scale = px.colors.sequential.Oryel,
        title = "Distribution by day of week"
    )
    fig2.update_layout(
        xaxis_tickangle = 30,
        title = dict( x = 0.5),
        xaxis_tickfont = dict(size = 9),
        yaxis_tickfont = dict(size = 9),
        plot_bgcolor = '#171730',
        paper_bgcolor = '#171730',
        font = dict(color = 'white')
    )

    for chain in chains:
        row = result[result["Chain"] == chain]['Percentage'].idxmax()
        fig2.add_trace(go.Scatter(
            x = [result.loc[[row]]['Day of Week']], 
            y = [chain], 
            mode = 'markers',
            marker_symbol = 'x',
            marker_size = 20,
            showlegend = False,
            marker_color = '#9CA1FF',
            name = '<-- Maximum'
            ))

    f.close()

    return fig, fig2