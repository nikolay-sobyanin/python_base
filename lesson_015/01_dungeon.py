# -*- coding: utf-8 -*-

# Подземелье было выкопано ящеро-подобными монстрами рядом с аномальной рекой, постоянно выходящей из берегов.
# Из-за этого подземелье регулярно затапливается, монстры выживают, но не герои, рискнувшие спуститься к ним в поисках
# приключений.
# Почуяв безнаказанность, ящеры начали совершать набеги на ближайшие деревни. На защиту всех деревень не хватило
# солдат и вас, как известного в этих краях героя, наняли для их спасения.
#
# Карта подземелья представляет собой json-файл под названием rpg.json. Каждая локация в лабиринте описывается объектом,
# в котором находится единственный ключ с названием, соответствующем формату "Location_<N>_tm<T>",
# где N - это номер локации (целое число), а T (вещественное число) - это время,
# которое необходимо для перехода в эту локацию. Например, если игрок заходит в локацию "Location_8_tm30000",
# то он тратит на это 30000 секунд.
# По данному ключу находится список, который содержит в себе строки с описанием монстров а также другие локации.
# Описание монстра представляет собой строку в формате "Mob_exp<K>_tm<M>", где K (целое число) - это количество опыта,
# которое получает игрок, уничтожив данного монстра, а M (вещественное число) - это время,
# которое потратит игрок для уничтожения данного монстра.
# Например, уничтожив монстра "Boss_exp10_tm20", игрок потратит 20 секунд и получит 10 единиц опыта.
# Гарантируется, что в начале пути будет две локации и один монстр
# (то есть в коренном json-объекте содержится список, содержащий два json-объекта, одного монстра и ничего больше).
#
# На прохождение игры игроку дается 123456.0987654321 секунд.
# Цель игры: за отведенное время найти выход ("Hatch")
#
# По мере прохождения вглубь подземелья, оно начинает затапливаться, поэтому
# в каждую локацию можно попасть только один раз,
# и выйти из нее нельзя (то есть двигаться можно только вперед).
#
# Чтобы открыть люк ("Hatch") и выбраться через него на поверхность, нужно иметь не менее 280 очков опыта.
# Если до открытия люка время заканчивается - герой задыхается и умирает, воскрешаясь перед входом в подземелье,
# готовый к следующей попытке (игра начинается заново).
#
# Гарантируется, что искомый путь только один, и будьте аккуратны в рассчетах!
# При неправильном использовании библиотеки decimal человек, играющий с вашим скриптом рискует никогда не найти путь.
#
# Также, при каждом ходе игрока ваш скрипт должен запоминать следущую информацию:
# - текущую локацию
# - текущее количество опыта
# - текущие дату и время (для этого используйте библиотеку datetime)
# После успешного или неуспешного завершения игры вам необходимо записать
# всю собранную информацию в csv файл dungeon.csv.
# Названия столбцов для csv файла: current_location, current_experience, current_date
#
#
# Пример взаимодействия с игроком:
#
# Вы находитесь в Location_0_tm0
# У вас 0 опыта и осталось 123456.0987654321 секунд до наводнения
# Прошло времени: 00:00
#
# Внутри вы видите:
# — Вход в локацию: Location_1_tm1040
# — Вход в локацию: Location_2_tm123456
# Выберите действие:
# 1.Атаковать монстра
# 2.Перейти в другую локацию
# 3.Сдаться и выйти из игры
#
# Вы выбрали переход в локацию Location_2_tm1234567890
#
# Вы находитесь в Location_2_tm1234567890
# У вас 0 опыта и осталось 0.0987654321 секунд до наводнения
# Прошло времени: 20:00
#
# Внутри вы видите:
# — Монстра Mob_exp10_tm10
# — Вход в локацию: Location_3_tm55500
# — Вход в локацию: Location_4_tm66600
# Выберите действие:
# 1.Атаковать монстра
# 2.Перейти в другую локацию
# 3.Сдаться и выйти из игры
#
# Вы выбрали сражаться с монстром
#
# Вы находитесь в Location_2_tm0
# У вас 10 опыта и осталось -9.9012345679 секунд до наводнения
#
# Вы не успели открыть люк!!! НАВОДНЕНИЕ!!! Алярм!
#
# У вас темнеет в глазах... прощай, принцесса...
# Но что это?! Вы воскресли у входа в пещеру... Не зря матушка дала вам оберег :)
# Ну, на этот-то раз у вас все получится! Трепещите, монстры!
# Вы осторожно входите в пещеру... (текст умирания/воскрешения можно придумать свой ;)
#
# Вы находитесь в Location_0_tm0
# У вас 0 опыта и осталось 123456.0987654321 секунд до наводнения
# Прошло уже 0:00:00
# Внутри вы видите:
#  ...
#  ...
#
# и так далее...
# Учитывая время и опыт, не забывайте о точности вычислений!


import json
import os
import time
import datetime
import csv
from decimal import Decimal
import re
from termcolor import cprint

# remaining_time = '123456.0987654321'
# если изначально не писать число в виде строки - теряется точность!

monster_pattern = r'(?:Mob|Boss|Boss\d{1,})_exp\d{1,}_tm\d{1,}'
location_pattern = r'Location_(?:[A-F]\d{1,}|\d{1,})_tm(?:\d{1,}\.\d{1,}|\d{1,})'
hatch_pattern = r'Hatch_tm(?:\d{1,}\.\d{1,}|\d{1,})'


