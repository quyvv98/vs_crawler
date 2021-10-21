from log import logger
import json
import viet_stock

f = open('./data/stocks.json')
stocks = json.load(f)

path = "https://vietstock-test.entrade.com.vn/history"

# resolutions= ["1", "3", "5", "10", "15", "30", "45", "60", "120", "180", "240", "D", "W", "M"]
resolutions = ["1", "D"]
for stock in stocks:
    # resolution = "1"
    for res in resolutions:
        handler = viet_stock.process(
            path, stock["code"], res)
    logger.info(f'Finish get ohlcs for {stock["code"]}')
    logger.log(f'{"=" * 100} ')
    logger.log(f'{"=" * 100} ')
