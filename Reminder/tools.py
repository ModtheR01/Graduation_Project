from datetime import datetime
import pytz
from langchain_core.tools import tool

@tool
def get_current_datetime():
    """
    use this tool whenever you want to get the current date and time of today you can use it when asked to put a reiminder or book a flieght or whenever the user needs to know todays date 
    you can also use this tool to be aware of the current date and time
    """
    tz = pytz.timezone("Africa/Cairo")
    return datetime.now(tz)

