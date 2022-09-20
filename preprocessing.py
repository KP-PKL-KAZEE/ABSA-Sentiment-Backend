# Load Libraries
import re
import pandas as pd
import time
import numpy as np

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

# Function Remove Unused Dots
## Function ini berfungsi menghilangkan titik (dots) yang tidak memiliki makna pada artikel.
def remove_unused_dots(arr_of_char):
  i=0
  while i < len(arr_of_char):
    if (arr_of_char[i] == "." and i != len(arr_of_char)):
      if(arr_of_char[i - 1].isdigit()):
        arr_of_char = arr_of_char[:i] + '' + arr_of_char[i+1:]
    i = i+1
  return "".join(arr_of_char)

# Function Preprocessing Text.
## Function ini berfungsi menghilangkan kata yang tidak diperlukan pada artikel
def preprocessing_text(sentences, aspect):
  # hapus url
  sentences = re.sub('\S+.com|\S+.co.id|\S+.co|\S+.id', '.', sentences)

  ### hapus titik yang bukan pemisah kalimat 
  ### (yang pemisah angka, Tbk., PT.)
  sentences = sentences.replace("PT.", "PT").replace("Tbk.", "Tbk")
  sentences = remove_unused_dots(sentences)

  ### Ambil kalimat yang mengandung emiten
  sentences = sentences.split('.')
  arr_sentence_dirt = clean_sentences(sentences, aspect)
  
  arr_sentence_clean = []
  arr_sentence_clean.extend(arr_sentence_dirt)
  i = 0
  while (i < (len(arr_sentence_clean))):
    arr_sentence_clean[i] = re.sub(r'[^\w\d\s\.]+', '', arr_sentence_clean[i]) 
    arr_sentence_clean[i] = arr_sentence_clean[i].lower()
    ### Menghapus angka
    arr_sentence_clean[i] = ''.join([x for x in arr_sentence_clean[i] if not x.isdigit()])
    i = i+1

  return arr_sentence_clean, arr_sentence_dirt 