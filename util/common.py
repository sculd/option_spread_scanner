import os


_ACCESS_TOKEN_TRADIER = os.environ['TRADIER_ACCESS_TOKEN']
API_KEY_WORLDTRADINGDATA = os.environ['WORLD_TRADING_DATA_API_KEY']
API_KEY_ALPHAVANTAGE = os.environ['API_KEY_ALPHAVANTAGE']
API_KEY_QUANDL = os.environ['API_KEY_QUANDL']

URL_BASE_TRADIER = 'https://sandbox.tradier.com'
URL_BASE_WORLDTRADING_DATA = 'https://api.worldtradingdata.com/api'
URL_BASE_ALPHAVANTAGE = 'https://www.alphavantage.co'
USL_BASE_QUANDL = 'https://www.quandl.com/api'

def get_auth_header_tradier():
    return {
        "Authorization":"Bearer " + _ACCESS_TOKEN_TRADIER,
        'Accept': 'application/json'
    }

