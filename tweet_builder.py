from datetime import date
from functools import partial
from http.server import test, HTTPServer, SimpleHTTPRequestHandler
from multiprocessing import Process
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from time import sleep
import io
import os
import sys

import csv_updater


def start_http_server():
  sys.stdout = open(os.devnull, "w")
  sys.stderr = open(os.devnull, "w")
  handler_class = partial(SimpleHTTPRequestHandler, directory="docs")
  test(handler_class)


def get_graph_screenshot():
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
  img = Image.open(io.BytesIO(png)).crop((
      2*el.rect["x"],
      2*el.rect["y"],
      2*(el.rect["x"] + el.rect["width"]),
      2*(el.rect["y"] + el.rect["height"])
      ))


  browser.close()
  http_server.terminate()
  http_server.join()

  return img


def text():
  return "{:,} new COVID-19 cases reported in Tokyo today.\nhttps://davidstosik.github.io/covid-tokyo-graph/".format(csv_updater.last_count())


def main():
  if not csv_updater.updated_csv_today():
    print(f"!!! This is based on data from {csv_updater.last_update()} !!!")

  print(text())
  get_graph_screenshot().save("graph.png")


if __name__ == '__main__':
  main()
