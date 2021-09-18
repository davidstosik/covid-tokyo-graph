import requests_cache
import requests
import os
import datetime


bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
twitter_username = "covidtokyograph"
requests_cache_session = requests_cache.CachedSession(".cache/requests_cache.sqlite")
auth_header = { "Authorization": f"Bearer {bearer_token}" }
tweet_model = "new COVID-19 cases reported in Tokyo" 


class TwitterException(Exception):
  def __init__(self, response):
    self.response = response
    self.message = self.generate_message()

  def generate_message(self):
    error = self.response.json()["errors"][0]
    if self.response.ok:
      return f"{error['title']}: {error['detail']}"
    else:
      return error["message"]


def get_twitter_path(path, **options):
  base = "https://api.twitter.com/2"
  response = requests_cache_session.get(base + path, headers = auth_header, **options)
  json = response.json()
  if "errors" in json:
    raise TwitterException(response)
  else:
    return json


def get_user_id(username):
  return get_twitter_path(f"/users/by/username/{username}")["data"]["id"]


def today_midnight_stamp():
  return datetime.datetime \
      .now() \
      .replace(hour=0, minute=0, second=0, microsecond=0) \
      .astimezone(datetime.timezone.utc) \
      .isoformat("T") \
      .replace("+00:00", "Z")


def get_todays_tweets(username):
  user_id = get_user_id(username)
  params = {
      "start_time": today_midnight_stamp(),
      "max_results": 20
      }
  return get_twitter_path(f"/users/{user_id}/tweets", params=params).get("data", [])


def twitted_today():
  tweets = get_todays_tweets(twitter_username)
  return any(tweet_model in tweet["text"] for tweet in tweets)
