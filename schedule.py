from __future__ import print_function
from httplib2 import Http
import os

from apiclient.discovery import build
from oauth2client import client, tools, file

from datetime import datetime

try:
  import argparse
  flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
  flags = None

# -------- LOGGER SETTING --------
from logging import getLogger, StreamHandler, Formatter, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
handler.setFormatter(Formatter(' %(levelname)s - %(asctime)s --> %(module)s: %(message)s'))
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False
# -------- LOGGER SETTING END --------


class Schedule:
  """docstring for Schedule"""
  __SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
  __CLIENT_SECRET_FILE = 'client_secret.json'
  __APPLICATION_NAME = 'Google Calendar API Python Quickstart'
  __CALENDAR_ID = 'primary'

  __RESULT_NUM = 7

  def __init__(self):
    """ コンストラクタ """

  def set_result_num(self, num):
    self.__RESULT_NUM = num


  def __credentials(self):
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
      os.makedirs(credential_dir)

    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')
    store = file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
      flow = client.flow_from_clientsecrets(self.__CLIENT_SECRET_FILE, self.__SCOPES)
      flow.user_agent = self.__APPLICATION_NAME

      if flags:
          credentials = tools.run_flow(flow, store, flags)
      else: # Needed only for compatibility with Python 2.6
          credentials = tools.run(flow, store)
      logger.debug('Storing credentials to ' + credential_path)

    return credentials


  def get(self):
    results = {}
    try:
      logger.debug('Getting the upcoming {} events'.format(self.__RESULT_NUM))
      credentials = self.__credentials()
      http = credentials.authorize(Http())
      service = build('calendar', 'v3', http=http)
      now = datetime.utcnow().isoformat() + 'Z'
      eventsResult = service.events().list(
        calendarId=self.__CALENDAR_ID,
        timeMin=now,
        maxResults=self.__RESULT_NUM,
        singleEvents=True,
        orderBy='startTime'
      ).execute()
      events = eventsResult.get('items', [])

      if not events:
        logger.debug('No upcoming events found.')
        return {}

      for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        # logger.debug(start, event['summary'])
        results[start] = event['summary']

    except:
      # logger.debug(events)
      return {}

    return results


def main():
  calendar = GoogleCalendar()
  result = calendar.get()

  logger.debug(result)

  path = os.path.dirname(os.path.abspath(__file__))
  f = open(path + '/results.json', 'w')
  f.write(str(result))


if __name__ == '__main__':
  main()
