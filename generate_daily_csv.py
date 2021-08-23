import constants
import csv
import requests_cache
import statistics

uri = constants.URIS['details']
session = requests_cache.CachedSession(backend='filesystem', cache_name='web_cache')
csv_response = session.get(uri)
csv_reader = csv.reader(csv_response.text.strip().split('\r\n'))
next(csv_reader) # Discard headers

output_path = "docs/daily.csv"
with open(output_path, 'w', newline='') as csv_output:
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
