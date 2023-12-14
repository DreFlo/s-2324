query_template = """
Generate text based on the data below. It has to follow the template roughly. Be creative in relation to the phrasing. The values in the data have to be there exactly.

data: %s

text base: %s
"""

data = {
    'recommendation': True, 
    'probability': 0.52070606, 
    'shap': {
        'NetDebtToEBITDA_sec_last': 0.09124822, 
        'FixedAssetTurnover_sec_last': -0.086266354, 
        'CapitalExpenditureCoverageRatio_last': -0.070350364, 
        'FreeCashFlow_sec_last': 0.070063144, 
        'CurrentRatio_third_last': 0.063605174
    }
}


text_base = """
We think <name> (<symbol>) is a <good if recomendation == True :  : bad> investment. We are exactly <probability> sure about this.

This recomendation is primarily based on the following metrics: <shap.keys.join(', ')>.
"""