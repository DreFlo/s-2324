import json
from external_apis.financial_apis_wrapper import FinancialAPIsWrapper
from model.company_facts import CompanyFacts
from utils.key_metric_functions import key_metric_function_map

def get_aapl_data():
    facts = FinancialAPIsWrapper.get_company_facts(symbol='AAPL')

    company_facts = CompanyFacts.from_sec_facts(sec_facts=facts)

    with open('resources/aapl_data.json', 'w') as f:
        f.write(json.dumps(company_facts.to_dict(), indent=2))

def get_test_data():
    symbols = []

    with open('resources/symbols', 'r') as f:
        symbols_file = f.read().split('\n')

        for i in range(1, len(symbols_file) - 2):
            symbols.append(symbols_file[i].split('|')[0])
    
    all_company_facts = {}
    
    for symbol in symbols:
        facts = FinancialAPIsWrapper.get_company_facts(symbol=symbol)
        
        company_facts = CompanyFacts.from_sec_facts(sec_facts=facts)

        all_company_facts[symbol] = company_facts.to_dict()

    with open('resources/test_data.json', 'w') as f:
        f.write(json.dumps(all_company_facts, indent=2))

if __name__ == '__main__':
    get_aapl_data()
    #get_test_data()