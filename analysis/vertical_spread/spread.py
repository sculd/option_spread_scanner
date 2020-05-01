class Verticalpread:
    def __init__(self, target_price, option_long, option_short):
        self.target_price = target_price
        self.option_long, self.option_short = option_long, option_short

    def _get_premium(self):
        premium = self.option_short.bid - self.option_long.ask
        return round(premium, 3)

    def get_profit(self):
        long = self.option_long.get_long_profit(self.target_price)
        short = self.option_short.get_short_profit(self.target_price)
        return round(long + short, 3)

    def __str__(self):
        return 'Spread(\n\tprofit:{profit}\n\tpremium:{premium}\n\ttarget_price:{target_price}\n\tlong:\n\t{long}\n\tshort:\n\t{short}\n)'.format(
            profit = self.get_profit(),
            premium = self._get_premium(),
            target_price = self.target_price,
            long = str(self.option_long),
            short = str(self.option_short)
        )

class VerticalSpreads:
    def __init__(self):
        self.spreads = []

    def __str__(self):
        return '\n'.join(map(lambda s: str(s), self.spreads)) if self.spreads else 'None'

    def filter_by_profit(self, target_profit):
        res = VerticalSpreads()
        for spread in self.spreads:
            if spread.get_profit() < target_profit:
                continue
            res.spreads.append(spread)
        return res

    def sort_by_profit(self):
        res = VerticalSpreads()
        for spread in self.spreads:
            res.spreads.append(spread)
        res.spreads = sorted(res.spreads, key = lambda s: -1 * s.get_profit())
        return res
