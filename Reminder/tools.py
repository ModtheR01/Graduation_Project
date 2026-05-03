from datetime import datetime,timedelta
import pytz
from flights.state_store import get_store
from langchain_core.tools import tool
import requests
from Users.models import User
from sending_emails.models import Tokens


GOOGLE_CALENDAR_URL = "https://www.googleapis.com/calendar/v3/calendars/primary/events"

@tool
def get_current_datetime():
    """
    use this tool whenever you want to get the current date and time of today you can use it when asked to put a reiminder or book a flieght or whenever the user needs to know todays date 
    you can also use this tool to be aware of the current date and time
    """
    tz = pytz.timezone("Africa/Cairo")
    return datetime.now(tz)

def create_calendar_event_tool( title: str, start_time_iso: str):
    """
    Create a Google Calendar event with a reminder.

    Args:
        user: Django user (must have access_token & refresh_token saved)
        title (str): event title
        start_time_iso (str): ISO datetime string (e.g. 2026-05-04T18:00:00)

    Returns:
        dict: event data or error
    """

    # 🔹 1. هات التوكنز من الداتا بيز (عدل حسب موديلك)
    store = get_store()
    user = store.get("user_id")
    user_obj = User.objects.get(pk=user)
    access_token = Tokens.objects.get(user_email=user_obj).access_token

    # 🔹 2. حول الوقت
    start_time = start_time_iso

    dt = datetime.fromisoformat(start_time)
    end_dt = dt + timedelta(minutes=30)

    # 🔹 3. body بتاع Google
    event = {
        "summary": title,
        "start": {
            "dateTime": dt.isoformat(),
            "timeZone": "Africa/Cairo",
        },
        "end": {
            "dateTime": end_dt.isoformat(),
            "timeZone": "Africa/Cairo",
        },
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "popup", "minutes": 45}
            ]
        }
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # 🔹 4. حاول تبعت
    response = requests.post(GOOGLE_CALENDAR_URL, json=event, headers=headers)

    # 🔹 5. النتيجة
    if response.status_code not in [200, 201]:
        return {
            "error": "Failed to create event",
            "details": response.text
        }

    data = response.json()

    return {
        "success": True,
        "event_id": data.get("id"),
        "link": data.get("htmlLink")
    }
