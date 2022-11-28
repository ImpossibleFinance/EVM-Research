import pandas as pd
import requests
import json

def data_by_url(internal_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
    }


    url = 'https://node-api.flipsidecrypto.com/api/v2/queries/' + internal_url
    r = requests.get(url, headers=headers).text
    json_object = json.loads(r)
    df = pd.DataFrame.from_dict(json_object)

    if 'Date(UTC)' in df:
        df['Date(UTC)'] = pd.to_datetime(df["Date(UTC)"])

    return df