from __future__ import annotations
from enum import Enum

class Form(Enum):
    _10Q = '10-Q'
    _10K = '10-K'

class CompanyFacts:
    def __init__(self) -> None:
        self.has_facts = False
        self.name = None
        self.__facts_by_form = None
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

    def from_sec_facts(sec_facts : dict) -> CompanyFacts:
        company_facts = CompanyFacts()

        company_facts.name = sec_facts['entityName']

        company_facts.__facts_by_form = {}

        for form in Form:
            company_facts.__facts_by_form[form] = CompanyFacts.__get_form_from_sec_facts(sec_facts=sec_facts['facts'], form=form)

        company_facts.has_facts = True

        return company_facts

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
            'key_metrics_by_form' : {}
        }

        for form in self.__facts_by_form:
            self_dict['facts_by_form'][form.value] = self.__facts_by_form[form]

        for form in self.__facts_by_form:
            self_dict['key_metrics_by_form'][form.value] = self.get_all_key_metrics(form=form)

        return self_dict

        