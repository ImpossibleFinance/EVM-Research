from datetime import timedelta
import numpy as np


from scripts.Functions import *


def active_and_passive_day_of_week(data):

    groups = data['CHAIN'].unique()

    active_days = []
    chains = []
    passive_days = []

    for group in groups:
        data_group = data[data['CHAIN'] == group]

        idmax = data_group['Value'].idxmax()
        idmin = data_group['Value'].idxmin()

        active_days.append(data_group['Day of Week'][idmax])
        chains.append(group)
        passive_days.append(data_group['Day of Week'][idmin])

    fig_active = kpi(chains, active_days, 'Most Active day', '')
    fig_passive = kpi(chains, passive_days, 'Most Passive day', '')

    return fig_active, fig_passive

def transactions_by_day_of_week(data, range, config):

    last_date = (max(data['Date(UTC)']))
    if range != 'All':
        last_data = (data[data['Date(UTC)'].between((last_date - timedelta(days = int(range))), last_date)])
    else:
        last_data = data

    A = (last_data.groupby(by = [last_data["Date(UTC)"].dt.day_name(), last_data["CHAIN"]])['Value'].mean()).to_frame()
    A['Day of Week'] = A.index.get_level_values(0)
    A['CHAIN'] = A.index.get_level_values(1)

    A['Day_id'] = np.where(A['Day of Week'] == 'Monday', '0',
                    np.where(A['Day of Week'] == 'Tuesday', '1',
                        np.where(A['Day of Week'] == 'Wednesday', '2', 
                            np.where(A['Day of Week'] == 'Thursday', '3',
                                np.where(A['Day of Week'] == 'Friday', '4',
                                    np.where(A['Day of Week'] == 'Saturday', '5',      
                                        '6'
                                    )
                                )
                            )
                        )
                    )
                )
    A.sort_values(['Day_id', 'Value'], inplace = True)
    A['Value'] = round(A['Value'], 2)

    A = A.reset_index(drop = True)

    fig_active, fig_passive = active_and_passive_day_of_week(A)

    fig_by_day_of_week = distribution_bars(A, 'Day of Week', 'Value', 'CHAIN', config, 'Distribution by day of week', False)

    return fig_by_day_of_week, fig_active, fig_passive