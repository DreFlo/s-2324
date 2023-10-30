from model.company_facts import CompanyFacts, Form

def current_ratio(company_facts : CompanyFacts, end : str, form : Form = Form._10Q, unit : str = 'USD') -> float | None:
    current_assets = company_facts.get_fact('AssetsCurrent', form=form, unit=unit)
    current_liabilities = company_facts.get_fact('LiabilitiesCurrent', form=form, unit=unit)

    if not current_assets or not current_liabilities or end not in current_assets or end not in current_liabilities:
        return None

    return {
        'fy' : current_assets[end]['fy'],
        'form' : current_assets[end]['form'],
        'filed' : current_assets[end]['filed'],
        'val' : current_assets[end]['val'] / current_liabilities[end]['val']
        }

key_metric_function_map = {
    'CurrentRatio' : current_ratio
}