# -*- coding: utf-8 -*-

from termcolor import cprint
from random import choice, sample

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

CAT_FOOD = 'cat_food'
HUMAN_FOOD = 'human_food'

verbose = False
native_cprint = cprint


def cprint(*args, **kwargs):
    if verbose:
        native_cprint(*args, **kwargs)


class House:

    def __init__(self):
        self.money = 100
        self.level_mess = 0
        self.fridge = {
            CAT_FOOD: 100,
            HUMAN_FOOD: 100
        }

    def __str__(self):
        return f'В доме денег {self.money}, еды {self.fridge[HUMAN_FOOD]}, еды кота для {self.fridge[CAT_FOOD]}, ' \
               f'уровень грязи {self.level_mess}.'

    def pollute_house(self):
        self.level_mess += 5


class General:

    def __init__(self, name, kind_food, voracity, coef_fullness):
        self.name = name
        self.kind_food = kind_food
        self.voracity = voracity
        self.coef_fullness = coef_fullness
        self.home = None
        self.fullness = 0
        self.total_eat = 0

    def is_alive(self):
        if self.fullness <= 0:
            cprint(f'{self.name} умер из-за голода!', color='red')
            return False
        else:
            return True

    def eat(self):
        if self.home.fridge[self.kind_food] >= self.voracity:
            cprint(f'{self.name} поел.', color='yellow')
            self.fullness += self.voracity * self.coef_fullness
            self.home.fridge[self.kind_food] -= self.voracity
            self.total_eat += self.voracity
        else:
            cprint(f'{self.name} нет еды!', color='red')
            self.fullness -= self.voracity * self.coef_fullness * 0.5  # Еды нет, поэтому в режиме сбережения энергии


class Human(General):

    def __init__(self, name, voracity):
        super().__init__(name=name, kind_food=HUMAN_FOOD, voracity=voracity, coef_fullness=1)
        self.fullness = 30
        self.happiness = 100

    def __str__(self):
        return f'Я {self.name}. Сытость {self.fullness} ед., счастья {self.happiness} ед.'

    def settle_in_house(self, house):
        self.home = house
        cprint(f'{self.name} вьехал в дом', color='green')

    def is_alive(self):
        if not super().is_alive():
            return False
        elif self.happiness < 10:
            cprint(f'{self.name} умер из-за депрессии!', color='red')
            return False
        else:
            return True

    def pick_up_cat(self, name_cat):
        new_cat = Cat(name=name_cat)
        new_cat.home = self.home
        cprint(f'{self.name} подобрал кота {new_cat.name}', color='cyan')
        return new_cat

    def act(self):
        if self.home.level_mess >= 90:
            self.happiness -= 10
        else:
            self.happiness -= 5


class Husband(Human):

    def __init__(self, name, salary):
        super().__init__(name=name, voracity=30)
        self.salary = salary
        self.total_money = 0

    def work(self):
        cprint(f'{self.name} сходил на работу', color='yellow')
        self.home.money += self.salary
        self.total_money += self.salary
        self.fullness -= 10

    def gaming(self):
        cprint(f'{self.name} поиграл в WoT.', color='yellow')
        self.happiness += 20
        self.fullness -= 10

    def caress_cat(self):
        cprint(f'{self.name} гладила кота.', color='yellow')
        self.happiness += 5
        self.fullness -= 10

    def act(self):
        super().act()
        if self.fullness <= 10:
            self.eat()
        elif self.happiness <= 40:
            self.gaming()
        elif self.home.money <= 600:
            self.work()
        else:
            choice([self.eat, self.work, self.gaming, self.caress_cat])()


class Wife(Human):

    def __init__(self, name):
        super().__init__(name=name, voracity=30)
        self.total_coat = 0

    def shopping(self):
        if self.home.money >= 70:
            cprint(f'{self.name} сходила в магазин за едой.', color='yellow')
            self.home.fridge[HUMAN_FOOD] += 70
            self.home.money -= 70
            self.fullness -= 10
        else:
            cprint(f'Деньги кончились!', color='red')

    def buy_fur_coat(self):
        if self.home.money >= 600:
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

    def buy_cat_food(self):
        if self.home.money >= 50:
            cprint(f'{self.name} сходила в магазин за едой для кота.', color='yellow')
            self.home.money -= 50
            self.home.fridge[CAT_FOOD] += 50
            self.fullness -= 10
        else:
            cprint(f'Денег на еду коту нет!', color='red')

    def caress_cat(self):
        cprint(f'{self.name} гладила кота.', color='yellow')
        self.happiness += 5
        self.fullness -= 10

    def act(self):
        super().act()
        if self.fullness <= 20:
            self.eat()
        elif self.happiness <= 40:
            self.buy_fur_coat()
        elif self.home.fridge[HUMAN_FOOD] <= 80:
            self.shopping()
        elif self.home.fridge[CAT_FOOD] <= 60:
            self.buy_cat_food()
        elif self.home.level_mess >= 90:
            self.clean_house()
        else:
            choice([self.eat, self.shopping, self.buy_fur_coat, self.caress_cat])()


