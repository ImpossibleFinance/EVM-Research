import json

from scripts.Functions import distribution_bars, kpi


def data_gmt():
    data_gmt = {
        'gmt' : [
            {
                'hours' : '0-0',
                'zone' : 'New Zealand'
            },
            {
                'hours' : '1-2',
                'zone' : 'Pacific Ocean'
            },
            {
                'hours' : '3-3',
                'zone' : 'Alaska'
            },
            {
                'hours' : '4-9',
                'zone' : 'American Zone'
            },
            {
                'hours' : '10-10',
                'zone' : 'Atlantic Ocean'
            },
            {
                'hours' : '11-14',
                'zone' : 'Europian region'
            },
            {
                'hours' : '15-15',
                'zone' : 'Middle East/Moscow'
            },
            {
                'hours' : '16-22',
                'zone' : 'Asian Zone'
            },
            {
                'hours' : '23-23',
                'zone' : 'Pacific Zone'
            }
        ]
    }

    json_string = json.dumps(data_gmt)
    gmt_time_zones = json.loads(json_string)

    return gmt_time_zones['gmt']

def active_gmt_hour(data):

    groups = data['CHAIN'].unique()

    active_gmt = []
    chains = []

    for group in groups:
        data_group = data[data['CHAIN'] == group]

        idmax = data_group['AVG_TXS_COUNT'].idxmax()

        active_gmt.append(data_group['GMT_HOUR'][idmax])
        chains.append(group)

    return active_gmt, chains

def distribution_by_gmt(current_data, chains_config):

    category_arr = []

    gmt_time_zones = data_gmt()

    fig_distribution = distribution_bars(current_data, 'GMT_HOUR', 'AVG_TXS_COUNT', 'CHAIN', chains_config, 'Distribution of EVM transactions by GMT hour', False)

    gmt_hours, chains = active_gmt_hour(current_data)

    for hour in gmt_hours:
        for item in gmt_time_zones:
            if hour >= int((item['hours']).split("-")[0]) and hour <= int((item['hours']).split("-")[1]):
                category_arr.append(item['zone'])

    return fig_distribution, kpi(chains, category_arr, 'Active Time Zones', '')