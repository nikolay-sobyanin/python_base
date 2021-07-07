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
# TODO При добавлении новых данных в базу попробуйте использовать метод get_or_create
# TODO Он либо создаст новую запись, либо укажет на то, что запись уже существует
# TODO По возвращенному айди можно будет обновить старую запись, вместо создания новой.
# TODO Обратите внимание на описание этого метода и на то, что он возвращает при использовании
# http://docs.peewee-orm.com/en/latest/peewee/api.html#Model.get_or_create
# TODO Returns:
#  Tuple of Model instance and boolean indicating if a new object was created.
# TODO Т.е. возвращается кортеж с ID элемента, который был найден или был создан
# TODO И возвращается True/False объект, который говорит о том, был ли объект создан
# TODO Если объект не был создан - его хорошо было бы обновить по вернувшемуся ID
# TODO Принцип примерно следующий:
# for data in data_to_save:
# TODO Сперва получаем данные из get_or_create по одному из полей(в данном случае по дате)
#     weather, created = Weather.get_or_create(
#         date=data['date'],
# TODO В defaults указываются остальные данные, которые будут использованы при создании записи
#         defaults={'temperature': data['temperature'], 'pressure': data['pressure'],
#                   'conditions': data['conditions'], 'wind': data['wind']})
#     if not created:
# TODO Если запись не создана - обновляем её
#         query = Weather.update(temperature=data['temperature'], pressure=data['pressure'],
#                                conditions=data['conditions'], wind=data['wind']).where(Weather.id == weather.id)
#         query.execute()

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
