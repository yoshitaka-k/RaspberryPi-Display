from websocket_server import WebsocketServer
import json

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


def new_client(client, server):
  message = 'New client {}:{} has joined.'.format(client['address'][0], client['address'][1])
  logger.debug(message)
  # server.send_message(client, json.dumps(message))


def client_left(client, server):
  message = 'Client {}:{} has left.'.format(client['address'][0], client['address'][1])
  logger.debug(message)
  # server.send_message(client, json.dumps(message))


def message_received(client, server, message):
  logger.debug('Message "{}" has been received from {}:{}'.format(message, client['address'][0], client['address'][1]))
  server.send_message(client, message)


def message_received_all(client, server, message):
  logger.debug('Message "{}" has been received from all'.format(message))
  server.send_message_to_all(message)


def main():
  server = WebsocketServer(port=8090, host='localhost')
  server.set_fn_new_client(new_client)
  server.set_fn_client_left(client_left)
  # server.set_fn_message_received(message_received)
  server.set_fn_message_received(message_received_all)
  server.run_forever()

if __name__ == '__main__':
  main()