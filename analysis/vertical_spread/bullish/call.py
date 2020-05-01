from analysis.vertical_spread.spread import Verticalpread, VerticalSpreads

class BullishVerticalCallSpread(Verticalpread):
    def __init__(self, target_price, call_long, call_short):
        super().__init__(target_price, call_long, call_short)

    def _get_risk(self):
        long = max(0, self.target_price - self.option_long.strike)
        short = min(0, self.option_short.strike - self.target_price)
        risk = long + short
        return round(risk, 3)

    def __str__(self):
        return super().__str__() + '\nBullishCallSpread(\n\trisk:{risk}\n)'.format(
            risk=self._get_risk()
        )

def get_profitable_call_spreads(option_chain, target_price):
    res = VerticalSpreads()
    n = len(option_chain.calls)
    for l in range(n):
        for s in range(l+1,n):
            spread = BullishVerticalCallSpread(target_price, option_chain.calls[l], option_chain.calls[s])
            if spread.get_profit() < 0: continue
            res.spreads.append(spread)
    return res


