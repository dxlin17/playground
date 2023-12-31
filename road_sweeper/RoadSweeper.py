import calendar
import datetime
from util.CalendarEvent import CalendarEventBuilder
from util.GoogleCalendarUtils import GoogleCalendarUtils

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def main():
    """Create a calendar, then create events for each first and third Friday of the month.

    Returns: None

    """
    scopes = ["https://www.googleapis.com/auth/calendar"]

    gcp = GoogleCalendarUtils(scopes)
    calendar_id = ""
    events = gcp.get_events_list(calendar_id)
    for event in events:
        start_date = datetime.datetime.strptime(event["start"]["date"], '%Y-%m-%d')
        start_time = datetime.time(10, 30)
        start_datetime = datetime.datetime.combine(start_date, start_time)
        end_datetime = start_datetime + datetime.timedelta(hours=1)

        update = {
            "start": CalendarEventBuilder.make_datetime_dict(start_datetime),
            "end": CalendarEventBuilder.make_datetime_dict(end_datetime),
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {
                        "method": "popup",
                        "minutes": 16 * 60 + 30
                    }
                ]
            }
        }

        gcp.update_event(calendar_id, event, update)


def get_first_dow_for_month(year, month, day_of_week):
    cal = calendar.Calendar()
    dows = sorted([day for day in cal.itermonthdays4(year, month) if day[-1] == day_of_week and day[1] == month])
    return dows[0]


if __name__ == "__main__":
    main()
