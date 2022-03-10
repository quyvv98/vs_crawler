from log import logger
import json
import viet_stock
import time
import os
from helper import symbol_status_helper
from data import stocks_helper

f = open('./data/vn30.json')
f = open('./data/stocks.json')
stocks = json.load(f)
# stocks = stocks[:100] + ['HPG', 'SSI']
# stocks = stocks_helper.get_all_symbols()[1000:]


domain = "https://vietstock-test.entrade.com.vn/history"

# resolutions= ["1", "3", "5", "10", "15", "30", "45", "60", "120", "180", "240", "D", "W", "M"]
# resolutions = ["1"]
resolutions = ["D"]
success_symbols = []
resolution = resolutions[0]
for file in os.listdir(f"./data/{resolution}"):
    if file != f"total_{resolution}.csv" and file != f"total_{resolution}_filter.csv" and file != f"total_{resolution}_filter.csv.zip" \
            and file != ".DS_Store":
        success_symbols.append(file[:3])

threads = []
max_threads = 10
group_index = -1
for i, stock in enumerate(stocks):
    if i % max_threads == 0:
        group_index += 1
        threads.append([])
    if stock in success_symbols:
        continue
    handler = viet_stock.Handler(domain, stock, resolutions)
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
