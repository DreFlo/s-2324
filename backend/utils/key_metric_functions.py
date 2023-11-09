from model.company_facts import CompanyFacts, Form

def current_ratio(company_facts : CompanyFacts, filed : str, form : Form = Form._10Q, unit : str = 'USD') -> dict | None:
    current_assets = company_facts.get_fact(fact='AssetsCurrent', form=form, unit=unit)
    current_liabilities = company_facts.get_fact(fact='LiabilitiesCurrent', form=form, unit=unit)

    if not current_assets or not current_liabilities or filed not in current_assets or filed not in current_liabilities:
        return None

    return {
        'fy' : current_assets[filed]['fy'],
        'form' : current_assets[filed]['form'],
        'filed' : filed,
        'val' : current_assets[filed]['val'] / current_liabilities[filed]['val'] if current_liabilities[filed]['val'] != 0 else None
        }

def debt_to_equity(company_facts : CompanyFacts, filed : str, form : Form = Form._10Q, unit : str = 'USD') -> dict | None:
    long_term_debt = company_facts.get_fact(fact='LongTermDebt', form=form, unit=unit)
    stockholders_equity = company_facts.get_fact(fact='StockholdersEquity', form=form, unit=unit)

    if not long_term_debt or not stockholders_equity or filed not in long_term_debt or filed not in stockholders_equity:
        return None

    return {
        'fy' : long_term_debt[filed]['fy'],
        'form' : long_term_debt[filed]['form'],
        'filed' : filed,
        'val' : long_term_debt[filed]['val'] / stockholders_equity[filed]['val'] if stockholders_equity[filed]['val'] != 0 else None
        }

def debt_to_assets(company_facts : CompanyFacts, filed : str, form : Form = Form._10Q, unit : str = 'USD') -> dict | None:
    long_term_debt = company_facts.get_fact(fact='LongTermDebt', form=form, unit=unit)
    assets = company_facts.get_fact(fact='Assets', form=form, unit=unit)

    if not long_term_debt or not assets or filed not in long_term_debt or filed not in assets:
        return None

    return {
        'fy' : long_term_debt[filed]['fy'],
        'form' : long_term_debt[filed]['form'],
        'filed' : filed,
        'val' : long_term_debt[filed]['val'] / assets[filed]['val'] if assets[filed]['val'] != 0 else None
        }

def market_cap(company_facts : CompanyFacts, filed : str, form : Form = Form._10Q, unit : str = 'USD') -> dict | None:
    common_stock_value = company_facts.get_fact(fact='CommonStockValue', form=form, unit=unit)
    common_stock_shares_outstanding = company_facts.get_fact(fact='EntityCommonStockSharesOutstanding', form=form, unit='shares')

    if not common_stock_value or not common_stock_shares_outstanding or filed not in common_stock_value or filed not in common_stock_shares_outstanding:
        return None

    return {
        'fy' : common_stock_value[filed]['fy'],
        'form' : common_stock_value[filed]['form'],
        'filed' : filed,
        'val' : common_stock_value[filed]['val'] * common_stock_shares_outstanding[filed]['val']
    }

def expenses(company_facts : CompanyFacts, filed : str, form : Form = Form._10Q, unit : str = 'USD') -> dict | None:
    operating_expenses = company_facts.get_fact(fact='OperatingExpenses', form=form, unit=unit)
    interest_expenses = company_facts.get_fact(fact='InterestExpense', form=form, unit=unit)
    sgna_expenses = company_facts.get_fact(fact='SellingGeneralAndAdministrativeExpense', form=form, unit=unit)
    income_taxes = company_facts.get_fact(fact='IncomeTaxesPaidNet', form=form, unit=unit)
    depreciation = company_facts.get_fact(fact='Depreciation', form=form, unit=unit)

    if not operating_expenses or not interest_expenses or not sgna_expenses or not income_taxes or not depreciation\
        or filed not in operating_expenses or filed not in interest_expenses or filed not in sgna_expenses\
        or filed not in income_taxes or filed not in depreciation:
        return None
    
    return {
        'fy' : operating_expenses[filed]['fy'],
        'form' : operating_expenses[filed]['form'],
        'filed' : filed,
        'val' : operating_expenses[filed]['val'] + interest_expenses[filed]['val'] + sgna_expenses[filed]['val'] + income_taxes[filed]['val'] + depreciation[filed]['val']
        }

def price_to_earnings_ratio(company_facts : CompanyFacts, filed : str, form : Form = Form._10Q, unit : str = 'USD') -> dict | None:
    _market_cap = market_cap(company_facts, filed, form, unit)
    net_income = company_facts.get_fact(fact='NetIncomeLoss', form=form, unit=unit)

    if not _market_cap or not net_income or filed not in net_income:
        return None
    
    return {
        'fy' : _market_cap['fy'],
        'form' : _market_cap['form'],
        'filed' : filed,
        'val' : _market_cap['val'] / net_income[filed]['val'] if net_income[filed]['val'] != 0 else None
        }

