from external_apis.financial_apis_wrapper import FinancialAPIsWrapper
from model.company_facts import CompanyFacts

def test_metric(metric : str):
    api_company_facts = FinancialAPIsWrapper.get_company_facts('AAPL')
    company_facts = CompanyFacts.from_sec_facts(api_company_facts)
    
    res = company_facts.get_key_metric(metric)

    print(metric)
    for end in res: 
        print(f'{end}:{res[end]}')
        
def get_metric_names():
    api_company_facts = FinancialAPIsWrapper.get_company_facts('AAPL')
        
    print(list(api_company_facts['facts']['us-gaap'].keys()))

    with open('metric_names.txt', 'w') as f:
        f.write(str(list(api_company_facts['facts']['us-gaap'].keys())))

if __name__ == '__main__':
    #test_metric('PriceToEarningsRatio')
    get_metric_names()