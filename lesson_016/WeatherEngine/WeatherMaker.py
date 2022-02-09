# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from datetime import date, datetime

from peewee import *


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

    def __init__(self, from_date, to_date=None):
        self.from_date = from_date
        self.to_date = to_date
        self.end_date_reached = False
        self.forecast_weather = []

    def parse(self):
        url = self._get_url_start(search_date=self.from_date)

        while True:
            html_data = self._get_html_data(url=url)
            self._parse_html(html_data=html_data)
            if self.end_date_reached:
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

    def _parse_html(self, html_data):
        if self.to_date is None:
            for tag in html_data.find_all(self._is_day):
                current_date = self._convert_ms_to_date(ms=int(tag['time']))

                if current_date == self.from_date:
                    weather, temperature_min, temperature_max = self._parse_day(tag)
                    self._add_day(current_date, weather, temperature_min, temperature_max)

                    self.end_date_reached = True
                    break
        else:
            for tag in html_data.find_all(self._is_day):
                current_date = self._convert_ms_to_date(ms=int(tag['time']))
                if self.from_date <= current_date <= self.to_date:
                    weather, temperature_min, temperature_max = self._parse_day(tag)
                    self._add_day(current_date, weather, temperature_min, temperature_max)

                    if current_date == self.to_date:
                        self.end_date_reached = True
                        break

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


# База данных
db = SqliteDatabase('weather.db')
table_name = 'Forecast weather'


class ForecastWeather(Model):
    date = DateField()
    weather = CharField()
    temperature = CharField()

    class Meta:
        database = db
        db_table = table_name


class DataBaseWeather:
    db_table = ForecastWeather

    if table_name not in db.get_tables():
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

    def get_forecasts(self, from_day, to_day=None):
        data = []
        if to_day is None:
            day = self.db_table.select().where(self.db_table.date == from_day)
            data.append({'date': day.date, 'weather': day.weather, 'temperature': day.temperature})
        else:
            for day in self.db_table.select().where((from_day <= self.db_table.date) % (self.db_table.date <= to_day)):
                data.append({'date': day.date, 'weather': day.weather, 'temperature': day.temperature})
        return data

    def del_forecasts(self, from_day, to_day=None):
        if to_day is None:
            query = self.db_table.delete().where(self.db_table.date == from_day)
            query.execute()
        else:
            query = self.db_table.delete().where((from_day <= self.db_table.date) % (self.db_table.date <= to_day))
            query.execute()


def main():
    day_1 = date(2022, 2, 2)
    day_2 = date(2022, 2, 12)
    parse_data = ParserWeather(from_date=day_1, to_date=day_2).parse()

    table_forecast = DataBaseWeather()
    table_forecast.clean_table()
    table_forecast.update_table(list_forecast=parse_data)

    data = table_forecast.get_all_forecasts()
    print(data)
    table_forecast.del_forecasts(date(2022, 2, 4), date(2022, 2, 9))
    data = table_forecast.get_all_forecasts()
    print(data)


if __name__ == '__main__':
    main()
