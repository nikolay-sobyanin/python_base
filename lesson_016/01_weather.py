# -*- coding: utf-8 -*-

# В очередной спешке, проверив приложение с прогнозом погоды, вы выбежали
# навстречу ревью вашего кода, которое ожидало вас в офисе.
# И тут же день стал хуже - вместо обещанной облачности вас встретил ливень.

# Вы промокли, настроение было испорчено, и на ревью вы уже пришли не в духе.
# В итоге такого сокрушительного дня вы решили написать свою программу для прогноза погоды
# из источника, которому вы доверяете.

# Для этого вам нужно:

# Создать модуль-движок с классом WeatherMaker, необходимым для получения и формирования предсказаний.
# В нём должен быть метод, получающий прогноз с выбранного вами сайта (парсинг + re) за некоторый диапазон дат,
# а затем, получив данные, сформировать их в словарь {погода: Облачная, температура: 10, дата:datetime...}

# Добавить класс ImageMaker.
# Снабдить его методом рисования открытки
# (использовать OpenCV, в качестве заготовки брать lesson_016/python_snippets/external_data/base.jpg):
#   С текстом, состоящим из полученных данных (пригодится cv2.putText)
#   С изображением, соответствующим типу погоды
# (хранятся в lesson_016/python_snippets/external_data/weather_img ,но можно нарисовать/добавить свои)
#   В качестве фона добавить градиент цвета, отражающего тип погоды
# Солнечно - от желтого к белому
# Дождь - от синего к белому
# Снег - от голубого к белому
# Облачно - от серого к белому

# Добавить класс DatabaseUpdater с методами:
#   Получающим данные из базы данных за указанный диапазон дат.
#   Сохраняющим прогнозы в базу данных (использовать peewee)

# Сделать программу с консольным интерфейсом, постаравшись все выполняемые действия вынести в отдельные функции.
# Среди действий, доступных пользователю, должны быть:
#   Добавление прогнозов за диапазон дат в базу данных
#   Получение прогнозов за диапазон дат из базы
#   Создание открыток из полученных прогнозов
#   Выведение полученных прогнозов на консоль
# При старте консольная утилита должна загружать прогнозы за прошедшую неделю.

# Рекомендации:
# Можно создать отдельный модуль для инициализирования базы данных.
# Как далее использовать эту базу данных в движке:
# Передавать DatabaseUpdater url-путь
# https://peewee.readthedocs.io/en/latest/peewee/playhouse.html#db-url
# Приконнектится по полученному url-пути к базе данных
# Инициализировать её через DatabaseProxy()
# https://peewee.readthedocs.io/en/latest/peewee/database.html#dynamically-defining-a-database


import datetime

from WeatherEngine.WeatherMaker import WeatherMarker
import WeatherEngine.DataBase as DataBase
from WeatherEngine.ImageMaker import ImageMarker
# TODO Разнесите код по соответствующим модулям, тут должен остаться только код запуска программы
# Создаем базу данных и таблицу в ней
DataBase.create_weather_table()

# парсим данные и получаем список прогноза погоды
weather = WeatherMarker()
weather.get_weather_forecast()
period = weather.get_period()

# Получаем данные за необходимый пероид
print(f'Доступен прогноз погоды с {period[0]} по {period[1]}')
print(f'Добавление данных в базу данных')
first_date = input(f'Введите начала периода в формате YYYY-MM-DD: ')
end_date = input(f'Введите окончание периода в формате YYYY-MM-DD: ')

first_date = datetime.datetime.strptime(first_date, '%Y-%m-%d').date()
end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
weather_period = weather.get_weather_forecast_period(first_date, end_date)

# Добавляем элементы в базу данных или обновляем их
for elem in weather_period:
    DataBase.add_or_update_field(
        date=elem['date'],
        weather=elem['weather'],
        temperature=elem['temperature']
    )

enter = input('Создать откртки по базе данных?: ')

if enter.lower() in ['да', 'yes']:
    for elem in DataBase.Weather.select():
        ImageMarker(elem.date.date(), elem.weather, elem.temperature).create_card()
else:
    print('Карточки не созданы!')
