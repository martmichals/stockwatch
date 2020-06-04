"""
    Configuration file for the application, sets key parameters
    Comments with (*) at the end must be set before running the program
"""
import logging
import os

TAG = 'config.py'
LOG_FILENAME = '/var/tmp/stockwatch.log'

# Stock tickers of interest, no more than 450 *
TICKERS_OF_INTEREST = ['MSFT', 'V']

# Path for data folder
DATA_PATH = '../data'

# File path for news folder
NEWS_PATH = DATA_PATH + '/news/'

# File path for stock data folder
STOCK_PATH = DATA_PATH + '/stocks/'

# Function to check that the configuration parameters are properly instantiated
def check_config():
    if len(TICKERS_OF_INTEREST) == 0:
        logging.exception('Improper instantiation of TICKERS_OF_INTEREST')
    elif not os.path.isdir(DATA_PATH):
        logging.exception('Improper instantiation of DATA_PATH')
    else:
        return True
    raise RuntimeError('Improper config.py parameters')

# Function that configures everything required for the program to run
def configure(mode):
    os.remove(LOG_FILENAME)
    if mode is 'debug':
        logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG, filename=LOG_FILENAME)
    if mode is 'production':
        logging.basicConfig(format='%(asctime)s %(message)s', level=logging.WARNING, filename=LOG_FILENAME)
    logging.getLogger().addHandler(logging.StreamHandler())
 
    if check_config():
        # Initialize folders for news and stocks
        if not os.path.isdir(NEWS_PATH):
            os.mkdir(NEWS_PATH)
        if not os.path.isdir(STOCK_PATH):
            os.mkdir(STOCK_PATH)

        logging.info('%s configure() completed successfully', TAG) # TODO - Change configuration to automatically include tag