class Monster:
    
    def __init__(self, name):
        self.name = name
        self.exp = 0
        self.time = 0

    def __str__(self):
        return f'Атаковать {self.name}'

    def get_exp_time(self):
        if re.fullmatch(monster_pattern, self.name):
            _, exp, time = self.name.split('_')
            self.exp = Decimal(exp[3:])
            self.time = Decimal(time[2:])
        else:
            raise ValueError('Неверно задано имя Монстра!')

    def interact(self, hero):
        self.get_exp_time()
        hero.exp += self.exp
        hero.past_time += self.time
        hero.remaining_time -= self.time
        hero.actual_location.actual_list_objects.remove(self)


class Location:

    def __init__(self, name, actual_list_objects):
        self.name = name
        self.actual_list_objects = actual_list_objects
        self.time = 0

    def __str__(self):
        return f'Перейти в {self.name}'

    def get_time(self):
        if re.fullmatch(location_pattern, self.name) or re.fullmatch(hatch_pattern, self.name):
            *_, time = self.name.split('_')
            self.time = Decimal(time[2:])
        else:
            raise ValueError('Неверно задано имя Монстра!')

    def interact(self, hero):
        self.get_time()
        hero.past_time += self.time
        hero.remaining_time -= self.time
        hero.actual_location = self


class Hero:

    PLAY_TIME = Decimal('123456.0987654321')

    def __init__(self, actual_location):
        self.actual_location = actual_location
        self.remaining_time = self.PLAY_TIME
        self.exp = 0
        self.past_time = 0


class Logger:

    FIELD_NAMES = ['current_location', 'current_experience', 'current_date']

    def __init__(self):
        self.name_file = 'dungeon.csv'

    def run(self):
        if os.path.isfile(self.name_file):
            os.remove(self.name_file)
        with open(self.name_file, 'a', newline='') as log_csv:
            writer = csv.writer(log_csv)
            writer.writerow(self.FIELD_NAMES)

    def add_log(self, log):
        with open(self.name_file, 'a', newline='') as log_csv:
            writer = csv.writer(log_csv)
            writer.writerow(log)


class Game:

    def __init__(self, path_file_game):
        self.path_game_file = path_file_game

    def play(self):
        game_map = self.get_game_map()
        hero = self.get_new_hero(game_map)
        logger = Logger()
        logger.run()

        while True:

            now_time = datetime.datetime.today().strftime('%d-%m-%y %H:%M:%S')
            log = [hero.actual_location.name, hero.exp, now_time]
            logger.add_log(log)

            self.print_result(hero)

            enter = self.choose_action(hero)
            if enter is None:
                cprint('Game over!', 'red')
                break

            hero.actual_location.actual_list_objects[enter].interact(hero)

            check = self.check_end_game(hero)
            if check is None:
                continue
            elif not check:
                hero = self.get_new_hero(game_map)
                continue
            else:
                break

    def get_game_map(self):
        with open(self.path_game_file, 'r') as file:
            game_map = json.load(file)
        return game_map

    def get_locations(self, obj_dict):
        list_objects = []
        if isinstance(obj_dict, dict) and len(obj_dict) > 0:
            name, objects = next(iter(obj_dict.items()))
            for obj in objects:
                if isinstance(obj, dict):
                    list_objects.append(self.get_locations(obj))
                else:
                    list_objects.append(Monster(obj))
            return Location(name, list_objects)
        else:
            raise ValueError('Неверно задана локация!!!')

    def get_new_hero(self, game_map):
        start_location = self.get_locations(game_map)
        return Hero(start_location)

    def choose_action(self, hero):
        while True:
            enter = input('Выберите действие: ')
            if enter.isdigit() and 1 <= int(enter) <= len(hero.actual_location.actual_list_objects):
                return int(enter) - 1
            elif enter.lower() == 'exit':
                return None
            else:
                print('Выбрано недействительное действие. Повторите выбор.')
                continue

    def print_result(self, hero):
        print()
        print('-' * 30)
        cprint(f'Вы находитесь в {hero.actual_location}.', 'green')
        cprint(f'У вас {hero.exp} опыта.', 'green')
        cprint(f'Осталось {hero.remaining_time} сек. до наводнения.', 'green')
        cprint(f'Прошло времени: {hero.past_time} сек.', 'green')
        print('-' * 30)
        print('Вы можете:')
        for i, elem in enumerate(hero.actual_location.actual_list_objects, 1):
            if isinstance(elem, Location):
                cprint(f'{i}) {elem}', 'blue')
            elif isinstance(elem, Monster):
                cprint(f'{i}) {elem}', 'blue')
        print('Введите exit, чтобы сдаться и выйти из игры!!!')

    def check_end_game(self, hero):
        if hero.remaining_time < 0:
            cprint('Наводнение!!! Вы не успели выйти!\nИгра начинается заново', 'red')
            time.sleep(3)
            return False
        elif len(hero.actual_location.actual_list_objects) == 0:
            cprint('Ты пришел в тупик! Выхода нет!\nИгра начинается заново', 'red')
            time.sleep(3)
            return False
        elif re.fullmatch(hatch_pattern, hero.actual_location.name):
            if hero.exp >= 280:
                print('Ура ты выиграл!')
                return True
            cprint('Ты нашел люк, но недостаточно опыта его открыть!\nИгра начинается заново', 'red')
            time.sleep(3)
            return False
        return None


def main():
    game = Game('rpg.json')
    game.play()


if __name__ == '__main__':
    main()
