from datetime import timedelta
import pandas as pd

def last_month_addresses(data):
    last_date = (max(data['Date(UTC)']))

    data_last_month_avg = (data[data['Date(UTC)'].between((last_date - timedelta(days = 30)), last_date)]).groupby('CHAIN').mean()
    data_last_month_avg['CHAIN'] = data_last_month_avg.index.get_level_values(0)
    data_last_month_avg = data_last_month_avg.reset_index(drop=True)

    return data_last_month_avg, last_date


def table_data(data):
    data_last_month_avg, last_date = last_month_addresses(data)

    table_data = data[data['Date(UTC)'] == last_date].merge(data_last_month_avg, on='CHAIN', how='inner', suffixes=('_1', '_2'))

    table_data['Pct txs'] = 100*(table_data['Value_1'] - table_data['Value_2'])/table_data['Value_2']
    table_data['Pct addresses'] = 100*(table_data['Active addresses_1'] - table_data['Active addresses_2'])/table_data['Active addresses_2']
    table_data['Pct time'] = -100*(table_data['Block time_1'] - table_data['Block time_2'])/table_data['Block time_1']
    table_data['Pct blocks'] = 100*(table_data['Blocks count_1'] - table_data['Blocks count_2'])/table_data['Blocks count_1']


    table_data_result  = pd.DataFrame()
    table_data_result['CHAIN'] = table_data['CHAIN']
    table_data_result = table_data_result.merge(data_last_month_avg, on='CHAIN', how='left')

    table_data_result['# of Transactions'] = [
        str("{:,.2f}".format(table_data['Value_1'][v])) + 
        " (" +
        str(round(table_data['Pct txs'][v], 2)) + 
        "%)"
        for v in range(len(table_data['Value_1']))]

    table_data_result['# of Active addresses'] = [
        str("{:,.2f}".format(table_data['Active addresses_1'][v])) + 
        " (" +
        str(round(table_data['Pct addresses'][v], 2)) + 
        "%)"
        for v in range(len(table_data['Active addresses_1']))]

    table_data_result['Block time [s]'] = [
        str("{:,.2f}".format(round(table_data['Block time_1'][v], 1))) + 
        " (" +
        str(round(table_data['Pct time'][v], 2)) + 
        "%)"
        for v in range(len(table_data['Block time_1']))]

    table_data_result['# of Blocks'] = [
        str("{:,.2f}".format(table_data['Blocks count_1'][v])) + 
        " (" +
        str(round(table_data['Pct blocks'][v], 2)) + 
        "%)"
        for v in range(len(table_data['Blocks count_1']))]
    
    table_data_result['Pct txs'] = table_data['Pct txs']
    table_data_result['Pct addresses'] = table_data['Pct addresses']
    table_data_result['Pct time'] = table_data['Pct time']
    table_data_result['Pct blocks'] = table_data['Pct blocks']

    return table_data_result, last_date