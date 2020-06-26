"""
    Main python file for the application
"""
from common import config, secrets
from news.news import NewsPuller
from datetime import datetime, timedelta, tzinfo
import argparse, logging, pytz

TAG = 'app.py -'

# -m <mode ['debug', 'production']>
parser = argparse.ArgumentParser(description='scrape stock statistics and news')
parser.add_argument('-m', '--mode', help='mode in which to run the script')
args = parser.parse_args()

config.configure(args.mode)

# Get yesterday's date, ensure that an hour has passed from yesterday (News API delay)
current_time = datetime.now(tz=pytz.timezone('US/Eastern'))
yesterday = current_time - timedelta(days=1) - timedelta(hours=1) 
if yesterday.hour < 1:
    logging.exception('%s Script ran too soon in the day', TAG)
    raise RuntimeError('Script was run too soon')

# Run data collection scripts for those days
news_puller = NewsPuller(secrets.NEWS_API_KEY)
news_puller.pullTickerNews(yesterday)