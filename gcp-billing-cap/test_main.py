import unittest
from unittest.mock import patch, MagicMock
import base64
import json

# Import the module to be tested
import main

class TestBillingCap(unittest.TestCase):
    @patch('main.PROJECT_ID', None)
    @patch('main.disable_billing')
    def test_missing_project_id(self, mock_disable_billing):
        # Create a mock event with cost exceeding budget
        data = json.dumps({"costAmount": 150.0, "budgetAmount": 100.0})
        event = {'data': base64.b64encode(data.encode('utf-8')).decode('utf-8')}

        # We need to temporarily set main.PROJECT_ID to None to simulate missing env var
        # Note: patch decorator handles this

        main.cap_billing(event, None)

        # disable_billing should not be called because PROJECT_ID is missing
        mock_disable_billing.assert_not_called()

    @patch('main.PROJECT_ID', 'test-project')
    @patch('main.disable_billing')
    def test_with_project_id(self, mock_disable_billing):
        data = json.dumps({"costAmount": 150.0, "budgetAmount": 100.0})
        event = {'data': base64.b64encode(data.encode('utf-8')).decode('utf-8')}

        main.cap_billing(event, None)

        mock_disable_billing.assert_called_once_with('test-project')

if __name__ == '__main__':
    unittest.main()
