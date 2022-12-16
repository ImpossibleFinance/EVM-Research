# EVM-Reserch

The analysis is a comparison of activity on EVM blockchains, including metrics such as daily transactions, active addresses, as well as average block creation time and daily block count.

## Links: 🥳

- 


## Usage on localhost

### Setup ⛏️

1. Create `.env` file
2. Put your ZettaBlock API key there like `API_KEY_ZETTA_BLOCK = "YOUR_API_KEY"`
3. Make a `csv_data` repository

### Run 🤖

Run via python and get all data as CSV file:
```basg
Upload_data.py
```

Or you can set up crontab -e script and get data every minute/hour/day

Start the UI:
```basg
gunicorn app:server -b:8080
```