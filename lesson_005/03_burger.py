# -*- coding: utf-8 -*-

# Создать модуль my_burger. В нем определить функции добавления инградиентов:
#  - булочки
#  - котлеты
#  - огурчика
#  - помидорчика
#  - майонеза
#  - сыра
# В каждой функции выводить на консоль что-то вроде "А теперь добавим ..."

# В этом модуле создать рецепт двойного чизбургера (https://goo.gl/zA3goZ)
# с помощью фукций из my_burger и вывести на консоль.

# Создать рецепт своего бургера, по вашему вкусу.
# Если не хватает инградиентов - создать соответствующие функции в модуле my_burger

import my_burger as mb

print('Рецепт двойного чизбургера: ')
mb.add_bun()
mb.add_cutlets()
mb.add_cheese()
mb.add_cutlets()
mb.add_cheese()
mb.add_cucumbers()
mb.add_tomato()
mb.add_sauce()
print('Двойной чизбургер готов!')

print(' ')

print('Рецепт бургера, который мне по вкусу: ')
mb.add_bun_with_sesame()
mb.add_cheese()
mb.add_big_cutlets()
mb.add_cheese()
mb.add_bacon()
mb.add_lettuce()
mb.add_tomato()
mb.add_onion()
mb.add_sauce()
print('Бургер готов!')

# зачет!