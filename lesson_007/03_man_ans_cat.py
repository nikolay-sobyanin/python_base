# -*- coding: utf-8 -*-

from random import randint
from termcolor import cprint

# Доработать практическую часть урока lesson_007/python_snippets/08_practice.py

# Необходимо создать класс кота. У кота есть аттрибуты - сытость и дом (в котором он живет).
# Кот живет с человеком в доме.
# Для кота дом характеризируется - миской для еды и грязью.
# Изначально в доме нет еды для кота и нет грязи.

# Доработать класс человека, добавив методы
#   подобрать кота - у кота появляется дом.
#   купить коту еды - кошачья еда в доме увеличивается на 50, деньги уменьшаются на 50.
#   убраться в доме - степень грязи в доме уменьшается на 100, сытость у человека уменьшается на 20.
# Увеличить кол-во зарабатываемых человеком денег до 150 (он выучил пайтон и устроился на хорошую работу :)

# Кот может есть, спать и драть обои - необходимо реализовать соответствующие методы.
# Когда кот спит - сытость уменьшается на 10
# Когда кот ест - сытость увеличивается на 20, кошачья еда в доме уменьшается на 10.
# Когда кот дерет обои - сытость уменьшается на 10, степень грязи в доме увеличивается на 5
# Если степень сытости < 0, кот умирает.
# Так же надо реализовать метод "действуй" для кота, в котором он принимает решение
# что будет делать сегодня

# Человеку и коту надо вместе прожить 365 дней.


class Man:

    def __init__(self, name):
        self.name = name
        self.fullness = 50
        self.house = None

    def __str__(self):
        return f'Я - {self.name}, сытость {self.fullness}'

    # Методы связанные с человеком
    def go_to_house(self, house):
        self.house = house
        self.fullness -= 10
        cprint(f'{self.name} вьехал в дом', color='cyan')

    def eat(self):
        if self.house.food >= 10:
            cprint(f'{self.name} поел', color='yellow')
            self.fullness += 10
            self.house.food -= 10
        else:
            cprint(f'{self.name} нет еды', color='red')

    def work(self):
        cprint(f'{self.name} сходил на работу', color='blue')
        self.house.money += 150
        self.fullness -= 10

    def watch_MTV(self):
        cprint(f'{self.name} смотрел MTV целый день', color='green')
        self.fullness -= 10

    def shopping(self):
        if self.house.money >= 50:
            cprint(f'{self.name} сходил в магазин за едой', color='magenta')
            self.house.money -= 50
            self.house.food += 50
        else:
            cprint(f'{self.name} деньги кончились!', color='red')

    # Методы связанные с котом
    def pick_up_cat(self, name_cat):
        new_cat = Cat(name=name_cat)
        new_cat.house = self.house
        cprint(f'{self.name} подобрал кота {new_cat.name}', color='cyan')
        return new_cat

    def buy_cat_food(self):
        if self.house.money >= 50:
            cprint(f'{self.name} сходил в магазин за едой для кота', color='magenta')
            self.house.money -= 50
            self.house.cat_food += 50
        else:
            cprint(f'{self.name} деньги кончились!', color='red')

    def clean_house(self):
        if self.house.mess >= 100:
            cprint(f'{self.name} убрал дом.', color='magenta')
            self.fullness -= 20
            self.house.mess -= 100
        else:
            cprint(f'Дома чисто!', color='red')

    def act(self):
        if self.fullness <= 0:
            cprint(f'{self.name} умер...', color='red')
            return
        dice = randint(1, 6)
        if self.fullness <= 20:
            self.eat()
        elif self.house.food <= 10:
            self.shopping()
        elif self.house.money <= 50:
            self.work()
        elif self.house.cat_food <= 10:
            self.buy_cat_food()
        elif self.house.mess >= 100:
            self.clean_house()
        elif dice == 1:
            self.work()
        elif dice == 2:
            self.eat()
        else:
            self.watch_MTV()


class Cat:

    def __init__(self, name):
        self.name = name
        self.fullness = 50
        self.house = None

    def __str__(self):
        return f'Я кот - {self.name}, сытость {self.fullness}'

    def eat(self):
        if self.house.cat_food >= 10:
            cprint(f'{self.name} поел', color='yellow')
            self.fullness += 20
            self.house.cat_food -= 10
        else:
            cprint(f'{self.name} нет еды', color='red')

    def sleep(self):
        cprint(f'{self.name} поспал', color='yellow')
        self.fullness -= 10

    def tear_wallpaper(self):
        cprint(f'{self.name} дерет обои', color='blue')
        self.house.mess += 5
        self.fullness -= 10

    def act(self):
        if self.fullness <= 0:
            cprint(f'{self.name} умер...', color='red')
            return
        dice = randint(1, 2)
        if self.fullness <= 20:
            self.eat()
        elif dice == 1:
            self.tear_wallpaper()
        else:
            self.sleep()


class House:

    def __init__(self):
        self.food = 50
        self.money = 0
        self.cat_food = 0
        self.mess = 0

    def __str__(self):
        return f'В доме: еды - {self.food}, денег - {self.money}, еды для кота - {self.cat_food}, грязь - {self.mess}.'


my_sweet_home = House()
nick = Man(name='Nick')
nick.go_to_house(house=my_sweet_home)
cat = nick.pick_up_cat(name_cat='Барсик')

for day in range(1, 366):
    print('================ день {} =================='.format(day))
    nick.act()
    cat.act()
    print('--- в конце дня ---')
    print(nick)
    print(cat)
    print(my_sweet_home)
    print()


# Усложненное задание (делать по желанию)
# Создать несколько (2-3) котов и подселить их в дом к человеку.
# Им всем вместе так же надо прожить 365 дней.

# (Можно определить критическое количество котов, которое может прокормить человек...)
