import requests
import datetime
import time
from log import logger
from helper import transform_data_helper, symbol_status_helper
import os
import threading
import os.path


class Handler(threading.Thread):
    def __init__(self, domain, symbol, resolutions):
        threading.Thread.__init__(self)
        self.resolutions = resolutions
        self.domain = domain
        self.symbol = symbol

    def run(self):
        for res in self.resolutions:
            process(self.domain, self.symbol, res)
        logger.info(f'DONE {self.symbol} !!!!!!!!!!!!!')


def process(domain, symbol, resolution):
    duration = datetime.timedelta(days=30*12*20)
    if resolution in ["1", "3", "5", "10", "15", "30", "45", "60", "120", "180", "240"]:
        duration = datetime.timedelta(days=7)

    dir = os.path.join(os.getcwd(), 'data', resolution)
    if not os.path.exists(dir):
        os.mkdir(dir)
    file = f"{dir}/{symbol}_{resolution}.csv"
    time_now = datetime.datetime.now()
    current_time = time_now
    data = []
    while True:
        start_time = current_time - duration
        
        time.sleep(1)
        ohlcs = get_history(domain, symbol, resolution, int(
            start_time.timestamp()), int(current_time.timestamp()))
        # time.sleep(2)
        current_time = start_time
        if ohlcs is None or len(ohlcs['t']) == 0:
            logger.info(
            f"Start save data with symbol: {symbol}  resolution: {resolution} "
            f"start: {current_time} end: {time_now} total: {len(data)} ")
            logger.log(f'{"=" * 100}')
            logger.log(f'{"=" * 100}')
            # Writing to csv file
            data_format_csv, _=transform_data_helper.convert_json_to_csv_type(
                data)
            with open(file, 'w') as outfile:
                outfile.write(data_format_csv)

            symbol_status_helper.mark_symbol_done(
                symbol, resolution, int(current_time.timestamp()), int(time_now.timestamp()), len(data))
            break
        entrade_ohlcs = transform_data_helper.convert_vietstock_2_entrade_data(
            ohlcs, symbol, resolution)
        data = data + entrade_ohlcs
        logger.info(
            f'Got stock ohlc for {symbol}, res: {resolution} from {start_time} to {current_time}. added: {len(entrade_ohlcs)}. total: {len(data)}')
        


def get_history(path, symbol, resolution, start, end):
    res=requests.get(path, {
        "symbol": symbol,
        "from": start,
        "to": end,
        "resolution": resolution,
    })
    try:
        res.raise_for_status()
    except Exception as e:
        logger.error(f'Request VietStock api fail with err {e}')
        return None
    return res.json()
    
