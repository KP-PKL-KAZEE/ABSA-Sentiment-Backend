# Get the Fast API image with Python version 3.7
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

# Create the directory for the container
WORKDIR /app
COPY requirements.txt ./requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app.py ./

COPY ./predictor.py ./

COPY ./preprocessing.py ./

COPY ./ABSA_SentimentMultiEmiten ./ABSA_SentimentMultiEmiten

# Copy the serialized model and the vectors
COPY ./models/bert_ABSA_11.pkl ./models/bert_ABSA_11.pkl
# COPY ./vectors/vectorizer.pickle ./vectors/vectorizer.pickle

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]