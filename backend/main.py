from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from queries import get_company_pred

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
    return get_company_pred(company_name)