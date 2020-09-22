#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Есть словарь координат городов
from pprint import pprint

sites = {
    'Moscow': (550, 370),
    'London': (510, 510),
    'Paris': (480, 480),
}

# Составим словарь словарей расстояний между ними
# расстояние на координатной сетке - ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

distances = {}

moscow = sites['Moscow']
london = sites['London']
paris = sites['Paris']

moscow_london = ((moscow[0] - london[0]) ** 2 + (moscow[1] - london[1]) ** 2)**0.5
moscow_paris = ((moscow[0] - paris[0]) ** 2 + (moscow[1] - paris[1]) ** 2)**0.5
london_paris = ((london[0] - paris[0]) ** 2 + (london[1] - paris[1]) ** 2)**0.5

distances['Moscow'] = {}
distances['Moscow']['London'] = moscow_london
distances['Moscow']['Paris'] = moscow_paris

distances['London'] = {}
distances['London']['Moscow'] = moscow_london
distances['London']['Paris'] = london_paris

distances['Paris'] = {}
distances['Paris']['Moscow'] = moscow_paris
distances['Paris']['London'] = london_paris

pprint(distances)

# Пример создания словарей
# d_1 = dict()
# d_1['room_x'] = {}
# d_1['room_y'] = {}
# d_1['room_z'] = {}
# lst = (1,2,3)		# номера включенных ламп
# d_1['room_x']['active_lamps'] = lst
# d_1['room_y']['active_lamps'] = lst + (4,5)
# d_1['room_z']['room_t'] = {}
# d_1['room_z']['room_t']['f_start_robot'] = True
# d_1['room_z']['f_conditioner'] = False
# d_1['room_z']['active_lamps'] = [1]
#
#
# lst = (1,2,3)		# номера включенных ламп
# d_2 = {
#     'room_x': {
#         'active_lamps': lst
#     },
#     'room_y': {
#         'active_lamps': lst + (4,5)
#     },
#     'room_z': {
#         'room_t': {
#             'f_start_robot': True
#         },
#         'f_conditioner': False,
#         'active_lamps': [1]
#     }
# }
#
# print(d_1 == d_2)


# Задание словаря вторым способом
distances_2 = {
    'Moscow': {
        'London': moscow_london,
        'Paris': moscow_paris
    },
    'London': {
        'Moscow': moscow_london,
        'Paris': london_paris
    },
    'Paris': {
        'Moscow': moscow_paris,
        'London': london_paris
    }
}

print(distances == distances_2)
pprint(distances_2)