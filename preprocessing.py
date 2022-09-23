# Load Libraries
import re
import pandas as pd
import time
import numpy as np
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

# Function Clean Unused Sentence
## Function ini digunakan untuk menghilangkan sentences yang tidak memiliki aspect / emiten didalamnya.
def clean_sentences(sentences, aspect):
  new_sentences =[]
  for sentence in sentences:
    if ((aspect in sentence)):
      index = sentence.index(aspect)
      if(len(sentence) > index+4):
        emiten = (sentence[index-1].isalpha() == False) and (sentence[index+4].isalpha() == False) 
      else:
        emiten = (sentence[index-1].isalpha() == False)
      if(emiten):
        new_sentences.append(sentence)
  return new_sentences

# Function Split Sentence
## Function ini berfungsi untuk split artikel menjadi kumpulan kalimat bermakna
def split_sentence(article):
  tokens = nltk.tokenize.sent_tokenize(article)
  return tokens

# Function Preprocessing Text
## Function ini berfungsi menghilangkan kata yang tidak diperlukan pada artikel
def preprocessing_text(article, aspect):
  # hapus url
  article = re.sub('\S+.com|\S+.co.id|\S+.co|\S+.id', '.', article)

  ### hapus titik yang bukan pemisah kalimat(Tbk., PT.)
  article = article.replace("PT.", "PT").replace("Tbk.", "Tbk")

  ### hapus titik yang bukan pemisah kalimat(titik dalam penomoran/urutan)
  for number in range(100):
    article = article.replace(" "+str(number)+". ", " " )

  ### split menjadi kumpulan kalimat bermakna
  sentences = split_sentence(article)

  ### hanya ambil kalimat yang mengandung emiten
  arr_sentence_dirt = clean_sentences(sentences, aspect)
  
  arr_sentence_clean = []
  arr_sentence_clean.extend(arr_sentence_dirt)
  i = 0
  while (i < (len(arr_sentence_clean))):
    # arr_sentence_dirt[i][0] = arr_sentence_dirt[i][0].upper()
    arr_sentence_clean[i] = re.sub(r'[^\w\d\s\.]+', '', arr_sentence_clean[i]) 
    arr_sentence_clean[i] = arr_sentence_clean[i].lower()
    ### Menghapus angka
    arr_sentence_clean[i] = ''.join([x for x in arr_sentence_clean[i] if not x.isdigit()])
    i = i+1

  return arr_sentence_clean, arr_sentence_dirt 