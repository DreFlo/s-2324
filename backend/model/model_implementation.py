import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import statistics

from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split, GridSearchCV, RepeatedStratifiedKFold
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score
from sklearn.preprocessing import LabelEncoder
from imblearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from lightgbm import LGBMClassifier

# Temporarily using a subset of the data since it's much quicker to load
data_file_path = 'resources/test_data_subset_10.json'
dataframe_file_path = 'resources/data_subset_10.csv'

def create_subset(size):
    with open('resources/test_data.json', 'r') as file:
        data = json.load(file)
        
    subset_dictionary = {key: data[key] for key in list(data.keys())[:size]}
    
    with open('resources/test_data_subset_' + str(size) + '.json', 'w') as file:
        json.dump(subset_dictionary, file)
        
    return

def is_less_than_one_month_apart(date1, date2):
    if date2 > date1:
        difference = abs(date1 - date2)
        
        one_month = timedelta(days=30)
        
        return difference < one_month

def data_prep():
    with open(data_file_path, 'r') as file:
        data = json.load(file)

    symbols = list(data.keys())
    
    dates = list(data[symbols[0]]['facts_by_form']['10-Q']['fileds']) + list(data[symbols[0]]['facts_by_form']['10-K']['fileds'])
    dates.sort()
    
    metrics = list(data[symbols[0]]['key_metrics_by_form']['10-Q'].keys())
    
    df = pd.DataFrame(columns=['symbol'])
    
    for metric in metrics:
        df[metric + '_last'] = None
        df[metric + '_sec_last'] = None
        df[metric + '_third_last'] = None
    
    df['buy'] = None
    
    for symbol in symbols:
        for j, date in enumerate(dates):
            if(j > 3 and j < len(dates) - 1):
                date_dt = datetime.strptime(date, '%Y-%m-%d')
                encoded_symbol = LabelEncoder().fit_transform([symbol])[0]
                row_values = [encoded_symbol]
                
                for metric in metrics: 
                    for d in [date, dates[j-1], dates[j-2]]:
                        if d in data[symbol]['key_metrics_by_form']['10-Q'][metric]:
                            if type(data[symbol]['key_metrics_by_form']['10-Q'][metric][d]) == dict:
                                row_values.append(data[symbol]['key_metrics_by_form']['10-Q'][metric][d]['val'])
                            else: 
                                row_values.append(np.nan)
                        elif d in data[symbol]['key_metrics_by_form']['10-K'][metric]:
                            if type(data[symbol]['key_metrics_by_form']['10-K'][metric][d]) == dict:
                                row_values.append(data[symbol]['key_metrics_by_form']['10-K'][metric][d]['val'])
                            else: 
                                row_values.append(np.nan)
                        else:
                            row_values.append(np.nan)
                
                stock_dates = list(data[symbol]['stock_price_history'].keys())
                stock_change = []
                for i, stock_date in enumerate(stock_dates):
                    stock_date_dt = datetime.strptime(stock_date, '%Y-%m-%d')
                    if is_less_than_one_month_apart(date_dt, stock_date_dt):
                        stock_change.append(data[symbol]['stock_price_history'][stock_date]['close'] - data[symbol]['stock_price_history'][stock_dates[i-1]]['open'])
                        break
                
                if len(stock_change) == 0:
                    continue
                else:
                    median = statistics.median(stock_change)
                    if median > 0:
                        row_values.append(1)
                    else:
                        row_values.append(0)
                        
                    df.loc[len(df)] = row_values
    
    df.dropna(how='all', inplace=True)
    
    df.to_csv(dataframe_file_path, index=False)
    
    return

def test_model(name, model, X_test, y_test):
    print(name + ":")
    print("Score: {:.4f}%".format(model.score(X_test, y_test) * 100))
    
    y_pred = model.predict(X_test)
    print("ROC-AUC:", roc_auc_score(y_test, y_pred))
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    
    return

