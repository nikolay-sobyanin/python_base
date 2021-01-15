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

    def __init__(self, name, voracity):
        self.name = name
        self.voracity = voracity
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
        if self.home.food >= self.voracity:
            cprint(f'{self.name} поел.', color='yellow')
            self.fullness += self.voracity
            self.home.food -= self.voracity
            self.total_eat += self.voracity
        else:
            cprint(f'{self.name} нет еды!', color='red')

    def is_alive(self):
        if self.fullness <= 0 or self.happiness < 10:
            cprint(f'{self.name} умер!', color='red')
            return False
        else:
            return True

    def act(self):
        if self.home.level_mess >= 90:
            self.happiness -= 10
        else:
            self.happiness -= 5


class Husband(Human):

    def __init__(self, name):
        super().__init__(name=name, voracity=30)
        self.total_money = 0

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
        super().act()
        if self.fullness <= 10:
            self.eat()
        elif self.happiness <= 25:
            self.gaming()
        elif self.home.money <= 400:
            self.work()
        else:
            choice([self.eat, self.work, self.gaming])()


class Wife(Human):

    def __init__(self, name):
        super().__init__(name=name, voracity=30)
        self.total_coat = 0

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
        super().act()
        if self.fullness <= 10:
            self.eat()
        elif self.home.food <= 60:
            self.shopping()
        elif self.happiness <= 25:
            self.buy_fur_coat()
        elif self.home.level_mess >= 110:
            self.clean_house()
        else:
            choice([self.eat, self.shopping, self.buy_fur_coat])()


class Child(Human):

    def __init__(self, name):
        super().__init__(name=name, voracity=10)
        self.total_coat = 0

    # TODO: закомментировал метод. Почему все равно работает?
    # def __str__(self):
    #     return super().__str__()

    # TODO: есть понимание "почему" работает и __str__ удалили?

    def sleep(self):
        cprint(f'{self.name} поспал.', color='yellow')
        self.fullness -= 10

    def act(self):
        if self.fullness <= 10:
            self.eat()
        else:
            choice([self.eat, self.sleep])()


home = House()
serge = Husband(name='Сережа')
masha = Wife(name='Маша')
petya = Child(name='Петя')
serge.settle_in_house(house=home)
masha.settle_in_house(house=home)
petya.settle_in_house(house=home)

for day in range(366):
    print()
    cprint(f'================== День {day} ==================', color='white')
    if not serge.is_alive() or not masha.is_alive() or not petya.is_alive():
        break
    serge.act()
    masha.act()
    petya.act()
    home.pollute_house()
    cprint('----------------- Показатели -----------------', color='blue')
    cprint(serge, color='cyan')
    cprint(masha, color='cyan')
    cprint(petya, color='cyan')
    cprint(home, color='cyan')

print()
cprint(f'За год заработано денег: {serge.total_money}.', color='magenta')
cprint(f'За год съедено еды: {serge.total_eat + masha.total_eat + petya.total_eat}.', color='magenta')
cprint(f'За год куплено шуб: {masha.total_coat}.', color='magenta')

#  Наша задача не просто сделать классы Муж и Жена, а сделать эти классы так, чтобы в случае чего от них можно было
#  наследоваться, а не копировать код из них создавая подклассы МужКаскадер или ДепрессивнаяЖена.
#  Помните мы изучали в 6ом модуле "принцип разделения ответственности"? Есть и другие принципы, аббревиатура: S.O.L.I.D.
#  S - single responsibility (единство ответственности)
#  O - open|close (принцип открытости/закрытости)
#  L - Принцип Барбары Лисков
#  I - Принцип разделения интерфейсов
#  D - Принцип инверсий зависимостей
#  .
#  Тогда мы познакомились с 1ым. Тот про которым мы говорим в act() - это "Принцип Барбары Лисков".
#  В двух словах он звучит так: "Подклассы должны дополнять, а не замещать поведение базового класса."
#  .
#  Что это означает?
#  Это значит, что в хорошем коде, вместо объекта класса родителя всегда можно подставить объект класса-наследника.
#  Допустим у нас был бы кусок кода:
#       mammal_obj = Mammal(...)
#       if mammal_obj.act():
#           print('success')
#  .
#  Мы берем пишет класс-наследник, например Man, а от него еще наследуем Wife. Выходит класс Wife - это "внучка"
#  класса Mammal. Хорошим тоном будет, если подставив Wife(...) в код выше, наш код сможет работать.
#       mammal_obj = Wife(...)      # да, это все еще mammal_obj, т.к. мы от него наследовались
#       if mammal_obj.act():
#           print('success')
#  .
#  Но если мы изменим сигнарутыр методов (что принимают и что возвращают) у классов-наследников, тогда их поведение
#  начнет отличаться от поведения родителя. В итоге, код становится не очевидным: вроде есть класс_1, от него
#  наследуется класс_2, а выходит, что класс_2 совсем не похож на класс_1, т.к. в нем переделали сигнатуры методов.
#  .
#  Примечание: сигнатура метода - это набор параметров + их типы, и то, что возвращает этот метод.

#  сейчас у нас как раз начинает проблема: нужно дублировать "return True\False" внутри act`ов наследников.
#  И это будет очень муторно. Поэтому мы лучше сделаем is_alive, который будет конкретно на этом специализироваться,
#  а act вообще будет без return.

# # ну идея неплохая. Тогда только 3 "столбица:
#         #  1. условие;
#         #  2. метод;
#         #  3. его параметры;
#         #  .
#         #  Сработало условие? вызываем метод и подставляем параметры. Пример:
#         def my_print(x, y, z, b):
#             print(x, y, z, b)
#
#         # параметры
#         params = [1, 'asdasdasd', None, False]
#         # проверка условия
#         if choice([1, 0]):
#             # вызов метода с распаковкой его параметров внутрь. Т.е. 1 подставится вместо "x", ... False вместо "b".
#             my_print(*params)
