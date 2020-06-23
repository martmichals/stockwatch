"""
    Script to pull relevant news information on stocks of interest
"""
import os, logging
from newsapi import NewsApiClient
from common import secrets, config
from datetime import datetime, timedelta

TAG = 'news_pull.py -'

class NewsPuller():
    def __init__(self, key):
        self._key = key
        self._ticker_path = '{}ticker-news/'.format(config.NEWS_PATH)
        self._pulls = 0

    @property
    def pulls(self):
        return self._pulls

    @pulls.setter
    def pulls(self, val):
        if (val > config.NEWS_DAILY_LIMIT):
            logging.exception('Exceeded News API daily request limit')
            raise RuntimeError('Exceeded the daily limit for news requests')
    
    def pullTickerNews(self, date):
        client = NewsApiClient(api_key=self._key)

        # Ensure news ticker folder exists, create a directory for news articles
        if not os.path.isdir(self._ticker_path):
            os.mkdir(self._ticker_path)

        # Create directory for the particular day
        full_path = '{}{}'.format(self._ticker_path, date.strftime('%m-%d-%Y'))

        # Remove this line later        
        os.rmdir(full_path)

        if os.path.isdir(full_path):
            logging.warning('%s data for %s exists already', TAG, date.strftime('%m-%d-%Y'))
            return
        os.mkdir(full_path)


        logging.info('%s pulling information for tickers', TAG)
        start_of_day = date.replace(second=0, minute=0, hour=0)
        end_of_day = start_of_day + timedelta(days=1)
        for ticker in config.COMPANIES_OF_INTEREST.keys():
            query = ticker if len(ticker) > 2 else config.COMPANIES_OF_INTEREST[ticker]
            all_for_ticker = client.get_everything(
                q=query,
                from_param=start_of_day,
                to=end_of_day,
                language='en',
                sort_by='relevancy',
                page_size=100
            ) 
            print(all_for_ticker['articles'][0]['url'])
            print(all_for_ticker['totalResults'])
            print(len(all_for_ticker['articles']))

if __name__ == '__main__':
    logging.error('%s Attempt to invoke from CLI', TAG)
    raise RuntimeError('%s invoked', TAG)