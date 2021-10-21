import copy
import json

import constant
from helper import time_helper


def mark_symbol_done(symbol, resolution, start, end, data_crawled):
    f = open('./data/success_symbols.json', "r")
    stocks = json.load(f)
    symbol_status = [(i, x) for (i, x) in enumerate(stocks[resolution]) if x['symbol'] == symbol]
    if len(symbol_status) > 0:
        index = symbol_status[0]
        stocks[resolution][index]({
            "symbol": symbol,
            "start": start,
            "end": end,
            "data_crawled": data_crawled,
            "time": time_helper.get_current_time_str(constant.DATE_TIME_FORMAT)
        })
    else:
        stocks[resolution].append({
            "symbol": symbol,
            "start": start,
            "end": end,
            "data_crawled": data_crawled,
            "time": time_helper.get_current_time_str(constant.DATE_TIME_FORMAT)
        })

    with open('./data/success_symbols.json', "w") as outfile:
        # raw_data = json.dumps(stocks)
        outfile.write(json.dumps(stocks, indent=4))


def mark_symbol_processing(symbols=None, resolution="1D"):
    f = open('./success_symbols.json', "r")
    stocks = json.load(f)

    for i, stock in enumerate(stocks[resolution]):
        if symbols is None:
            stocks[resolution] = []
        elif stock['symbol'] in symbols:
            del stocks[resolution][i]

    with open('./success_symbols.json', "w") as outfile:
        # raw_data = json.dumps(stocks)
        outfile.write(json.dumps(stocks))


def filter_symbol_status(resolution="1D"):
    f = open('./success_symbols.json', "r")
    stocks = json.load(f)
    existed_symbols = set()
    new_stocks_in_res = []
    stocks[resolution].reverse()
    for stock in stocks[resolution]:
        if stock['symbol'] in existed_symbols:
            continue
        new_stocks_in_res.append(stock)
        existed_symbols.add(stock['symbol'])
    stocks[resolution] = new_stocks_in_res
    with open('./success_symbols.json', "w") as outfile:
        # raw_data = json.dumps(stocks)
        outfile.write(json.dumps(stocks, indent=4))


def is_symbol_done(symbol, resolution, success_symbols=None):
    if success_symbols is None:
        f = open('./data/success_symbols.json', "r")
        stocks = json.load(f)
    else:
        stocks = success_symbols
    is_existed = any(symbol == stock['symbol'] for stock in stocks[resolution])
    return is_existed