class Cat(General):

    def __init__(self, name):
        super().__init__(name=name, kind_food=CAT_FOOD, voracity=10, coef_fullness=2)
        self.fullness = 30

    def __str__(self):
        return f'Я кот {self.name}. Сытость {self.fullness} ед.'

    def sleep(self):
        cprint(f'{self.name} поспал.', color='yellow')
        self.fullness -= 10

    def soil(self):
        cprint(f'{self.name} дерет обои.', color='yellow')
        self.home.level_mess += 5
        self.fullness -= 10

    def act(self):
        if self.fullness <= 20:
            self.eat()
        else:
            choice([self.sleep, self.soil])()


class Child(Human):

    def __init__(self, name):
        super().__init__(name=name, voracity=10)
        self.total_coat = 0

    def sleep(self):
        cprint(f'{self.name} поспал.', color='yellow')
        self.fullness -= 10

    def act(self):
        if self.fullness <= 10:
            self.eat()
        else:
            choice([self.eat, self.sleep])()


class Experiment:
    """ Семья из 3-х человек (муж, жена, ребенок).
    Определить со скольми котами сможет выжить семья при различных условиях. """

    def __init__(self, salary, money_incidents, food_incidents, numb_of_cats,  numb_of_experiments):
        self.salary = salary
        self.money_incidents = money_incidents
        self.food_incidents = food_incidents
        self.numb_of_cats = numb_of_cats
        self.numb_of_experiments = numb_of_experiments
        self.successful_experiments = 0
        self.weight_experiment = 0

    def __str__(self):
        return f'|{self.salary:^20}|{self.numb_of_cats:^20}|{self.food_incidents:^20}|{self.money_incidents:^20}|' \
               f'{self.numb_of_experiments:^20}|{self.successful_experiments:^25}|{self.weight_experiment:^20.4f}|'

    def __lt__(self, other):
        if self.weight_experiment < other.weight_experiment:
            return True
        else:
            return False

    def give_weight(self):
        x1 = self.successful_experiments / self.numb_of_experiments
        x2 = self.food_incidents / 5
        x3 = self.money_incidents / 5
        x4 = 200 / self.salary
        return (0.45 * x1) + (0.15 * x2) + (0.15 * x3) + (0.25 * x4)

    def create_residents(self, home):
        home_residents_list = [
            Husband(name='Сережа', salary=self.salary),
            Wife(name='Маша'),
            Child(name='Петя')
        ]
        for resident in home_residents_list:
            resident.settle_in_house(house=home)
        # Коты
        for i in range(self.numb_of_cats):
            name_cat = f'Кот {i + 1}'
            home_residents_list.append(home_residents_list[0].pick_up_cat(name_cat=name_cat))
        return home_residents_list

    def simulate(self):
        for _ in range(self.numb_of_experiments):
            successful_experiment = True

            days_year = range(1, 365 + 1)
            days_money_incidents = sorted(sample(days_year, self.money_incidents))  # TODO: отлично
            days_food_incidents = sorted(sample(days_year, self.food_incidents))

            home = House()
            home_residents_list = self.create_residents(home=home)
            for day in days_year:
                for home_resident in home_residents_list:
                    home_resident.act()
                    successful_experiment &= home_resident.is_alive()
                home.pollute_house()

                if day in days_money_incidents:
                    home.money //= 2
                if day in days_food_incidents:
                    home.fridge[CAT_FOOD] //= 2
                    home.fridge[HUMAN_FOOD] //= 2

                if not successful_experiment:
                    break
            self.successful_experiments += successful_experiment
        self.weight_experiment = self.give_weight()


results = []
for food_incidents in range(6):
    for money_incidents in range(6):
        for salary in range(200, 401, 50):
            experiment = Experiment(salary, money_incidents, food_incidents, numb_of_cats=3, numb_of_experiments=5)
            experiment.simulate()
            results.append(experiment)

results.sort(reverse=True)
print(f'{"Наилучшие эксперименты":^153}')
print(f'{"-":-^153}')
print(f'|{"Зарплата":^20}|{"Кол-во котов":^20}|{"Пропадание еды":^20}|{"Пропадание денег":^20}|'
      f'{"Кол-во экспериментов":^20}|{"Удачных экспериментов":^25}|{"Вес экперимента":^20}|')
print(f'{"-":-^153}')
for exp in results[:6]:
    print(exp)
    print(f'{"-":-^153}')
