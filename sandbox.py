import ingest.update
import ingest.option_chains.option_chains

symbol = 'AMZN'
#ingest.update.update(symbol)
chains = ingest.option_chains.option_chains.get_option_chains(symbol)
#print(chains)

print('bullish call')
import analysis.vertical_spread.bullish.call
spreads = analysis.vertical_spread.bullish.call.get_profitable_call_spreads(chains.get_chain_of_expiration('2020-05-08'), 2400)
print(spreads.filter_by_profit(40).sort_by_profit())


print('bearish put')
import analysis.vertical_spread.bearish.put
spreads = analysis.vertical_spread.bearish.put.get_profitable_put_spreads(chains.get_chain_of_expiration('2020-05-08'), 2400)
#print(spreads)



