import sys
import requests
from PyQt5.QtWidgets import (QApplication , QWidget , QLabel ,
                             QPushButton , QLineEdit ,QVBoxLayout)
from PyQt5.QtCore import Qt

class weatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter your city :" ,self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather" , self)
        self.temperature_label = QLabel(self)
        self.emoji_Label = QLabel(self)
        self.description_Label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")   # FIXED

        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_Label)
        vbox.addWidget(self.description_Label)
        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_Label.setAlignment(Qt.AlignCenter)
        self.description_Label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")              # FIXED
        self.get_weather_button.setObjectName("get_weather_button")  # FIXED
        self.temperature_label.setObjectName("temperature_label")    # FIXED
        self.emoji_Label.setObjectName("emoji_Label")            # FIXED
        self.description_Label.setObjectName("description_Label")    # FIXED

        self.setStyleSheet("""
           QLabel , QPushButton{
                font-family: calibri;      /* FIXED */
                     }    
         QLabel#city_label{
                 font-size :40px;
                 font-style : italic;                   
                            } 
          QLineEdit#city_input{
                font-size :40px;           
                           }  
           QPushButton#get_weather_button{
                   font-size :30px;
                   font-weight : bold;            
                         }  
            QLabel#temperature_label{
                    font-size :75px;       
                           }  
            QLabel#emoji_Label{
                font-size :30px;
                font-family: Segoe UI Emoji;        
                           }               
            QLabel#description_Label{
                 font-size : 50px;            
                           }                                                          
                            """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "699432f944ae35001db0291a6326b35e"
        city = self.city_input.text()

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"  # FIXED

        try:
             response = requests.get(url)
             response.raise_for_status()
             data = response.json()   # FIXED

             if data["cod"] == 200:
                 self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
             self.display_error(f"HTTP error:\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error")

        except requests.exceptions.Timeout:
             self.display_error("Timeout Error")

        except requests.exceptions.TooManyRedirects:
             self.display_error("Too many Redirects")

        except requests.exceptions.RequestException as req_error:   # FIXED
            self.display_error(f"Request Error\n{req_error}")

    def display_weather(self,data):
        self.temperature_label.setStyleSheet("font-size : 75px;")
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]

        self.temperature_label.setText(f"{temperature_c :.0f}°C")
        self.emoji_Label.setText(self.get_weather_emoji(weather_id))   # FIXED
        self.description_Label.setText(weather_description)

    def display_error(self,message):
         self.temperature_label.setStyleSheet("font-size : 30px;")
         self.temperature_label.setText(message)
         self.emoji_Label.clear()
         self.description_Label.clear()

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"    
        elif 300 <= weather_id <= 321:
              return "🌦️" 
        elif 500 <= weather_id <= 531:
              return "🌧️" 
        elif 600 <= weather_id <= 622:
              return "❄️" 
        elif 701 <= weather_id <= 741:
              return "🌫️" 
        elif weather_id == 800:
              return "☀️"
        elif 801 <= weather_id <= 804:
              return "☁️"
        else:
            return ""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = weatherApp()     
    weather_app.show()
    sys.exit(app.exec_())