print()
print(f'{"Наихудшие эксперименты эксперименты":^153}')
print(f'{"-":-^153}')
print(f'|{"Зарплата":^20}|{"Кол-во котов":^20}|{"Пропадание еды":^20}|{"Пропадание денег":^20}|'
      f'{"Кол-во экспериментов":^20}|{"Удачных экспериментов":^25}|{"Вес экперимента":^20}|')
print(f'{"-":-^153}')
for exp in results[-6:]:
    print(exp)
    print(f'{"-":-^153}')


# Класс Эксперимент.
#  Сделайте небольшой класс Experiment.
#  В конструкторе будут все поля: число людей, кошек, ЗП, частота пропадания еды и денег, число повторений эксперимента,
#  число удачных повторений.
#  Так же нужно будет перегрузить оператор сравнения - __lt__.
#  Примечание: "__lt__" - метод вызывается при использовании оператора "<".
#  Например:   "exp_1 < exp_2" по факту вызовет следующее "Experiment.__lt__(exp_1, exp_2)".
#  Должно возвращать True или False.
#  .
#  Запускаем несколько вложенных циклов (по ЗП, кол-во кошек и т.п.), перебираем разные наборы
#  параметров. Проводим симуляции, результаты сохраняем в объекты Experiment().
#  Все результаты сохраняются в список Experiment`ов.
#  Перегрузка оператора __lt__ позволит нам отсортировать список стандартной функцией
#  sorted(my_list) и взять срез лучших и худших 5 примеров.
#  .
#  Далее, перегрузив метод __str__ у Experiment мы сможем печатать информацию об экспериментах в цикле, не
#  зная ничего о его полях, логика будет инкапсулировано в класс Эксперимент. Т.е. 1 раз написали, а дальше
#  используем, и не приходится каждый раз вспоминать, какое поле должно быть больше, меньше или
#  равно нулю.
#  .
#  p.s. так же можно добавить поле "число повторений". Чем больше повторений, тем более
#  достоверны результаты эксперимента.


#  Коэффициент. Вес эксперимента.
#  У класса Experiment нужно добавить ф-цию "отдай вес". Вес эксперимента, т.е. насколько он,
#  скажем так, "крут" (т.е. эксперимент с 1 человеком, ЗП 10000, и 0 котами нас не слишком
#  интересует, поэтому его вес должен быть низкий; а вот случай, где 3 человека и 4 кота
#  выживают на 200 рублей - для нас интересен (конечно, если он успешен)).
#  .
#  Это нам пригодится для сравнения Экспериментов между собой. Мы можем ввести "веса" и сранивать этим результат, и
#  определить какой наиболее сторгий набор параметров позволит нам прокормить как можно больше котов.
#  .
#  Пример как посчитать вес:
#     вес_эксперимента = (число_успешных_попыток_эксперимента / (общее_число попыток + 3))
#                        * (число_пропаж_еды / 5)
#                        * (число_пропаж_денег / 7)
#                        * (число_человек * 30 + число_котов * 20) / ЗП
#  Посчитанный вес будет отражать ценность данного эксперимента. И будет учитывать все параметры.
#  Я написал приблизительную формулу. Вероятно, вы можете ее уточнить, т.к. например понимаете
#  что какой-то из параметров доментирует над другими.
#  .
#  Наша задача: определить эксперитмен, отражающий самый-самый экстремальный способ выживания семьи.
#  .
#  Основной плюс: мы используем средства питона,
#  1. перегрузив __lt__ может использовать sort() + срезы для получения лучших/худших;
#  2. перегрузив __str__ можем получать инфу об эксперименте не вдаваясь в то, какие поля у эксперимента.

# ===================== 1 ЧАСТЬ ДЗ =====================
# home = House()
# serge = Husband(name='Сережа')
# masha = Wife(name='Маша')
# petya = Child(name='Петя')
# serge.settle_in_house(house=home)
# masha.settle_in_house(house=home)
# petya.settle_in_house(house=home)
# cat = serge.pick_up_cat(name_cat='Барсик')
#
# for day in range(366):
#     print(end='\n\n')
#     cprint(f'================== День {day} ==================', color='white')
#     f_success = True
#     for home_resident in (serge, masha, petya, cat):
#         home_resident.act()
#         f_success &= home_resident.is_alive()
#         cprint(home_resident, color='cyan')
#         cprint('-------------------------------------------', color='blue')
#     home.pollute_house()
#     cprint(home, color='cyan')
#     if not f_success:
#         break
#
# print(end='\n\n')
# cprint(f'За год заработано денег: {serge.total_money}.', color='magenta')
# cprint(f'За год съедено еды: {serge.total_eat + masha.total_eat + petya.total_eat}.', color='magenta')
# cprint(f'За год куплено шуб: {masha.total_coat}.', color='magenta')
# cprint(f'За год кот съел еды: {cat.total_eat}.', color='magenta')

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
