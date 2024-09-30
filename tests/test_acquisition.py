import unittest
from unittest.mock import patch, MagicMock
from utils.Acquisition import Acquisition
import requests


class TestAcquisition(unittest.TestCase):

    @patch('utils.StatusService')
    @patch('utils.RawService')
    def test_insert_status(self, mock_raw_service, mock_status_service):
        # Setup mock
        mock_status_service.return_value.save.return_value = [{'id': 1}]
        
        # Test insert_status method
        status_id = Acquisition.insert_status('Raw', '2024-09-29', '2024-09-30')
        self.assertEqual(status_id, 1)
        mock_status_service.return_value.save.assert_called_once()

    @patch('utils.StatusService')
    def test_update_status(self, mock_status_service):
        # Setup mock
        mock_status_service.return_value.find_by_id.return_value = [{'status': 0}]
        
        # Test update_status method
        Acquisition.update_status(1, 1)
        mock_status_service.return_value.update.assert_called_once()

    @patch('requests.get')
    def test_fetch_leave_data(self, mock_requests_get):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {'data': [], 'meta': {'total': 0, 'size': 10000}}
        mock_requests_get.return_value = mock_response
        
        # Test fetch_leave_data method
        data = Acquisition.fetch_leave_data('2024-09-01', '2024-09-30', 1)
        self.assertEqual(data['meta']['total'], 0)
        mock_requests_get.assert_called_once_with(
            Acquisition.Configuration.LEAVE_API_URL,
            headers={'Authorization': Acquisition.Configuration.LEAVE_API_HEADER},
            params={
                'fetchType': 'all',
                'startDate': '2024-09-01',
                'endDate': '2024-09-30',
                'size': 10000,
                'roleType': 'issuer',
                'page': 1
            }
        )

    @patch('utils.Acquisition.process_leave_data')
    @patch('utils.Acquisition.fetch_leave_data')
    def test_fetch_and_process_data(self, mock_fetch_leave_data, mock_process_leave_data):
        # Setup mocks
        mock_fetch_leave_data.return_value = {'data': [], 'meta': {'total': 0, 'size': 10000}}
        
        # Test fetch_and_process_data method
        Acquisition.fetch_and_process_data('2024-09-01', '2024-09-30', 1, 1)
        mock_process_leave_data.assert_called_once_with([], Acquisition.Raw, Acquisition.aquisition_service)

    @patch('utils.Acquisition.fetch_and_process_data')
    @patch('utils.Acquisition.create_date_ranges')
    def test_fetch_all_leave_data(self, mock_create_date_ranges, mock_fetch_and_process_data):
        # Setup mocks
        mock_create_date_ranges.return_value = [('2024-09-01', '2024-09-30')]
        
        # Test fetch_all_leave_data method
        Acquisition.fetch_all_leave_data('2024-09-01', '2024-09-30')
        mock_fetch_and_process_data.assert_called_once_with('2024-09-01', '2024-09-30', 1, mock.ANY)

    @patch('utils.Acquisition.fetch_and_process_etl')
    @patch('utils.Acquisition.insert_status')
    @patch('utils.Acquisition.get_data_count')
    def test_initiate_etl(self, mock_get_data_count, mock_insert_status, mock_fetch_and_process_etl):
        # Setup mock for data count and status insertion
        mock_get_data_count.return_value = [{'total_count': 10000}]
        mock_insert_status.return_value = 1
        
        # Test initiate_etl method
        Acquisition.initiate_etl('user', '2024-09-01')
        mock_insert_status.assert_called_once_with('user', '2024-09-01')
        self.assertEqual(mock_fetch_and_process_etl.call_count, 1)  # Only one call for 10000 records


if __name__ == '__main__':
    unittest.main()
