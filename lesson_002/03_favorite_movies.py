#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Есть строка с перечислением фильмов

my_favorite_movies = 'Терминатор, Пятый элемент, Аватар, Чужие, Назад в будущее'

# Выведите на консоль с помощью индексации строки, последовательно:
#   первый фильм
#   последний
#   второй
#   второй с конца

# Запятая не должна выводиться.  Переопределять my_favorite_movies нельзя
# Использовать .split() или .find()или другие методы строки нельзя - пользуйтесь только срезами,
# как указано в задании!

first_film = my_favorite_movies[:10]
last_film = my_favorite_movies[-15:]
second_film = my_favorite_movies[12:24]
last_film_2 = my_favorite_movies[-22:-17]

print(first_film)
print(last_film)
print(second_film)
print(last_film_2)