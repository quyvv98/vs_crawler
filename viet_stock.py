import requests
import datetime
import time
from log import logger
from helper import transform_data_helper
import os
import os.path


def process(domain, symbol, resolution):
    duration = datetime.timedelta(days=30*12*50)
    if resolution in ["1", "3", "5", "10", "15", "30", "45", "60", "120", "180", "240"]:
        duration = datetime.timedelta(days=7)

    current_time = datetime.datetime.now()
    dirname = os.path.dirname(__file__)
    dir = os.path.join(os.getcwd(), 'data', resolution)
    if not os.path.exists(dir):
        os.mkdir(dir)
    file = f"{dir}/{symbol}_{resolution}.csv"
    with open(file, 'w') as outfile:
        outfile.write(
            f"time,timestamp,symbol,open,high,low,close,volume,resolution,last_updated\n")

    while True:
        start_time = current_time - duration
        logger.info(
            f'Get stock ohlc for {symbol}, res: {resolution} from {start_time} to {current_time}')

        ohlcs = get_history(domain, symbol, resolution, int(
            start_time.timestamp()), int(current_time.timestamp()))
        current_time = start_time
        if ohlcs is None or len(ohlcs['t']) == 0:
            logger.info(f'Finish get ohlcs for {symbol} with res {resolution} at time {current_time}')
            logger.log(f'{"=" * 100}')
            break
        entrade_ohlcs = transform_data_helper.convert_vietstock_2_entrade_data(
            ohlcs, symbol, resolution)
        logger.info(
            f"Start save data with symbol: {symbol}  resolution: {resolution} "
            f"start: {start_time} end: {current_time} total: {len(ohlcs['t'])} ")
        # Writing to csv file
        _, data_format_csv = transform_data_helper.convert_json_to_csv_type(
            entrade_ohlcs)
        with open(file, 'a') as outfile:
            outfile.write(data_format_csv)


def get_history(path, symbol, resolution, start, end):
    res = requests.get(path, {
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
