import json
import os
import csv
import constant
from datetime import datetime
import math


def group(resolution, date_filter=None):
    ohlcs = [
        'time,timestamp,symbol,open,high,low,close,volume,resolution,last_updated\n']
    if date_filter is None:
        date_filter = datetime.utcnow()
    else:
        date_filter = datetime.strptime(
            f"{date_filter} 23:59:59", constant.DATE_TIME_FORMAT)

    for file in os.listdir(f"./{resolution}"):
        if file != f"total_{resolution}.csv" and file != f"total_{resolution}_filter.csv" and file != f"total_{resolution}_filter.csv.zip" \
                and file != ".DS_Store":
            with open(f'./{resolution}/{file}', 'r') as f1:
                r = csv.reader(f1)
                ohlcs_symbol = []
                print(file)
                for i, row in enumerate(r):
                    if i > 0:
                        date = datetime.strptime(
                            row[0], constant.DATE_TIME_FORMAT)
                        if resolution == "D":
                            row[8] = "DAY"
                        row[3] = str(float(row[3]))
                        row[4] = str(float(row[4]))
                        row[5] = str(float(row[5]))
                        row[6] = str(float(row[6]))
                        row[7] = str(float(row[7]))

                        if date < date_filter:
                            row_str = ','.join(row) + "\n"
                            ohlcs.append(row_str)
                            ohlcs_symbol.append(row_str)

    with open(f'./{resolution}/total_{resolution}_filter.csv', 'w') as f3:
        f3.write(''.join(ohlcs))

    # with open('./success_symbols.json', 'w') as f4:
    #     f4.write(json.dumps(symbol_status, indent=4))


# group("1")
group("D", "2021-07-13")
