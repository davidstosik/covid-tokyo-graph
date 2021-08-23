import constants
import csv
import hashlib
import os
import requests
import statistics

cache_dir = 'tmp/cache'
uri = constants.URIS['details']
uri_md5 = hashlib.md5(uri.encode('utf-8')).hexdigest()
cache_path = f'{cache_dir}/get_{uri_md5}'

if not os.path.exists(cache_dir):
  os.makedirs(cache_dir)

if os.path.exists(cache_path):
  print('=== Using existing cache ===')
else:
  csv_response = requests.get(uri)
  with open(cache_path, 'w', newline='') as cache_file:
    print(csv_response.content.decode('utf-8-sig').strip(), file=cache_file)

output_path = "docs/daily.csv"

with open(output_path, 'w', newline='') as csv_output:
  csv_writer = csv.writer(csv_output)

  csv_writer.writerow(['date', 'count', 'rolling week average'])

  with open(cache_path, 'r', newline='') as csv_input:
    csv_reader = csv.reader(csv_input)

    next(csv_reader) # Discard headers

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
          statistics.mean(rolling_seven)
          ]
      csv_writer.writerow(row)



