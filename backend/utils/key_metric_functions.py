from model.company_facts import CompanyFacts, Form

def current_ratio(company_facts : CompanyFacts, end : str, form : Form = Form._10Q, unit : str = 'USD') -> dict | None:
    current_assets = company_facts.get_fact(fact='AssetsCurrent', form=form, unit=unit)
    current_liabilities = company_facts.get_fact(fact='LiabilitiesCurrent', form=form, unit=unit)

    if not current_assets or not current_liabilities or end not in current_assets or end not in current_liabilities:
        return None

    return {
        'fy' : current_assets[end]['fy'],
        'form' : current_assets[end]['form'],
        'filed' : current_assets[end]['filed'],
        'val' : current_assets[end]['val'] / current_liabilities[end]['val'] if current_liabilities[end]['val'] != 0 else None
        }

def debt_to_equity(company_facts : CompanyFacts, end : str, form : Form = Form._10Q, unit : str = 'USD') -> dict | None:
    long_term_debt = company_facts.get_fact(fact='LongTermDebt', form=form, unit=unit)
    stockholders_equity = company_facts.get_fact(fact='StockholdersEquity', form=form, unit=unit)

    if not long_term_debt or not stockholders_equity or end not in long_term_debt or end not in stockholders_equity:
        return None

    return {
        'fy' : long_term_debt[end]['fy'],
        'form' : long_term_debt[end]['form'],
        'filed' : long_term_debt[end]['filed'],
        'val' : long_term_debt[end]['val'] / stockholders_equity[end]['val'] if stockholders_equity[end]['val'] != 0 else None
        }

def debt_to_assets(company_facts : CompanyFacts, end : str, form : Form = Form._10Q, unit : str = 'USD') -> dict | None:
    long_term_debt = company_facts.get_fact(fact='LongTermDebt', form=form, unit=unit)
    assets = company_facts.get_fact(fact='Assets', form=form, unit=unit)

    if not long_term_debt or not assets or end not in long_term_debt or end not in assets:
        return None

    return {
        'fy' : long_term_debt[end]['fy'],
        'form' : long_term_debt[end]['form'],
        'filed' : long_term_debt[end]['filed'],
        'val' : long_term_debt[end]['val'] / assets[end]['val'] if assets[end]['val'] != 0 else None
        }

def market_cap(company_facts : CompanyFacts, end : str, form : Form = Form._10Q, unit : str = 'USD') -> dict | None:
    common_stock_value = company_facts.get_fact(fact='CommonStockValue', form=form, unit=unit)
    common_stock_shares_outstanding = company_facts.get_fact(fact='CommonStockSharesOutstanding', form=form, unit=unit)

    if not common_stock_value or not common_stock_shares_outstanding or end not in common_stock_value or end not in common_stock_shares_outstanding:
        return None

    return {
        'fy' : common_stock_value[end]['fy'],
        'form' : common_stock_value[end]['form'],
        'filed' : common_stock_value[end]['filed'],
        'val' : common_stock_value[end]['val'] * common_stock_shares_outstanding[end]['val']
        }

def expenses(company_facts : CompanyFacts, end : str, form : Form = Form._10Q, unit : str = 'USD') -> dict | None:
    operating_expenses = company_facts.get_fact(fact='OperatingExpenses', form=form, unit=unit)
    interest_expenses = company_facts.get_fact(fact='InterestExpense', form=form, unit=unit)
    sgna_expenses = company_facts.get_fact(fact='SellingGeneralAndAdministrativeExpense', form=form, unit=unit)
    income_taxes = company_facts.get_fact(fact='IncomeTaxesPaidNet', form=form, unit=unit)
    depreciation = company_facts.get_fact(fact='Depreciation', form=form, unit=unit)

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

def price_to_earnings_ratio(company_facts : CompanyFacts, end : str, form : Form = Form._10Q, unit : str = 'USD') -> dict | None:
    _market_cap = market_cap(company_facts, end, form, unit)
    net_income = company_facts.get_fact(fact='NetIncomeLoss', form=form, unit=unit)

    if not _market_cap or not net_income or end not in net_income:
        return None
    
    return {
        'fy' : _market_cap['fy'],
        'form' : _market_cap['form'],
        'filed' : _market_cap['filed'],
        'val' : _market_cap['val'] / net_income[end]['val'] if net_income[end]['val'] != 0 else None
        }

def price_to_sales_ratio(company_facts : CompanyFacts, end : str, form : Form = Form._10Q, unit : str = 'USD') -> dict | None:
    common_stock_value = company_facts.get_fact(fact='CommonStockValue', form=form, unit=unit)
    _revenue = revenue(company_facts, end, form, unit)
    outstanding_shares = company_facts.get_fact(fact='EntityCommonStockSharesOutstanding', form=form, unit='shares')

    if not common_stock_value or not _revenue or not outstanding_shares or end not in common_stock_value or end not in outstanding_shares:
        return None
    
    return {
        'fy' : common_stock_value[end]['fy'],
        'form' : common_stock_value[end]['form'],
        'filed' : common_stock_value[end]['filed'],
        'val' : common_stock_value[end]['val'] / (_revenue['val'] / outstanding_shares[end]['val']) if _revenue['val'] != 0 and outstanding_shares[end]['val'] != 0 else None
        }

