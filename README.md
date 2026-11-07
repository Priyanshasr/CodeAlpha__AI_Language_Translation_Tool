# 🌐 LinguaBridge AI — Language Translation Tool

> **CodeAlpha Artificial Intelligence Internship Project**

A modern, web-based Language Translation Tool that enables users to translate text across 17+ languages instantly using the MyMemory Translation API. Built with Flask (Python) backend and a clean, responsive HTML/CSS/JavaScript frontend.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1-green?logo=flask)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📋 Problem Statement

Language barriers hinder global communication. There is a need for a simple, accessible, and fast tool that can translate text between multiple languages in real time — without requiring users to install desktop software or sign up for paid services.

## ✨ Features

- **Real-time Translation** — Powered by the MyMemory Translation API
- **17+ Languages** — English, Hindi, Spanish, French, German, Chinese, Japanese, Korean, Arabic, Portuguese, Russian, Bengali, Tamil, Telugu, Marathi, Gujarati, Urdu
- **Detect Language** — Auto-detect source language (where API supports it)
- **Swap Languages** — One-click source ↔ target swap (swaps text too)
- **Copy Translation** — Copy translated output to clipboard instantly
- **Character Counter** — Live character count (max 5000)
- **Translation History** — Recent translations stored in localStorage
- **Loading Indicator** — Spinner animation during API requests
- **Error Handling** — Clear error messages for invalid inputs, API failures
- **Responsive Design** — Desktop, tablet, and mobile-friendly
- **Secure** — API calls routed through the backend; no keys exposed in the browser

## 🛠️ Technologies Used

| Layer        | Technology                        |
|-------------|-----------------------------------|
| Frontend     | HTML5, CSS3, Vanilla JavaScript   |
| Backend      | Python 3, Flask                   |
| Translation  | MyMemory Translation API          |
| HTTP Client  | Python `requests`                 |
| Config       | `python-dotenv`                   |
| Fonts        | Google Fonts (Inter)              |
| Icons        | Font Awesome 6                    |

## 📁 Project Structure

```
language-translator/
│
├── app.py                  # Flask application & API routes
├── translator.py           # Translation provider (MyMemory API)
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── .gitignore              # Git ignore rules
├── README.md               # Project documentation
│
├── templates/
│   └── index.html          # Main HTML template
│
└── static/
    ├── css/
    │   └── style.css       # Application stylesheet
    ├── js/
    │   └── script.js       # Frontend JavaScript logic
    └── images/             # Static images (if any)
```

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Internet connection (for MyMemory API)

### Step 1: Clone the Repository

```bash
git clone https://github.com/Priyanshasr/CodeAlpha_LanguageTranslationTool.git
cd CodeAlpha_LanguageTranslationTool
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

```bash
copy .env.example .env
```

Edit `.env` if needed (the default configuration works out of the box with MyMemory's free tier).

### Step 5: Run the Application

```bash
python app.py
```

The application will start at: **http://localhost:5000**

## ⚙️ API Configuration

### MyMemory Translation API (Default)

The project uses the **MyMemory Translation API** which provides free translations:
- **No API key required** for basic usage
- Up to ~5000 characters per day on the free tier
- Optional: Add your email in `.env` as `MYMEMORY_EMAIL=your@email.com` to increase limits

### Switching Translation Providers

The translation logic is encapsulated in `translator.py`. To use a different provider:
1. Create a new class with a `translate(text, source, target)` method
2. Return `{"success": bool, "translated_text": str, "error": str}`
3. Update the import in `app.py`

## 📡 API Endpoints

### `GET /api/health`

Health check endpoint.

**Response:**
```json
{
  "success": true,
  "status": "healthy",
  "service": "LinguaBridge AI Translation API",
  "supported_languages": { "en": "English", "hi": "Hindi", ... }
}
```

### `POST /api/translate`

Translate text from one language to another.

**Request:**
```json
{
  "text": "Hello, how are you?",
  "source": "en",
  "target": "hi"
}
```

**Response (Success):**
```json
{
  "success": true,
  "translated_text": "नमस्ते, आप कैसे हैं?",
  "source": "en",
  "target": "hi"
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "Text field is required and cannot be empty."
}
```

### `GET /api/languages`

Returns the list of supported languages.

## 📸 Screenshots

> Add screenshots of the application here after running it locally.

| Screenshot | Description |
|-----------|-------------|
| Home Page | Hero section with translator card |
| Translation | English to Hindi translation result |
| Mobile View | Responsive mobile layout |
| History | Translation history panel |

## 🔮 Future Enhancements

- [ ] Speech-to-text input (Web Speech API)
- [ ] Text-to-speech for translated output
- [ ] File upload translation (PDF, DOCX)
- [ ] Dark mode toggle
- [ ] Google Cloud Translation API integration
- [ ] User accounts with cloud-synced history
- [ ] Batch translation mode
- [ ] Translation quality scoring

## 📄 License

This project is created for educational purposes as part of the **CodeAlpha AI Internship**.

## 🙏 Acknowledgments

- [CodeAlpha](https://www.codealpha.tech/) — Internship program
- [MyMemory Translation API](https://mymemory.translated.net/) — Translation service
- [Font Awesome](https://fontawesome.com/) — Icons
- [Google Fonts](https://fonts.google.com/) — Inter typeface

---

**Made with ❤️ for CodeAlpha AI Internship**
