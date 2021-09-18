from datetime import date
from os import path

import csv
import requests_cache
import statistics

import constants


DAILY_CSV_PATH = "docs/daily.csv"


def update_csv():
  uri = constants.URIS['details']
  session = requests_cache.CachedSession(".cache/requests_cache.sqlite")
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


def last_data():
  if path.isfile(DAILY_CSV_PATH):
    with open(DAILY_CSV_PATH, 'r') as daily_csv:
      for line in daily_csv: # go to last line
        pass
      last_update, count, _ = list(csv.reader([line]))[0]

      return date.fromisoformat(last_update), int(count)


def last_count():
  return last_data()[1]


def last_update():
  return last_data()[0]


def updated_csv_today():
  return last_update() == date.today()
