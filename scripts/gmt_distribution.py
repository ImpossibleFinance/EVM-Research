
from scripts.Functions import *


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

        idmax = data_group['Avg # of transactions'].idxmax()

        active_gmt.append(data_group['GMT hour'][idmax])
        chains.append(group)

    return active_gmt, chains

def distribution_by_gmt(current_data, chains_config):

    category_arr = []

    gmt_time_zones = data_gmt()

    fig_distribution = create_ez_bar(
            current_data, 
            'GMT hour', 
            'Avg # of transactions',
            None,
            'CHAIN', 
            chains_config,
            False,
            []
        )

    gmt_hours, chains = active_gmt_hour(current_data)

    for hour in gmt_hours:
        for item in gmt_time_zones:
            if hour >= int((item['hours']).split("-")[0]) and hour <= int((item['hours']).split("-")[1]):
                category_arr.append(item['zone'])

    return fig_distribution, create_ez_kpi(chains, category_arr, '', '', True)