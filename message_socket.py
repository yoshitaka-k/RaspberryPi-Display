from websocket import create_connection
import json


class MessageSocket:
  """ Websocket 管理クラス """
  results = {}
  ws = None


  def __init__(self):
    """ コンストラクタ """
    # if self.ws is None:
    #   self.__connect()
    self.results = {}


  def __connect(self):
    """ 接続 """
    self.ws = create_connection("ws://localhost:8090")


  def __close(self):
    """ 切断 """
    if self.ws is not None:
      self.ws.close()


  def clear(self):
    """ 送信メセージ内容を初期化 """
    self.results = {}


  def add(self, key, value):
    """ 送信メセージ内容に追加 """
    self.results[key] = value


  def send(self):
    """ メッセージ送信 """
    self.__connect()
    self.ws.send(json.dumps(self.results))
    self.__close()


def main():
  socket = MessageSocket()
  socket.add('test', 'TEST')
  socket.send()

if __name__ == '__main__':
  main()
