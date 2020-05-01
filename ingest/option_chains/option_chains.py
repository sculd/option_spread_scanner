import requests, os, pickle, time
import util.common
from ingest.option_chains import option_expiration

_FILENAME_SAVED_OPTION_CHAINS = 'option_chains.pickle'

_OPTION_CHAINS_PATH = '/v1/markets/options/chains?symbol={symbol}&expiration={expiration}'

_request_cnt = 0

from enum import Enum

class OPTION_TYPE(Enum):
    CALL = 1
    PUT = 2

class Option:
    def __init__(self, option_type, symbol, expiration, strike, bid, ask, open_interest, volume):
        self.option_type, self.symbol, self.expiration, self.strike, self.bid, self.ask, self.open_interest, self.volume = option_type, symbol, expiration, strike, bid, ask, open_interest, volume

    def __str__(self):
        return 'option type: {t}, symbol: {symbol}, expiration: {expiration}, strike: {strike}, bid: {bid}, ask: {ask}, open_interest: {open_interest}, volume: {volume}'.format(
            t = self.option_type, symbol = self.symbol, expiration = self.expiration, strike = self.strike, bid = self.bid, ask = self.ask, open_interest = self.open_interest, volume= self.volume
        )

    def get_long_profit(self, target_price):
        if self.option_type is OPTION_TYPE.CALL:
            return max(0, target_price  - self.strike) - self.ask
        elif self.option_type is OPTION_TYPE.PUT:
            return max(0, self.strike - target_price) - self.ask
        return 0

    def get_short_profit(self, target_price):
        if self.option_type is OPTION_TYPE.CALL:
            return min(0, self.strike - target_price) + self.bid
        elif self.option_type is OPTION_TYPE.PUT:
            return min(0, target_price - self.strike) + self.bid
        return 0


class OptionChain:
    def __init__(self, expiration):
        self.expiration = expiration
        self.calls = []
        self.puts = []

    def __str__(self):
        return 'expiration: {expiration}\ncalls:\n{calls}\nputs:\n{puts}'.format(
            expiration = self.expiration,
            calls = '\n'.join(map(lambda c: str(c), self.calls)),
            puts = '\n'.join(map(lambda p: str(p), self.puts)),
        )

class OptionChains:
    def __init__(self):
        self.option_chains = []

    def __str__(self):
        return 'option_chains:\n{option_chains}'.format(
            option_chains = '\n'.join(map(lambda c: str(c), self.option_chains))
        )

    def get_chain_of_expiration(self, expiration):
        for chain in self.option_chains:
            if chain.expiration == expiration:
                return chain
        return None

def _request_option_chain_for_expiration(symbol, expiration):
    param_option = {
        'symbol': symbol,
        'expiration': expiration
    }

    response = requests.get(util.common.URL_BASE_TRADIER + _OPTION_CHAINS_PATH.format(**param_option),
        data={},
        headers=util.common.get_auth_header_tradier()
    )
    print('option chain request for symbol: %s, expiration: %s, response: %d' % (symbol, expiration, response.status_code))
    respoonse_js = response.json()
    chain = OptionChain(expiration)
    chain_for_expiration = respoonse_js['options']['option']
    for option_quote in chain_for_expiration:
        if option_quote['open_interest'] == 0:
            continue
        if option_quote['option_type'] == 'call':
            option_type = OPTION_TYPE.CALL
        elif option_quote['option_type'] == 'put':
            option_type = OPTION_TYPE.PUT
        else:
            print('unkown option type: {t}'.format(t=option_quote['option_type']))
            continue

        option = Option(option_type, symbol, expiration, option_quote['strike'], option_quote['bid'], option_quote['ask'], option_quote['open_interest'], option_quote['volume'])
        if option_quote['option_type'] == 'call':
            chain.calls.append(option)
        elif option_quote['option_type'] == 'put':
            chain.puts.append(option)

    return chain

def _request_option_chain(symbol):
    global _request_cnt
    res = OptionChains()
    expirations = option_expiration.get_option_expiration(symbol)
    for expiration in expirations:
        chain = _request_option_chain_for_expiration(symbol, expiration['date'])
        _request_cnt += 1
        print('_request_cnt: %d, symbol: %s, expiration: %s' % (_request_cnt, symbol, expiration['date']))
        res.option_chains.append(chain)
    return res


def update_option_chain(symbol):
    global _request_cnt
    if _request_cnt > 53:
        time.sleep(60)
        _request_cnt = 0

    chains_loaded = {}
    try:
        with open(_FILENAME_SAVED_OPTION_CHAINS, 'rb') as handle:
            chains_loaded.update(pickle.load(handle))
    except Exception as e:
        pass

    res = _request_option_chain(symbol)
    chains_loaded[symbol] = res
    with open(_FILENAME_SAVED_OPTION_CHAINS, 'wb') as handle:
        pickle.dump(chains_loaded, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return res


def get_option_chains(symbol):
    chains_loaded = {}
    try:
        with open(_FILENAME_SAVED_OPTION_CHAINS, 'rb') as handle:
            chains_loaded.update(pickle.load(handle))
            if symbol in chains_loaded:
                return chains_loaded[symbol]
    except Exception as e:
        pass

    return update_option_chain(symbol)



