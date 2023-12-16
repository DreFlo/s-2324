import json
import os

def cache_prediction(prediction : dict) -> None:
    prediction_cache = None

    # Load cache if exists else create new cache and init empty cache
    if os.path.exists('prediction_cache.json'):
        with open('prediction_cache.json', 'r') as cache_file:
            prediction_cache = json.load(cache_file)
    else:
        prediction_cache = {}

    # Add new prediction to cache
    prediction_cache[prediction['symbol']] = prediction

    # Write cache to file
    with open('prediction_cache.json', 'w') as cache_file:
        json.dump(prediction_cache, cache_file)

def get_cached_prediction(symbol : str) -> dict | None:
    prediction_cache = None

    # Load cache if exists else return None
    if os.path.exists('prediction_cache.json'):
        with open('prediction_cache.json', 'r') as cache_file:
            prediction_cache = json.load(cache_file)
    else:
        return None

    # Return cached prediction if exists else return None
    if symbol in prediction_cache:
        return prediction_cache[symbol]
    else:
        return None
    
def get_cached_predictions() -> dict | None:
    prediction_cache = None

    # Load cache if exists else return None
    if os.path.exists('prediction_cache.json'):
        with open('prediction_cache.json', 'r') as cache_file:
            prediction_cache = json.load(cache_file)
    else:
        return None

    # Return cached prediction if exists else return None
    return prediction_cache
