from analysis.vertical_spread.spread import Verticalpread, VerticalSpreads

class BearishVerticalPutSpread(Verticalpread):
    def __init__(self, target_price, put_long, put_short):
        super().__init__(target_price, put_long, put_short)

    def _get_risk(self):
        long = max(0, self.option_long.strike - self.target_price)
        short = min(0, self.target_price - self.option_short.strike)
        risk = long + short
        return round(risk, 3)

    def __str__(self):
        return super().__str__() + '\nBearishPutSpread(\n\trisk:{risk}\n)'.format(
            risk=self._get_risk()
        )

def get_profitable_put_spreads(option_chain, target_price):
    res = VerticalSpreads()
    n = len(option_chain.puts)
    for s in range(n):
        for l in range(s+1,n):
            spread = BearishVerticalPutSpread(target_price, option_chain.puts[l], option_chain.puts[s])
            if spread.get_profit() < 0: continue
            res.spreads.append(spread)
    return res


