from model.company_facts import CompanyFacts
from external_apis.financial_apis_wrapper import FinancialAPIsWrapper
import json
from model_prep import load_to_dataframe
import pandas as pd
from datetime import datetime
import statistics
import numpy as np
import joblib

from datetime import datetime
from sklearn.preprocessing import LabelEncoder

def create_df_row():
    data = json.load(open("resources/test_data_subset_1.json", 'r'))

    symbols = list(data.keys())
        
    metrics = list(data[symbols[0]]['key_metrics_by_form']['10-Q'].keys())
    
    df = pd.DataFrame(columns=['symbol'])
    
    df['stock_change_before'] = None
    
    for metric in metrics:
        metric_df = pd.DataFrame(columns=[metric + '_last', metric + '_sec_last', metric + '_third_last'])
        df = pd.concat([df, metric_df], axis=1)
    
    for symbol in symbols:
        
        encoded_symbol = LabelEncoder().fit_transform([symbol])[0]
        
        date_dt = datetime.now()
        row_values = [encoded_symbol]
        
        stock_dates = list(data[symbol]['stock_price_history'].keys())
        stock_change_before = []
        for i, stock_date in enumerate(stock_dates):
            stock_date_dt = datetime.strptime(stock_date, '%Y-%m-%d')

            if (stock_date_dt - date_dt).days > -30 and (stock_date_dt - date_dt).days < 0:
                stock_change_before.append(data[symbol]['stock_price_history'][stock_date]['close'] - data[symbol]['stock_price_history'][stock_dates[i-1]]['close'])
        
        if len(stock_change_before) == 0:
            row_values.append(np.nan)
        else:
            row_values.append(statistics.median(stock_change_before))
        
        dates_before = list(data[symbol]['facts_by_form']['10-Q']['fileds']) + list(data[symbol]['facts_by_form']['10-K']['fileds'])
        
        for metric in metrics: 
            found_no = 0

            for _date in dates_before[::-1]:
                if found_no == 3:
                    break
                
                if _date in data[symbol]['key_metrics_by_form']['10-Q'][metric]:
                    if type(data[symbol]['key_metrics_by_form']['10-Q'][metric][_date]) == dict:
                        row_values.append(data[symbol]['key_metrics_by_form']['10-Q'][metric][_date]['val'])
                        found_no += 1
                        continue
                
                if _date in data[symbol]['key_metrics_by_form']['10-K'][metric]:
                    if type(data[symbol]['key_metrics_by_form']['10-K'][metric][_date]) == dict:
                        row_values.append(data[symbol]['key_metrics_by_form']['10-K'][metric][_date]['val'])
                        found_no += 1
                        continue
            
            while found_no < 3:
                row_values.append(np.nan)
                found_no += 1

        df.loc[len(df)] = row_values
        
    return df

def get_company_pred(company_name):
    
    #Get company info
    """ symbol = company_name
    company_info = CompanyFacts.from_symbol(symbol=symbol, financial_api_wrapper=FinancialAPIsWrapper).to_dict()
    
    print(company_info) """
    
    #Create dataframe from info
    df = create_df_row()
    
    #Load model and select features
    model = joblib.load('model.pkl') 
    
    # selected_features = model.selected_features
    selected_features = ['stock_change_before', 'total_revenue_last']
    
    #Select features from dataframe
    df = df[selected_features]
    
    #Get prediction probability [[0.1, 0.9]]
    pred_proba = model.predict_proba(df)
    
    recommendation = pred_proba[0][1] > 0.5
    probability = pred_proba[0][1]
    
    return {'recommendation': recommendation, 'probability': probability}


if __name__ == '__main__':
    get_company_pred('AAPL')