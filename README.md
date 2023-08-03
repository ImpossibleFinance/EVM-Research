# EVM-Reserch

The analysis is a comparison of activity on EVM blockchains, including metrics such as daily transactions, active addresses, as well as average block creation time and daily block count.

There are 4 sectors, namely:

- On-chain Transactions metrics
- EVM Wallets metrics
- Block time and Blocks count
- Price of native tokens

The data is updated automatically every Monday:

```basg
0 0 * * 1 python3 upload_app.py >/dev/null 2>&1
```

All the libraries that were used are in the ***requirements.txt*** file 

## Links: 🥳

- Public Link: https://evm-stats.impossible.finance/


## Usage on localhost

### Setup ⛏️

1. Create `.env` file
2. Put your Dune API key there like `DUNE_API_KEY = "YOUR_API_KEY"`
3. Put global path to your repo, like `GLOBAL_PATH = "/home/.../EVM-Research"`
4. Make a `csv_data` repository
5. Put your global path to the directory like `GLOBAL_PATH = "..."`

### Run 🤖

Run via python and get all data as CSV file:
```basg
upload_app.py
```

Or you can set up crontab -e script and get data every minute/hour/day

Start the UI:
```basg
gunicorn app:server -b:8080
```


To check if there is all good or not (missed any dates):
```basg
check_fallout.py
```


### Some snapshots 📸

![image](https://github.com/0xKARTOD/EVM-Research/assets/100310858/a52eadb6-3df5-4cb8-b187-79e8766cebbb)
