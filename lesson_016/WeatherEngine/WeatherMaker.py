import requests
from bs4 import BeautifulSoup
import datetime


class ParserWeather:

    DATA_PARSE = {
        'day': {'tag': 'div', 'css_class': 'forecast-briefly__day'},
        'weather': {'tag': 'div', 'css_class': 'forecast-briefly__condition'},
        'temperature': {'tag': 'span', 'css_class': 'temp__value temp__value_with-unit'},
        'date': {'tag': 'time', 'css_class': 'time forecast-briefly__date'},
    }

    URL_WEATHER = 'https://yandex.ru/pogoda/213?utm_source=serp&utm_campaign=wizard&utm_medium=desktop' \
                  '&utm_content=wizard_desktop_main&utm_term=title '

    def __init__(self):
        self.resource_weather = self.URL_WEATHER

    def parse_weather_forecast(self):
        response = requests.get(self.resource_weather)
        if response.status_code == 200:
            list_weather = []
            list_days = self.parse_days(html_text=response.text)
            for day in list_days:
                day_weather = self.parse_weather_day(day)
                if day_weather['date'] >= datetime.date.today():
                    list_weather.append(day_weather)
                else:
                    continue
            return list_weather
        else:
            print('Error get html data!')

    def parse_days(self, html_text):
        html_doc = BeautifulSoup(html_text, features='html.parser')
        list_days = html_doc.find_all(self.DATA_PARSE['day']['tag'], self.DATA_PARSE['day']['css_class'])
        return list_days

    def parse_weather_day(self, day):
        date_str = day.find(self.DATA_PARSE['date']['tag'], self.DATA_PARSE['date']['css_class'])['datetime'][0:10]
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        weather = day.find(self.DATA_PARSE['weather']['tag'], self.DATA_PARSE['weather']['css_class']).text
        temperature = day.find(self.DATA_PARSE['temperature']['tag'], self.DATA_PARSE['temperature']['css_class']).text
        return {'date': date, 'weather': weather, 'temperature': temperature}


class WeatherMarker:

    def __init__(self):
        self.parser = ParserWeather()
        self.list_weather = None

    def get_weather_forecast(self):
        list_weather = self.parser.parse_weather_forecast()
        self.list_weather = sorted(list_weather, key=lambda x: x['date'], reverse=False)

    def get_period(self):
        start_date = self.list_weather[0]['date']
        finish_date = self.list_weather[-1]['date']
        return start_date, finish_date

    def get_index(self, date):
        for i, elem in enumerate(self.list_weather):
            if elem['date'] == date:
                index = i
                break
        return index

    def get_weather_forecast_period(self, start_date, finish_date):
        start_index = self.get_index(start_date)
        finish_index = self.get_index(finish_date)
        return self.list_weather[start_index:finish_index + 1]