def grid_search(X_train, y_train, X_test, y_test):
    model_params = {
    'svm': {
        'model': SVC(gamma='auto'),
        'params' : {
            'classifier__C': [1, 10, 20, 50, 100],
            'classifier__kernel': ['rbf', 'linear', 'poly'],
            'classifier__degree': [1, 2]
        }
    },
    'random_forest': {
        'model': RandomForestClassifier(),
        'params': {
            'classifier__n_estimators': [75,100,150,200],
            'classifier__criterion': ['gini', 'entropy'],
            'classifier__bootstrap' : ["True", "False"],
            'classifier__max_depth' : [7,8,9,10],
            'classifier__max_features': ['sqrt', 'log2'],
            'classifier__n_jobs' : [5]
        }
    },
    'logistic_regression' : {
        'model': LogisticRegression(multi_class='auto', max_iter=300),
        'params': {
            'classifier__solver': ['lbfgs', 'liblinear'],
            'classifier__C': np.geomspace(1e-5, 1e5, num=20)
        }
    },
    'neural_network': {
        'model': MLPClassifier(max_iter=100),
        'params': {
            'classifier__hidden_layer_sizes': [(50,50,50), (50,100,50), (100,)],
            'classifier__activation': ['tanh', 'relu'],
            'classifier__solver': ['sgd', 'adam'],
            'classifier__alpha': [0.0001, 0.05],
            'classifier__learning_rate': ['constant','adaptive'],
        }
    },
    'knn': {
        'model': KNeighborsClassifier(),
        'params': {
            'classifier__n_neighbors': [1,10,1],
            'classifier__leaf_size': [20,40,1],
            'classifier__p': [1,2],
            'classifier__weights': ('uniform', 'distance'),
            'classifier__metric': ('minkowski', 'chebyshev')
        }
    },
    'lightGBM': {
        'model': LGBMClassifier(objective="binary", random_state=0),
        'params': {
            'classifier__num_leaves': np.arange(2, 5, 1),
            'classifier__max_depth': np.arange(1, 4, 1),
            'classifier__n_estimators': np.arange(50, 101, 25)
        }
        
    },
    'decision_tree': {
        'model': DecisionTreeClassifier(),
        'params' : {
            'classifier__criterion' : ['gini', 'entropy'],
            'classifier__max_depth' : range(1, 20),
            'classifier__min_samples_split' : range(1, 15),
            'classifier__min_samples_leaf' : range(1, 10)
        }
    }
}
    
    kf = RepeatedStratifiedKFold(n_splits=10, n_repeats=10, random_state=0)

    scores = []
    for model_name, mp in model_params.items():
        if model_name != 'lightGBM':
            continue
        #pipeline = Pipeline([('smote', SMOTE(random_state=42)), ('classifier', mp['model'])])
        pipeline = Pipeline([('classifier', mp['model'])])
        grid_search = GridSearchCV(pipeline,
                                param_grid=mp['params'],
                                return_train_score=False,
                                cv=kf,
                                n_jobs=-1,
                                verbose=1)
        
        grid_search.fit(X_train, y_train)
        scores.append({
            'model': model_name,
            'best_score': grid_search.best_score_,
            'best_params': grid_search.best_params_
        })
    
    df = pd.DataFrame(scores, columns=['model', 'best_score', 'best_params'])
    
    lightGBM_model = LGBMClassifier(objective="binary", random_state=0, max_depth=df.iloc[0]['best_params']['classifier__max_depth'], n_estimators=df.iloc[0]['best_params']['classifier__n_estimators'], num_leaves=df.iloc[0]['best_params']['classifier__num_leaves'])
    lightGBM_model.fit(X_train, y_train)
    
    test_model('LightGBM with gridsearch:', lightGBM_model, X_test, y_test)
    
    return scores

def create_model():
    df = pd.read_csv(dataframe_file_path)
    
    X = df.drop('buy', axis=1)
    y = df['buy']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    #Baseline model
    model = LGBMClassifier()
    model.fit(X_train, y_train)
    
    test_model('Baseline lightGBM model:', model, X_test, y_test)
    
    grid_search(X_train, y_train, X_test, y_test)
    
    return

def explain_model():
    
    return

if __name__ == '__main__':
    #data_prep()
    create_model()
    