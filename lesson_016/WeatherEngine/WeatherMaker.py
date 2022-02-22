# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
from peewee import *
import os
import cv2
import re
import shutil

DB = SqliteDatabase('weather.db')
TABLE_NAME = 'Forecast weather'
BASE_DIR = os.path.dirname(__file__)


class ForecastWeather(Model):
    date = DateField()
    weather = CharField()
    temperature = CharField()

    class Meta:
        database = DB
        db_table = TABLE_NAME


class DataBaseWeather:
    db_table = ForecastWeather

    if TABLE_NAME not in DB.get_tables():
        db_table.create_table()

    def clean_table(self):
        self.db_table.drop_table()
        self.db_table.create_table()

    def update_table(self, list_forecast):
        for day in list_forecast:
            self._add_or_update_field(
                date=day['date'],
                weather=day['weather'],
                temperature=day['temperature']
            )

    def _add_or_update_field(self, date, weather, temperature):
        day_weather, created = self.db_table.get_or_create(date=date, defaults={
            'weather': weather,
            'temperature': temperature,
        })

        if not created:
            query = self.db_table.update(
                weather=weather,
                temperature=temperature,
            ).where(self.db_table.id == day_weather.id)
            query.execute()

    def get_all_forecasts(self):
        data = []
        for day in self.db_table.select().order_by(self.db_table.date):
            data.append({'date': day.date, 'weather': day.weather, 'temperature': day.temperature})
        return data

    def get_forecasts(self, from_date, to_date=None):
        data = []
        if to_date is None:
            to_date = from_date
        for day in self.db_table.select().where((from_date <= self.db_table.date) % (self.db_table.date <= to_date)):
            data.append({'date': day.date, 'weather': day.weather, 'temperature': day.temperature})
        return data

    def del_forecasts(self, from_day, to_day=None):
        if to_day is None:
            query = self.db_table.delete().where(self.db_table.date == from_day)
            query.execute()
        else:
            query = self.db_table.delete().where((from_day <= self.db_table.date) % (self.db_table.date <= to_day))
            query.execute()


class ParserWeather:
    DOMAIN = 'https://msk.nuipogoda.ru'

    MONTHS = {
        1: 'январь',
        2: 'февраль',
        3: 'март',
        4: 'апрель',
        5: 'май',
        6: 'июнь',
        7: 'июль',
        8: 'август',
        9: 'сентябрь',
        10: 'октябрь',
        11: 'ноябрь',
        12: 'декабрь',
    }

    def __init__(self):
        self.forecast_weather = []

    def parse(self, from_date, to_date=None):
        url = self._get_url_start(search_date=from_date)

        while True:
            html_data = self._get_html_data(url=url)
            if self._parse_html(html_data, from_date, to_date):
                break
            else:
                url = self._get_url_next_month(html_data)
        return self.forecast_weather

    def clean_data(self):
        if self.forecast_weather:
            self.forecast_weather = []

    def _get_url_start(self, search_date):
        today = date.today()
        if today.year == search_date.year and today.month <= search_date.month:
            return self.DOMAIN + f'/погода-на-{self.MONTHS[search_date.month]}'
        else:
            return self.DOMAIN + f'/{self.MONTHS[search_date.month]}-{search_date.year}'

    def _get_html_data(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, features='html.parser')
        return soup

    def _parse_html(self, html_data, from_date, to_date):
        end_date_reached = False
        if to_date is None:
            to_date = from_date
        for tag in html_data.find_all(self._is_day):
            current_date = self._convert_ms_to_date(ms=int(tag['time']))
            if from_date <= current_date <= to_date:
                weather, temperature_min, temperature_max = self._parse_day(tag)
                self._add_day(current_date, weather, temperature_min, temperature_max)
                if current_date == to_date:
                    end_date_reached = True
                    break
        return end_date_reached

    def _is_day(self, tag):
        return True if tag.name == 'td' and 'time' in tag.attrs else False

    def _parse_day(self, tag):
        weather = tag.find('div', class_='cl_title').get_text(separator=" ")
        temperature_min = tag.find('span', class_='min').text
        temperature_max = tag.find('span', class_='max').text
        return weather, temperature_min, temperature_max

    def _convert_ms_to_date(self, ms):
        return datetime.fromtimestamp(ms / 1000).date()

    def _get_url_next_month(self, html_data):
        next_month = html_data.find('a', class_='next-month')
        return self.DOMAIN + next_month['href']

    def _add_day(self, current_date, weather, temperature_min, temperature_max):
        self.forecast_weather.append({
            'date': current_date,
            'weather': weather,
            'temperature': f'от {temperature_min} до {temperature_max}',
        })


