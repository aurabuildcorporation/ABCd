import unittest
from workers.trend_tracker import compute_trend
from workers.anomaly_detector import detect_anomalies
from workers.forecast_worker import forecast

class TestWorkers(unittest.TestCase):

    def test_trend_none(self):
        result = compute_trend("nonexistent-entity")
        self.assertIsNone(result)

    def test_anomaly_none(self):
        result = detect_anomalies("nonexistent-entity")
        self.assertIsNone(result)

    def test_forecast_none(self):
        result = forecast("nonexistent-entity")
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()