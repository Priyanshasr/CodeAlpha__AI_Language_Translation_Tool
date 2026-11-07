"""
Translation Provider Module
Implements MyMemory Translation API integration with intelligent fallback.
Designed to be modular — handles rate limits (HTTP 429) gracefully.
"""

import os
import requests


class MyMemoryTranslator:
    """
    Translation provider using MyMemory Translation API with automated fallback.
    Endpoint: https://api.mymemory.translated.net/get
    Free tier: up to ~5000 chars/day without email, up to ~50000 with email.
    Includes automated fallback to ensure 100% uptime when cloud platforms (e.g. Render)
    share IP addresses that exceed MyMemory's free rate limits.
    """

    BASE_URL = "https://api.mymemory.translated.net/get"
    FALLBACK_URL = "https://translate.googleapis.com/translate_a/single"
    TIMEOUT = 12  # seconds

    def __init__(self, email=None):
        """
        Initialize the translator.

        Args:
            email: Optional email to increase the free API usage limit.
        """
        self.email = email or os.getenv("MYMEMORY_EMAIL")

    def translate(self, text, source, target):
        """
        Translate text from source language to target language.

        Args:
            text: The text to translate.
            source: Source language code (e.g., 'en' or 'auto').
            target: Target language code (e.g., 'hi').

        Returns:
            dict: {
                "success": bool,
                "translated_text": str or None,
                "error": str or None
            }
        """
        # If source and target are the same, return text directly
        if source == target:
            return {
                "success": True,
                "translated_text": text,
                "error": None
            }

        # First attempt: MyMemory Translation API
        try:
            langpair = f"{source}|{target}"
            params = {
                "q": text,
                "langpair": langpair
            }

            if self.email:
                params["de"] = self.email

            response = requests.get(
                self.BASE_URL,
                params=params,
                timeout=self.TIMEOUT
            )

            # If rate-limited (HTTP 429), fall back immediately
            if response.status_code == 429:
                return self._translate_fallback(text, source, target)

            response.raise_for_status()
            data = response.json()

            response_status = data.get("responseStatus")

            if response_status == 200:
                translated_text = data.get("responseData", {}).get("translatedText", "")
                if translated_text:
                    return {
                        "success": True,
                        "translated_text": translated_text,
                        "error": None
                    }
                else:
                    return self._translate_fallback(text, source, target)
            elif response_status in (403, 429):
                # Rate limit / quota reached on MyMemory, trigger fallback
                return self._translate_fallback(text, source, target)
            else:
                # Other non-200 status from MyMemory, try fallback
                fallback_res = self._translate_fallback(text, source, target)
                if fallback_res["success"]:
                    return fallback_res
                error_msg = data.get("responseDetails", "Translation error.")
                return {
                    "success": False,
                    "translated_text": None,
                    "error": f"Translation API error: {error_msg}"
                }

        except requests.exceptions.HTTPError as e:
            # If 429 or 5xx, try fallback
            if e.response is not None and e.response.status_code in (429, 500, 502, 503, 504):
                return self._translate_fallback(text, source, target)
            fallback_res = self._translate_fallback(text, source, target)
            if fallback_res["success"]:
                return fallback_res
            return {
                "success": False,
                "translated_text": None,
                "error": f"Translation service returned an error: {e}"
            }
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.RequestException):
            # Attempt fallback on network issues with MyMemory
            fallback_res = self._translate_fallback(text, source, target)
            if fallback_res["success"]:
                return fallback_res
            return {
                "success": False,
                "translated_text": None,
                "error": "Could not connect to translation service. Please check your internet connection."
            }
        except Exception:
            return self._translate_fallback(text, source, target)

    def _translate_fallback(self, text, source, target):
        """
        Backup translation provider to guarantee high availability when MyMemory rate-limits.
        """
        try:
            sl = "auto" if source == "auto" else source
            params = {
                "client": "gtx",
                "sl": sl,
                "tl": target,
                "dt": "t",
                "q": text
            }
            res = requests.get(self.FALLBACK_URL, params=params, timeout=self.TIMEOUT)
            res.raise_for_status()
            data = res.json()
            if data and isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
                translated_text = "".join(seg[0] for seg in data[0] if seg and seg[0])
                if translated_text:
                    return {
                        "success": True,
                        "translated_text": translated_text,
                        "error": None
                    }
            return {
                "success": False,
                "translated_text": None,
                "error": "Translation service is temporarily busy. Please try again in a few moments."
            }
        except Exception as e:
            return {
                "success": False,
                "translated_text": None,
                "error": f"Translation failed: {str(e)}"
            }
