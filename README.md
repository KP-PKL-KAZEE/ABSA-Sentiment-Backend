# Backend for ABSA Sentiment Project

## Getting Started

This will give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Installation

#### Prerequisites
* Python 3.7.6

#### Setting Up
1. Clone repository.
```sh
    git clone https://github.com/dzakirafabillah/ABSA-Sentiment-Project-PKL-KP
```
2. Go to backend directory
```sh
    cd backend
```
3. Clone additional repository 
```sh
    git clone https://github.com/1tangerine1day/Aspect-Term-Extraction-and-Analysis.git
``` 
4. Rename the previous repository to ABSA_SentimentMultiEmiten and save it in the backend folder.
5. Download the training model and save it in 
```sh
    /backend/models
``` 
6. Install Requirements 
    `pip install -r requirements.txt`

#### Menjalanan API
1. Build API 
    `uvicorn app:app --reload`

### Folder Structure :
![image](https://user-images.githubusercontent.com/61398214/186295869-4f9ac588-eb67-48aa-bada-b88d325abe8d.png)
