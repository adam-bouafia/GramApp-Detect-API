from flask import Flask, request

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

nltk.download('stopwords')
nltk.download('punkt')

app = Flask(__name__)

# Preprocess the data
def preprocess(text, language):
    # Convert to lowercase
    text = text.lower()
    # Remove non-alphabetic characters
    text = "".join([char for char in text if char.isalpha() or char.isspace()])
    # Remove stopwords
    if language == "english":
        stop_words = set(stopwords.words("english"))
    elif language == "french":
        stop_words = set(stopwords.words("french"))
    elif language == "arabic":
        stop_words = set(nltk.corpus.stopwords.words('arabic'))
    words = word_tokenize(text)
    words = [word for word in words if word not in stop_words]
    return words

# Generate the language model
def language_model(words):
    freq_dist = FreqDist(words)
    return freq_dist

# Detect the language of a query
@app.route('/detect', methods=['GET', 'POST'])
def detect_language():
    if request.method == 'GET':
        return "This is a GET request."
    elif request.method == 'POST':
        text = request.json['text']
        models = request.json['models']
        preprocessed_text = preprocess(text, "english")
        probabilities = {}
        for language, model in models.items():
            prob = 0
            for word in preprocessed_text:
                prob += model.freq(word)
            probabilities[language] = prob
        total_prob = sum(probabilities.values())
        if total_prob == 0:
            return "No language model found for the given text."
        result = {}
        for language, prob in probabilities.items():
            result[language] = prob/total_prob*100
        return result


# Train the model
def train_model(texts_by_language):
    models = {}
    for language, texts in texts_by_language.items():
        words = []
        for text in texts:
            words += preprocess(text, language)
        models[language] = language_model(words)
    return models

if __name__ == '__main__':
    texts_by_language = {
        "english": [
            "hello", "world",
            "how", "are", "you",
            "i", "am", "fine",
        ],
        "french": [
            "bonjour", "tout", "le", "monde",
            "comment", "allez", "vous",
            "je", "vais", "bien",
        ],
        "arabic": [
            "مرحبا", "كيف", "حالك",
            "أنا", "بخير",
        ],
    }
    models = train_model(texts_by_language)
    app.run(debug=True)
