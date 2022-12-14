# Load Libraries.
import pandas as pd
import numpy as np
from transformers import AutoTokenizer
import torch
from torch.nn.utils.rnn import pad_sequence
from ABSA_SentimentMultiEmiten.model.bert import bert_ABSA
import preprocessing

# Function Load Model.
def load_model(model, path):
    model.load_state_dict(torch.load(path, map_location=torch.device('cpu')), strict=False)
    return model

# Define / Initialization from Model.
DEVICE = torch.device("cpu")
pretrain_model_name = "indolem/indobert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(pretrain_model_name)
model_ABSA = bert_ABSA(pretrain_model_name).to(DEVICE)
model_path = './models/bert_ABSA_11.pkl'
model_ABSA = load_model(model_ABSA, model_path)

# Function Predict Sentiment Analysis
## Function ini mengembalikan nilai sentiment analisis kalimat (sentence) terhadap emiten (aspect)
def predict(sentence, aspect, tokenizer):
    t1 = tokenizer.tokenize(sentence)
    t2 = tokenizer.tokenize(aspect)

    word_pieces = ['[cls]']
    word_pieces += t1
    word_pieces += ['[sep]']
    word_pieces += t2

    segment_tensor = [0] + [0]*len(t1) + [0] + [1]*len(t2)

    ids = tokenizer.convert_tokens_to_ids(word_pieces)
    input_tensor = torch.tensor([ids]).to(DEVICE)
    segment_tensor = torch.tensor(segment_tensor).to(DEVICE)

    with torch.no_grad():
        outputs = model_ABSA(input_tensor, None, None, segments_tensors=segment_tensor)
        _, predictions = torch.max(outputs, dim=1)
    
    return word_pieces, predictions, outputs

# Function Controller Predict
# Output this Function :
## Sentence : Sentence / Kalimat yang displit untuk prediksi kemudian disatukan per aspact.
## Aspect : Emiten yang di predict.
## Sentiment : Nilai Sentiment Hasil Function Predict
def predict_sentence(s, aspect):
  arr_sentence_clean, arr_sentence_dirt  = preprocessing.preprocessing_text(s, aspect)

  output = []
  i = 0
  sentiments = ["Negative", "Neutral", "Positive"]
  final_sentence_clean = ""
  final_sentence_dirt = ""

  while (i < (len(arr_sentence_clean))):
    final_sentence_clean = final_sentence_clean + " " + arr_sentence_clean[i]
    final_sentence_dirt = final_sentence_dirt + " " + arr_sentence_dirt[i]
    i = i+1

  x, y, z = predict(final_sentence_clean , aspect, tokenizer)  
  y_str = str(y)
  sentiment = sentiments[int(y_str[8])]
  if final_sentence_clean != "" :
    output.append({
      "sentence": final_sentence_dirt.strip(),
      "aspect": aspect,
      "sentiment": sentiment
    })
  
  return output

# Function Controller Predict
# Output this Function :
## Sentence : Sentence / Kalimat yang displit untuk prediksi.
## Aspect : Emiten yang di predict.
## Sentiment : Nilai Sentiment Hasil Function Predict
def predict_sentence_asli(s, aspect):
  arr_sentence_clean, arr_sentence_dirt  = preprocessing.preprocessing_text(s, aspect)

  output = []
  i = 0
  sentiments = ["Negative", "Neutral", "Positive"]
  
  while (i < (len(arr_sentence_clean))):
    x, y, z = predict(arr_sentence_clean[i] , aspect, tokenizer)
    
    y_str = str(y)
    sentiment = sentiments[int(y_str[8])]
    output.append({
      "sentence": arr_sentence_dirt[i].strip(),
      "aspect": aspect,
      "sentiment": sentiment
    })
    i = i+1
  
  return output

# Function Get All Datalist Emiten
def get_data_emiten():
  #Data emiten ini diambil dari website www.idx.co.id dan discrapping pada tanggal 22 Agustus 2022.
  return pd.read_csv("./data/daftar_emiten.csv")

# Function Controller Predict Emiten Saham
def get_final_sentiment_artikel(artikel, data_emiten=[]):
  output = []

  # 1 input/predict all emiten
  if(data_emiten==[]): 
    data_emiten = get_data_emiten().KodeEmiten
  # 2 Input/predict specific emiten
  else: 
    data_emiten = data_emiten.split()
  # Predict Emiten from Input or Datalist
  for emiten in data_emiten:
    if(emiten in artikel):
      output.extend(predict_sentence(artikel, emiten))
  
  return output