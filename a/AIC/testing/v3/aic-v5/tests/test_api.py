import unittest
from app import app

class TestFlaskAPI(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_index_route(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)

    def test_score_api_missing_entity(self):
        res = self.client.post("/api/score", json={})
        self.assertEqual(res.status_code, 400)

if __name__ == "__main__":
    unittest.main()