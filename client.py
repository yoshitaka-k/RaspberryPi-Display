from message_socket import MessageSocket
import json

from weather import Weather
from schedule import Schedule

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


def get_weather():
  weather = Weather()
  return weather.get()


def get_calendar():
  schedule = Schedule()
  schedule.set_result_num(3)
  return schedule.get()


def main():
  socket = MessageSocket()
  socket.add('weather', get_weather())
  socket.add('schedule', get_calendar())
  socket.send()

if __name__ == '__main__':
  main()
