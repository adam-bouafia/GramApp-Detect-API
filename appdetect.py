from flask import Flask, request, jsonify
from langdetect import detect_langs

app = Flask(__name__)

@app.route('/detect', methods=['POST'])
def detect_language():
    text = request.json['text']
    langs = detect_langs(text)
    detected_lang = ''
    for lang in langs:
        if lang.lang in ['ar', 'fr', 'en']:
            detected_lang = lang.lang
            break
    return jsonify({'language': detected_lang})

if __name__ == '__main__':
    app.run()
