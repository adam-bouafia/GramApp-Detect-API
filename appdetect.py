from flask import Flask, request, jsonify
from langdetect import detect

app = Flask(__name__)

@app.route('/detect', methods=['POST'])
def detect_language():
    data = request.get_json()
    if 'text' not in data:
        return jsonify({'error': 'Missing text field in request'})
    text = data['text']
    detected_lang = detect(text)
    if detected_lang in ['ar', 'fr', 'en']:
        return jsonify({'language': detected_lang})
    else:
        return jsonify({'error': 'Language not detected or not supported'})

if __name__ == '__main__':
    app.run()
