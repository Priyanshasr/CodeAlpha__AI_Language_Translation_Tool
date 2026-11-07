"""
Automated Test Suite for LinguaBridge AI
Tests backend API endpoints, validation, error handling, and MyMemory translation.
"""

import sys
import unittest

# Ensure stdout handles unicode
sys.stdout.reconfigure(encoding="utf-8")

from app import app
from translator import MyMemoryTranslator


class TestTranslatorModule(unittest.TestCase):
    """Test the MyMemoryTranslator class directly."""

    def setUp(self):
        self.translator = MyMemoryTranslator()

    def test_en_to_hi(self):
        result = self.translator.translate("Hello, how are you?", "en", "hi")
        self.assertTrue(result["success"])
        self.assertIsNotNone(result["translated_text"])
        print(f"\n[Test] Direct en->hi: 'Hello, how are you?' -> {result['translated_text']}")

    def test_hi_to_en(self):
        result = self.translator.translate("नमस्ते", "hi", "en")
        self.assertTrue(result["success"])
        self.assertIsNotNone(result["translated_text"])
        print(f"[Test] Direct hi->en: 'नमस्ते' -> {result['translated_text']}")

    def test_same_language_in_module(self):
        result = self.translator.translate("Hello", "en", "en")
        self.assertTrue(result["success"])


class TestFlaskEndpoints(unittest.TestCase):
    """Test Flask routes and API validation."""

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"LinguaBridge", response.data)
        print("\n[Test] GET / returns 200 and contains 'LinguaBridge'")

    def test_health_endpoint(self):
        response = self.app.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["status"], "healthy")
        self.assertIn("en", data["supported_languages"])
        print("[Test] GET /api/health returns healthy status and supported languages")

    def test_languages_endpoint(self):
        response = self.app.get("/api/languages")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertIn("hi", data["languages"])
        print("[Test] GET /api/languages returns language list")

    def test_translate_en_to_hi(self):
        response = self.app.post("/api/translate", json={
            "text": "Good morning",
            "source": "en",
            "target": "hi"
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertIsNotNone(data["translated_text"])
        print(f"[Test] POST /api/translate en->hi: {data['translated_text']}")

    def test_translate_hi_to_en(self):
        response = self.app.post("/api/translate", json={
            "text": "नमस्ते",
            "source": "hi",
            "target": "en"
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertIsNotNone(data["translated_text"])
        print(f"[Test] POST /api/translate hi->en: {data['translated_text']}")

    def test_empty_text_validation(self):
        response = self.app.post("/api/translate", json={
            "text": "   ",
            "source": "en",
            "target": "hi"
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data["success"])
        self.assertIn("error", data)
        print(f"[Test] Empty text validation: {data['error']}")

    def test_missing_language_code(self):
        response = self.app.post("/api/translate", json={
            "text": "Hello",
            "source": "",
            "target": "hi"
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data["success"])
        print(f"[Test] Missing source code validation: {data['error']}")

    def test_unsupported_language_code(self):
        response = self.app.post("/api/translate", json={
            "text": "Hello",
            "source": "xyz_unsupported",
            "target": "hi"
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data["success"])
        print(f"[Test] Unsupported source code validation: {data['error']}")

    def test_same_source_and_target(self):
        response = self.app.post("/api/translate", json={
            "text": "Identical text test",
            "source": "en",
            "target": "en"
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["translated_text"], "Identical text test")
        print(f"[Test] Same source & target: {data['translated_text']}")

    def test_non_json_request(self):
        response = self.app.post("/api/translate", data="raw text", content_type="text/plain")
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data["success"])
        print(f"[Test] Non-JSON payload validation: {data['error']}")


if __name__ == "__main__":
    unittest.main()