class PostcardMaker:

    IMG_BASE = os.path.join(BASE_DIR, 'image/base.jpg')
    ICONS = {
        'rain': 'rain.jpg',
        'snow': 'snow.jpg',
        'cloud': 'cloud.jpg',
        'sun': 'sun.jpg',
    }

    PATH_ICONS = os.path.join(BASE_DIR, 'image/weather_img')
    DIR_POSTCARD = os.path.join(BASE_DIR, 'weather_cards')

    KEYS_FORECAST = {
        'rain': ['дождь', 'гроза', 'осадки'],
        'snow': ['снег', 'град'],
        'cloud': ['облачно', 'пасмурно'],
        'sun': ['ясно', 'солнце'],
    }

    def __init__(self):
        self.day = None
        self.weather = None
        self.temperature = None
        self.img_base = cv2.imread(self.IMG_BASE)

    def create_card(self, date, weather, temperature):
        self.day = date
        self.weather = weather
        self.temperature = temperature

        draw_bg, name_icon = self._get_bg_and_icon()
        draw_bg()
        self._insert_icon(name_icon)
        self._insert_text_weather()
        self._save_card()

    def view_image(self, name_of_window):
        cv2.namedWindow(name_of_window, cv2.WINDOW_NORMAL)
        cv2.imshow(name_of_window, self.img_base)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def del_all_postcard(self):
        if os.path.isdir(self.DIR_POSTCARD):
            shutil.rmtree(self.DIR_POSTCARD)
            os.mkdir(self.DIR_POSTCARD)

    def _draw_bg_sunny(self):
        img_width = self.img_base.shape[1]
        i = 0
        k = 0
        for _ in range(img_width):
            self.img_base[:, i:i + 2] = (k, 255, 255)
            i += 2
            k += 1

    def _draw_bg_snowy(self):
        img_width = self.img_base.shape[1]
        i = 0
        k = 0
        for _ in range(img_width):
            self.img_base[:, i:i + 2] = (255, k, k)
            i += 2
            k += 1

    def _draw_bg_cloudy(self):
        img_width = self.img_base.shape[1]
        i = 0
        k = 0
        for _ in range(img_width):
            self.img_base[:, i:i + 2] = (128 + k, 128 + k, 128 + k)
            i += 2
            k += 0.5

    def _draw_bg_rainy(self):
        img_width = self.img_base.shape[1]
        i = 0
        k = 0
        for _ in range(img_width):
            self.img_base[:, i:i + 2] = (150, k, k)
            i += 2
            k += 1

    def _get_bg_and_icon(self):
        if list(filter(self.substring_in_string, self.KEYS_FORECAST['rain'])):
            return self._draw_bg_rainy, self.ICONS['rain']
        elif list(filter(self.substring_in_string, self.KEYS_FORECAST['snow'])):
            return self._draw_bg_snowy, self.ICONS['snow']
        elif list(filter(self.substring_in_string, self.KEYS_FORECAST['sun'])):
            return self._draw_bg_sunny, self.ICONS['sun']
        elif list(filter(self.substring_in_string, self.KEYS_FORECAST['cloud'])):
            return self._draw_bg_cloudy, self.ICONS['cloud']
        else:
            print('Не нашли такую погоду!')

    def substring_in_string(self, sub):
        return bool([word for word in self.weather.split() if sub.lower() in word.lower()])

    def _insert_icon(self, name_icon):
        icon = cv2.imread(self.PATH_ICONS + f'/{name_icon}')
        icon_height, icon_width, _ = icon.shape
        sx = 25
        sy = 25
        self.img_base[sx:sx + icon_width, sy: sy + icon_height] = icon

    def _insert_text_weather(self):
        font = cv2.FONT_HERSHEY_COMPLEX
        size = 0.5
        color = (0, 0, 0)

        text_date = f'Дата {self.day}'
        cv2.putText(self.img_base, text_date, (150, 100), font, size, color, 1)

        text_weather = f'Погода {self.weather}'
        cv2.putText(self.img_base, text_weather, (150, 120), font, size, color, 1)

        text_temperature = f'Температура {self.temperature}'
        cv2.putText(self.img_base, text_temperature, (150, 140), font, size, color, 1)

    def _save_card(self):
        if not os.path.isdir(self.DIR_POSTCARD):
            os.mkdir(self.DIR_POSTCARD)
        path = self.DIR_POSTCARD + f'/{self.day}.jpg'
        cv2.imwrite(path, self.img_base)


