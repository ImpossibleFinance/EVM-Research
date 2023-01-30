# EVM-Reserch

The analysis is a comparison of activity on EVM blockchains, including metrics such as daily transactions, active addresses, as well as average block creation time and daily block count.

There are 3 sectors, namely:

- Main On-chain metrics
- Stablecoins on EVM chains
- Price of native tokens

And in the "Main On-chain metrics", you can select 3 different category: Transactions, Active Addresses and Blocks. Each of those 3 category will show you some interesting data.

## Links: 🥳

- Public test: http://35.179.77.209:5000/


## Usage on localhost

### Setup ⛏️

1. Create `.env` file
2. Put your Dune API key there like `DUNE_API_KEY = "YOUR_API_KEY"`
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