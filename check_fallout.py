
from scripts.Functions import *



##############################################################################
############################# DATA ###########################################
##############################################################################

class CheckDataFallout():

    def __init__(self):
        self.data = read_data_from_csv('data/data.csv')

        self.unqiue_dates = self.data['Date(UTC)'].unique()

        self.create_timeseries()

        self.unqiue_dates = pd.to_datetime(self.unqiue_dates, format = '%y%m%d')

    def create_timeseries(self):

        self.first_date = (min(self.data['Date(UTC)']))
        self.end_date = (max(self.data['Date(UTC)']))

        self.timeseries = pd.date_range(
            start = self.first_date, 
            end = self.end_date
        )

        return True
    
    def find_fallouts(self):

        self.fallout_dates = []

        for index in self.timeseries:
            if index not in self.unqiue_dates:

                self.fallout_dates.append(index)

        print(self.fallout_dates)
        print(len(self.unqiue_dates))


CheckDataFallout().find_fallouts()