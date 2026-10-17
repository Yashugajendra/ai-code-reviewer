import json
import sqlite3
import unittest
from unittest.mock import patch, MagicMock

from app import app, Review, Issue, ALLOWED_LANGUAGES, MAX_CODE_CHARS


class TestCodeReviewer(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        # Use a consistent test owner cookie
        self.owner_id = "testowner00000000000000000000001"
        self.client.set_cookie("owner_id", self.owner_id)

    def test_homepage_render(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        html = res.get_data(as_text=True)
        self.assertIn("AI Code Reviewer", html)
        self.assertIn("CodeMirror", html)
        self.assertIn("Export Markdown", html)

    def test_input_validation_empty_code(self):
        res = self.client.post("/api/review", json={"code": "   ", "language": "Python"})
        self.assertEqual(res.status_code, 400)
        data = res.get_json()
        self.assertIn("Please paste some code", data["error"])

    def test_input_validation_unsupported_language(self):
        res = self.client.post("/api/review", json={"code": "print(1)", "language": "Ruby"})
        self.assertEqual(res.status_code, 400)
        data = res.get_json()
        self.assertIn("Unsupported language", data["error"])

    def test_input_validation_too_long(self):
        long_code = "a" * (MAX_CODE_CHARS + 10)
        res = self.client.post("/api/review", json={"code": long_code, "language": "Python"})
        self.assertEqual(res.status_code, 413)
        data = res.get_json()
        self.assertIn("Code is too long", data["error"])

    def test_history_crud_and_isolation(self):
        # 1. Check history for test owner
        res = self.client.get("/api/history")
        self.assertEqual(res.status_code, 200)
        items_before = res.get_json()["items"]

        # Insert a mock review directly for test owner
        from app import get_db
        with app.app_context():
            db = get_db()
            cur = db.execute(
                "INSERT INTO reviews (owner, created_at, language, code, rating, summary, result_json)"
                " VALUES (?, ?, ?, ?, ?, ?, ?)",
                (self.owner_id, "2026-10-17T00:00:00Z", "Python", "def foo(): pass",
                 9, "Great clean code.", json.dumps({
                     "summary": "Great clean code.",
                     "language_matches": True,
                     "bugs": [],
                     "security": [],
                     "performance": [],
                     "best_practices": [],
                     "rating": 9
                 }))
            )
            review_id = cur.lastrowid
            db.commit()

        # 2. History list now contains this review
        res = self.client.get("/api/history")
        self.assertEqual(res.status_code, 200)
        items = res.get_json()["items"]
        self.assertEqual(len(items), len(items_before) + 1)
        self.assertEqual(items[0]["id"], review_id)

        # 3. Retrieve specific item
        res_item = self.client.get(f"/api/history/{review_id}")
        self.assertEqual(res_item.status_code, 200)
        item_data = res_item.get_json()
        self.assertEqual(item_data["code"], "def foo(): pass")
        self.assertEqual(item_data["language"], "Python")
        self.assertEqual(item_data["review"]["rating"], 9)

        # 4. Check owner isolation: another owner cannot access or delete this review
        client_b = app.test_client()
        client_b.set_cookie("owner_id", "testowner00000000000000000000002")
        res_b = client_b.get(f"/api/history/{review_id}")
        self.assertEqual(res_b.status_code, 404)

        del_b = client_b.delete(f"/api/history/{review_id}")
        self.assertEqual(del_b.status_code, 404)

        # 5. Test owner deletes their review
        del_res = self.client.delete(f"/api/history/{review_id}")
        self.assertEqual(del_res.status_code, 200)
        self.assertTrue(del_res.get_json().get("ok"))

        # 6. Verify it is gone
        del_again = self.client.delete(f"/api/history/{review_id}")
        self.assertEqual(del_again.status_code, 404)

    @patch("app.client.models.generate_content")
    def test_mock_review_endpoint(self, mock_gen):
        mock_response = MagicMock()
        mock_response.parsed = Review(
            summary="Test function is valid and runs efficiently.",
            language_matches=True,
            bugs=[],
            security=[],
            performance=[],
            best_practices=[
                Issue(
                    title="Add docstring",
                    severity="low",
                    line=1,
                    explanation="Functions should have docstrings.",
                    suggestion="Add a docstring under def add."
                )
            ],
            rating=9
        )
        mock_gen.return_value = mock_response

        res = self.client.post("/api/review", json={
            "code": "def add(x, y):\n    return x + y",
            "language": "Python"
        })
        self.assertEqual(res.status_code, 200)
        payload = res.get_json()
        self.assertIn("id", payload)
        self.assertEqual(payload["review"]["rating"], 9)
        self.assertEqual(len(payload["review"]["best_practices"]), 1)

    def test_stats_endpoint(self):
        # Empty stats
        empty_client = app.test_client()
        empty_client.set_cookie("owner_id", "fresh_empty_owner_000000000001")
        res = empty_client.get("/api/stats")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["total_reviews"], 0)
        self.assertEqual(data["avg_rating"], 0.0)
        self.assertIn("Python", data["languages"])
        self.assertIn("Java", data["languages"])
        self.assertIn("JavaScript", data["languages"])
        self.assertIn("C++", data["languages"])


if __name__ == "__main__":
    unittest.main()