def price_to_cash_flow_ratio(company_facts : CompanyFacts, end : str, form : Form = Form._10Q, unit : str = 'USD') -> dict | None:
    operating_cash_flow = company_facts.get_fact(fact='NetCashProvidedByUsedInOperatingActivities', form=form, unit=unit)

    _market_cap = market_cap(company_facts, end, form, unit)

    if not operating_cash_flow or not _market_cap or end not in operating_cash_flow:
        return None
    
    return {
        'fy' : operating_cash_flow[end]['fy'],
        'form' : operating_cash_flow[end]['form'],
        'filed' : operating_cash_flow[end]['filed'],
        'val' : _market_cap['val'] / operating_cash_flow[end]['val'] if operating_cash_flow[end]['val'] != 0 else None
        }

def price_to_free_cash_flow_ratio(company_facts : CompanyFacts, end : str, form : Form = Form._10Q, unit : str = 'USD') -> dict | None:
    _free_cash_flow = free_cash_flow(company_facts, end, form, unit)

    _market_cap = market_cap(company_facts, end, form, unit)

    if not _free_cash_flow or not _market_cap:
        return None
    
    return {
        'fy' : _free_cash_flow[end]['fy'],
        'form' : _free_cash_flow[end]['form'],
        'filed' : _free_cash_flow[end]['filed'],
        'val' : _market_cap['val'] / _free_cash_flow['val'] if _free_cash_flow['val'] != 0 else None
        }

def price_to_book_ratio(company_facts : CompanyFacts, end : str, form : Form = Form._10Q, unit : str = 'USD') -> dict | None:
    _market_cap = market_cap(company_facts, end, form, unit)
    book_value = company_facts.get_fact(fact='StockholdersEquity', form=form, unit=unit)

    if not _market_cap or not book_value or end not in book_value:
        return None
    
    return {
        'fy' : _market_cap['fy'],
        'form' : _market_cap['form'],
        'filed' : _market_cap['filed'],
        'val' : _market_cap['val'] / book_value[end]['val'] if book_value[end]['val'] != 0 else None
        }

def enterprise_value(company_facts : CompanyFacts, end : str, form : Form = Form._10Q, unit : str = 'USD') -> dict | None:
    _market_cap = market_cap(company_facts, end, form, unit)
    outstanding_debt = company_facts.get_fact(fact='LongTermDebt', form=form, unit=unit)
    cash = company_facts.get_fact(fact='CashAndCashEquivalentsAtCarryingValue', form=form, unit=unit)

    if not _market_cap or not outstanding_debt or not cash or end not in outstanding_debt or end not in cash:
        return None
    
    return {
        'fy' : _market_cap['fy'],
        'form' : _market_cap['form'],
        'filed' : _market_cap['filed'],
        'val' : _market_cap['val'] - outstanding_debt[end]['val'] + cash[end]['val']
        }

def sales_ratio_to_enterprise_value_to_sales(company_facts : CompanyFacts, end : str, form : Form = Form._10Q, unit : str = 'USD') -> dict | None:
    _enterprise_value = enterprise_value(company_facts, end, form, unit)
    _revenue = revenue(company_facts, end, form, unit)

    if not _enterprise_value or not _revenue:
        return None
    
    return {
        'fy' : _enterprise_value['fy'],
        'form' : _enterprise_value['form'],
        'filed' : _enterprise_value['filed'],
        'val' : _enterprise_value['val'] / _revenue['val'] if _revenue['val'] != 0 else None
        }

def revenue(company_facts : CompanyFacts, end : str, form : Form = Form._10Q, unit : str = 'USD') -> dict | None:
    operating_income_loss = company_facts.get_fact(fact='OperatingIncomeLoss', form=form, unit=unit)
    operating_expenses = company_facts.get_fact(fact='OperatingExpenses', form=form, unit=unit)

    if not operating_income_loss or not operating_expenses or end not in operating_expenses or end not in operating_income_loss:
        return None
    
    return {
        'fy' : operating_expenses[end]['fy'],
        'form' : operating_expenses[end]['form'],
        'filed' : operating_expenses[end]['filed'],
        'val' : operating_income_loss[end]['val'] + operating_expenses[end]['val']
    }

