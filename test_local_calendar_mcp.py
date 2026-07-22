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
import json
import requests
from datetime import datetime, timedelta, timezone

from local_calendar_mcp import list_events

class TestListEvents(unittest.TestCase):
    @patch('local_calendar_mcp.get_auth_headers')
    @patch('local_calendar_mcp.requests.get')
    def test_list_events_success(self, mock_get, mock_get_auth_headers):
        mock_get_auth_headers.return_value = {"Authorization": "Bearer fake_token"}

        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "items": [
                {
                    "summary": "Meeting",
                    "start": {"dateTime": "2026-06-16T10:00:00Z"},
                    "end": {"dateTime": "2026-06-16T11:00:00Z"},
                    "description": "Discuss stuff",
                    "location": "Room 1"
                },
                {
                    "summary": "All Day Event",
                    "start": {"date": "2026-06-17"},
                    "end": {"date": "2026-06-18"}
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
        result_str = list_events(calendar_id="test_calendar", start_time="2026-06-16T00:00:00Z", end_time="2026-06-17T00:00:00Z", max_results=5)
        result = json.loads(result_str)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["summary"], "Meeting")
        self.assertEqual(result[0]["start"], "2026-06-16T10:00:00Z")
        self.assertEqual(result[1]["summary"], "All Day Event")
        self.assertEqual(result[1]["start"], "2026-06-17")
        self.assertEqual(result[1]["description"], "")

        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertEqual(args[0], "https://www.googleapis.com/calendar/v3/calendars/test_calendar/events")
        self.assertEqual(kwargs["params"]["timeMin"], "2026-06-16T00:00:00Z")
        self.assertEqual(kwargs["params"]["timeMax"], "2026-06-17T00:00:00Z")
        self.assertEqual(kwargs["params"]["maxResults"], 5)

    @patch('local_calendar_mcp.get_auth_headers')
    @patch('local_calendar_mcp.requests.get')
    def test_list_events_default_times(self, mock_get, mock_get_auth_headers):
        mock_get_auth_headers.return_value = {"Authorization": "Bearer fake_token"}

        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"items": []}
        mock_get.return_value = mock_response

        # We need to freeze time to reliably test the default parameters if we want to be exact,
        # but we can also just check that they look like ISO strings that end with Z.
        result_str = list_events()
        self.assertEqual(result_str, "[]")

        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args

        timeMin = kwargs["params"]["timeMin"]
        timeMax = kwargs["params"]["timeMax"]

        self.assertTrue(timeMin.endswith("Z"))
        self.assertTrue(timeMax.endswith("Z"))

        # Verify it defaults to primary
        self.assertEqual(args[0], "https://www.googleapis.com/calendar/v3/calendars/primary/events")

    @patch('local_calendar_mcp.get_auth_headers')
    @patch('local_calendar_mcp.requests.get')
    def test_list_events_api_error(self, mock_get, mock_get_auth_headers):
        mock_get_auth_headers.return_value = {"Authorization": "Bearer fake_token"}

        # We can either make mock_get raise directly or have raise_for_status raise
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error")
        mock_get.return_value = mock_response

        result_str = list_events()
        self.assertTrue(result_str.startswith("Error listing events:"))
        self.assertIn("404 Client Error", result_str)

if __name__ == '__main__':
    unittest.main()
