import unittest
import json
from flask import Flask
from flask_testing import TestCase

# Import the Flask app and blueprints from the main file
from main import app
from controller import AquisitionController, FileController, EtlController, VisualizeController


class FlaskAppTest(TestCase):
    def create_app(self):
        # Set up the Flask app for testing with blueprints registered
        app.config['TESTING'] = True
        app.register_blueprint(AquisitionController.aquisition)
        app.register_blueprint(FileController.file_blueprint)
        app.register_blueprint(EtlController.etl)
        app.register_blueprint(VisualizeController.viz)
        return app

    # Test the health check route
    def test_health_check(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'configuration', response.data.lower())

    # Test the home route
    def test_home_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Api Access', response.data)

    # Test the POST /api/v1/etl/load route with missing data
    def test_etl_load_invalid_input(self):
        response = self.client.post('/api/v1/etl/load', data={})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid Input', response.data)

    # Test the /api/v1/acquire/insert route
    def test_acquisition_insert(self):
        response = self.client.post('/api/v1/acquire/insert', data={"start_date": "2024-03-01", "end_date": "2024-03-02"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Insert operation started', response.data)

    # Test the /api/v1/viz/sample/download route with valid parameters
    def test_download_valid_plot_type(self):
        response = self.client.get('/api/v1/viz/sample/download/department')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'image/png')

    # Test the /api/v1/viz/sample/download route with an invalid plot type
    def test_download_invalid_plot_type(self):
        response = self.client.get('/api/v1/viz/sample/download/invalid')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid plot type', response.data)

    # Test the sample page GET route
    def test_sample_get(self):
        response = self.client.get('/sample?startdate=2024-03-01&enddate=2024-08-12')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'sample', response.data)

    # Test the sample page POST route with invalid date format
    def test_sample_post_invalid_date(self):
        response = self.client.post('/sample', data={"startdate": "2024-13-01", "todate": "2024-08-12"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid date format', response.data)

    # Test the swagger route
    def test_swagger_route(self):
        response = self.client.get('/swagger')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'swagger', response.data.lower())


if __name__ == '__main__':
    unittest.main()
