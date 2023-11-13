import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import shap
import timeshap

from timeshap.utils import calc_avg_event
from timeshap.explainer import local_feat

#tf.compat.v1.disable_v2_behavior() - this removes an error but we get others

import tensorflow as tf


# Temporarily using a subset of the data since it's much quicker to load
data_file_path = 'resources/test_data_subset_100.json'

def create_subset(size):
    with open('resources/test_data.json', 'r') as file:
        data = json.load(file)
        
    subset_dictionary = {key: data[key] for key in list(data.keys())[:size]}
    
    with open('resources/test_data_subset_' + str(size) + '.json', 'w') as file:
        json.dump(subset_dictionary, file)
        
    return

def data_prep():
    with open(data_file_path, 'r') as file:
        data = json.load(file)

    symbols = list(data.keys())
    
    dates = list(data[symbols[0]]['facts_by_form']['10-Q']['fileds']) + list(data[symbols[0]]['facts_by_form']['10-K']['fileds'])
    dates.sort()
    
    metrics = list(data[symbols[0]]['key_metrics_by_form']['10-Q'].keys())
    
    data_array = np.zeros((len(symbols), len(dates), len(metrics)))
    
    for i, symbol in enumerate(symbols):
        for j, date in enumerate(dates):
            for k, metric in enumerate(metrics):
                if date in data[symbol]['key_metrics_by_form']['10-Q'][metric]:
                    if type(data[symbol]['key_metrics_by_form']['10-Q'][metric][date]) == dict:
                        data_array[i, j, k] = data[symbol]['key_metrics_by_form']['10-Q'][metric][date]['val']
                    else: 
                        data_array[i, j, k] = np.nan
                elif date in data[symbol]['key_metrics_by_form']['10-K'][metric]:
                    if type(data[symbol]['key_metrics_by_form']['10-K'][metric][date]) == dict:
                        data_array[i, j, k] = data[symbol]['key_metrics_by_form']['10-K'][metric][date]['val']
                    else: 
                        data_array[i, j, k] = np.nan
                else:
                    data_array[i, j, k] = np.nan
    
    return data_array, symbols, dates, metrics
    
    """ fig = go.Figure()
    fig.add_trace(go.Scatter(y=y_test, mode='lines', name='Actual'))
    fig.add_trace(go.Scatter(y=y_pred, mode='lines+markers', name='Predicted'))
    fig.show() """
    
    #average_event = calc_avg_event(data_array, num_metrics)
    #print(average_event)
    # Everything above this is fully working
    
    # Below is for explainer stuff
    
    # Use the training data for deep explainer => can use fewer instances
    #explainer = shap.DeepExplainer(model, x_train)
    
    #shap_values = explainer.shap_values(x_test[:5])
    
    # init the JS visualization code
    #shap.initjs()
    
    #shap_values_2D = shap_values[0].reshape(-1,10)
    #X_test_2D = x_test.reshape(-1,10)
    
    #x_test_2d = pd.DataFrame(data=X_test_2D, columns = metrics)
    #shap.summary_plot(shap_values_2D, x_test_2d)
    #shap.summary_plot(shap_values_2D, x_test_2d, plot_type="bar")
    
    return

def create_model(data_array, symbols, dates, metrics):
    num_companies, num_dates, num_metrics = data_array.shape
    
    labels = np.random.randint(2, size=(num_companies,))
    
    x_train = data_array[:90]
    y_train = labels[:90]
    
    x_test = data_array[90:]
    y_test = labels[90:]
    
    print(x_train.shape, y_train.shape)
    print(x_test.shape, y_test.shape)
    
    model = tf.keras.Sequential()
    
    model.add(tf.keras.layers.LSTM(50, input_shape=(num_dates, num_metrics)))
    model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    model.fit(x_train, y_train, epochs=10, batch_size=32)
    
    model.save('resources/model.keras')
    
    predictions = model.predict(x_test)    
    y_pred = (predictions > 0.5).astype(int)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=y_test, mode='lines', name='Actual'))
    fig.add_trace(go.Scatter(y=y_pred, mode='lines+markers', name='Predicted'))
    fig.show()
    
    return

def explain_model(data_array, symbols, dates, metrics):
    print(data_array.shape)
    
    #model = tf.keras.models.load_model('resources/model.keras')
    
    #f_hs = lambda x, y=None: model.predict_last_hs(x, y)
    #pos_x_data = data_array[metrics]
    
    #local_feat()
    
    
    #print(metrics)
    
    #average_event = calc_avg_event(data_array, numerical_feats=metrics, categorical_feats=[])
    #print(average_event)
    
    return

if __name__ == '__main__':
    #create_subset(100)
    data_array, symbols, dates, metrics = data_prep()
    #create_model(data_array, symbols, dates, metrics)
    explain_model(data_array, symbols, dates, metrics)