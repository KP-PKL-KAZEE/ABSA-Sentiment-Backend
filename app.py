# Load the libraries
from fastapi import FastAPI, HTTPException
import predictor
import torch
from transformers import AutoTokenizer
from ABSA_SentimentMultiEmiten.model.bert import bert_ABSA

# Initialize an instance of FastAPI
app = FastAPI()

# Define the default route 
@app.get("/")
def root():
    return {"message": "Welcome to Your Sentiment Classification FastAPI"}

@app.post("/predict_sentiment_all_emiten")
def predict_sentiment_all_emiten(news):
    if(not(news)):
        raise HTTPException(status_code=400, 
                            detail = "Please Provide a valid text message")

    return predictor.get_final_sentiment_artikel(news)

@app.post("/predict_sentiment_specific_emiten")
def predict_sentiment_specific_emiten(news, aspect):
    if(not(news)):
        raise HTTPException(status_code=400, 
                            detail = "Please Provide a valid text message")

    return predictor.get_final_sentiment_artikel(news, aspect)