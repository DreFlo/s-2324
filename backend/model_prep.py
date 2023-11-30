import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import statistics
import random
import seaborn as sb

from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split, GridSearchCV, RepeatedStratifiedKFold
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score, f1_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from imblearn.pipeline import Pipeline
from sklearn.feature_selection import SelectFromModel

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier
from skopt import BayesSearchCV

from imblearn.over_sampling import SMOTE


def load_to_dataframe(data_file_path : str, sample_size : int | None = None):
    data = json.load(open(data_file_path, 'r'))

    if sample_size is not None:
        data = {symbol: data[symbol] for symbol in list(data.keys())[:sample_size]}

    symbols = list(data.keys())
        
    metrics = list(data[symbols[0]]['key_metrics_by_form']['10-Q'].keys())
    
    df = pd.DataFrame(columns=['symbol'])
    
    df['stock_change_before'] = None
    df['buy'] = None
    
    for metric in metrics:
        metric_df = pd.DataFrame(columns=[metric + '_last', metric + '_sec_last', metric + '_third_last'])
        df = pd.concat([df, metric_df], axis=1)
    
    for symbol in symbols:
        dates = list(data[symbol]['facts_by_form']['10-Q']['fileds']) + list(data[symbol]['facts_by_form']['10-K']['fileds'])
        dates = list(set(dates))
        dates.sort()
        
        if len(dates) < 6:
            continue
        
        encoded_symbol = LabelEncoder().fit_transform([symbol])[0]
        
        start_date = datetime.strptime(dates[3], '%Y-%m-%d')
        end_date = datetime.strptime(dates[-2], '%Y-%m-%d')
        random_dates = []

        for _ in range(len(dates) // 2):
            random_date = start_date + (end_date - start_date) * random.random()
            random_dates.append(random_date.strftime('%Y-%m-%d'))
        
        for date in random_dates:
            date_dt = datetime.strptime(date, '%Y-%m-%d')
            row_values = [encoded_symbol]
            
            stock_dates = list(data[symbol]['stock_price_history'].keys())
            stock_change_over = []
            stock_change_before = []
            for i, stock_date in enumerate(stock_dates):
                stock_date_dt = datetime.strptime(stock_date, '%Y-%m-%d')
                
                if (stock_date_dt - date_dt).days < 30 and (stock_date_dt - date_dt).days > 0:
                    stock_change_over.append(data[symbol]['stock_price_history'][stock_date]['close'] - data[symbol]['stock_price_history'][stock_dates[i-1]]['close'])
                elif (stock_date_dt - date_dt).days > -30 and (stock_date_dt - date_dt).days < 0:
                    stock_change_before.append(data[symbol]['stock_price_history'][stock_date]['close'] - data[symbol]['stock_price_history'][stock_dates[i-1]]['close'])
            
            if len(stock_change_over) == 0 or len(stock_change_before) == 0:
                continue
            else:
                row_values.append(statistics.median(stock_change_before))
                
                median_over = statistics.median(stock_change_over)
                if median_over > 0:
                    row_values.append(1)
                else:
                    row_values.append(0)
            
            dates_before = [_date for _date in dates if _date <= date]
            
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
                
    df.dropna(how='all', inplace=True)
    
    return df

def test_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    print('Confusion Matrix:')
    print(confusion_matrix(y_test, y_pred))
    print()
    
    print('Classification Report:')
    print(classification_report(y_test, y_pred))
    print()
    
    print('ROC AUC Score:')
    print(roc_auc_score(y_test, y_pred_proba))
    print()
    
    print('F1 Score:')
    print(f1_score(y_test, y_pred))
    print()

def scale_data(X_train, X_test, scaler=StandardScaler()):
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    return X_train, X_test

def select_features(model, X_train, y_train, X_test, _y_test, threshold='median'):
    select = SelectFromModel(model, threshold=threshold)
    select.fit(X_train, y_train)
    
    # array with columns that were selected
    selected_features = select.get_support()

    return X_train[:, selected_features], X_test[:, selected_features]

def get_best_feature_importance_threshold(model, X_train, y_train, X_test, y_test):
    thresholds = np.sort(model.feature_importances_)
    thresholds = thresholds[thresholds > 0]
    
    best_threshold = None
    best_score = 0
    
    for threshold in thresholds:
        X_train_selected, X_test_selected = select_features(model, X_train, y_train, X_test, y_test, threshold=threshold)
        model.fit(X_train_selected, y_train)
        
        y_pred_proba = model.predict_proba(X_test_selected)[:, 1]
        score = roc_auc_score(y_test, y_pred_proba)
        
        if score > best_score:
            best_score = score
            best_threshold = threshold
    
    return best_threshold

def bayesian_search(model, X_train, y_train, X_test, y_test, params, cv=5, n_iter=100):
    search = BayesSearchCV(model, params, n_iter=n_iter, cv=cv, scoring='roc_auc', random_state=42)
    search.fit(X_train, y_train)
    
    print('Best Score:')
    print(search.best_score_)
    print()
    
    print('Best Params:')
    print(search.best_params_)
    print()
    
    test_model(search.best_estimator_, X_test, y_test)
    
    return search.best_estimator_

def log_function(func, *args, **kwargs):
    print('Running function: ' + func.__name__)
    print()
    
    start = datetime.now()

    result = func(*args, **kwargs)

    end = datetime.now()

    print('Function ' + func.__name__ + ' finished in ' + str(end - start))

    return result

def make_model(model_name, params) -> XGBClassifier:
    df = log_function(load_to_dataframe, 'resources/test_data.json', sample_size=600)
    
    X = df.drop(['symbol', 'buy'], axis=1)
    y = df['buy']
    
    X_train, X_test, y_train, y_test = log_function(train_test_split, X, y, random_state=42)
    
    X_train, X_test = log_function(scale_data, X_train, X_test)

    oversample = SMOTE(random_state=1234)
    X_train, y_train = oversample.fit_resample(X_train, y_train)
    
    model = model_name(random_state=42)
    model.fit(X_train, y_train)

    log_function(test_model, model, X_test, y_test)

    best_threshold = log_function(get_best_feature_importance_threshold, model, X_train, y_train, X_test, y_test)

    X_train, X_test = log_function(select_features, model, X_train, y_train, X_test, y_test, threshold=best_threshold)

    model = model_name(random_state=42)
    model.fit(X_train, y_train)

    log_function(test_model, model, X_test, y_test)
    model = Pipeline([
        ('classifier', model_name(random_state=42))
    ])

    model = log_function(bayesian_search, model, X_train, y_train, X_test, y_test, params, cv=5, n_iter=100)

    log_function(test_model, model, X_test, y_test)

    return model

if __name__ == '__main__':
    model = make_model(XGBClassifier,
               {
                    'classifier__gamma': [0,0.1,0.2,0.4,0.8,1.6,3.2,6.4],
                    'classifier__learning_rate': [n for n in np.arange(0, 0.7, 0.1)],
                    'classifier__max_depth': [n for n in range(4, 10, 1)],
                    'classifier__n_estimators': [n for n in range(50, 350, 50)],
                    'classifier__reg_alpha': [0,0.1,0.2,0.4,0.8,1.6,3.2,6.4,12.8,25.6,51.2,102.4,200],
                    'classifier__reg_lambda': [0.6, 1.0, 1.6,3.2,6.4,12.8,25.6,51.2,102.4,200]
                }
    )

    model.save_model('xgb_model.json')

# if __name__ == '__main__':
#     make_model(LGBMClassifier,
#                {
#             'classifier__num_leaves': [n for n in np.arange(2, 10, 1)],
#             'classifier__max_depth': [n for n in np.arange(1, 6, 1)],
#             'classifier__n_estimators': [n for n in np.arange(50, 151, 25)]
#         })

# if __name__ == '__main__':
#     make_model(HistGradientBoostingClassifier,
#                {
#             'classifier__max_depth': [n for n in np.arange(1, 6, 1)],
#             'classifier__max_iter': [n for n in np.arange(50, 151, 25)]
#         }
#     )