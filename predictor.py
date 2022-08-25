import pandas as pd
import numpy as np
from transformers import AutoTokenizer
import torch
from torch.nn.utils.rnn import pad_sequence
from ABSA_SentimentMultiEmiten.model.bert import bert_ABSA
import preprocessing

def load_model(model, path):
    model.load_state_dict(torch.load(path, map_location=torch.device('cpu')), strict=False)
    return model

DEVICE = torch.device("cpu")
pretrain_model_name = "indolem/indobert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(pretrain_model_name)
model_ABSA = bert_ABSA(pretrain_model_name).to(DEVICE)
model_path = './models/bert_ABSA_11.pkl'
model_ABSA = load_model(model_ABSA, model_path)

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

def predict_sentence(s, aspect):
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

def get_data_emiten():
  #Data emiten ini diambil dari website www.idx.co.id 
  #dan discrapping pada tanggal 22 Agustus 2022.
  return pd.read_csv("./data/daftar_emiten.csv")

def get_final_sentiment_artikel(artikel, data_emiten=[]):
  output = []
  
  if(data_emiten==[]): # 1 input/predict all emiten
    data_emiten = get_data_emiten().KodeEmiten
  else: # 2 Input/predict specific emiten
    data_emiten = data_emiten.split()

  for emiten in data_emiten:
    if(emiten in artikel):
      output.extend(predict_sentence(artikel, emiten))
  
  return output