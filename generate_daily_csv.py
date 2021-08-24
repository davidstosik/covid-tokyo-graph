import constants
import csv
from datetime import date
import requests_cache
import statistics
import sys

DAILY_CSV_PATH = "docs/daily.csv"

with open(DAILY_CSV_PATH, 'r') as daily_csv:
  for line in daily_csv: # go to last line
    pass
  last_update = list(csv.reader([line])][0][0]
  if date.fromisoformat(last_update) == date.today():
    print("Today's data was already added. Aborting...")
    sys.exit()

uri = constants.URIS['details']
session = requests_cache.CachedSession(backend='filesystem', cache_name='web_cache')
csv_response = session.get(uri)
csv_reader = csv.reader(csv_response.text.strip().split('\r\n'))
next(csv_reader) # Discard headers

with open(DAILY_CSV_PATH, 'w', newline='') as csv_output:
  csv_writer = csv.writer(csv_output)
  csv_writer.writerow(['date', 'count', 'rolling week average'])

  rolling_seven = []
  previous_total = int(next(csv_reader)[4])

  for row in csv_reader:
    date = row[3]
    total = int(row[4])

    count = total - previous_total
    previous_total = total

    rolling_seven.insert(0, count)

    if len(rolling_seven) > 7:
      rolling_seven.pop()

    row = [
        date,
        count,
        round(statistics.mean(rolling_seven))
        ]
    csv_writer.writerow(row)
