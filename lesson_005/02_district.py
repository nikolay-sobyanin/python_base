# -*- coding: utf-8 -*-

# Составить список всех живущих на районе и Вывести на консоль через запятую
# Формат вывода: На районе живут ...
# подсказка: для вывода элементов списка через запятую можно использовать функцию строки .join()
# https://docs.python.org/3/library/stdtypes.html#str.join


from district.central_street.house1.room1 import folks as cs_h1_r1
from district.central_street.house1.room2 import folks as cs_h1_r2
from district.central_street.house2.room1 import folks as cs_h2_r1
from district.central_street.house2.room2 import folks as cs_h2_r2

from district.soviet_street.house1.room1 import folks as ss_h1_r1
from district.soviet_street.house1.room2 import folks as ss_h1_r2
from district.soviet_street.house2.room1 import folks as ss_h2_r1
from district.soviet_street.house2.room2 import folks as ss_h2_r2

folks_in_the_area = ', '.join(cs_h1_r1 + cs_h1_r2 + cs_h2_r1 + cs_h2_r2 + ss_h1_r1 + ss_h1_r2 + ss_h2_r1 + ss_h2_r2)

print(f'На районе живут {folks_in_the_area}.')

# зачет!