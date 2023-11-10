import json
import time
from external_apis.financial_apis_wrapper import FinancialAPIsWrapper
from model.company_facts import CompanyFacts
from random import shuffle

def get_aapl_data():
    company_facts = CompanyFacts.from_symbol(symbol='AAPL', financial_api_wrapper=FinancialAPIsWrapper)

    with open('resources/aapl_data.json', 'w') as f:
        f.write(json.dumps(company_facts.to_dict(), indent=2))

def get_test_data():
    symbols = []

    with open('resources/symbols', 'r') as f:
        symbols_file = f.read().split('\n')

        for i in range(1, len(symbols_file) - 2):
            symbols.append(symbols_file[i].split('|')[0])
    
    all_company_facts = {}

    # randomize order of symbols
    shuffle(symbols)
    
    for symbol in symbols[:2000]:
        print(f'Getting data for {symbol}')

        try:
            company_facts = CompanyFacts.from_symbol(symbol=symbol, financial_api_wrapper=FinancialAPIsWrapper)
        except Exception as e:
            print(f'Failed to get data for {symbol} - {e.__class__.__name__} - {e}')
            continue

        all_company_facts[symbol] = company_facts.to_dict()

    with open('resources/test_data.json', 'w') as f:
        f.write(json.dumps(all_company_facts, indent=2))

if __name__ == '__main__':
    #get_aapl_data()
    get_test_data()