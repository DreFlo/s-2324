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

def debt_to_equity(company_facts : CompanyFacts, end : str, form : Form = Form._10Q, unit : str = 'USD') -> float | None:
    long_term_debt = company_facts.get_fact('LongTermDebt', form=form, unit=unit)
    stockholders_equity = company_facts.get_fact('StockholdersEquity', form=form, unit=unit)

    if not long_term_debt or not stockholders_equity or end not in long_term_debt or end not in stockholders_equity:
        return None

    return {
        'fy' : long_term_debt[end]['fy'],
        'form' : long_term_debt[end]['form'],
        'filed' : long_term_debt[end]['filed'],
        'val' : long_term_debt[end]['val'] / stockholders_equity[end]['val']
        }

def debt_to_assets(company_facts : CompanyFacts, end : str, form : Form = Form._10Q, unit : str = 'USD') -> float | None:
    long_term_debt = company_facts.get_fact('LongTermDebt', form=form, unit=unit)
    assets = company_facts.get_fact('Assets', form=form, unit=unit)

    if not long_term_debt or not assets or end not in long_term_debt or end not in assets:
        return None

    return {
        'fy' : long_term_debt[end]['fy'],
        'form' : long_term_debt[end]['form'],
        'filed' : long_term_debt[end]['filed'],
        'val' : long_term_debt[end]['val'] / assets[end]['val']
        }

def market_cap(company_facts : CompanyFacts, end : str, form : Form = Form._10Q, unit : str = 'USD') -> float | None:
    common_stock_value = company_facts.get_fact('CommonStockValue', form=form, unit=unit)
    common_stock_shares_outstanding = company_facts.get_fact('CommonStockSharesOutstanding', form=form, unit=unit)

    if not common_stock_value or not common_stock_shares_outstanding or end not in common_stock_value or end not in common_stock_shares_outstanding:
        return None

    return {
        'fy' : common_stock_value[end]['fy'],
        'form' : common_stock_value[end]['form'],
        'filed' : common_stock_value[end]['filed'],
        'val' : common_stock_value[end]['val'] * common_stock_shares_outstanding[end]['val']
        }

def expenses(company_facts : CompanyFacts, end : str, form : Form = Form._10Q, unit : str = 'USD') -> float | None:
    operating_expenses = company_facts.get_fact('OperatingExpenses', form=form, unit=unit)
    interest_expenses = company_facts.get_fact('InterestExpense', form=form, unit=unit)
    sgna_expenses = company_facts.get_fact('SellingGeneralAndAdministrativeExpense', form=form, unit=unit)
    income_taxes = company_facts.get_fact('IncomeTaxesPaidNet', form=form, unit=unit)
    depreciation = company_facts.get_fact('Depreciation', form=form, unit=unit)

    if not operating_expenses or not interest_expenses or not sgna_expenses or not income_taxes or not depreciation\
        or end not in operating_expenses or end not in interest_expenses or end not in sgna_expenses\
        or end not in income_taxes or end not in depreciation:
        return None
    
    return {
        'fy' : operating_expenses[end]['fy'],
        'form' : operating_expenses[end]['form'],
        'filed' : operating_expenses[end]['filed'],
        'val' : operating_expenses[end]['val'] + interest_expenses[end]['val'] + sgna_expenses[end]['val'] + income_taxes[end]['val'] + depreciation[end]['val']
        }

def price_to_earnings_ratio(company_facts : CompanyFacts, end : str, form : Form = Form._10Q, unit : str = 'USD') -> float | None:
    common_stock_value = company_facts.get_fact('CommonStockValue', form=form, unit=unit)
    revenues = company_facts.get_fact('Revenues', form=form, unit=unit)


# TODO How the fuck do i get total debt
def net_debt_to_ebitda(company_facts : CompanyFacts, end : str, form : Form = Form._10Q, unit : str = 'USD') -> float | None:
    cash_and_cash_equivalents = company_facts.get_fact('CashAndCashEquivalentsAtCarryingValue', form=form, unit=unit)
    # 'LongTermDebt'


key_metric_function_map = {
    'CurrentRatio' : current_ratio,
    'DebtToEquity' : debt_to_equity,
    'DebtToAssets' : debt_to_assets
}