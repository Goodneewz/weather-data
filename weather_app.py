import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("WEATHER_API_KEY")

#import traceback

#def excepthook(exc_type, exc_value, exc_tb):
#    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
#    print("Caught error:\n", tb)

#sys.excepthook = excepthook


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Weather App'
        self.city_country = QLabel(self)
        self.city_label = QLabel("Enter city name", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_country)
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_country.setAlignment(Qt.AlignCenter)
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_country.setObjectName("city_country")
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: Arial;
                font-size: 40;
            }
            QLabel#city_country{
                font-size: 45px;
                font-family: courier;
            }
            QLabel#city_label{
                font-size: 38px;
                font-family: Tahoma;
            }
            QLineEdit#city_input{
                font-size: 40px;
                font-style: italic; 
            }
            QPushButton#get_weather_button{
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#temperature_label{
                font-size: 65px;
            }
            QLineLabel#emoji_label{
                font-size: 1000px;
                font-family: "Segoe UI emoji", Arial;
            }
            QLabel#description_label{
                font-size: 35px;
                font-family
            }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        city = self.city_input.text().strip()
    
        if not city:
            self.display_error("Please enter a city name")
            return

        url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            self.display_weather(data)


#            if data["cod"] == "200":
#                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad Request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API key")
                case 403:
                    self.display_error("Forbidden:\nAccess Denied")
                case 404:
                    self.display_error("Not Found:\nCity not found")
                case 500:
                    self.display_error("Internal Server Error:\nPlease try again later")
                case 502:
                    self.display_error("Gateway Unavailable:\nInvalid response from server")
                case 503:
                    self.display_error("Service Unavailable:\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from server")
                case _:
                    self.display_error(f"HTTP Error occurred:\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("TooManyRedirects:\nPlease check the URL")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")

    def display_error(self, message):
#        print(f"DEBUG APP FEEDBACK: {message}")
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 75px;")
        temperature_f = data["current"]["temp_f"]
        temperature_c = data["current"]["temp_c"]
#        temperature_f = (temperature_k * 9 / 5) - 459.67
        weather_id = data["current"]["condition"]["code"]
        weather_description = data["current"]["condition"]["text"]
        city_region = data["location"]["region"]
        city_country = data["location"]["country"]
        print(data)
        print(weather_id)
        print(weather_description)

        self.city_country.setText(city_country)
        self.city_label.setText(city_region)
        self.temperature_label.setText(f"{temperature_c:.0f}°C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(f"{weather_description}")

    @staticmethod
    def get_weather_emoji(weather_id):

        if weather_id == 1273 or weather_id == 1276 or weather_id == 1279 or weather_id == 1282:
            return "⛈️"
        elif 1063 <= weather_id <= 1083:
            return "🌦️"
        elif 1186 <= weather_id <= 1201 or 1243 <= weather_id <= 1246:
            return "🌧️"
        elif 1114 <= weather_id <= 1117 or 1210 <= weather_id <= 1225 or 1255 <= weather_id <= 1258:
            return "❄️"
        elif weather_id == 1030:  # Mist or Fog
            return "🌫️"
        elif weather_id == 1000:  # Sunny / Clear
            return "☀️"
        elif 1003 <= weather_id <= 1009:  # Cloudy ranges
            return "☁️"
        else:
            return "🌤️"

if  __name__ == '__main__':
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
