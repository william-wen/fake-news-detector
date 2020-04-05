# fake-news-detector

The model is called `fake_news_classifier.joblib`. The vectorizer used to convert words into numbers the model can recognize is called `tfidf_vectorizer.joblib`

### How to make a prediction with the model:

```
from joblib import dump, load

pac = load("fake_news_classifier.joblib")
tfidf_vectorizer = load("tfidf_vectorizer.joblib")

vectorized_string = tfidf_vectorizer.transform(
    ["Increased SO2 submissions detected above China indicates that China maybe burning bodies without telling the rest of 
    the world. They say they have the disease under control but we all know president Xi Jinping is snake oil salesman who
    will do anything if it means he'll stay popular and remain in power. What an idiot! God bless free America and our
    president, Donald Trump."]
)

prediction = pac.predict(vectorized_string)

# Output: array(['FAKE'], dtype='<U4')
```

### How to start

First, we recommend running 
```
cd frontend
npm install
```
in order to install the required packages

## Starting the servers

To start the Flask backend, 

```
cd frontend
npm run start-api
```

To start the React Frontend,

```
cd frontend
npm run start
```