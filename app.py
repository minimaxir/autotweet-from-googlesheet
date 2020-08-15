from starlette.applications import Starlette
from starlette.responses import JSONResponse

import uvicorn
import os
import random
import time
import tweepy
import gspread

# Twitter app configuration information: required
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
ACCESS_KEY = os.environ.get("ACCESS_KEY")
ACCESS_SECRET = os.environ.get("ACCESS_SECRET")

assert all(
    [CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET]
), "Not all Twitter app config tokens have been specified."

# Google Sheet configuration information
SHEET_KEY = os.environ.get("SHEET_KEY")
SHEET_NAME = os.environ.get("SHEET_NAME", "Sheet1")
SERVICE_ACCOUNT_KEY = os.environ.get("SERVICE_ACCOUNT_KEY", "key.json")
RANDOMIZE = os.environ.get("RANDOMIZE", 1)

assert SHEET_KEY, "A SHEET_KEY must be specified"

app = Starlette(debug=False)

# Needed to avoid cross-domain issues
response_header = {"Access-Control-Allow-Origin": "*"}


@app.route("/", methods=["GET", "POST", "HEAD"])
async def post_tweet(request):

    # Set up Twitter client
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    # Set up Google Sheets client
    gc = gspread.service_account(SERVICE_ACCOUNT_KEY)
    sh = gc.open_by_key(SHEET_KEY)
    ws = sh.worksheet(SHEET_NAME)

    # Select a tweet
    tweets = ws.get_all_records()
    tweets_filtered = list(filter(lambda x: not x["Tweet Timestamp"], tweets))
    assert len(tweets_filtered) > 0, "No untweeted tweets remaining"
    if RANDOMIZE:
        tweet = random.choice(tweets_filtered)["Tweet"]
    else:
        tweet = tweets_filtered[0]["Tweet"]

    # Post the tweet to Twitter
    t = api.update_status(tweet)
    t_timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    t_url = f"https://twitter.com/{t.user.screen_name}/status/{t.id_str}"

    # Update the corresponding Google Sheet row w/ metadata
    tweet_cell = ws.findall(tweet)
    assert len(tweet_cell) == 1, "There are multiple matches to the tweet."
    ws.update_cell(tweet_cell[0].row, 2, t_timestamp)
    ws.update_cell(tweet_cell[0].row, 3, t_url)

    return JSONResponse({"text": f"Tweet posted! {t_url}"}, headers=response_header)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
