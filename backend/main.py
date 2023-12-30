from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from queries import get_company_pred
from utils.cache_utils import get_cached_predictions

from typing import Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def root():
    return {'message' : 'Hello, world!'}

@app.get('/predict')
def predict(company_name: str):
    prediction = get_company_pred(company_name)
    
    if prediction  == -1:
        raise HTTPException(status_code=404, detail=f'No results found for company {company_name}.<br> Check if the company name is correct and if it is in the NASDAQ.')
    elif prediction == -2:
        raise HTTPException(status_code=404, detail=f'We weren\'t able to get historical data for company {company_name}.<br> It might be that the company is too new or that the API is down.')
    else:
        return prediction

@app.get('/rankings')
def rankings(num: Optional[int] = -1):
    return get_cached_predictions(num)