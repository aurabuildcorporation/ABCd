import unittest
import requests
from config.settings import NODE_ENGINE_URL

class TestScoringEngine(unittest.TestCase):

    def test_score_endpoint(self):
        payload = {"entity": "Test Entity"}
        res = requests.post(f"{NODE_ENGINE_URL}/score", json=payload)
        self.assertEqual(res.status_code, 200)

        data = res.json()
        self.assertIn("score", data)
        self.assertIn("confidence", data)
        self.assertIsInstance(data["score"], float)
        self.assertIsInstance(data["confidence"], float)

if __name__ == "__main__":
    unittest.main()