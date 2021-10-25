from log import logger
import json
import viet_stock
import time
from helper import symbol_status_helper


f = open('./data/vn30.json')
stocks = json.load(f)
stocks = stocks["symbols"]

f = open('./data/success_symbols.json')
success_symbols = json.load(f)


domain = "https://vietstock-test.entrade.com.vn/history"

# resolutions= ["1", "3", "5", "10", "15", "30", "45", "60", "120", "180", "240", "D", "W", "M"]
resolutions = ["1", "D"]
threads = []
max_threads = 10
group_index = -1
for i, stock in enumerate(stocks):
    if i % max_threads == 0:
        group_index += 1
        threads.append([])
    symbol_resolutions =  symbol_status_helper.filter_resolution(stock, resolutions, success_symbols)
    handler = viet_stock.Handler(domain, stock, symbol_resolutions)
    threads[group_index].append(handler)

i = 0
for group_threads in threads:
    for thread in group_threads:
        i += 1
        logger.log(f'{"*" * 100} ')
        logger.info(f'Processing . {i}/{len(stocks)} ')
        logger.log(f'{"*" * 100} ')
        thread.start()
    for thread in group_threads:
        thread.join()

    time.sleep(10)



