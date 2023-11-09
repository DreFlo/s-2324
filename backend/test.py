from external_apis.financial_apis_wrapper import FinancialAPIsWrapper
from model.company_facts import CompanyFacts
from utils.key_metric_functions import key_metric_function_map

def test_metric(metric : str):
    api_company_facts = FinancialAPIsWrapper.get_company_facts('AAPL')
    company_facts = CompanyFacts.from_sec_facts(api_company_facts)
    
    res = company_facts.get_key_metric(metric)

    print(metric)
        
def get_metric_names():
    api_company_facts = FinancialAPIsWrapper.get_company_facts('AAPL')
        
    print(list(api_company_facts['facts']['us-gaap'].keys()))

    with open('metric_names.txt', 'w') as f:
        f.write(str(list(api_company_facts['facts']['us-gaap'].keys())))

if __name__ == '__main__':
    for key_metric in key_metric_function_map:
        test_metric(key_metric)
        print()