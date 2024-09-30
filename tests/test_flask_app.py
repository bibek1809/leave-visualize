import unittest
import logging
from app import app
from utils import Configuration

# Disable logging from external libraries
logging.getLogger("JdbcDatabase").setLevel(logging.WARNING)  # or logging.ERROR

class FlaskAppTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        cls.app.testing = True
        cls.valid_passcode = Configuration.LIMITER_CODE

    def test_health_check(self):
        response = self.app.get('/health', headers={"X-Custom-Passcode": self.valid_passcode})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"database": True})

    def test_etl_load_valid(self):
        response = self.app.post('/api/v1/etl/load', headers={"X-Custom-Passcode": self.valid_passcode})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Insert operation started for", response.json["message"])
        self.assertIn("Table initiated as", response.json["message"])

    def test_acquisition_insert_valid(self):
        response = self.app.post('/api/v1/acquire/insert', json={"data": "sample"}, headers={"X-Custom-Passcode": self.valid_passcode})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Insert operation started for", response.json["message"])
        self.assertIn("to", response.json["message"])



if __name__ == '__main__':
    unittest.main(verbosity=1)  # Show only test results
