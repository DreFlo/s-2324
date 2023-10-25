import secedgar

def get_cik(ticker):
    lookups = secedgar.cik_lookup.CIKLookup([ticker] if type(ticker) == str else ticker, user_agent="Name (email)")
    return [lookup for lookup in lookups.lookup_dict.values()][0]

get_cik('aapl')