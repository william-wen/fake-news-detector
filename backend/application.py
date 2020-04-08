from app import app
from flask import Flask
from flask import request
from flask import jsonify
from bs4 import BeautifulSoup
from joblib import dump, load
from bs4.element import Comment
import urllib.request
import requests
import validators
import time
import json
import re


app = Flask(__name__)

@app.route('/parse_url', methods=["POST"])

# validates the url sent by the user, return error if not confirm to proper url format
def parse_url():
    message = ''
    prediction = None
    request_url = json.loads(request.data).get('url')
    if request_url is None:
        message = "No url in request data"
    valid=valid=validators.url(request_url)
    if not valid:
        message = "Not a valid url"
    if not message:
        try:
            html = requests.get(request_url).content
            message = text_from_html(html)
            prediction = prediction_response(html)
        except Exception as e:
            message = "The following error happened:" + str(e)
    return {'message':message
    , "prediction":prediction
    }

# takes all the text from <p> tags in the website, which is the article
def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    ps = soup.findAll('p')
    all_text = ""
    for p in ps:
        all_text = all_text + p.text
    return all_text.strip()

# run the ML model on the submitted article
def prediction_response(text):
    pac = load("../models/fake_news_classifier.joblib")
    tfidf_vectorizer = load("../models/tfidf_vectorizer.joblib")
    vectorized_string = tfidf_vectorizer.transform([text])
    prediction = pac.predict(vectorized_string)
    return str(prediction[0])
    
# Output: array(['FAKE'], dtype='<U4')

