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
    prediction = ''
    title = ''
    request_url = json.loads(request.data).get('url')
    if request_url is None:
        message = "No url in request data"
    valid=valid=validators.url(request_url)
    if not valid:
        message = "Not a valid url"
    if not message:
        try:
            html = requests.get(request_url).content
            text_content = text_from_html(html)
            title = article_title_from_html(html)
            message = text_content
            prediction = prediction_response(text_content)
        except Exception as e:
            message = "The following error happened:" + str(e)
    return {'message':message, "title":title, "prediction":prediction}

# takes all the text from <p> tags in the website, which is the article
def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    ps = soup.findAll('p')
    all_text = ""
    for p in ps:
        all_text = all_text + p.text
    return all_text.strip()

# gets the article title from the website
def article_title_from_html(body):
    soup = BeautifulSoup(body, "html.parser")
    all_h = soup.findAll(["h1", "h2", "h3"])
    return all_h[0].text.strip()

# run the ML model on the submitted article
def prediction_response(text):
    pac = load("../models/fake_news_classifier.joblib")
    tfidf_vectorizer = load("../models/tfidf_vectorizer.joblib")
    # text = """U.S. Secretary of State John F. Kerry said Monday that he will stop in Paris later this week, amid criticism that no top American officials attended Sundayâ€™s unity march against terrorism.Kerry said he expects to arrive in Paris Thursday evening, as he heads home after a week abroad. He said he will fly to France at the conclusion of a series of meetings scheduled for Thursday in Sofia, Bulgaria. He plans to meet the next day with Foreign Minister Laurent Fabius and President Francois Hollande, then return to Washington.The visit by Kerry, who has family and childhood ties to the country and speaks fluent French, could address some of the criticism that the United States snubbed France in its darkest hour in many years.The French press on Monday was filled with questions about why neither President Obama nor Kerry attended Sundayâ€™s march, as about 40 leaders of other nations did. Obama was said to have stayed away because his own security needs can be taxing on a country, and Kerry had prior commitments.Among roughly 40 leaders who did attend was Israeli Prime Minister Benjamin Netanyahu, no stranger to intense security, who marched beside Hollande through the city streets. The highest ranking U.S. officials attending the march were Jane Hartley, the ambassador to France, and Victoria Nuland, the assistant secretary of state for European affairs. Attorney General Eric H. Holder Jr. was in Paris for meetings with law enforcement officials but did not participate in the march.Kerry spent Sunday at a business summit hosted by Indiaâ€™s prime minister, Narendra Modi. The United States is eager for India to relax stringent laws that function as barriers to foreign investment and hopes Modiâ€™s government will act to open the huge Indian market for more American businesses.In a news conference, Kerry brushed aside criticism that the United States had not sent a more senior official to Paris as â€œquibbling a little bit.â€ He noted that many staffers of the American Embassy in Paris attended the march, including the ambassador. He said he had wanted to be present at the march himself but could not because of his prior commitments in India.But that is why I am going there on the way home, to make it crystal clear how passionately we feel about the events that have taken place there,â€ he said.And I donâ€™t think the people of France have any doubts about Americaâ€™s understanding of what happened, of our personal sense of loss and our deep commitment to the people of France in this moment of trauma.â€"""
    vectorized_string = tfidf_vectorizer.transform([text])
    prediction = pac.predict(vectorized_string)
    return str(prediction[0])
    
# Output: array(['FAKE'], dtype='<U4')

