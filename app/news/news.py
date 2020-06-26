"""
    Script to pull relevant news information on stocks of interest
"""
import os, logging, csv
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
        self._pulls = val
    
    def pullTickerNews(self, date):
        client = NewsApiClient(api_key=self._key)

        # Ensure news ticker folder exists, create a directory for news articles
        if not os.path.isdir(self._ticker_path):
            os.mkdir(self._ticker_path)

        # Create directory for the particular day
        full_path = '{}{}'.format(self._ticker_path, date.strftime('%m-%d-%Y'))

        # Remove this line later - for testing only 
        if os.path.isdir(full_path):
            os.rmdir(full_path)
        # END OF LINE REMOVAL

        if os.path.isdir(full_path):
            logging.warning('%s data for %s exists already', TAG, date.strftime('%m-%d-%Y'))
            return
        os.mkdir(full_path)


        start_of_day = date.replace(second=0, minute=0, hour=0)
        end_of_day = start_of_day + timedelta(days=1)

        # Grab the data for every ticker
        for ticker in config.COMPANIES_OF_INTEREST.keys():
            logging.info('%s pulling information for %s', TAG, ticker)
            all_for_ticker = client.get_everything(
                q=config.COMPANIES_OF_INTEREST[ticker],
                from_param=start_of_day,
                to=end_of_day,
                language='en',
                sort_by='relevancy',
                page_size=100
            )
            self.pulls += 1

            # Write the data into a csv file
            if all_for_ticker['status'] == 'ok' and all_for_ticker['totalResults'] is not 0:
                logging.info('%s the program pulled %d articles for %s', TAG, all_for_ticker['totalResults'], ticker)

                with open('{}/{}.csv'.format(full_path, ticker), 'w') as file:
                    # Formatting for csv writing
                    csv_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    for article in all_for_ticker['articles']:
                        format_for_csv = lambda value : str(value or 'None').replace('\n', ' ')
                        # src-id, src-name, author, title, url, description
                        csv_writer.writerow([
                            format_for_csv(article['source']['id']),
                            format_for_csv(article['source']['name']),
                            format_for_csv(article['author']),
                            format_for_csv(article['title']),
                            format_for_csv(article['url']),
                            format_for_csv(article['description'])
                        ])
            else:
                logging.warn('%s no data pulled for %s', TAG, ticker)

            # TODO : Strip HTML tags
