from flask import Flask, request, send_file, jsonify, render_template
from gtts import gTTS
from googletrans import Translator
import os
from flask_cors import CORS  # <-- ADD THIS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


translator = Translator()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/translate", methods=["POST"])
def translate_text():
    data = request.json
    text = data.get("text")
    target_lang = data.get("target_lang")
    if not text or not target_lang:
        return jsonify({"error": "Missing text or target_lang"}), 400
    translated = translator.translate(text, dest=target_lang)
    return jsonify({"translated_text": translated.text})

@app.route("/generate_audio", methods=["POST"])
def generate_audio():
    data = request.json
    text = data.get("text")
    lang = data.get("lang")
    if not text or not lang:
        return jsonify({"error": "Missing text or lang"}), 400
    try:
        tts = gTTS(text=text, lang=lang)
        filepath = "temp.mp3"
        tts.save(filepath)
        return send_file(filepath, as_attachment=True, mimetype='audio/mpeg')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)