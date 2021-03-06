import json


def mark_symbol_done(symbol, resolution, start, end, data_crawled):
    return
    f = open('./data/success_symbols.json', "r")
    stocks = json.load(f)
    f.close()
    if resolution not in stocks:
        stocks[resolution] = []
    symbol_status = [i for (i, x) in enumerate(
        stocks[resolution]) if x['symbol'] == symbol]
    if len(symbol_status) > 0:
        index = symbol_status[0]
        stocks[resolution][index]({
            "symbol": symbol,
            "start": start,
            "end": end,
            "data_crawled": data_crawled,
        })
    else:
        stocks[resolution].append({
            "symbol": symbol,
            "start": start,
            "end": end,
            "data_crawled": data_crawled,
        })

    with open('./data/success_symbols.json', "w") as outfile:
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


def filter_resolution(symbol, success_symbols):
    unsuccessful_res = []
    filter_symbols = [s for s in success_symbols
                      if s["symbol"] == symbol]
    if not filter_symbols:
        unsuccessful_res.append(res)

    return unsuccessful_res
