from dataclasses import asdict
import os.path
from typing import List, Dict

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleCalendarUtils(object):
    def __init__(self, scopes):
        self.scopes = scopes
        self.creds = self.refresh_gcp_creds()

    def refresh_gcp_creds(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", self.scopes)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", self.scopes
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        return creds

    def create_events(self, calendar_id: str, events: List) -> None:
        """Insert events into the specified calendar

        Args:
            calendar_id:
            events:

        Returns:

        """
        try:
            service = build("calendar", "v3", credentials=self.creds)

            for event in events:
                (
                    service.events()
                    .insert(calendarId=calendar_id, body=asdict(event))
                    .execute()
                )

        except HttpError as error:
            print(f"An error occurred: {error}")

    def get_events_list(self, calendar_id: str) -> List:
        try:
            service = build("calendar", "v3", credentials=self.creds)

            events_result = (
                service.events()
                .list(calendarId=calendar_id)
                .execute()
            )
            
            return events_result['items']
        except HttpError as error:
            print(f"An error occurred: {error}")

    def update_event(self, calendar_id: str, event: Dict, update_dict: Dict) -> None:
        try:
            service = build("calendar", "v3", credentials=self.creds)

            for key, value in update_dict.items():
                print(f"Updating: {key}, {value}")
                event[key] = value

            (
                service.events()
                .update(calendarId=calendar_id, eventId=event["id"], body=event)
                .execute()
            )
        except HttpError as error:
            print(f"An error occurred: {error}")

    def create_calendar(self, calendar_name):
        pass

    def list_calendars(self):
        try:
            service = build("calendar", "v3", credentials=self.creds)

            events_result = (
                service.calendarList()
                .list()
                .execute()
            )

            return events_result['items']
        except HttpError as error:
            print(f"An error occurred: {error}")
