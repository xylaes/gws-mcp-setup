import unittest
from unittest.mock import patch, MagicMock
import requests
import json
import local_calendar_mcp

class TestListCalendars(unittest.TestCase):
    @patch('local_calendar_mcp.get_auth_headers')
    @patch('local_calendar_mcp.requests.get')
    def test_list_calendars_success(self, mock_get, mock_headers):
        mock_headers.return_value = {"Authorization": "Bearer fake"}

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "items": [
                {
                    "id": "cal1",
                    "summary": "Calendar 1",
                    "primary": True,
                    "accessRole": "owner"
                }
            ]
        }
        mock_get.return_value = mock_response

        result = local_calendar_mcp.list_calendars()
        calendars = json.loads(result)

        self.assertEqual(len(calendars), 1)
        self.assertEqual(calendars[0]["id"], "cal1")
        self.assertEqual(calendars[0]["primary"], True)

    @patch('local_calendar_mcp.get_auth_headers')
    @patch('local_calendar_mcp.requests.get')
    def test_list_calendars_error(self, mock_get, mock_headers):
        mock_headers.return_value = {"Authorization": "Bearer fake"}
        mock_get.side_effect = requests.exceptions.RequestException("API connection error")

        result = local_calendar_mcp.list_calendars()

        self.assertTrue(result.startswith("Error listing calendars: API connection error"))

if __name__ == '__main__':
    unittest.main()
