# -*- coding: utf-8 -*-

from termcolor import cprint
from random import choice


######################################################## Часть первая
#
# Создать модель жизни небольшой семьи.
#
# Каждый день участники жизни могут делать только одно действие.
# Все вместе они должны прожить год и не умереть.
#
# Муж может:
#   есть,
#   играть в WoT,
#   ходить на работу,
# Жена может:
#   есть,
#   покупать продукты,
#   покупать шубу,
#   убираться в доме,

# Все они живут в одном доме, дом характеризуется:
#   кол-во денег в тумбочке (в начале - 100)
#   кол-во еды в холодильнике (в начале - 50)
#   кол-во грязи (в начале - 0)
#
# У людей есть имя, степень сытости (в начале - 30) и степень счастья (в начале - 100).
#
# Любое действие, кроме "есть", приводит к уменьшению степени сытости на 10 пунктов
# Кушают взрослые максимум по 30 единиц еды, степень сытости растет на 1 пункт за 1 пункт еды.
# Степень сытости не должна падать ниже 0, иначе чел умрет от голода.
#
# Деньги в тумбочку добавляет муж, после работы - 150 единиц за раз.
# Еда стоит 10 денег 10 единиц еды. Шуба стоит 350 единиц.
#
# Грязь добавляется каждый день по 5 пунктов, за одну уборку жена может убирать до 100 единиц грязи.
# Если в доме грязи больше 90 - у людей падает степень счастья каждый день на 10 пунктов,
# Степень счастья растет: у мужа от игры в WoT (на 20), у жены от покупки шубы (на 60, но шуба дорогая)
# Степень счастья не должна падать ниже 10, иначе чел умирает от депрессии.
#
# Подвести итоги жизни за год: сколько было заработано денег, сколько сьедено еды, сколько куплено шуб.


class House:

    def __init__(self):
        self.money = 100
        self.food = 50
        self.level_mess = 0

    def __str__(self):
        return f'В доме денег {self.money}, еды {self.food}, уровень грязи {self.level_mess}.'

    def pollute_house(self):
        self.level_mess += 5


class Human:

    def __init__(self, name):
        self.name = name
        self.fullness = 30
        self.happiness = 100
        self.home = None
        self.total_eat = 0

    def __str__(self):
        return f'Я {self.name}. Сытость {self.fullness} ед., счастья {self.happiness} ед.'

    def settle_in_house(self, house):
        self.home = house
        cprint(f'{self.name} вьехал в дом', color='green')

    def eat(self):
        if self.home.food >= 30:
            cprint(f'{self.name} поел.', color='yellow')
            self.fullness += 30
            self.home.food -= 30
            self.total_eat += 30
        else:
            cprint(f'{self.name} нет еды!', color='red')

    def act(self):
        if self.home.level_mess >= 90:
            self.happiness -= 10
        else:
            self.happiness -= 5

        if self.fullness <= 0 or self.happiness < 10:
            cprint(f'{self.name} умер!', color='red')
            return True

        if self.fullness <= 10:
            self.eat()
            return True
        else:
            return False


class Husband(Human):

    def __init__(self, name):
        super().__init__(name=name)
        self.total_money = 0

    def __str__(self):
        return super().__str__()

    def work(self):
        cprint(f'{self.name} сходил на работу', color='yellow')
        self.home.money += 150
        self.total_money += 150
        self.fullness -= 10

    def gaming(self):
        cprint(f'{self.name} поиграл в WoT.', color='yellow')
        self.happiness += 20
        self.fullness -= 10

    def act(self):
        if not super().act():
            if self.happiness <= 25:
                self.gaming()
            elif self.home.money <= 300:
                self.work()
            else:
                choice([self.eat, self.gaming, self.work])()


class Wife(Human):

    def __init__(self, name):
        super().__init__(name=name)
        self.total_coat = 0

    def __str__(self):
        return super().__str__()

    def shopping(self):
        if self.home.money >= 60:
            cprint(f'{self.name} сходила в магазин за едой.', color='yellow')
            self.home.food += 60
            self.home.money -= 60
            self.fullness -= 10
        else:
            cprint(f'Деньги кончились!', color='red')

    def buy_fur_coat(self):
        if self.home.money >= 400:
            cprint(f'{self.name} купила шубу. Урааа!.', color='yellow')
            self.happiness += 60
            self.home.money -= 350
            self.fullness -= 10
            self.total_coat += 1
        else:
            cprint(f'Денег на шубу нет!', color='red')

    def clean_house(self):
        level_mess = min(100, self.home.level_mess)
        if level_mess:
            cprint(f'{self.name} убрала дом.', color='yellow')
            self.home.level_mess -= level_mess
            self.fullness -= 10
        else:
            cprint(f'Дома чисто!', color='red')

    def act(self):
        if not super().act():
            if self.home.food <= 60:
                self.shopping()
            elif self.happiness <= 25:
                self.buy_fur_coat()
            elif self.home.level_mess >= 110:
                self.clean_house()
            else:
                choice([self.eat, self.shopping, self.buy_fur_coat])()


home = House()
serge = Husband(name='Сережа')
masha = Wife(name='Маша')
serge.settle_in_house(house=home)
masha.settle_in_house(house=home)

for day in range(365):
    print()
    cprint(f'================== День {day} ==================', color='white')
    serge.act()
    masha.act()
    home.pollute_house()
    cprint('----------------- Показатели -----------------', color='blue')
    cprint(serge, color='cyan')
    cprint(masha, color='cyan')
    cprint(home, color='cyan')

print()
cprint(f'За год заработано денег: {serge.total_money}.', color='magenta')
cprint(f'За год съедено еды: {serge.total_eat + masha.total_eat}.', color='magenta')
cprint(f'За год куплено шуб: {masha.total_coat}.', color='magenta')
