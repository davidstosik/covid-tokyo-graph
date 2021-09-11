from http.server import test, HTTPServer, SimpleHTTPRequestHandler
from functools import partial
from multiprocessing import Process
from time import sleep
from datetime import date
import csv
import os
import sys

from selenium import webdriver
from selenium.webdriver import ChromeOptions

DAILY_CSV_PATH = "docs/daily.csv"

def start_http_server():
    sys.stdout = open(os.devnull, "w")
    sys.stderr = open(os.devnull, "w")
    handler_class = partial(SimpleHTTPRequestHandler, directory="docs")
    test(handler_class)

if __name__ == '__main__':
    with open(DAILY_CSV_PATH, 'r') as daily_csv:
      for line in daily_csv: # go to last line
        pass
      last_update, count, _ = list(csv.reader([line]))[0]
      if date.fromisoformat(last_update) < date.today():
        print("Today's data isn't available yet.")
        sys.exit()


      print("{:,} new COVID-19 cases reported in Tokyo today.\nhttps://davidstosik.github.io/covid-tokyo-graph-python/".format(int(count)))


    http_server = Process(target=start_http_server)
    http_server.daemon = True
    http_server.start()


    options = ChromeOptions()
    options.headless = True
    options.add_argument(f"--force-device-scale-factor=2.0")
    options.add_argument("--window-size=800,800")
    browser = webdriver.Chrome(options=options)
    browser.get('http://localhost:8000')
    el = browser.find_element_by_id('daily-new')

    sleep(3) # TODO figure a better way to wait

    png = browser.get_screenshot_as_png()
    import io
    from PIL import Image

    img = Image.open(io.BytesIO(png))
    img.crop((
        2*el.rect["x"],
        2*el.rect["y"],
        2*(el.rect["x"] + el.rect["width"]),
        2*(el.rect["y"] + el.rect["height"])
        )).save("graph.png")


    browser.close()
    http_server.terminate()
    http_server.join()
