import requests, os, pickle, time
import util.common


_FILENAME_SAVED_QUOTES_HISTORY = 'quotes.history.pickle'

_FILENAME_HISTORY_CSV = 'quotes.history.csv'

_QUOTE_PATH_WORLDTRADINGDATA = '/v1/history_multi_single_day?symbol={symbol}%date={date}&api_token={api_token}'

_QUERY_PATH_ALPHAVANTAGE_DAILY_QUOTE  = '/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={apikey}'

_QUERY_PATH_QUANDL_DAILY_QUOTE  = '/v3/datasets/EOD/{symbol}?start_date={start_date}&end_date={end_date}&api_key={api_key}'

_request_cnt_alphavantage = 0

def download_histories_csv(start_date, end_date):
    # _FILENAME_HISTORY_CSV
    with open(_FILENAME_HISTORY_CSV, 'w') as outfile:
        outfile.write('date,close,open,high,low,volume,symbol\n')

        for symbol in open('snp100.sample.txt', 'r'):
            symbol = symbol.strip()
            if not symbol:
                print('symbol: %s is not valid thus skipping' % (symbol))
                continue
            print('[download_histories_csv] processing symbol: %s' % (symbol))

            param_option = {
                'symbol': symbol,
                'start_date': start_date,
                'end_date': end_date,
                'api_key': util.common.API_KEY_QUANDL,
            }

            if _request_cnt_alphavantage > 120:
                time.sleep(60)
                _request_cnt = 0

            response = requests.get(
                util.common.USL_BASE_QUANDL + _QUERY_PATH_QUANDL_DAILY_QUOTE.format(**param_option),
                data={}
                )

            res = response.json()
            if not res:
                print('The response is invalid: %s' % (res))
                continue

            if 'dataset' not in res:
                print('The response does not have dataset: %s' % (res))
                continue

            if 'data' not in res['dataset']:
                print('The response data does not have data: %s' % (res))
                continue

            data = res['dataset']['data']
            out_lines = []
            for data_for_date in data:
                date_str, close, open_, high, low, volume = data_for_date[0], data_for_date[4], data_for_date[1], data_for_date[2], data_for_date[3], data_for_date[5]
                out_lines.append('{date_str},{close},{open},{high},{low},{volume},{symbol}\n'.format(date_str=date_str, close=close, open=open_, high=high, low=low, volume=volume, symbol=symbol))
            outfile.writelines(out_lines)


_request_cnt = 0

def get_quote_at_date(symbol, date):
    global _request_cnt
    quotes_loaded = {}
    try:
        with open(_FILENAME_SAVED_QUOTES_HISTORY, 'rb') as handle:
            quotes_loaded.update(pickle.load(handle))
            if symbol in quotes_loaded:
                return quotes_loaded[symbol]
    except Exception as e:
        pass

    param_option={
        'symbol': symbol,
        'date': date,
        'api_token': util.common.API_KEY_WORLDTRADINGDATA,
    }

    if _request_cnt > 230:
        time.sleep(60)
        _request_cnt = 0
        with open(_FILENAME_SAVED_QUOTES_HISTORY, 'wb') as handle:
            pickle.dump(quotes_loaded, handle, protocol=pickle.HIGHEST_PROTOCOL)

    response = requests.get(util.common.URL_BASE_WORLDTRADING_DATA + _QUOTE_PATH_WORLDTRADINGDATA.format(**param_option),
        data={},
        headers=util.common.get_auth_header_tradier()
    )

    res = response.json()

    quotes_loaded[symbol] = res
    with open(_FILENAME_SAVED_QUOTES_HISTORY, 'wb') as handle:
        pickle.dump(quotes_loaded, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return res





