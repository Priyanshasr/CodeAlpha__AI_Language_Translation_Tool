"""
Translation Provider Module
Implements MyMemory Translation API integration.
Designed to be modular — can be replaced with another provider easily.
"""

import requests


class MyMemoryTranslator:
    """
    Translation provider using MyMemory Translation API.
    Endpoint: https://api.mymemory.translated.net/get
    Free tier: up to ~5000 chars/day without API key, more with key.
    """

    BASE_URL = "https://api.mymemory.translated.net/get"
    TIMEOUT = 15  # seconds

    def __init__(self, email=None):
        """
        Initialize the MyMemory translator.

        Args:
            email: Optional email to increase the free API usage limit.
        """
        self.email = email

    def translate(self, text, source, target):
        """
        Translate text from source language to target language.

        Args:
            text: The text to translate.
            source: Source language code (e.g., 'en').
            target: Target language code (e.g., 'hi').

        Returns:
            dict: {
                "success": bool,
                "translated_text": str or None,
                "error": str or None
            }
        """
        try:
            # If source and target are the same, return text directly
            if source == target:
                return {
                    "success": True,
                    "translated_text": text,
                    "error": None
                }

            # Build the language pair parameter (e.g., "en|hi")
            langpair = f"{source}|{target}"

            params = {
                "q": text,
                "langpair": langpair
            }

            # Add email if provided (increases free tier limit)
            if self.email:
                params["de"] = self.email

            response = requests.get(
                self.BASE_URL,
                params=params,
                timeout=self.TIMEOUT
            )

            response.raise_for_status()
            data = response.json()

            # Check the response status
            response_status = data.get("responseStatus")

            if response_status == 200:
                translated_text = data.get("responseData", {}).get("translatedText", "")

                if not translated_text:
                    return {
                        "success": False,
                        "translated_text": None,
                        "error": "The API returned an empty translation."
                    }

                return {
                    "success": True,
                    "translated_text": translated_text,
                    "error": None
                }
            elif response_status == 403:
                return {
                    "success": False,
                    "translated_text": None,
                    "error": "Daily translation limit exceeded. Please try again later."
                }
            else:
                error_msg = data.get("responseDetails", "Unknown error from translation API.")
                return {
                    "success": False,
                    "translated_text": None,
                    "error": f"Translation API error: {error_msg}"
                }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "translated_text": None,
                "error": "Translation request timed out. Please try again."
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "translated_text": None,
                "error": "Could not connect to the translation service. Check your internet connection."
            }
        except requests.exceptions.HTTPError as e:
            return {
                "success": False,
                "translated_text": None,
                "error": f"Translation service returned an error: {e}"
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "translated_text": None,
                "error": f"Translation request failed: {e}"
            }
        except (ValueError, KeyError) as e:
            return {
                "success": False,
                "translated_text": None,
                "error": f"Failed to parse translation response: {e}"
            }