def price_to_sales_ratio(company_facts : CompanyFacts, filed : str, form : Form = Form._10Q, unit : str = 'USD') -> dict | None:
    _market_cap = market_cap(company_facts, filed, form, unit)
    _revenue = revenue(company_facts, filed, form, unit)

    if not _market_cap or not _revenue:
        return None
    
    return {
        'fy' : _market_cap['fy'],
        'form' : _market_cap['form'],
        'filed' : filed,
        'val' : _market_cap['val'] / _revenue['val'] if _revenue['val'] != 0 else None
        }

def price_to_cash_flow_ratio(company_facts : CompanyFacts, filed : str, form : Form = Form._10Q, unit : str = 'USD') -> dict | None:
    operating_cash_flow = company_facts.get_fact(fact='NetCashProvidedByUsedInOperatingActivities', form=form, unit=unit)

    _market_cap = market_cap(company_facts, filed, form, unit)

    if not operating_cash_flow or not _market_cap or filed not in operating_cash_flow:
        return None
    
    return {
        'fy' : operating_cash_flow[filed]['fy'],
        'form' : operating_cash_flow[filed]['form'],
        'filed' : filed,
        'val' : _market_cap['val'] / operating_cash_flow[filed]['val'] if operating_cash_flow[filed]['val'] != 0 else None
        }

def price_to_free_cash_flow_ratio(company_facts : CompanyFacts, filed : str, form : Form = Form._10Q, unit : str = 'USD') -> dict | None:
    _free_cash_flow = free_cash_flow(company_facts, filed, form, unit)

    _market_cap = market_cap(company_facts, filed, form, unit)

    if not _free_cash_flow or not _market_cap:
        return None
    
    return {
        'fy' : _free_cash_flow[filed]['fy'],
        'form' : _free_cash_flow[filed]['form'],
        'filed' : filed,
        'val' : _market_cap['val'] / _free_cash_flow['val'] if _free_cash_flow['val'] != 0 else None
        }

def price_to_book_ratio(company_facts : CompanyFacts, filed : str, form : Form = Form._10Q, unit : str = 'USD') -> dict | None:
    _market_cap = market_cap(company_facts, filed, form, unit)
    book_value = company_facts.get_fact(fact='StockholdersEquity', form=form, unit=unit)

    if not _market_cap or not book_value or filed not in book_value:
        return None
    
    return {
        'fy' : _market_cap['fy'],
        'form' : _market_cap['form'],
        'filed' : filed,
        'val' : _market_cap['val'] / book_value[filed]['val'] if book_value[filed]['val'] != 0 else None
        }

def enterprise_value(company_facts : CompanyFacts, filed : str, form : Form = Form._10Q, unit : str = 'USD') -> dict | None:
    _market_cap = market_cap(company_facts, filed, form, unit)
    outstanding_debt = company_facts.get_fact(fact='LongTermDebt', form=form, unit=unit)
    cash = company_facts.get_fact(fact='CashAndCashEquivalentsAtCarryingValue', form=form, unit=unit)

    if not _market_cap or not outstanding_debt or not cash or filed not in outstanding_debt or filed not in cash:
        return None
    
    return {
        'fy' : _market_cap['fy'],
        'form' : _market_cap['form'],
        'filed' : filed,
        'val' : _market_cap['val'] + outstanding_debt[filed]['val'] - cash[filed]['val']
        }

def sales_ratio_to_enterprise_value_to_sales(company_facts : CompanyFacts, filed : str, form : Form = Form._10Q, unit : str = 'USD') -> dict | None:
    _enterprise_value = enterprise_value(company_facts, filed, form, unit)
    _revenue = revenue(company_facts, filed, form, unit)

    if not _enterprise_value or not _revenue:
        return None
    
    return {
        'fy' : _enterprise_value['fy'],
        'form' : _enterprise_value['form'],
        'filed' : filed,
        'val' : _enterprise_value['val'] / _revenue['val'] if _revenue['val'] != 0 else None
        }

def revenue(company_facts : CompanyFacts, filed : str, form : Form = Form._10Q, unit : str = 'USD') -> dict | None:
    operating_income_loss = company_facts.get_fact(fact='OperatingIncomeLoss', form=form, unit=unit)
    operating_expenses = company_facts.get_fact(fact='OperatingExpenses', form=form, unit=unit)

    if not operating_income_loss or not operating_expenses or filed not in operating_expenses or filed not in operating_income_loss:
        return None
    
    return {
        'fy' : operating_expenses[filed]['fy'],
        'form' : operating_expenses[filed]['form'],
        'filed' : filed,
        'val' : operating_income_loss[filed]['val'] + operating_expenses[filed]['val']
    }