class WeatherMarker:

    DATE_FORMAT = '%d.%m.%Y'

    def __init__(self):
        self.today = date.today()
        self.data_base = DataBaseWeather()
        self.parser = ParserWeather()
        self.postcard_maker = PostcardMaker()
        self.actions = {
            1: {'name': 'Посмотреть всю базу данных', 'action': self._print_db},
            2: {'name': 'Посмотреть базу данных за определенный период', 'action': self._print_part_db},
            3: {'name': 'Добавить в базу данных новые прогнозы', 'action': self._add_forecasts},
            4: {'name': 'Удалить из базы данных прогнозы', 'action': self._del_forecasts},
            5: {'name': 'Удалить из базы данных все прогнозы', 'action': self._del_all_forecasts},
            6: {'name': 'Создать открытки из базы данных', 'action': self._create_postcards},
            7: {'name': 'Удалить все открытки', 'action': self._del_all_postcards},
        }

    def run(self):
        self._start()
        while True:
            action = self._menu()
            if action is None:
                print('Работа скрипта окончена. Пока!')
                break
            action()

    def _start(self):
        print(f'Привет!\n'
              f'Ты запустил скрипт для создания базы данных прогноза погоды!\n'
              f'Сегодня {self.today.strftime(self.DATE_FORMAT)}. '
              f'Добавить или обновить в базе данных прогноз погоды на 7 дней?')

        while True:
            enter = input('Ответ да\\нет: ')
            if enter.lower() in ['да', 'yes', 'нет', 'no']:
                break
            else:
                print('Неверный ввод! Попробуй еще раз!\n')

        if enter.lower() in ['да', 'yes']:
            data = self.parser.parse(from_date=self.today, to_date=(self.today + timedelta(days=7)))
            self.data_base.update_table(data)

    def _menu(self):
        print('Меню:')
        for key, value in sorted(self.actions.items(), key=lambda x: x[0]):
            print(f'{key} - {value["name"]}')
        print('0 - Окончание работы скрипта')

        while True:
            enter = input('Выберите действие: ')
            if enter.isdigit() and 0 <= int(enter) <= len(self.actions):
                break
            else:
                print('Неверный ввод! Попробуй еще раз!\n')

        if enter == '0':
            return None
        else:
            return self.actions[int(enter)]['action']

    def _print_db(self):
        data = self.data_base.get_all_forecasts()
        self._print_table(data)

    def _print_part_db(self):
        from_date, to_date = self._input_period()
        data = self.data_base.get_forecasts(from_date, to_date)
        self._print_table(data)

    def _input_period(self):
        while True:
            print('Дата начала.')
            from_date = self._input_date()
            print('Дата окончания (введи 0 если не требуется).')
            to_date = self._input_date()

            if to_date is None or from_date <= to_date:
                return from_date, to_date
            else:
                print('Неверный ввод дат! Попробуй еще раз!\n')

    def _input_date(self):
        pattern = r'\d{2}.\d{2}.\d{4}'
        while True:
            enter = input('Введите дату в формате DD.MM.YYYY: ')
            if re.match(pattern, enter):
                return datetime.strptime(enter, self.DATE_FORMAT).date()
            elif enter == '0':
                return None
            else:
                print('Неверный ввод! Попробуй еще раз!\n')

    def _print_table(self, data):
        width = 30
        string_line = '-' * (width * 3 + 4)
        print(string_line)
        print(f'|{"Дата":^{width}}|{"Погода":^{width}}|{"Температура":^{width}}|')
        print(string_line)

        for day in data:
            print(
                f'|{day["date"].strftime(self.DATE_FORMAT):^{width}}'
                f'|{day["weather"]:^{width}}'
                f'|{day["temperature"]:^{width}}|')
            print(string_line)

    def _add_forecasts(self):
        from_date, to_date = self._input_period()
        data = self.parser.parse(from_date=from_date, to_date=to_date)
        self.data_base.update_table(data)
        print('Прогнозы погоды добавлены в базу данных!\n')

    def _del_forecasts(self):
        from_date, to_date = self._input_period()
        self.data_base.del_forecasts(from_date, to_date)
        print('Прогнозы погоды удалены из базы данных!\n')

    def _del_all_forecasts(self):
        self.data_base.clean_table()
        print('База данных очищена!\n')

    def _create_postcards(self):
        data = self.data_base.get_all_forecasts()
        for day in data:
            self.postcard_maker.create_card(**day)
        print('Открытки созданы!\n')

    def _del_all_postcards(self):
        self.postcard_maker.del_all_postcard()
        print('Открытки удалены!\n')


def main():
    weather_marker = WeatherMarker()
    weather_marker.run()


if __name__ == '__main__':
    main()

