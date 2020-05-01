import requests, os, pickle, time
import util.common

# util.common.API_KEY_WORLDTRADINGDATA

_FILENAME_SAVED_QUOTES = 'quotes.pickle'

_QUOTE_PATH = '/v1/markets/quotes?symbols={symbol}'

_request_cnt = 0


def get_quote(symbol, force_update = False):
    global _request_cnt
    quotes_loaded = {}
    try:
        with open(_FILENAME_SAVED_QUOTES, 'rb') as handle:
            quotes_loaded.update(pickle.load(handle))
            if not force_update and symbol in quotes_loaded:
                return quotes_loaded[symbol]
    except Exception as e:
        pass

    param_option={'symbol': symbol}

    if _request_cnt > 53:
        time.sleep(60)
        _request_cnt = 0
        with open(_FILENAME_SAVED_QUOTES, 'wb') as handle:
            pickle.dump(quotes_loaded, handle, protocol=pickle.HIGHEST_PROTOCOL)

    response = requests.get(util.common.URL_BASE_TRADIER + _QUOTE_PATH.format(**param_option),
        data={},
        headers=util.common.get_auth_header_tradier()
    )

    json_response = response.json()
    if 'quotes' not in json_response:
        print('quotes not present')
        print(json_response)
        return {}
    if 'quote' not in json_response['quotes']:
        print('quote not present in quotes')
        print(json_response)
        return {}

    res = json_response['quotes']['quote']

    quotes_loaded[symbol] = res
    with open(_FILENAME_SAVED_QUOTES, 'wb') as handle:
        pickle.dump(quotes_loaded, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return res


def get_week_52_relative(symbol):
    qt = get_quote(symbol)
    if qt is None: 
        return None
    p = 1.0 * (qt['ask'] + qt['bid']) / 2.0
    week_52_spread = qt['week_52_high'] - qt['week_52_low']
    low_to_p = p - qt['week_52_low']
    return 1.0 * low_to_p / week_52_spread


def update_quote(symbol):
    print('updating quote for {symbol}'.format(symbol=symbol))
    return get_quote(symbol, force_update=True)

