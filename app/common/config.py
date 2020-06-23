"""
    Configuration file for the application, sets key parameters
    Variables denotes with (*) at the end of the corresponding comment must be set before running the program
"""
import secrets
import logging, os

# REQUIRED
DATA_PATH = '/home/martmichals/stockwatch/app/data/'       # Path for data folder *
COMPANIES_OF_INTEREST = {'MSFT': 'Microsoft', 'V': 'Visa'} # Stock tickers of interest, no more than 450 *

# Script info
TAG = 'config.py -'
LOG_FILEPATH = '/var/tmp/stockwatch.log'
MODES = ['production', 'debug']

# News data path and limit
NEWS_PATH = DATA_PATH + '/news/'
NEWS_DAILY_LIMIT = 500

# File path for stock data folder
STOCK_PATH = DATA_PATH + '/stocks/'

# People for which news is pulled - market "influencers"
PEOPLE = [
    'Warren Buffet', 
    'Bill McNabb', 
    'Jamie Dimon', 
    'Lloyd Blankfein', 
    'Larry Fink', 
    'Carl Icahn', 
    'Sergio Ermotti', 
    'Jeffery Gundlach', 
    'John Stumpf']

# Indecies for which statistics are pulled
COUNTRIES = ['us', 'ch', 'ru'] # Countries for which top headlines are pulled

# Function to check that the configuration parameters are properly instantiated
def check_config():
    if len(COMPANIES_OF_INTEREST.keys()) == 0:
        logging.exception('Improper instantiation of COMPANIES_OF_INTEREST')
    elif not os.path.isdir(DATA_PATH):
        logging.exception('Improper instantiation of DATA_PATH')
    else:
        if len(secrets.NEWS_API_KEY) is 0:
            logging.exception('%s The news API key is empty, please fill before re-running', TAG)
        elif len(secrets.FINNHUB_API_KEY) is 0:
            logging.exception('%s The finnhub API key is empty, please fill before re-running', TAG)
        else:
            return True
        raise ValueError('Key should not be empty')
    raise RuntimeError('Improper config.py parameters')

# Function that configures everything required for the program to run
def configure(mode):
    open(LOG_FILEPATH, 'w').close()
    if mode == 'debug':
        logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG, filename=LOG_FILEPATH)
    elif mode == 'production':
        logging.basicConfig(format='%(asctime)s %(message)s', level=logging.WARNING, filename=LOG_FILEPATH)
    else:
        raise RuntimeError('Incorrect mode passed as an argument') 
    logging.getLogger().addHandler(logging.StreamHandler())

    check_config()

    # Initialize folders for news and stocks
    if not os.path.isdir(NEWS_PATH):
        os.mkdir(NEWS_PATH)
    if not os.path.isdir(STOCK_PATH):
        os.mkdir(STOCK_PATH)

    logging.info('%s configure() completed successfully', TAG)
