from datetime import datetime
import requests
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


class Weather:
  """ 天気予報取得の管理クラス """
  TOKYO_ID = "1850147"
  TOKYO_LAT = "35.689499"
  TOKYO_LON = "139.691711"

  ICON_URL = "http://openweathermap.org/img/w/{}.png"

  def __init__(self):
    """コンストラクタ"""
    now = datetime.now().strftime('%s')
    date = datetime.fromtimestamp(int(now))
    print("{0} => {1}".format(now, date))


  def get(self):
    owm = self.__openweathermap()
    results = {}
    results["dt"] = owm["dt"]
    results["dt_text"] = str(datetime.fromtimestamp(int(owm["dt"])))
    results["icon"] = owm["weather"][0]["icon"]
    results["icon_url"] = self.ICON_URL.format(owm["weather"][0]["icon"])
    results["weather_id"] = owm["weather"][0]["id"]
    results["weather_text"] = self.__openweathermap_weather_code(owm["weather"][0]["id"])
    results["weather"] = owm["weather"][0]["main"]
    results["weather_jpn"] = self.__openweathermap_weather(owm["weather"][0]["main"])
    results["temp"] = owm["main"]["temp"]
    results["temp_min"] = owm["main"]["temp_min"]
    results["temp_max"] = owm["main"]["temp_max"]
    results["humidity"] = owm["main"]["humidity"]
    results["wind_speed"] = owm["wind"]["speed"]
    results["wind_deg"] = self.__set_wind_dig_jpn(owm["wind"]["deg"])
    results["clouds"] = owm["clouds"]["all"]
    results["sunrise"] = owm["sys"]["sunrise"]
    results["sunrise_text"] = str(datetime.fromtimestamp(int(owm["sys"]["sunrise"])))
    results["sunset"] = owm["sys"]["sunset"]
    results["sunset_text"] = str(datetime.fromtimestamp(int(owm["sys"]["sunset"])))
    return results

  def get_openweathermap(self):
    """ 天気情報を取得する """
    return self.__openweathermap()


  def __openweathermap(self):
    """ OpenWeatherMapAPIからの情報を取得する """
    APIKEY = ""
    URL = "https://api.openweathermap.org/data/2.5/weather"
    r = requests.post(URL + "?id={0}&APPID={1}&units=metric".format(self.TOKYO_ID, APIKEY))
    return r.json()


  def __set_wind_dig_jpn(self, dig):
    if dig < 22.5:
      dig += 360

    if dig >= 337.5 and 382.5 <= dig:
      return '北'
    if dig >= 22.5 and 67.5 <= dig:
      return '北東'
    elif dig >= 67.5 and 112.5 <= dig:
      return '東'
    elif dig >= 112.5 and 157.5 <= dig:
      return '南東'
    elif dig >= 157.5 and 202.5 <= dig:
      return '南'
    elif dig >= 202.5 and 247.5 <= dig:
      return '南西'
    elif dig >= 247.5 and 292.5:
      return '西'
    elif dig >= 292.5 and 337.5:
      return '北西'


  def __openweathermap_weather(self, weather):
    japanese = {
      'Clear': '晴れ',
      'Clouds': 'くもり',
      'Rain': '雨',
      'Snow': '雪',
      'Dust': '砂',
    }
    return japanese[weather]

  def __openweathermap_weather_code(self, weather_id):
    codes = {
      200: '小雨と雷雨',
      201: '雨と雷雨',
      202: '大雨と雷雨',
      210: '光雷雨',
      211: '雷雨',
      212: '重い雷雨',
      221: 'ぼろぼろの雷雨',
      230: '小雨と雷雨',
      231: '霧雨と雷雨',
      232: '濃い霧雨と雷雨',
      300: '軽い霧',
      301: '霧雨',
      302: '重い強度霧雨',
      310: '光強度霧雨の雨',
      311: '霧雨の雨',
      312: '重い強度霧雨の雨',
      313: 'にわかの雨と霧雨',
      314: '重いにわかの雨と霧雨',
      321: 'にわか霧雨',
      500: '少量の雨',
      501: '適度な雨',
      502: '重い強度の雨',
      503: '非常に激しい雨',
      504: '極端な雨',
      511: '雨氷',
      520: '光強度のにわかの雨',
      521: 'にわかの雨',
      522: '重い強度にわかの雨',
      531: '不規則なにわかの雨',
      600: '小雪',
      601: '雪',
      602: '大雪',
      611: 'みぞれ',
      612: 'にわかみぞれ',
      615: '光雨と雪',
      616: '雨や雪',
      620: '光のにわか雪',
      621: 'にわか雪',
      622: '重いにわか雪',
      701: 'ミスト',
      711: '煙',
      721: 'ヘイズ',
      731: '砂、ほこり旋回する',
      741: '霧',
      751: '砂',
      761: 'ほこり',
      762: '火山灰',
      771: 'スコール',
      781: '竜巻',
      800: '晴天',
      801: '薄い雲',
      802: '雲',
      803: '曇りがち',
      804: '厚い;',
      900: '竜巻',
      901: '熱帯低気圧',
      902: 'ハリケーン',
      903: 'コールド',
      904: 'ホット',
      905: '風が強い',
      906: '雹',
      951: '落ち着いた',
      952: 'そよ風',
      953: 'そよ風',
      954: '中風',
      955: '新鮮な風',
      956: '強い風',
      957: '高風、近くの暴風',
      958: 'ガール',
      959: '深刻な暴風',
      960: '嵐',
      961: '暴風雨',
      962: 'ハリケーン',
    }
    return codes[weather_id]


if __name__ == '__main__':
  weather = Weather()
  owm = weather.get_openweathermap()
  logger.debug(owm)
  print("openWeatherMap")
  print("時間 : {}".format(owm["dt"]))
  print("時間 : {}".format(datetime.fromtimestamp(int(owm["dt"]))))
  print("天気ID : {}".format(owm["weather"][0]["id"]))
  print("天気 : {}".format(owm["weather"][0]["main"]))
  print("気温 : {}".format(owm["main"]["temp"]))
  print("最低気温 : {}".format(owm["main"]["temp_min"]))
  print("最高気温 : {}".format(owm["main"]["temp_max"]))
  print("湿度 : {}%".format(owm["main"]["humidity"]))
  print("風向き : {}".format(owm["wind"]["deg"]))
  print("風速 : {}m/s".format(owm["wind"]["speed"]))
  print("曇り : {}%".format(owm["clouds"]["all"]))
  print("日の出：{}".format(datetime.fromtimestamp(int(owm["sys"]["sunrise"]))))
  print("日の入：{}".format(datetime.fromtimestamp(int(owm["sys"]["sunset"]))))
