# autotweet-from-googlesheet

A minimal proof-of-concept Python script to tweet human-curated Tweets on a schedule using [Google Cloud Run](https://cloud.google.com/run) and [Google Cloud Scheduler](https://cloud.google.com/scheduler) sourced from [Google Sheets](https://www.google.com/sheets/about/), making running the bot free and can scale to effectively an unlimited number of bots if necessary.

This tool is intended to be used for curated AI-generated tweets, e.g. generated from [GPT-3](https://openai.com/blog/openai-api/).

## Usage

### Twitter Setup

First, [create an app](https://developer.twitter.com/en/portal/projects-and-apps) on Twitter, and generate the relevant keys for the target account.

### Google Sheets Setup

As [noted](https://gspread.readthedocs.io/en/latest/oauth2.html) in the [documentation for gspread](https://gspread.readthedocs.io/en/latest/), you will need to set up a Service Account for your Google Compute Engine project, and enable the Google Sheets API and Google Drive API.

Then, [clone this Google Sheet](https://docs.google.com/spreadsheets/d/1gO-eNHJss8hHieLTvxHoFM3C1sits_bHwgH0UHAPn0M/edit?usp=sharing) to your Google Drive, which is preformated with a compatable schema w/ formatting optimizations (such as a warning if your Tweet is too long).

Then, share the share the sheet with the email generated for the Service account.

You will need the `SHEET_KEY` from the URL of your Sheet for the next step (e.g. `1gO-eNHJss8hHieLTvxHoFM3C1sits_bHwgH0UHAPn0M` from the template above)

### Automation Setup

With `app.py` and the Service Account credentials file (expected: `key.json`), build a Docker container using the provided Dockerfile and upload it to the Google Container Registry.

Create a Cloud Run service using the uploaded container, (128MB Memory is sufficient). You will need to set up Environment Variables accordingly:

Required:

- `CONSUMER_KEY`
- `CONSUMER_SECRET`
- `ACCESS_KEY`
- `ACCESS_SECRET`
- `SHEET_KEY`

Optional:

- `SHEET_NAME` (default: `Sheet1`)
- `SERVICE_ACCOUNT_KEY` (default: `key.json`)
- `RANDOMIZE` (default: `1`, set to 0 to tweet untweeted tweets as they appear in the sheet)

Then, set up Google Cloud Scheduler which hits the service. (you can then set a cron for the container timing).

After the tweet is made, the timestamp and the URL for the resulting tweet will then be logged to the sheet. The Python script will prevent the same tweet from being made twice.

## Notes

- Yes, including the Service Account credentials in plaintext is not optimal security practice; however there isn't really a good alternative. Let me know if there's a better way to do that.
- You can use the same container and/or Google Sheet for multiple accounts, just change the Environment Variables accordingly.

## Maintainer/Creator

Max Woolf ([@minimaxir](https://minimaxir.com))

_Max's open-source projects are supported by his [Patreon](https://www.patreon.com/minimaxir) and [GitHub Sponsors](https://github.com/sponsors/minimaxir). If you found this project helpful, any monetary contributions to the Patreon are appreciated and will be put to good creative use._

## License

MIT
