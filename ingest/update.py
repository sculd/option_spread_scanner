import ingest.option_chains.option_chains
import ingest.quotes.quote

def update(symbol):
    ingest.option_chains.option_chains.update_option_chain(symbol)
    ingest.quotes.quote.update_quote(symbol)
