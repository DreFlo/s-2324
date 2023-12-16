from __future__ import annotations
from enum import Enum
from external_apis.financial_apis_wrapper import FinancialAPIsWrapper

class Form(Enum):
    _10Q = '10-Q'
    _10K = '10-K'

class CompanyFacts:
    def __init__(self) -> None:
        self.has_facts = False
        self.name = None
        self.symbol = None
        self.__facts_by_form = None
        self.__stock_price_history = None
        self.__adjusted_outstanding_shares = None
        pass

    def __get_form_from_sec_facts(sec_facts : dict, form : Form = Form._10Q) -> dict:
        form_data = {'fileds' : set()}
        for taxonomy in sec_facts:
            for tag in sec_facts[taxonomy]:
                if 'units' not in sec_facts[taxonomy][tag]:
                    continue

                for unit in sec_facts[taxonomy][tag]['units']:
                    for datapoint in sec_facts[taxonomy][tag]['units'][unit]:
                        if 'form' not in datapoint or datapoint['form'] != form.value or 'filed' not in datapoint:
                            continue

                        if tag not in form_data:
                            form_data[tag] = {
                                'label' : tag['label'] if 'label' in tag else tag,
                                'units' : {}
                            }

                        if unit not in form_data[tag]['units']:
                            form_data[tag]['units'][unit] = {}

                        form_data[tag]['units'][unit][datapoint['filed']] = {key : value for key, value in datapoint.items() if key != 'filed'}
                        form_data['fileds'].add(datapoint['filed'])

        form_data['fileds'] = sorted(list(form_data['fileds']))

        return form_data
    
    def __get_stock_splits(self) -> dict:
        stock_splits = self.get_fact(fact='StockholdersEquityNoteStockSplitConversionRatio1', form=Form._10Q, unit='pure')

        if not stock_splits:
            return None
        
        stock_split_for_date = {}

        for split in stock_splits.values():
            if split['end'] not in stock_split_for_date:
                stock_split_for_date[split['end']] = split['val']

        return stock_split_for_date

    def __from_finacial_information(symbol : str, sec_facts : dict, stock_price_history) -> CompanyFacts:
        company_facts = CompanyFacts()

        company_facts.name = sec_facts['entityName']

        company_facts.symbol = symbol

        company_facts.__facts_by_form = {}

        for form in Form:
            company_facts.__facts_by_form[form] = CompanyFacts.__get_form_from_sec_facts(sec_facts=sec_facts['facts'], form=form)

        company_facts.has_facts = sum([len(company_facts.__facts_by_form[form]['fileds']) > 0 for form in company_facts.__facts_by_form])

        company_facts.__stock_price_history = stock_price_history

        company_facts.__adjusted_outstanding_shares = company_facts.__calculate_adjusted_outstanding_shares()

        return company_facts
    
    def from_symbol(symbol : str, financial_api_wrapper : FinancialAPIsWrapper) -> CompanyFacts:
        facts = financial_api_wrapper.get_company_facts(symbol=symbol)
        stock_price_history = financial_api_wrapper.get_company_stock_price_history(symbol=symbol)
        return CompanyFacts.__from_finacial_information(symbol=symbol, sec_facts=facts, stock_price_history=stock_price_history)

    def get_fact(self, fact : str, form : Form = Form._10Q, unit : str = None) -> dict | None:
        if not self.has_facts:
            return None
        
        if form not in self.__facts_by_form:
            return None
        
        if fact not in self.__facts_by_form[form]:
            return None
        
        fact_data = self.__facts_by_form[form][fact]

        if not unit:
            return fact_data
        elif unit and unit in fact_data['units']:
            return fact_data['units'][unit]
        
        return None
    
    def __get_form(self, form : Form = Form._10Q) -> dict | None:
        if not self.has_facts:
            return None
        if form not in self.__facts_by_form:
            return None
        return self.__facts_by_form[form]
    
    def get_key_metric(self, key_metric : str, form : Form = Form._10Q) -> dict | None:
        from utils.key_metric_functions import key_metric_function_map
        form_data = self.__get_form(form=form)
        if not form_data:
            return None
        return {filed : key_metric_function_map[key_metric](company_facts=self, filed=filed, form=form) for filed in form_data['fileds']}
    
    def get_all_key_metrics(self, form : Form = Form._10Q) -> dict | None:
        from utils.key_metric_functions import key_metric_function_map
        form_data = self.__get_form(form=form)
        if not form_data:
            return None
        return {key_metric : self.get_key_metric(key_metric=key_metric, form=form) for key_metric in key_metric_function_map}
    
    def to_dict(self) -> dict:
        self_dict = {
            'name' : self.name,
            'has_facts' : self.has_facts,
            'facts_by_form' : {},
            'key_metrics_by_form' : {},
            'stock_price_history' : self.__stock_price_history,
            'symbol' : self.symbol,
            'adjusted_outstanding_shares' : self.__adjusted_outstanding_shares,
        }

        for form in self.__facts_by_form:
            self_dict['facts_by_form'][form.value] = self.__facts_by_form[form]

        for form in self.__facts_by_form:
            self_dict['key_metrics_by_form'][form.value] = self.get_all_key_metrics(form=form)

        return self_dict

    def get_adjusted_stock_price(self, date : str, moment : str = None) -> dict | float | None:
        if not moment:
            return self.__stock_price_history[date]
        elif moment in self.__stock_price_history[date]:
            return self.__stock_price_history[date][moment]
        return None
    
    def __calculate_adjusted_outstanding_shares(self) -> float | None:
        common_stock_outstanding = self.get_fact(fact='EntityCommonStockSharesOutstanding', form=Form._10Q, unit='shares')

        if not common_stock_outstanding:
            return None
        
        stock_splits = self.__get_stock_splits()

        if not stock_splits:
            return common_stock_outstanding
        
        adjusted_common_stock_outstanding = {}

        for date in common_stock_outstanding:
            common_stock_outstanding_for_date = common_stock_outstanding[date]['val']
            
            for split_date in stock_splits:
                if split_date < date:
                    common_stock_outstanding_for_date *= stock_splits[split_date]

            adjusted_common_stock_outstanding[date] = {
                'fy' : common_stock_outstanding[date]['fy'],
                'val' : common_stock_outstanding_for_date,
            }

        return adjusted_common_stock_outstanding
    
    def get_adjusted_outstanding_shares(self, date : str) -> float | None:
        if not self.__adjusted_outstanding_shares:
            return None
        
        if date not in self.__adjusted_outstanding_shares:
            return None

        return self.__adjusted_outstanding_shares[date]['val']