import requests
import json

def get_symbols(floor):
    path = "https://services.entrade.com.vn/chart-api/symbols"
    res = requests.get(path, {
        "type": floor
    })
    res.raise_for_status()
    return res.json()


def get_all_symbols():
    all_symbols = []
    for floor in ["upcom", "hose", "hnx"]:
        symbols = get_symbols(floor)
        for symbol in symbols.get("symbols"):
            if symbol not in all_symbols and len(symbol) == 3:
                all_symbols.append(symbol)
    return all_symbols


all = get_all_symbols()
with open('./stocks.json', "w") as outfile:
    outfile.write(json.dumps(all, indent=4))