def ebit(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    operating_income_loss = company_facts.get_fact(fact='OperatingIncomeLoss', form=form, unit=unit)
    cogs = company_facts.get_fact(fact='CostOfGoodsAndServicesSold', form=form, unit=unit)

    if not operating_income_loss or not cogs or end not in operating_income_loss or end not in cogs:
        return None
    
    return {
        'fy' : operating_income_loss[end]['fy'],
        'form' : operating_income_loss[end]['form'],
        'filed' : operating_income_loss[end]['filed'],
        'val' : operating_income_loss[end]['val'] - cogs[end]['val']
    }

def ebitda(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    _ebit = ebit(company_facts, end, form, unit)
    depreciation = company_facts.get_fact(fact='Depreciation', form=form, unit=unit)

    if not _ebit or not depreciation or end not in depreciation:
        return None
    
    return {
        'fy' : _ebit['fy'],
        'form' : _ebit['form'],
        'filed' : _ebit['filed'],
        'val' : _ebit['val'] + depreciation[end]['val']
    }

def enterprise_value_over_ebitda(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    _enterprise_value = enterprise_value(company_facts, end, form, unit)
    _ebitda = ebitda(company_facts, end, form, unit)

    if not _enterprise_value or not _ebitda:
        return None
    
    return {
        'fy' : _enterprise_value['fy'],
        'form' : _enterprise_value['form'],
        'filed' : _enterprise_value['filed'],
        'val' : _enterprise_value['val'] / _ebitda['val'] if _ebitda['val'] != 0 else None
    }

def enterprise_value_to_operating_cash_flow(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    _enterprise_value = enterprise_value(company_facts, end, form, unit)
    operating_cash_flow = company_facts.get_fact(fact='NetCashProvidedByUsedInOperatingActivities', form=form, unit=unit)

    if not _enterprise_value or not operating_cash_flow or end not in operating_cash_flow:
        return None
    
    return {
        'fy' : _enterprise_value['fy'],
        'form' : _enterprise_value['form'],
        'filed' : _enterprise_value['filed'],
        'val' : _enterprise_value['val'] / operating_cash_flow[end]['val'] if operating_cash_flow[end]['val'] != 0 else None
    }

def earnings_yield(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    _ebit = ebit(company_facts, end, form, unit)
    _market_cap = market_cap(company_facts, end, form, unit)

    if not _ebit or not _market_cap:
        return None
    
    return {
        'fy' : _ebit['fy'],
        'form' : _ebit['form'],
        'filed' : _ebit['filed'],
        'val' : _ebit['val'] / _market_cap['val'] if _market_cap['val'] != 0 else None
    }

def free_cash_flow(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    operating_cash_flow = company_facts.get_fact(fact='NetCashProvidedByUsedInOperatingActivities', form=form, unit=unit)
    capital_expenditures = company_facts.get_fact(fact='PaymentsToAcquirePropertyPlantAndEquipment', form=form, unit=unit)

    if not operating_cash_flow or not capital_expenditures or end not in operating_cash_flow or end not in capital_expenditures:
        return None
    
    return {
        'fy' : operating_cash_flow[end]['fy'],
        'form' : operating_cash_flow[end]['form'],
        'filed' : operating_cash_flow[end]['filed'],
        'val' : operating_cash_flow[end]['val'] - capital_expenditures[end]['val']
    }

def free_cash_flow_yield(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    _free_cash_flow = free_cash_flow(company_facts, end, form, unit)
    _market_cap = market_cap(company_facts, end, form, unit)

    if not _free_cash_flow or not _market_cap:
        return None
    
    return {
        'fy' : _free_cash_flow['fy'],
        'form' : _free_cash_flow['form'],
        'filed' : _free_cash_flow['filed'],
        'val' : _free_cash_flow['val'] / _market_cap['val'] if _market_cap['val'] != 0 else None
    }

def net_debt_to_ebitda(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    total_debt = company_facts.get_fact(fact='Liabilities', form=form, unit=unit)
    cash = company_facts.get_fact(fact='CashAndCashEquivalentsAtCarryingValue', form=form, unit=unit)
    _ebitda = ebitda(company_facts, end, form, unit)

    if not total_debt or not cash or not _ebitda or end not in total_debt or end not in cash:
        return None
    
    return {
        'fy' : total_debt[end]['fy'],
        'form' : total_debt[end]['form'],
        'filed' : total_debt[end]['filed'],
        'val' : (total_debt[end]['val'] - cash[end]['val']) / _ebitda['val'] if _ebitda['val'] != 0 else None
    }

def interest_coverage_ratio(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    _ebit = ebit(company_facts, end, form, unit)
    interest_expense = company_facts.get_fact(fact='InterestExpense', form=form, unit=unit)

    if not _ebit or not interest_expense or end not in interest_expense:
        return None
    
    return {
        'fy' : _ebit['fy'],
        'form' : _ebit['form'],
        'filed' : _ebit['filed'],
        'val' : _ebit['val'] / interest_expense[end]['val'] if interest_expense[end]['val'] != 0 else None
    }

def income_quality(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    cash_flow_from_operations = company_facts.get_fact(fact='NetCashProvidedByUsedInOperatingActivities', form=form, unit=unit)
    net_income = company_facts.get_fact(fact='NetIncomeLoss', form=form, unit=unit)

    if not cash_flow_from_operations or not net_income or end not in cash_flow_from_operations or end not in net_income:
        return None
    
    return {
        'fy' : cash_flow_from_operations[end]['fy'],
        'form' : cash_flow_from_operations[end]['form'],
        'filed' : cash_flow_from_operations[end]['filed'],
        'val' : cash_flow_from_operations[end]['val'] / net_income[end]['val']
    }

def dividend_yield(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    dividends = company_facts.get_fact(fact='PaymentsOfDividendsTotal', form=form, unit=unit)
    _market_cap = market_cap(company_facts, end, form, unit)

    if not dividends or not _market_cap or end not in dividends:
        return None
    
    return {
        'fy' : dividends[end]['fy'],
        'form' : dividends[end]['form'],
        'filed' : dividends[end]['filed'],
        'val' : dividends[end]['val'] / _market_cap['val']
    }

def payout_ratio(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    dividends = company_facts.get_fact(fact='PaymentsOfDividendsTotal', form=form, unit=unit)
    net_income = company_facts.get_fact(fact='NetIncomeLoss', form=form, unit=unit)

    if not dividends or not net_income or end not in dividends or end not in net_income:
        return None
    
    return {
        'fy' : dividends[end]['fy'],
        'form' : dividends[end]['form'],
        'filed' : dividends[end]['filed'],
        'val' : dividends[end]['val'] / net_income[end]['val']
    }

def sales_general_and_administrative_to_revenue(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    sgna_expenses = company_facts.get_fact(fact='SellingGeneralAndAdministrativeExpense', form=form, unit=unit)
    _revenue = revenue(company_facts, end, form, unit)

    if not sgna_expenses or not _revenue or end not in sgna_expenses:
        return None
    
    return {
        'fy' : sgna_expenses[end]['fy'],
        'form' : sgna_expenses[end]['form'],
        'filed' : sgna_expenses[end]['filed'],
        'val' : sgna_expenses[end]['val'] / _revenue['val'] if _revenue['val'] != 0 else None
    }

def return_on_tangible_assets(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    _ebit = ebit(company_facts, end, form, unit)
    tangible_assets = company_facts.get_fact(fact='Assets', form=form, unit=unit)
    goodwill = company_facts.get_fact(fact='Goodwill', form=form, unit=unit)

    if not _ebit or not tangible_assets or not goodwill or end not in tangible_assets or end not in goodwill:
        return None
    
    return {
        'fy' : _ebit['fy'],
        'form' : _ebit['form'],
        'filed' : _ebit['filed'],
        'val' : _ebit['val'] / (tangible_assets[end]['val'] - goodwill[end]['val']) if tangible_assets[end]['val'] - goodwill[end]['val'] != 0 else None
    }

def tangible_asset_value(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    tangible_assets = company_facts.get_fact(fact='Assets', form=form, unit=unit)
    goodwill = company_facts.get_fact(fact='Goodwill', form=form, unit=unit)

    if not tangible_assets or not goodwill or end not in tangible_assets or end not in goodwill:
        return None
    
    return {
        'fy' : tangible_assets[end]['fy'],
        'form' : tangible_assets[end]['form'],
        'filed' : tangible_assets[end]['filed'],
        'val' : tangible_assets[end]['val'] - goodwill[end]['val']
    }

def net_current_asset_value(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    current_assets = company_facts.get_fact(fact='AssetsCurrent', form=form, unit=unit)
    current_liabilities = company_facts.get_fact(fact='LiabilitiesCurrent', form=form, unit=unit)

    if not current_assets or not current_liabilities or end not in current_assets or end not in current_liabilities:
        return None
    
    return {
        'fy' : current_assets[end]['fy'],
        'form' : current_assets[end]['form'],
        'filed' : current_assets[end]['filed'],
        'val' : current_assets[end]['val'] - current_liabilities[end]['val']
    }

def revenue_per_share(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    _revenue = revenue(company_facts, end, form, unit)
    outstanding_shares = company_facts.get_fact(fact='EntityCommonStockSharesOutstanding', form=form, unit='shares')

    if not _revenue or not outstanding_shares or end not in outstanding_shares:
        return None
    
    return {
        'fy' : _revenue['fy'],
        'form' : _revenue['form'],
        'filed' : _revenue['filed'],
        'val' : _revenue['val'] / outstanding_shares[end]['val'] if outstanding_shares[end]['val'] != 0 else None
    }

def interest_debt_per_share(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    interest_expense = company_facts.get_fact(fact='InterestExpense', form=form, unit=unit)
    outstanding_debt = company_facts.get_fact(fact='LongTermDebt', form=form, unit=unit)
    outstanding_shares = company_facts.get_fact(fact='EntityCommonStockSharesOutstanding', form=form, unit='shares')

    if not interest_expense or not outstanding_debt or not outstanding_shares or end not in interest_expense or end not in outstanding_debt or end not in outstanding_shares:
        return None
    
    return {
        'fy' : interest_expense[end]['fy'],
        'form' : interest_expense[end]['form'],
        'filed' : interest_expense[end]['filed'],
        'val' : (interest_expense[end]['val'] + outstanding_debt[end]['val']) / outstanding_shares[end]['val'] if outstanding_shares[end]['val'] != 0 else None
    }

def return_on_equity(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    net_income = company_facts.get_fact(fact='NetIncomeLoss', form=form, unit=unit)
    stockholders_equity = company_facts.get_fact(fact='StockholdersEquity', form=form, unit=unit)

    if not net_income or not stockholders_equity or end not in net_income or end not in stockholders_equity:
        return None
    
    return {
        'fy' : net_income[end]['fy'],
        'form' : net_income[end]['form'],
        'filed' : net_income[end]['filed'],
        'val' : net_income[end]['val'] / stockholders_equity[end]['val'] if stockholders_equity[end]['val'] != 0 else None
    }

def capex_per_share(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    capex = company_facts.get_fact(fact='PaymentsToAcquirePropertyPlantAndEquipment', form=form, unit=unit)
    outstanding_shares = company_facts.get_fact(fact='EntityCommonStockSharesOutstanding', form=form, unit='shares')

    if not capex or not outstanding_shares or end not in capex or end not in outstanding_shares:
        return None
    
    return {
        'fy' : capex[end]['fy'],
        'form' : capex[end]['form'],
        'filed' : capex[end]['filed'],
        'val' : capex[end]['val'] / outstanding_shares[end]['val'] if outstanding_shares[end]['val'] != 0 else None
    }

def quick_ratio(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    current_assets = company_facts.get_fact(fact='AssetsCurrent', form=form, unit=unit)
    current_liabilities = company_facts.get_fact(fact='LiabilitiesCurrent', form=form, unit=unit)
    inventory = company_facts.get_fact(fact='InventoryNet', form=form, unit=unit)

    if not current_assets or not current_liabilities or not inventory or end not in current_assets or end not in current_liabilities or end not in inventory:
        return None
    
    return {
        'fy' : current_assets[end]['fy'],
        'form' : current_assets[end]['form'],
        'filed' : current_assets[end]['filed'],
        'val' : (current_assets[end]['val'] - inventory[end]['val']) / current_liabilities[end]['val'] if current_liabilities[end]['val'] != 0 else None
    }

def cash_ratio(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    cash = company_facts.get_fact(fact='CashAndCashEquivalentsAtCarryingValue', form=form, unit=unit)
    current_liabilities = company_facts.get_fact(fact='LiabilitiesCurrent', form=form, unit=unit)

    if not cash or not current_liabilities or end not in cash or end not in current_liabilities:
        return None
    
    return {
        'fy' : cash[end]['fy'],
        'form' : cash[end]['form'],
        'filed' : cash[end]['filed'],
        'val' : cash[end]['val'] / current_liabilities[end]['val'] if current_liabilities[end]['val'] != 0 else None
    }

def gross_profit_margin(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    gross_profit = company_facts.get_fact(fact='GrossProfit', form=form, unit=unit)
    _revenue = revenue(company_facts, end, form, unit)

    if not gross_profit or not _revenue or end not in gross_profit:
        return None
    
    return {
        'fy' : gross_profit[end]['fy'],
        'form' : gross_profit[end]['form'],
        'filed' : gross_profit[end]['filed'],
        'val' : gross_profit[end]['val'] / _revenue['val'] if _revenue['val'] != 0 else None
    }

def return_on_assets(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    net_income = company_facts.get_fact(fact='NetIncomeLoss', form=form, unit=unit)
    assets = company_facts.get_fact(fact='Assets', form=form, unit=unit)

    if not net_income or not assets or end not in net_income or end not in assets:
        return None
    
    return {
        'fy' : net_income[end]['fy'],
        'form' : net_income[end]['form'],
        'filed' : net_income[end]['filed'],
        'val' : net_income[end]['val'] / assets[end]['val'] if assets[end]['val'] != 0 else None
    }

def return_on_equity(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    net_income = company_facts.get_fact(fact='NetIncomeLoss', form=form, unit=unit)
    stockholders_equity = company_facts.get_fact(fact='StockholdersEquity', form=form, unit=unit)

    if not net_income or not stockholders_equity or end not in net_income or end not in stockholders_equity:
        return None
    
    return {
        'fy' : net_income[end]['fy'],
        'form' : net_income[end]['form'],
        'filed' : net_income[end]['filed'],
        'val' : net_income[end]['val'] / stockholders_equity[end]['val'] if stockholders_equity[end]['val'] != 0 else None
    }

def return_on_capital_employed(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    _ebit = ebit(company_facts, end, form, unit)
    total_assets = company_facts.get_fact(fact='Assets', form=form, unit=unit)
    current_liabilities = company_facts.get_fact(fact='LiabilitiesCurrent', form=form, unit=unit)

    if not _ebit or not total_assets or not current_liabilities or end not in total_assets or end not in current_liabilities:
        return None
    
    return {
        'fy' : _ebit['fy'],
        'form' : _ebit['form'],
        'filed' : _ebit['filed'],
        'val' : _ebit['val'] / (total_assets[end]['val'] - current_liabilities[end]['val']) if (total_assets[end]['val'] - current_liabilities[end]['val']) != 0 else None
    }

def company_equity_multiplier(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    total_assets = company_facts.get_fact(fact='Assets', form=form, unit=unit)
    stockholders_equity = company_facts.get_fact(fact='StockholdersEquity', form=form, unit=unit)

    if not total_assets or not stockholders_equity or end not in total_assets or end not in stockholders_equity:
        return None
    
    return {
        'fy' : total_assets[end]['fy'],
        'form' : total_assets[end]['form'],
        'filed' : total_assets[end]['filed'],
        'val' : total_assets[end]['val'] / stockholders_equity[end]['val'] if stockholders_equity[end]['val'] != 0 else None
    }

def net_income_per_ebt(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    net_income = company_facts.get_fact(fact='NetIncomeLoss', form=form, unit=unit)
    ebt = company_facts.get_fact(fact='IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments', form=form, unit=unit)

    if not net_income or not ebt or end not in net_income or end not in ebt:
        return None
    
    return {
        'fy' : net_income[end]['fy'],
        'form' : net_income[end]['form'],
        'filed' : net_income[end]['filed'],
        'val' : net_income[end]['val'] / ebt[end]['val'] if ebt[end]['val'] != 0 else None
    }

def long_term_debt_to_capitalization(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    long_term_debt = company_facts.get_fact(fact='LongTermDebt', form=form, unit=unit)
    total_stockholders_equity = company_facts.get_fact(fact='StockholdersEquity', form=form, unit=unit)

    if not long_term_debt or not total_stockholders_equity or end not in long_term_debt or end not in total_stockholders_equity:
        return None
    
    return {
        'fy' : long_term_debt[end]['fy'],
        'form' : long_term_debt[end]['form'],
        'filed' : long_term_debt[end]['filed'],
        'val' : long_term_debt[end]['val'] / total_stockholders_equity[end]['val'] if total_stockholders_equity[end]['val'] != 0 else None
    }

def total_debt_to_capitalization(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    total_debt = company_facts.get_fact(fact='Liabilities', form=form, unit=unit)
    total_stockholders_equity = company_facts.get_fact(fact='StockholdersEquity', form=form, unit=unit)

    if not total_debt or not total_stockholders_equity or end not in total_debt or end not in total_stockholders_equity:
        return None
    
    return {
        'fy' : total_debt[end]['fy'],
        'form' : total_debt[end]['form'],
        'filed' : total_debt[end]['filed'],
        'val' : total_debt[end]['val'] / total_stockholders_equity[end]['val'] if total_stockholders_equity[end]['val'] != 0 else None
    }

def fixed_asset_turnover(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    _revenue = revenue(company_facts, end, form, unit)
    net_ppe = company_facts.get_fact(fact='PropertyPlantAndEquipmentNet', form=form, unit=unit)

    if not _revenue or not net_ppe or end not in net_ppe:
        return None
    
    return {
        'fy' : _revenue['fy'],
        'form' : _revenue['form'],
        'filed' : _revenue['filed'],
        'val' : _revenue['val'] / net_ppe[end]['val'] if net_ppe[end]['val'] != 0 else None
    }

def operating_cash_flow_sales_ratio(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    operating_cash_flow = company_facts.get_fact(fact='NetCashProvidedByUsedInOperatingActivities', form=form, unit=unit)
    _revenue = revenue(company_facts, end, form, unit)

    if not operating_cash_flow or not _revenue or end not in operating_cash_flow:
        return None
    
    return {
        'fy' : operating_cash_flow[end]['fy'],
        'form' : operating_cash_flow[end]['form'],
        'filed' : operating_cash_flow[end]['filed'],
        'val' : operating_cash_flow[end]['val'] / _revenue['val'] if _revenue['val'] != 0 else None
    }

def free_cash_flow_sales_ratio(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    _free_cash_flow = free_cash_flow(company_facts, end, form, unit)
    _revenue = revenue(company_facts, end, form, unit)

    if not _free_cash_flow or not _revenue:
        return None
    
    return {
        'fy' : _free_cash_flow['fy'],
        'form' : _free_cash_flow['form'],
        'filed' : _free_cash_flow['filed'],
        'val' : _free_cash_flow['val'] / _revenue['val'] if _revenue['val'] != 0 else None
    }

def cash_flow_coverage_ratio(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    operating_cash_flow = company_facts.get_fact(fact='NetCashProvidedByUsedInOperatingActivities', form=form, unit=unit)
    outstanding_debt = company_facts.get_fact(fact='LongTermDebt', form=form, unit=unit)

    if not operating_cash_flow or not outstanding_debt or end not in operating_cash_flow or end not in outstanding_debt:
        return None
    
    return {
        'fy' : operating_cash_flow[end]['fy'],
        'form' : operating_cash_flow[end]['form'],
        'filed' : operating_cash_flow[end]['filed'],
        'val' : operating_cash_flow[end]['val'] / outstanding_debt[end]['val'] if outstanding_debt[end]['val'] != 0 else None
    }

def short_term_coverage_ratio(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    cash = company_facts.get_fact(fact='CashAndCashEquivalentsAtCarryingValue', form=form, unit=unit)
    short_term_investments = company_facts.get_fact(fact='AvailableForSaleSecuritiesCurrent', form=form, unit=unit)
    receivables = company_facts.get_fact(fact='AccountsReceivableNetCurrent', form=form, unit=unit)
    current_liabilities = company_facts.get_fact(fact='LiabilitiesCurrent', form=form, unit=unit)

    if not cash or not short_term_investments or not receivables or not current_liabilities or end not in cash or end not in short_term_investments or end not in receivables or end not in current_liabilities:
        return None
    
    return {
        'fy' : cash[end]['fy'],
        'form' : cash[end]['form'],
        'filed' : cash[end]['filed'],
        'val' : (cash[end]['val'] + short_term_investments[end]['val'] + receivables[end]['val']) / current_liabilities[end]['val'] if current_liabilities[end]['val'] != 0 else None
    }

def capital_expenditure_coverage_ratio(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    operating_cash_flow = company_facts.get_fact(fact='NetCashProvidedByUsedInOperatingActivities', form=form, unit=unit)
    capital_expenditures = company_facts.get_fact(fact='PaymentsToAcquirePropertyPlantAndEquipment', form=form, unit=unit)

    if not operating_cash_flow or not capital_expenditures or end not in operating_cash_flow or end not in capital_expenditures:
        return None
    
    return {
        'fy' : operating_cash_flow[end]['fy'],
        'form' : operating_cash_flow[end]['form'],
        'filed' : operating_cash_flow[end]['filed'],
        'val' : operating_cash_flow[end]['val'] / capital_expenditures[end]['val'] if capital_expenditures[end]['val'] != 0 else None
    }

def dividend_paid_and_capex_coverage_ratio(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    operating_cash_flow = company_facts.get_fact(fact='NetCashProvidedByUsedInOperatingActivities', form=form, unit=unit)
    dividends = company_facts.get_fact(fact='PaymentsOfDividendsTotal', form=form, unit=unit)
    capital_expenditures = company_facts.get_fact(fact='PaymentsToAcquirePropertyPlantAndEquipment', form=form, unit=unit)

    if not operating_cash_flow or not dividends or not capital_expenditures or end not in operating_cash_flow or end not in dividends or end not in capital_expenditures:
        return None
    
    return {
        'fy' : operating_cash_flow[end]['fy'],
        'form' : operating_cash_flow[end]['form'],
        'filed' : operating_cash_flow[end]['filed'],
        'val' : operating_cash_flow[end]['val'] / (dividends[end]['val'] + capital_expenditures[end]['val']) if (dividends[end]['val'] + capital_expenditures[end]['val']) != 0 else None
    }

def operating_profit_margin(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    operating_income_loss = company_facts.get_fact(fact='OperatingIncomeLoss', form=form, unit=unit)
    _revenue = revenue(company_facts, end, form, unit)

    if not operating_income_loss or not _revenue or end not in operating_income_loss:
        return None
    
    return {
        'fy' : operating_income_loss[end]['fy'],
        'form' : operating_income_loss[end]['form'],
        'filed' : operating_income_loss[end]['filed'],
        'val' : operating_income_loss[end]['val'] / _revenue['val'] if _revenue['val'] != 0 else None
    }

def pretax_profit_margin(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:  
    ebt = company_facts.get_fact(fact='IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments', form=form, unit=unit)
    _revenue = revenue(company_facts, end, form, unit)

    if not ebt or not _revenue or end not in ebt:
        return None
    
    return {
        'fy' : ebt[end]['fy'],
        'form' : ebt[end]['form'],
        'filed' : ebt[end]['filed'],
        'val' : ebt[end]['val'] / _revenue['val'] if _revenue['val'] != 0 else None
    }

def net_profit_margin(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    net_income = company_facts.get_fact(fact='NetIncomeLoss', form=form, unit=unit)
    _revenue = revenue(company_facts, end, form, unit)

    if not net_income or not _revenue or end not in net_income:
        return None
    
    return {
        'fy' : net_income[end]['fy'],
        'form' : net_income[end]['form'],
        'filed' : net_income[end]['filed'],
        'val' : net_income[end]['val'] / _revenue['val'] if _revenue['val'] != 0 else None
    }

def ni_per_ebt(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    net_income = company_facts.get_fact(fact='NetIncomeLoss', form=form, unit=unit)
    ebt = company_facts.get_fact(fact='IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments', form=form, unit=unit)

    if not net_income or not ebt or end not in net_income or end not in ebt:
        return None
    
    return {
        'fy' : net_income[end]['fy'],
        'form' : net_income[end]['form'],
        'filed' : net_income[end]['filed'],
        'val' : net_income[end]['val'] / ebt[end]['val'] if ebt[end]['val'] != 0 else None
    }

def ebt_per_ebit(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    ebt = company_facts.get_fact(fact='IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments', form=form, unit=unit)
    _ebit = ebit(company_facts, end, form, unit)

    if not ebt or not _ebit or end not in ebt:
        return None
    
    return {
        'fy' : ebt[end]['fy'],
        'form' : ebt[end]['form'],
        'filed' : ebt[end]['filed'],
        'val' : ebt[end]['val'] / _ebit['val'] if _ebit['val'] != 0 else None
    }

def debt_ratio(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    total_liabilities = company_facts.get_fact(fact='Liabilities', form=form, unit=unit)
    total_assets = company_facts.get_fact(fact='Assets', form=form, unit=unit)

    if not total_liabilities or not total_assets or end not in total_liabilities or end not in total_assets:
        return None
    
    return {
        'fy' : total_liabilities[end]['fy'],
        'form' : total_liabilities[end]['form'],
        'filed' : total_liabilities[end]['filed'],
        'val' : total_liabilities[end]['val'] / total_assets[end]['val'] if total_assets[end]['val'] != 0 else None
    }

def debt_equity_ratio(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    total_liabilities = company_facts.get_fact(fact='Liabilities', form=form, unit=unit)
    stockholders_equity = company_facts.get_fact(fact='StockholdersEquity', form=form, unit=unit)

    if not total_liabilities or not stockholders_equity or end not in total_liabilities or end not in stockholders_equity:
        return None
    
    return {
        'fy' : total_liabilities[end]['fy'],
        'form' : total_liabilities[end]['form'],
        'filed' : total_liabilities[end]['filed'],
        'val' : total_liabilities[end]['val'] / stockholders_equity[end]['val'] if stockholders_equity[end]['val'] != 0 else None
    }

def cash_flow_to_debt_ratio(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    operating_cash_flow = company_facts.get_fact(fact='NetCashProvidedByUsedInOperatingActivities', form=form, unit=unit)
    total_debt = company_facts.get_fact(fact='Liabilities', form=form, unit=unit)

    if not operating_cash_flow or not total_debt or end not in operating_cash_flow or end not in total_debt:
        return None
    
    return {
        'fy' : operating_cash_flow[end]['fy'],
        'form' : operating_cash_flow[end]['form'],
        'filed' : operating_cash_flow[end]['filed'],
        'val' : operating_cash_flow[end]['val'] / total_debt[end]['val'] if total_debt[end]['val'] != 0 else None
    }

def asset_turnover(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    _revenue = revenue(company_facts, end, form, unit)
    total_assets = company_facts.get_fact(fact='Assets', form=form, unit=unit)

    if not _revenue or not total_assets or end not in total_assets:
        return None
    
    return {
        'fy' : _revenue['fy'],
        'form' : _revenue['form'],
        'filed' : _revenue['filed'],
        'val' : _revenue['val'] / total_assets[end]['val'] if total_assets[end]['val'] != 0 else None
    }

def enterprise_value_multiplier(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    _enterprise_value = enterprise_value(company_facts, end, form, unit)
    _ebitda = ebitda(company_facts, end, form, unit)

    if not _enterprise_value or not _ebitda:
        return None
    
    return {
        'fy' : _enterprise_value['fy'],
        'form' : _enterprise_value['form'],
        'filed' : _enterprise_value['filed'],
        'val' : _enterprise_value['val'] / _ebitda['val'] if _ebitda['val'] != 0 else None
    }

def return_on_invested_capital(company_facts: CompanyFacts, end: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    assets = company_facts.get_fact(fact='Assets', form=form, unit=unit)
    current_liabilities = company_facts.get_fact(fact='LiabilitiesCurrent', form=form, unit=unit)
    _ebit = ebit(company_facts, end, form, unit)
    
    if not assets or not current_liabilities or not _ebit or end not in assets or end not in current_liabilities:
        return None
    
    ROI = _ebit['val'] / (assets[end]['val'] - current_liabilities[end]['val']) if (assets[end]['val'] - current_liabilities[end]['val']) != 0 else None
    
    return {
        'fy' : assets[end]['fy'],
        'form' : assets[end]['form'],
        'filed' : assets[end]['filed'],
        'val' : ROI
    }
    
key_metric_function_map = {
    'CurrentRatio' : current_ratio,
    'DebtToEquity' : debt_to_equity,
    'DebtToAssets' : debt_to_assets,
    'MarketCapitalization' : market_cap,
    'Expenses' : expenses,
    'PriceToEarningsRatio' : price_to_earnings_ratio,
    'PriceToSalesRatio' : price_to_sales_ratio,
    'PriceToCashFlowRatio' : price_to_cash_flow_ratio,
    'PriceToFreeCashFlowsRatio' : price_to_free_cash_flow_ratio,
    'PriceToBookRatio' : price_to_book_ratio,
    'EnterpriseValue' : enterprise_value,
    'SalesRatioToEnterpriseValueSales' : sales_ratio_to_enterprise_value_to_sales,
    'Revenue' : revenue,
    'EBIT' : ebit,
    'EBITDA' : ebitda,
    'EnterpriseValueOverEBITDA' : enterprise_value_over_ebitda,
    'EnterpriseValueToOperatingCashFlow' : enterprise_value_to_operating_cash_flow,
    'EarningsYield' : earnings_yield,
    'FreeCashFlow' : free_cash_flow,
    'FreeCashFlowYield' : free_cash_flow_yield,
    'NetDebtToEBITDA' : net_debt_to_ebitda,
    'InterestCoverageRatio' : interest_coverage_ratio,
    'IncomeQuality' : income_quality,
    'DividendYield' : dividend_yield,
    'PayoutRatio' : payout_ratio,
    'SalesGeneralAndAdministrativeToRevenue' : sales_general_and_administrative_to_revenue,
    'ReturnOnTangibleAssets' : return_on_tangible_assets,
    'TangibleAssetValue' : tangible_asset_value,
    'NetCurrentAssetValue' : net_current_asset_value,
    'RevenuePerShare' : revenue_per_share,
    'InterestDebtPerShare' : interest_debt_per_share,
    'ReturnOnEquity' : return_on_equity,
    'CapexPerShare' : capex_per_share,
    'QuickRatio' : quick_ratio,
    'CashRatio' : cash_ratio,
    'GrossProfitMargin' : gross_profit_margin,
    'ReturnOnAssets' : return_on_assets,
    'ReturnOnEquity' : return_on_equity,
    'ReturnOnCapitalEmployed' : return_on_capital_employed,
    'CompanyEquityMultiplier' : company_equity_multiplier,
    'NetIncomePerEBT' : net_income_per_ebt,
    'LongTermDebtToCapitalization' : long_term_debt_to_capitalization,
    'TotalDebtToCapitalization' : total_debt_to_capitalization,
    'FixedAssetTurnover' : fixed_asset_turnover,
    'OperatingCashFlowSalesRatio' : operating_cash_flow_sales_ratio,
    'FreeCashFlowSalesRatio' : free_cash_flow_sales_ratio,
    'CashFlowCoverageRatio' : cash_flow_coverage_ratio,
    'ShortTermCoverageRatio' : short_term_coverage_ratio,
    'CapitalExpenditureCoverageRatio' : capital_expenditure_coverage_ratio,
    'DividendPaidAndCapexCoverageRatio' : dividend_paid_and_capex_coverage_ratio,
    'OperatingProfitMargin' : operating_profit_margin,
    'PretaxProfitMargin' : pretax_profit_margin,
    'NetProfitMargin' : net_profit_margin,
    'NIPerEBT' : ni_per_ebt,
    'EBTPerEBIT' : ebt_per_ebit,
    'DebtRatio' : debt_ratio,
    'DebtEquityRatio' : debt_equity_ratio,
    'CashFlowToDebtRatio' : cash_flow_to_debt_ratio,
    'AssetTurnover' : asset_turnover,
    'EnterpriseValueMultiplier' : enterprise_value_multiplier,
    'ReturnOnInvestedCapital' : return_on_invested_capital
}