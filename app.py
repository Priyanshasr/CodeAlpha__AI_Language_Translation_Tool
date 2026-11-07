"""
LinguaBridge AI - Language Translation Tool
Flask Backend Application
CodeAlpha AI Internship Project
"""

import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from translator import MyMemoryTranslator

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize the translator
translator = MyMemoryTranslator(email=os.getenv("MYMEMORY_EMAIL"))

# Supported languages with their codes
SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "zh": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
    "ar": "Arabic",
    "pt": "Portuguese",
    "ru": "Russian",
    "bn": "Bengali",
    "ta": "Tamil",
    "te": "Telugu",
    "mr": "Marathi",
    "gu": "Gujarati",
    "ur": "Urdu"
}

MAX_TEXT_LENGTH = 5000


@app.route("/")
def index():
    """Render the main translation page."""
    return render_template("index.html")


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint to verify the backend is running."""
    return jsonify({
        "success": True,
        "status": "healthy",
        "service": "LinguaBridge AI Translation API",
        "supported_languages": SUPPORTED_LANGUAGES
    })


@app.route("/api/translate", methods=["POST"])
def translate():
    """
    Translate text from source language to target language.

    Request JSON:
        {
            "text": "Hello, how are you?",
            "source": "en",
            "target": "hi"
        }

    Response JSON:
        {
            "success": true,
            "translated_text": "...",
            "source": "en",
            "target": "hi"
        }
    """
    # Validate content type
    if not request.is_json:
        return jsonify({
            "success": False,
            "error": "Request must be JSON. Set Content-Type to application/json."
        }), 400

    data = request.get_json()

    # Validate required fields
    text = data.get("text", "").strip()
    source = data.get("source", "").strip().lower()
    target = data.get("target", "").strip().lower()

    if not text:
        return jsonify({
            "success": False,
            "error": "Text field is required and cannot be empty."
        }), 400

    if len(text) > MAX_TEXT_LENGTH:
        return jsonify({
            "success": False,
            "error": f"Text exceeds maximum length of {MAX_TEXT_LENGTH} characters."
        }), 400

    if not source:
        return jsonify({
            "success": False,
            "error": "Source language code is required."
        }), 400

    if not target:
        return jsonify({
            "success": False,
            "error": "Target language code is required."
        }), 400

    # Validate language codes
    if source != "auto" and source not in SUPPORTED_LANGUAGES:
        return jsonify({
            "success": False,
            "error": f"Unsupported source language code: '{source}'. Supported codes: {', '.join(SUPPORTED_LANGUAGES.keys())}"
        }), 400

    if target not in SUPPORTED_LANGUAGES:
        return jsonify({
            "success": False,
            "error": f"Unsupported target language code: '{target}'. Supported codes: {', '.join(SUPPORTED_LANGUAGES.keys())}"
        }), 400

    if source == target:
        return jsonify({
            "success": True,
            "translated_text": text,
            "source": source,
            "target": target,
            "note": "Source and target languages are the same."
        })

    # Perform translation
    try:
        result = translator.translate(text, source, target)

        if result["success"]:
            return jsonify({
                "success": True,
                "translated_text": result["translated_text"],
                "source": source,
                "target": target
            })
        else:
            return jsonify({
                "success": False,
                "error": result.get("error", "Translation failed. Please try again.")
            }), 502

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"An unexpected error occurred: {str(e)}"
        }), 500


@app.route("/api/languages", methods=["GET"])
def get_languages():
    """Return the list of supported languages."""
    return jsonify({
        "success": True,
        "languages": SUPPORTED_LANGUAGES
    })


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "true").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
