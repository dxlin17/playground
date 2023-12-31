from dataclasses import dataclass
import datetime


@dataclass
class CalendarEvent:
    start: dict
    end: dict
    summary: str

    description: str
    reminders: dict

    def __repr__(self):
        return f"{self.start}"


class CalendarEventBuilder:
    """Builder class for the CalendarEvent dataclass object.

    Attributes:
        description:
        summary:
        reminders:
        start_date:
        end_date:
    """
    def __init__(self):
        self.description = ""
        self.summary = None
        self.reminders = {
            'useDefault': True
        }
        self.start_date = None
        self.end_date = None

    def with_start_date(self, start_date):
        self.start_date = CalendarEventBuilder.make_datetime_dict(start_date)
        self.end_date = start_date + datetime.timedelta(hours=1)
        return self

    def with_end_date(self, end_date):
        self.end_date = CalendarEventBuilder.make_datetime_dict(end_date)
        return self

    def with_reminders(self, use_default: bool, overrides: list):
        self.reminders = {
            "useDefault": use_default,
            "overrides": overrides
        }
        return self

    def with_summary(self, summary):
        self.summary = summary
        return self

    def with_description(self, description):
        self.description = description
        return self

    @staticmethod
    def make_datetime_dict(datetime_obj, timezone="America/Los_Angeles"):
        return {
            "dateTime": datetime.datetime.strftime(datetime_obj.astimezone(), "%Y-%m-%dT%H:%M:%S%z"),
            "timeZone": timezone
        }

    def build(self):
        return CalendarEvent(self.start_date, self.end_date, self.summary, self.description, self.reminders)


if __name__ == '__main__':
    event_builder = CalendarEventBuilder()
    date = datetime.date(2023, 10, 13)

    event = event_builder.with_start_date(date).build()
    print(event)