def ebit(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    operating_income_loss = company_facts.get_fact(fact='OperatingIncomeLoss', form=form, unit=unit)
    cogs = company_facts.get_fact(fact='CostOfGoodsAndServicesSold', form=form, unit=unit)

    if not operating_income_loss or not cogs or filed not in operating_income_loss or filed not in cogs:
        return None
    
    return {
        'fy' : operating_income_loss[filed]['fy'],
        'form' : operating_income_loss[filed]['form'],
        'filed' : filed,
        'val' : operating_income_loss[filed]['val'] - cogs[filed]['val']
    }

def ebitda(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    _ebit = ebit(company_facts, filed, form, unit)
    depreciation = company_facts.get_fact(fact='Depreciation', form=form, unit=unit)

    if not _ebit or not depreciation or filed not in depreciation:
        return None
    
    return {
        'fy' : _ebit['fy'],
        'form' : _ebit['form'],
        'filed' : filed,
        'val' : _ebit['val'] + depreciation[filed]['val']
    }

def enterprise_value_over_ebitda(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    _enterprise_value = enterprise_value(company_facts, filed, form, unit)
    _ebitda = ebitda(company_facts, filed, form, unit)

    if not _enterprise_value or not _ebitda:
        return None
    
    return {
        'fy' : _enterprise_value['fy'],
        'form' : _enterprise_value['form'],
        'filed' : filed,
        'val' : _enterprise_value['val'] / _ebitda['val'] if _ebitda['val'] != 0 else None
    }

def enterprise_value_to_operating_cash_flow(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    _enterprise_value = enterprise_value(company_facts, filed, form, unit)
    operating_cash_flow = company_facts.get_fact(fact='NetCashProvidedByUsedInOperatingActivities', form=form, unit=unit)

    if not _enterprise_value or not operating_cash_flow or filed not in operating_cash_flow:
        return None
    
    return {
        'fy' : _enterprise_value['fy'],
        'form' : _enterprise_value['form'],
        'filed' : filed,
        'val' : _enterprise_value['val'] / operating_cash_flow[filed]['val'] if operating_cash_flow[filed]['val'] != 0 else None
    }

def earnings_yield(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    _ebit = ebit(company_facts, filed, form, unit)
    _market_cap = market_cap(company_facts, filed, form, unit)

    if not _ebit or not _market_cap:
        return None
    
    return {
        'fy' : _ebit['fy'],
        'form' : _ebit['form'],
        'filed' : filed,
        'val' : _ebit['val'] / _market_cap['val'] if _market_cap['val'] != 0 else None
    }

def free_cash_flow(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    operating_cash_flow = company_facts.get_fact(fact='NetCashProvidedByUsedInOperatingActivities', form=form, unit=unit)
    capital_expenditures = company_facts.get_fact(fact='PaymentsToAcquirePropertyPlantAndEquipment', form=form, unit=unit)

    if not operating_cash_flow or not capital_expenditures or filed not in operating_cash_flow or filed not in capital_expenditures:
        return None
    
    return {
        'fy' : operating_cash_flow[filed]['fy'],
        'form' : operating_cash_flow[filed]['form'],
        'filed' : filed,
        'val' : operating_cash_flow[filed]['val'] - capital_expenditures[filed]['val']
    }

def free_cash_flow_yield(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    _free_cash_flow = free_cash_flow(company_facts, filed, form, unit)
    _market_cap = market_cap(company_facts, filed, form, unit)

    if not _free_cash_flow or not _market_cap:
        return None
    
    return {
        'fy' : _free_cash_flow['fy'],
        'form' : _free_cash_flow['form'],
        'filed' : filed,
        'val' : _free_cash_flow['val'] / _market_cap['val'] if _market_cap['val'] != 0 else None
    }

def net_debt_to_ebitda(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    total_debt = company_facts.get_fact(fact='Liabilities', form=form, unit=unit)
    cash = company_facts.get_fact(fact='CashAndCashEquivalentsAtCarryingValue', form=form, unit=unit)
    _ebitda = ebitda(company_facts, filed, form, unit)

    if not total_debt or not cash or not _ebitda or filed not in total_debt or filed not in cash:
        return None
    
    return {
        'fy' : total_debt[filed]['fy'],
        'form' : total_debt[filed]['form'],
        'filed' : filed,
        'val' : (total_debt[filed]['val'] - cash[filed]['val']) / _ebitda['val'] if _ebitda['val'] != 0 else None
    }

def interest_coverage_ratio(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    _ebit = ebit(company_facts, filed, form, unit)
    interest_expense = company_facts.get_fact(fact='InterestExpense', form=form, unit=unit)

    if not _ebit or not interest_expense or filed not in interest_expense:
        return None
    
    return {
        'fy' : _ebit['fy'],
        'form' : _ebit['form'],
        'filed' : filed,
        'val' : _ebit['val'] / interest_expense[filed]['val'] if interest_expense[filed]['val'] != 0 else None
    }

def income_quality(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    cash_flow_from_operations = company_facts.get_fact(fact='NetCashProvidedByUsedInOperatingActivities', form=form, unit=unit)
    net_income = company_facts.get_fact(fact='NetIncomeLoss', form=form, unit=unit)

    if not cash_flow_from_operations or not net_income or filed not in cash_flow_from_operations or filed not in net_income:
        return None
    
    return {
        'fy' : cash_flow_from_operations[filed]['fy'],
        'form' : cash_flow_from_operations[filed]['form'],
        'filed' : filed,
        'val' : cash_flow_from_operations[filed]['val'] / net_income[filed]['val']
    }

def dividend_yield(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    dividends = company_facts.get_fact(fact='Dividends', form=form, unit=unit)
    _market_cap = market_cap(company_facts, filed, form, unit)

    if not dividends or not _market_cap or filed not in dividends:
        return None
    
    return {
        'fy' : dividends[filed]['fy'],
        'form' : dividends[filed]['form'],
        'filed' : filed,
        'val' : dividends[filed]['val'] / _market_cap['val']
    }

def payout_ratio(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    dividends = company_facts.get_fact(fact='Dividends', form=form, unit=unit)
    net_income = company_facts.get_fact(fact='NetIncomeLoss', form=form, unit=unit)

    if not dividends or not net_income or filed not in dividends or filed not in net_income:
        return None
    
    return {
        'fy' : dividends[filed]['fy'],
        'form' : dividends[filed]['form'],
        'filed' : filed,
        'val' : dividends[filed]['val'] / net_income[filed]['val']
    }

def sales_general_and_administrative_to_revenue(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    sgna_expenses = company_facts.get_fact(fact='SellingGeneralAndAdministrativeExpense', form=form, unit=unit)
    _revenue = revenue(company_facts, filed, form, unit)

    if not sgna_expenses or not _revenue or filed not in sgna_expenses:
        return None
    
    return {
        'fy' : sgna_expenses[filed]['fy'],
        'form' : sgna_expenses[filed]['form'],
        'filed' : filed,
        'val' : sgna_expenses[filed]['val'] / _revenue['val'] if _revenue['val'] != 0 else None
    }

def return_on_tangible_assets(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    _ebit = ebit(company_facts, filed, form, unit)
    tangible_assets = company_facts.get_fact(fact='Assets', form=form, unit=unit)
    goodwill = company_facts.get_fact(fact='Goodwill', form=form, unit=unit)

    if not _ebit or not tangible_assets or not goodwill or filed not in tangible_assets or filed not in goodwill:
        return None
    
    return {
        'fy' : _ebit['fy'],
        'form' : _ebit['form'],
        'filed' : filed,
        'val' : _ebit['val'] / (tangible_assets[filed]['val'] - goodwill[filed]['val']) if tangible_assets[filed]['val'] - goodwill[filed]['val'] != 0 else None
    }

def tangible_asset_value(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    tangible_assets = company_facts.get_fact(fact='Assets', form=form, unit=unit)
    goodwill = company_facts.get_fact(fact='Goodwill', form=form, unit=unit)
    liabilities = company_facts.get_fact(fact='Liabilities', form=form, unit=unit)

    if not tangible_assets or not goodwill or not liabilities or filed not in tangible_assets or filed not in goodwill or filed not in liabilities:
        return None
    
    return {
        'fy' : tangible_assets[filed]['fy'],
        'form' : tangible_assets[filed]['form'],
        'filed' : filed,
        'val' : tangible_assets[filed]['val'] - goodwill[filed]['val'] - liabilities[filed]['val']
    }

def working_capital(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    current_assets = company_facts.get_fact(fact='AssetsCurrent', form=form, unit=unit)
    current_liabilities = company_facts.get_fact(fact='LiabilitiesCurrent', form=form, unit=unit)

    if not current_assets or not current_liabilities or filed not in current_assets or filed not in current_liabilities:
        return None
    
    return {
        'fy' : current_assets[filed]['fy'],
        'form' : current_assets[filed]['form'],
        'filed' : filed,
        'val' : current_assets[filed]['val'] - current_liabilities[filed]['val']
    }

def net_current_asset_value(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    current_assets = company_facts.get_fact(fact='AssetsCurrent', form=form, unit=unit)
    current_liabilities = company_facts.get_fact(fact='LiabilitiesCurrent', form=form, unit=unit)

    if not current_assets or not current_liabilities or filed not in current_assets or filed not in current_liabilities:
        return None
    
    return {
        'fy' : current_assets[filed]['fy'],
        'form' : current_assets[filed]['form'],
        'filed' : filed,
        'val' : current_assets[filed]['val'] - current_liabilities[filed]['val']
    }

def revenue_per_share(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    _revenue = revenue(company_facts, filed, form, unit)
    outstanding_shares = company_facts.get_fact(fact='EntityCommonStockSharesOutstanding', form=form, unit='shares')

    if not _revenue or not outstanding_shares or filed not in outstanding_shares:
        return None
    
    return {
        'fy' : _revenue['fy'],
        'form' : _revenue['form'],
        'filed' : filed,
        'val' : _revenue['val'] / outstanding_shares[filed]['val'] if outstanding_shares[filed]['val'] != 0 else None
    }

def interest_debt_per_share(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    interest_expense = company_facts.get_fact(fact='InterestExpense', form=form, unit=unit)
    outstanding_debt = company_facts.get_fact(fact='LongTermDebt', form=form, unit=unit)
    outstanding_shares = company_facts.get_fact(fact='EntityCommonStockSharesOutstanding', form=form, unit='shares')

    if not interest_expense or not outstanding_debt or not outstanding_shares or filed not in interest_expense or filed not in outstanding_debt or filed not in outstanding_shares:
        return None
    
    return {
        'fy' : interest_expense[filed]['fy'],
        'form' : interest_expense[filed]['form'],
        'filed' : filed,
        'val' : (interest_expense[filed]['val'] + outstanding_debt[filed]['val']) / outstanding_shares[filed]['val'] if outstanding_shares[filed]['val'] != 0 else None
    }

def return_on_equity(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    net_income = company_facts.get_fact(fact='NetIncomeLoss', form=form, unit=unit)
    stockholders_equity = company_facts.get_fact(fact='StockholdersEquity', form=form, unit=unit)

    if not net_income or not stockholders_equity or filed not in net_income or filed not in stockholders_equity:
        return None
    
    return {
        'fy' : net_income[filed]['fy'],
        'form' : net_income[filed]['form'],
        'filed' : filed,
        'val' : net_income[filed]['val'] / stockholders_equity[filed]['val'] if stockholders_equity[filed]['val'] != 0 else None
    }

def capex_per_share(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    capex = company_facts.get_fact(fact='PaymentsToAcquirePropertyPlantAndEquipment', form=form, unit=unit)
    outstanding_shares = company_facts.get_fact(fact='EntityCommonStockSharesOutstanding', form=form, unit='shares')

    if not capex or not outstanding_shares or filed not in capex or filed not in outstanding_shares:
        return None
    
    return {
        'fy' : capex[filed]['fy'],
        'form' : capex[filed]['form'],
        'filed' : filed,
        'val' : capex[filed]['val'] / outstanding_shares[filed]['val'] if outstanding_shares[filed]['val'] != 0 else None
    }

def quick_ratio(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    current_assets = company_facts.get_fact(fact='AssetsCurrent', form=form, unit=unit)
    current_liabilities = company_facts.get_fact(fact='LiabilitiesCurrent', form=form, unit=unit)
    inventory = company_facts.get_fact(fact='InventoryNet', form=form, unit=unit)

    if not current_assets or not current_liabilities or not inventory or filed not in current_assets or filed not in current_liabilities or filed not in inventory:
        return None
    
    return {
        'fy' : current_assets[filed]['fy'],
        'form' : current_assets[filed]['form'],
        'filed' : filed,
        'val' : (current_assets[filed]['val'] - inventory[filed]['val']) / current_liabilities[filed]['val'] if current_liabilities[filed]['val'] != 0 else None
    }

def cash_ratio(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    cash = company_facts.get_fact(fact='CashAndCashEquivalentsAtCarryingValue', form=form, unit=unit)
    current_liabilities = company_facts.get_fact(fact='LiabilitiesCurrent', form=form, unit=unit)

    if not cash or not current_liabilities or filed not in cash or filed not in current_liabilities:
        return None
    
    return {
        'fy' : cash[filed]['fy'],
        'form' : cash[filed]['form'],
        'filed' : filed,
        'val' : cash[filed]['val'] / current_liabilities[filed]['val'] if current_liabilities[filed]['val'] != 0 else None
    }

def gross_profit_margin(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    gross_profit = company_facts.get_fact(fact='GrossProfit', form=form, unit=unit)
    _revenue = revenue(company_facts, filed, form, unit)

    if not gross_profit or not _revenue or filed not in gross_profit:
        return None
    
    return {
        'fy' : gross_profit[filed]['fy'],
        'form' : gross_profit[filed]['form'],
        'filed' : filed,
        'val' : gross_profit[filed]['val'] / _revenue['val'] if _revenue['val'] != 0 else None
    }

def return_on_assets(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    net_income = company_facts.get_fact(fact='NetIncomeLoss', form=form, unit=unit)
    assets = company_facts.get_fact(fact='Assets', form=form, unit=unit)

    if not net_income or not assets or filed not in net_income or filed not in assets:
        return None
    
    return {
        'fy' : net_income[filed]['fy'],
        'form' : net_income[filed]['form'],
        'filed' : filed,
        'val' : net_income[filed]['val'] / assets[filed]['val'] if assets[filed]['val'] != 0 else None
    }

def return_on_equity(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    net_income = company_facts.get_fact(fact='NetIncomeLoss', form=form, unit=unit)
    stockholders_equity = company_facts.get_fact(fact='StockholdersEquity', form=form, unit=unit)

    if not net_income or not stockholders_equity or filed not in net_income or filed not in stockholders_equity:
        return None
    
    return {
        'fy' : net_income[filed]['fy'],
        'form' : net_income[filed]['form'],
        'filed' : filed,
        'val' : net_income[filed]['val'] / stockholders_equity[filed]['val'] if stockholders_equity[filed]['val'] != 0 else None
    }

def return_on_capital_employed(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    _ebit = ebit(company_facts, filed, form, unit)
    total_assets = company_facts.get_fact(fact='Assets', form=form, unit=unit)
    current_liabilities = company_facts.get_fact(fact='LiabilitiesCurrent', form=form, unit=unit)

    if not _ebit or not total_assets or not current_liabilities or filed not in total_assets or filed not in current_liabilities:
        return None
    
    return {
        'fy' : _ebit['fy'],
        'form' : _ebit['form'],
        'filed' : filed,
        'val' : _ebit['val'] / (total_assets[filed]['val'] - current_liabilities[filed]['val']) if (total_assets[filed]['val'] - current_liabilities[filed]['val']) != 0 else None
    }

def company_equity_multiplier(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    total_assets = company_facts.get_fact(fact='Assets', form=form, unit=unit)
    stockholders_equity = company_facts.get_fact(fact='StockholdersEquity', form=form, unit=unit)

    if not total_assets or not stockholders_equity or filed not in total_assets or filed not in stockholders_equity:
        return None
    
    return {
        'fy' : total_assets[filed]['fy'],
        'form' : total_assets[filed]['form'],
        'filed' : filed,
        'val' : total_assets[filed]['val'] / stockholders_equity[filed]['val'] if stockholders_equity[filed]['val'] != 0 else None
    }

def net_income_per_ebt(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    net_income = company_facts.get_fact(fact='NetIncomeLoss', form=form, unit=unit)
    ebt = company_facts.get_fact(fact='IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments', form=form, unit=unit)

    if not net_income or not ebt or filed not in net_income or filed not in ebt:
        return None
    
    return {
        'fy' : net_income[filed]['fy'],
        'form' : net_income[filed]['form'],
        'filed' : filed,
        'val' : net_income[filed]['val'] / ebt[filed]['val'] if ebt[filed]['val'] != 0 else None
    }

def long_term_debt_to_capitalization(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    long_term_debt = company_facts.get_fact(fact='LongTermDebt', form=form, unit=unit)
    total_stockholders_equity = company_facts.get_fact(fact='StockholdersEquity', form=form, unit=unit)

    if not long_term_debt or not total_stockholders_equity or filed not in long_term_debt or filed not in total_stockholders_equity:
        return None
    
    return {
        'fy' : long_term_debt[filed]['fy'],
        'form' : long_term_debt[filed]['form'],
        'filed' : filed,
        'val' : long_term_debt[filed]['val'] / total_stockholders_equity[filed]['val'] if total_stockholders_equity[filed]['val'] != 0 else None
    }

def total_debt_to_capitalization(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    total_debt = company_facts.get_fact(fact='Liabilities', form=form, unit=unit)
    total_stockholders_equity = company_facts.get_fact(fact='StockholdersEquity', form=form, unit=unit)

    if not total_debt or not total_stockholders_equity or filed not in total_debt or filed not in total_stockholders_equity:
        return None
    
    return {
        'fy' : total_debt[filed]['fy'],
        'form' : total_debt[filed]['form'],
        'filed' : filed,
        'val' : total_debt[filed]['val'] / total_stockholders_equity[filed]['val'] if total_stockholders_equity[filed]['val'] != 0 else None
    }

def fixed_asset_turnover(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    _revenue = revenue(company_facts, filed, form, unit)
    net_ppe = company_facts.get_fact(fact='PropertyPlantAndEquipmentNet', form=form, unit=unit)

    if not _revenue or not net_ppe or filed not in net_ppe:
        return None
    
    return {
        'fy' : _revenue['fy'],
        'form' : _revenue['form'],
        'filed' : filed,
        'val' : _revenue['val'] / net_ppe[filed]['val'] if net_ppe[filed]['val'] != 0 else None
    }

def operating_cash_flow_sales_ratio(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    operating_cash_flow = company_facts.get_fact(fact='NetCashProvidedByUsedInOperatingActivities', form=form, unit=unit)
    _revenue = revenue(company_facts, filed, form, unit)

    if not operating_cash_flow or not _revenue or filed not in operating_cash_flow:
        return None
    
    return {
        'fy' : operating_cash_flow[filed]['fy'],
        'form' : operating_cash_flow[filed]['form'],
        'filed' : filed,
        'val' : operating_cash_flow[filed]['val'] / _revenue['val'] if _revenue['val'] != 0 else None
    }

def free_cash_flow_sales_ratio(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    _free_cash_flow = free_cash_flow(company_facts, filed, form, unit)
    _revenue = revenue(company_facts, filed, form, unit)

    if not _free_cash_flow or not _revenue:
        return None
    
    return {
        'fy' : _free_cash_flow['fy'],
        'form' : _free_cash_flow['form'],
        'filed' : filed,
        'val' : _free_cash_flow['val'] / _revenue['val'] if _revenue['val'] != 0 else None
    }

def cash_flow_coverage_ratio(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    operating_cash_flow = company_facts.get_fact(fact='NetCashProvidedByUsedInOperatingActivities', form=form, unit=unit)
    outstanding_debt = company_facts.get_fact(fact='LongTermDebt', form=form, unit=unit)

    if not operating_cash_flow or not outstanding_debt or filed not in operating_cash_flow or filed not in outstanding_debt:
        return None
    
    return {
        'fy' : operating_cash_flow[filed]['fy'],
        'form' : operating_cash_flow[filed]['form'],
        'filed' : filed,
        'val' : operating_cash_flow[filed]['val'] / outstanding_debt[filed]['val'] if outstanding_debt[filed]['val'] != 0 else None
    }

def short_term_coverage_ratio(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    cash = company_facts.get_fact(fact='CashAndCashEquivalentsAtCarryingValue', form=form, unit=unit)
    short_term_investments = company_facts.get_fact(fact='AvailableForSaleSecuritiesCurrent', form=form, unit=unit)
    receivables = company_facts.get_fact(fact='AccountsReceivableNetCurrent', form=form, unit=unit)
    current_liabilities = company_facts.get_fact(fact='LiabilitiesCurrent', form=form, unit=unit)

    if not cash or not short_term_investments or not receivables or not current_liabilities or filed not in cash or filed not in short_term_investments or filed not in receivables or filed not in current_liabilities:
        return None
    
    return {
        'fy' : cash[filed]['fy'],
        'form' : cash[filed]['form'],
        'filed' : filed,
        'val' : (cash[filed]['val'] + short_term_investments[filed]['val'] + receivables[filed]['val']) / current_liabilities[filed]['val'] if current_liabilities[filed]['val'] != 0 else None
    }

def capital_expenditure_coverage_ratio(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    operating_cash_flow = company_facts.get_fact(fact='NetCashProvidedByUsedInOperatingActivities', form=form, unit=unit)
    capital_expenditures = company_facts.get_fact(fact='PaymentsToAcquirePropertyPlantAndEquipment', form=form, unit=unit)

    if not operating_cash_flow or not capital_expenditures or filed not in operating_cash_flow or filed not in capital_expenditures:
        return None
    
    return {
        'fy' : operating_cash_flow[filed]['fy'],
        'form' : operating_cash_flow[filed]['form'],
        'filed' : filed,
        'val' : operating_cash_flow[filed]['val'] / capital_expenditures[filed]['val'] if capital_expenditures[filed]['val'] != 0 else None
    }

def dividend_paid_and_capex_coverage_ratio(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    operating_cash_flow = company_facts.get_fact(fact='NetCashProvidedByUsedInOperatingActivities', form=form, unit=unit)
    dividends = company_facts.get_fact(fact='Dividends', form=form, unit=unit)
    capital_expenditures = company_facts.get_fact(fact='PaymentsToAcquirePropertyPlantAndEquipment', form=form, unit=unit)

    if not operating_cash_flow or not dividends or not capital_expenditures or filed not in operating_cash_flow or filed not in dividends or filed not in capital_expenditures:
        return None
    
    return {
        'fy' : operating_cash_flow[filed]['fy'],
        'form' : operating_cash_flow[filed]['form'],
        'filed' : filed,
        'val' : operating_cash_flow[filed]['val'] / (dividends[filed]['val'] + capital_expenditures[filed]['val']) if (dividends[filed]['val'] + capital_expenditures[filed]['val']) != 0 else None
    }

def operating_profit_margin(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    operating_income_loss = company_facts.get_fact(fact='OperatingIncomeLoss', form=form, unit=unit)
    _revenue = revenue(company_facts, filed, form, unit)

    if not operating_income_loss or not _revenue or filed not in operating_income_loss:
        return None
    
    return {
        'fy' : operating_income_loss[filed]['fy'],
        'form' : operating_income_loss[filed]['form'],
        'filed' : filed,
        'val' : operating_income_loss[filed]['val'] / _revenue['val'] if _revenue['val'] != 0 else None
    }

def pretax_profit_margin(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:  
    ebt = company_facts.get_fact(fact='IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments', form=form, unit=unit)
    _revenue = revenue(company_facts, filed, form, unit)

    if not ebt or not _revenue or filed not in ebt:
        return None
    
    return {
        'fy' : ebt[filed]['fy'],
        'form' : ebt[filed]['form'],
        'filed' : filed,
        'val' : ebt[filed]['val'] / _revenue['val'] if _revenue['val'] != 0 else None
    }

def net_profit_margin(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    net_income = company_facts.get_fact(fact='NetIncomeLoss', form=form, unit=unit)
    _revenue = revenue(company_facts, filed, form, unit)

    if not net_income or not _revenue or filed not in net_income:
        return None
    
    return {
        'fy' : net_income[filed]['fy'],
        'form' : net_income[filed]['form'],
        'filed' : filed,
        'val' : net_income[filed]['val'] / _revenue['val'] if _revenue['val'] != 0 else None
    }

def ni_per_ebt(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    net_income = company_facts.get_fact(fact='NetIncomeLoss', form=form, unit=unit)
    ebt = company_facts.get_fact(fact='IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments', form=form, unit=unit)

    if not net_income or not ebt or filed not in net_income or filed not in ebt:
        return None
    
    return {
        'fy' : net_income[filed]['fy'],
        'form' : net_income[filed]['form'],
        'filed' : filed,
        'val' : net_income[filed]['val'] / ebt[filed]['val'] if ebt[filed]['val'] != 0 else None
    }

def ebt_per_ebit(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    ebt = company_facts.get_fact(fact='IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments', form=form, unit=unit)
    _ebit = ebit(company_facts, filed, form, unit)

    if not ebt or not _ebit or filed not in ebt:
        return None
    
    return {
        'fy' : ebt[filed]['fy'],
        'form' : ebt[filed]['form'],
        'filed' : filed,
        'val' : ebt[filed]['val'] / _ebit['val'] if _ebit['val'] != 0 else None
    }

def debt_ratio(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    total_liabilities = company_facts.get_fact(fact='Liabilities', form=form, unit=unit)
    total_assets = company_facts.get_fact(fact='Assets', form=form, unit=unit)

    if not total_liabilities or not total_assets or filed not in total_liabilities or filed not in total_assets:
        return None
    
    return {
        'fy' : total_liabilities[filed]['fy'],
        'form' : total_liabilities[filed]['form'],
        'filed' : filed,
        'val' : total_liabilities[filed]['val'] / total_assets[filed]['val'] if total_assets[filed]['val'] != 0 else None
    }

def debt_equity_ratio(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    total_liabilities = company_facts.get_fact(fact='Liabilities', form=form, unit=unit)
    stockholders_equity = company_facts.get_fact(fact='StockholdersEquity', form=form, unit=unit)

    if not total_liabilities or not stockholders_equity or filed not in total_liabilities or filed not in stockholders_equity:
        return None
    
    return {
        'fy' : total_liabilities[filed]['fy'],
        'form' : total_liabilities[filed]['form'],
        'filed' : filed,
        'val' : total_liabilities[filed]['val'] / stockholders_equity[filed]['val'] if stockholders_equity[filed]['val'] != 0 else None
    }

def cash_flow_to_debt_ratio(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    operating_cash_flow = company_facts.get_fact(fact='NetCashProvidedByUsedInOperatingActivities', form=form, unit=unit)
    total_debt = company_facts.get_fact(fact='Liabilities', form=form, unit=unit)

    if not operating_cash_flow or not total_debt or filed not in operating_cash_flow or filed not in total_debt:
        return None
    
    return {
        'fy' : operating_cash_flow[filed]['fy'],
        'form' : operating_cash_flow[filed]['form'],
        'filed' : filed,
        'val' : operating_cash_flow[filed]['val'] / total_debt[filed]['val'] if total_debt[filed]['val'] != 0 else None
    }

def asset_turnover(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    _revenue = revenue(company_facts, filed, form, unit)
    total_assets = company_facts.get_fact(fact='Assets', form=form, unit=unit)

    if not _revenue or not total_assets or filed not in total_assets:
        return None
    
    return {
        'fy' : _revenue['fy'],
        'form' : _revenue['form'],
        'filed' : filed,
        'val' : _revenue['val'] / total_assets[filed]['val'] if total_assets[filed]['val'] != 0 else None
    }

def enterprise_value_multiplier(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> float | None:
    _enterprise_value = enterprise_value(company_facts, filed, form, unit)
    _ebitda = ebitda(company_facts, filed, form, unit)

    if not _enterprise_value or not _ebitda:
        return None
    
    return {
        'fy' : _enterprise_value['fy'],
        'form' : _enterprise_value['form'],
        'filed' : filed,
        'val' : _enterprise_value['val'] / _ebitda['val'] if _ebitda['val'] != 0 else None
    }

def return_on_invested_capital(company_facts: CompanyFacts, filed: str, form: Form = Form._10Q, unit : str = 'USD') -> dict | None:
    assets = company_facts.get_fact(fact='Assets', form=form, unit=unit)
    current_liabilities = company_facts.get_fact(fact='LiabilitiesCurrent', form=form, unit=unit)
    _ebit = ebit(company_facts, filed, form, unit)
    
    if not assets or not current_liabilities or not _ebit or filed not in assets or filed not in current_liabilities:
        return None
    
    ROI = _ebit['val'] / (assets[filed]['val'] - current_liabilities[filed]['val']) if (assets[filed]['val'] - current_liabilities[filed]['val']) != 0 else None
    
    return {
        'fy' : assets[filed]['fy'],
        'form' : assets[filed]['form'],
        'filed' : filed,
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
    'WorkingCapital' : working_capital,
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