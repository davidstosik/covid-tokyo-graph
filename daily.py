import sys

import csv_updater
import tweet_builder
import twitter


def send_tweet():
  print("Will send follwowing tweet:")
  print(tweet_builder.text())
  tweet_builder.get_graph_screenshot().save("graph.png")


def main():
  if csv_updater.updated_csv_today():
    print("Today's data was already added.")
  else:
    print("Fetching today's data and updating.")
    csv_updater.update_csv()

  if not csv_updater.updated_csv_today():
    print("No update yet. Aborting...")
    sys.exit()

  if twitter.twitted_today():
    print("Today's tweet was already sent.")
  else:
    print("Sending a tweet.")
    send_tweet()


if __name__ == "__main__":
  main()
