from datetime import timezone, datetime
import constant
from helper import time_helper


def convert_vietstock_2_entrade_data(stocks, symbol, resolution):
    entrade_stocks = []
    for index in range(len(stocks['t'])):

        entrade = {}
        entrade['timestamp'] = stocks['t'][index]
        candle_time = datetime.fromtimestamp(stocks['t'][index])
        entrade['time'] = datetime.strftime(candle_time, constant.DATE_TIME_FORMAT)
        time_now = datetime.utcnow()
        entrade['last_updated'] = int(datetime.timestamp(time_now))
        entrade['symbol'] = symbol
        entrade['resolution'] = resolution
        entrade['open'] = round(stocks['o'][index], 2)
        entrade['high'] = round(stocks['h'][index], 2)
        entrade['low'] = round(stocks['l'][index], 2)
        entrade['close'] = round(stocks['c'][index], 2)
        entrade['volume'] = round(stocks['v'][index], 2)

        entrade_stocks.append(entrade)
    return entrade_stocks


def convert_json_to_csv_type(data):
    csv_data = f"time,timestamp,symbol,open,high,low,close,volume,resolution,last_updated\n"
    body = ""
    for stock in data:
        res = 'DAY' if stock['resolution'] == '1D' else 'MIN1'
        row = f"{stock['time']},{stock['timestamp']},{stock['symbol']}," \
              f"{stock['open']},{stock['high']},{stock['low']},{stock['close']},{stock['volume']}," \
              f"{res},{stock['last_updated']}\n"
        body += row
    csv_data += body
    return csv_data, body
