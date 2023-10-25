import secedgar
import os
import json
import requests

from dotenv import load_dotenv
from requests.structures import CaseInsensitiveDict

load_dotenv()

# TODO Need to credit Financial Modelling Prep in app
FMP_API_URL = 'https://financialmodelingprep.com/api/v3/'
FMP_API_KEY = os.getenv('FMP_API_KEY')

EDGAR_API_URL = 'https://data.sec.gov/api/'

class FinancialAPIsWrapper:
    def __init__(self) -> None:
        pass

    def __authorized_fmp_request(self, endpoint : str, params : CaseInsensitiveDict) -> (list | dict):
        params['apikey'] = FMP_API_KEY
        return requests.get(url=f'{FMP_API_URL}{endpoint}', params=params).json()
    
    def __edgar_request(self, endpoint : str, resource : str) -> (list | dict):
        headers = CaseInsensitiveDict({'user-agent' : 'Name (email)'})
        return requests.get(url=f'{EDGAR_API_URL}{endpoint}/{resource}', headers=headers).json()

    def __get_cik(self, symbol : str) -> str:
        lookups = secedgar.cik_lookup.CIKLookup([symbol], user_agent='Name (email)')
        return f'{int([lookup for lookup in lookups.lookup_dict.values()][0]):010}'
    
    # Query supersedes other arguments
    def search_company(self, query : dict = None, search_str : str = None, limit : int = None, exchange : str = 'NASDAQ') -> (list | None):
        if query:
            return self.__authorized_fmp_request('search', CaseInsensitiveDict(query))
        elif search_str:
            return self.__authorized_fmp_request('search', CaseInsensitiveDict({'query' : search_str, 'limit' : limit, 'exchange' : exchange}))
        return None
    
    # Symbol supersedes other arguments
    def get_company_facts(self, symbol : str = None, cik : str = None) -> dict:
        if symbol:
            cik = self.__get_cik(symbol=symbol)
        if cik and len(cik) == 10:
            return self.__edgar_request(endpoint='xbrl/companyfacts', resource=f'CIK{cik}.json')
        return None
    
finacial_apis_wrapper = FinancialAPIsWrapper()
search_results = finacial_apis_wrapper.search_company(search_str='apple')
facts = finacial_apis_wrapper.get_company_facts(symbol=search_results[0]['symbol'])

with open('facts.scratch.json', 'w') as scratch:
    scratch.write(json.dumps(facts, indent=2))
