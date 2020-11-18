# -*- coding: utf-8 -*-

# Вывести на консоль жителей комнат (модули room_1 и room_2)
# Формат: В комнате room_1 живут: ...

import room_1
import room_2

folks_room_1 = ', '.join(room_1.folks)  # Погуглил данный оператор
folks_room_2 = ', '.join(room_2.folks)

print(f'В комнате room_1 живут: {folks_room_1}.')
print(f'В комнате room_2 живут: {folks_room_2}.')

# зачет!