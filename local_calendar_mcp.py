import google.auth
import google.auth.transport.requests
import requests
import json
import urllib.parse
from datetime import datetime, timedelta, timezone
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("Local Google Calendar MCP")

_cached_credentials = None

def get_auth_headers():
    """Retrieves fresh Google ADC authentication headers."""
    global _cached_credentials

    if _cached_credentials is None:
        _cached_credentials, project = google.auth.default()

    if not _cached_credentials.valid:
        auth_req = google.auth.transport.requests.Request()
        _cached_credentials.refresh(auth_req)

    return {
        "Authorization": f"Bearer {_cached_credentials.token}",
        "Accept": "application/json"
    }

@mcp.tool()
def list_calendars() -> str:
    """Lists all Google Calendars for the authenticated user."""
    try:
        headers = get_auth_headers()
        url = "https://www.googleapis.com/calendar/v3/users/me/calendarList"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        calendars = []
        for item in data.get("items", []):
            calendars.append({
                "id": item.get("id"),
                "summary": item.get("summary"),
                "primary": item.get("primary", False),
                "accessRole": item.get("accessRole")
            })
        return json.dumps(calendars, indent=2)
    except Exception as e:
        return f"Error listing calendars: {str(e)}"

@mcp.tool()
def list_events(calendar_id: str = "primary", start_time: str = None, end_time: str = None, max_results: int = 10) -> str:
    """Lists calendar events for a specific calendar.
    
    Args:
        calendar_id: The ID of the calendar (defaults to "primary").
        start_time: ISO format lower bound (e.g. "2026-06-16T00:00:00Z"). Defaults to start of today.
        end_time: ISO format upper bound (e.g. "2026-06-17T00:00:00Z"). Defaults to end of today.
        max_results: Maximum number of events to return (max 100).
    """
    try:
        headers = get_auth_headers()
        
        # Default time boundaries to today if not provided
        if not start_time:
            start_time = datetime.now(timezone.utc).replace(tzinfo=None).replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + "Z"
        if not end_time:
            end_time = (datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + "Z"
            
        safe_calendar_id = urllib.parse.quote(calendar_id, safe="")
        url = f"https://www.googleapis.com/calendar/v3/calendars/{safe_calendar_id}/events"
        params = {
            "timeMin": start_time,
            "timeMax": end_time,
            "maxResults": max_results,
            "singleEvents": "true",
            "orderBy": "startTime"
        }
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        events = []
        for item in data.get("items", []):
            events.append({
                "summary": item.get("summary"),
                "start": item.get("start", {}).get("dateTime") or item.get("start", {}).get("date"),
                "end": item.get("end", {}).get("dateTime") or item.get("end", {}).get("date"),
                "description": item.get("description", ""),
                "location": item.get("location", "")
            })
        return json.dumps(events, indent=2)
    except Exception as e:
        return f"Error listing events: {str(e)}"

if __name__ == "__main__":
    mcp.run()
