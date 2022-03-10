from datetime import timezone, datetime
import constant


def convert_vietstock_2_entrade_data(stocks, symbol, resolution):
    entrade_stocks = []
    for index in range(len(stocks['t'])):

        entrade = {}
        entrade['timestamp'] = stocks['t'][index]
        candle_time = datetime.fromtimestamp(
            stocks['t'][index], tz=timezone.utc)
        entrade['time'] = datetime.strftime(
            candle_time, constant.DATE_TIME_FORMAT)
        time_now = datetime.now()
        entrade['last_updated'] = int(datetime.timestamp(time_now))
        entrade['symbol'] = symbol
        entrade['resolution'] = resolution
        # entrade['open'] = round(float(stocks['o'][index]) / 1000, 2)
        # entrade['high'] = round(float(stocks['h'][index]) / 1000, 2)
        # entrade['low'] = round(float(stocks['l'][index]) / 1000, 2)
        # entrade['close'] = round(float(stocks['c'][index]) / 1000, 2)
        entrade['open'] = float(stocks['o'][index]) / 1000
        entrade['high'] = float(stocks['h'][index]) / 1000
        entrade['low'] = float(stocks['l'][index]) / 1000
        entrade['close'] = float(stocks['c'][index]) / 1000
        entrade['volume'] = stocks['v'][index]

        entrade_stocks.insert(0, entrade)
    return entrade_stocks


def convert_json_to_csv_type(data):
    csv_data = f"time,timestamp,symbol,open,high,low,close,volume,resolution,last_updated\n"
    body = ""
    for stock in data:
        res = 'DAY' if stock['resolution'] == 'D' else 'MIN1'
        row = f"{stock['time']},{stock['timestamp']},{stock['symbol']}," \
              f"{stock['open']},{stock['high']},{stock['low']},{stock['close']},{stock['volume']}," \
              f"{res},{stock['last_updated']}\n"
        body += row
    csv_data += body
    return csv_data, body
