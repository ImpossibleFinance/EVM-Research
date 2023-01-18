from requests import get, post
import pandas as pd
from datetime import date, timedelta
import os
from dotenv import load_dotenv
import json
import time

data_name_array = ['data', 'price_data', 'gmt_hour_data', 'stablecoins']

load_dotenv()
API_KEY = os.getenv('DUNE_API_KEY')
HEADER = {"x-dune-api-key" : API_KEY}

BASE_URL = "https://api.dune.com/api/v1/"

def make_api_url(module, action, ID):
    """
    We shall use this function to generate a URL to call the API.
    """

    url = BASE_URL + module + "/" + ID + "/" + action

    return url


def get_query_status(execution_id):
    """
    Takes in an execution ID.
    Fetches the status of query execution using the API
    Returns the status response object
    """
    
    url = make_api_url("execution", "status", execution_id)
    response = get(url, headers=HEADER)
    
    return response


def get_query_results(execution_id):
    """
    Takes in an execution ID.
    Fetches the results returned from the query using the API
    Returns the results response object
    """
    
    url = make_api_url("execution", "results", execution_id)
    response = get(url, headers=HEADER)
    
    return response

def execute_query_with_params(query_id, param_dict):
    """
    Takes in the query ID. And a dictionary containing parameter values.
    Calls the API to execute the query.
    Returns the execution ID of the instance which is executing the query.
    """
    
    url = make_api_url("query", "execute", query_id)
    response = post(url, headers=HEADER, json={"query_parameters" : param_dict})

    execution_id = response.json()['execution_id']
    
    return execution_id

days_to_subtract = 30

today = date.today()
today = today.strftime("%Y-%m-%d")
last_date = date.today() - timedelta(days = days_to_subtract)

today = today + " 00:00:00"
last_date = str(last_date) + " 00:00:00"

parameters = {
    "Start Date" : last_date,
    "End Date" : today
}

f = open('requests_config.json')
query_config = json.load(f)

for name in data_name_array:
    query_id = (list(filter(lambda x:x["file_name"] == name, query_config)))[0]["dune_id"]

    execution_id = execute_query_with_params(query_id, parameters)

    while True:

        res = get_query_status(execution_id)
        res = res.json()

        print(name, "has status: ", res['state'])

        if res['state'] == 'QUERY_STATE_COMPLETED':
            break

        time.sleep(60)
    
    responce = get_query_results(execution_id)
    df = pd.DataFrame(responce.json()['result']['rows'])
    df = df.rename(columns = {"DATE": "Date(UTC)"})
    df = df.sort_values(by=['Date(UTC)'])
    df = df.reset_index(drop=True)

    df['Date(UTC)'] = df['Date(UTC)'].str.replace('T00:00:00Z','')

    try:
        if 'Date(UTC)' in df:
            data_from_file = pd.read_csv('csv_data/' + str(name) + '.csv')

            first_date = (min(df['Date(UTC)']))

            result = pd.concat([data_from_file[data_from_file["Date(UTC)"] <= first_date], df[df["Date(UTC)"] > first_date]], ignore_index=True)
            result.to_csv('csv_data/' + str(name) + '.csv', index = False)

            print("Rewriting CSV with new dates " + name)

        else:
            df.to_csv('csv_data/' + str(name) + '.csv', index = False)
            print("Rewriting whole CSV: " + name)
    except:
        df.to_csv('csv_data/' + str(name) + '.csv', index = False)
        print("Writing new CSV: " + name)


f.close()