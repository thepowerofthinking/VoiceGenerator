from flask import Flask, request, send_file, jsonify, render_template
from flask_cors import CORS
from gtts import gTTS
from googletrans import Translator
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # ✅ CORS setup here

translator = Translator()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    if not data or 'text' not in data or 'target_lang' not in data:
        return jsonify({"error": "Missing parameters"}), 400

    try:
        translated = translator.translate(data['text'], dest=data['target_lang'])
        return jsonify({"translated_text": translated.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate_audio', methods=['POST'])
def generate_audio():
    data = request.json
    if not data or 'text' not in data or 'lang' not in data:
        return jsonify({"error": "Missing parameters"}), 400

    try:
        tts = gTTS(text=data['text'], lang=data['lang'])
        file_path = "temp.mp3"
        tts.save(file_path)
        return send_file(file_path, mimetype="audio/mpeg", as_attachment=False)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
