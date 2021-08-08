from peewee import *

db = SqliteDatabase('WeatherEngine\weather.db')


class BaseTable(Model):
    class Meta:
        database = db


class Weather(BaseTable):
    date = DateTimeField()
    weather = CharField()
    temperature = CharField()

    class Meta:
        db_table = 'Forecast weather'


def create_weather_table():
    Weather.create_table()


def del_table():
    Weather.drop_table()


def add_or_update_field(date, weather, temperature):
    day_weather, created = Weather.get_or_create(date=date, defaults={
        'weather': weather,
        'temperature': temperature,
    })

    if not created:
        query = Weather.update(
            weather=weather,
            temperature=temperature,
        ).where(Weather.id == day_weather.id)
        query.execute()
