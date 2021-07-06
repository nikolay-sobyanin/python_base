# Ссылка для получения погоды:

# https://yandex.ru/pogoda/213?utm_source=serp&utm_campaign=wizard&utm_medium=desktop&utm_content=wizard_desktop_main&utm_term=title

import requests
from bs4 import BeautifulSoup
import peewee
import datetime

resource_weather = 'https://yandex.ru/pogoda/213?utm_source=serp&utm_campaign=wizard&utm_medium=desktop&utm_content=wizard_desktop_main&utm_term=title'
response = requests.get(resource_weather)

database = peewee.SqliteDatabase('weather.db')


class BaseTable(peewee.Model):
    class Meta:
        database = database


class Weather(BaseTable):
    weather = peewee.CharField()
    temperature = peewee.CharField()
    date = peewee.DateTimeField()


database.create_tables([Weather])

if response.status_code == 200:
    html_doc = BeautifulSoup(response.text, features='html.parser')
    list_days = html_doc.find_all('div', {'class': 'forecast-briefly__day'})

    for day in list_days:
        weather = day.find('div', {'class': 'forecast-briefly__condition'}).text
        temperature = day.find('span', {'class': 'temp__value temp__value_with-unit'}).text
        date = day.find('time', {'class': 'time forecast-briefly__date'})['datetime'][0:10]
        Weather.create(
            weather=weather,
            temperature=temperature,
            date=datetime.date(int(date[0:4]), int(date[5:7]), int(date[8:10])),
        )
else:
    print('Error get html data!')
