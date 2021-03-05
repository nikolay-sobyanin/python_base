# -*- coding: utf-8 -*-


# Заполнить все поля в билете на самолет.
# Создать функцию, принимающую параметры: ФИО, откуда, куда, дата вылета,
# и заполняющую ими шаблон билета Skillbox Airline.
# Шаблон взять в файле lesson_013/images/ticket_template.png
# Пример заполнения lesson_013/images/ticket_sample.png
# Подходящий шрифт искать на сайте ofont.ru




# TODO: не используемый импорт.
import os
from PIL import Image, ImageDraw, ImageFont, ImageColor


def make_ticket(fio, from_, to, date):
    data = {
        fio.upper(): (45, 125),
        from_.upper(): (45, 195),
        to.upper(): (45, 260),
        date.upper(): (287, 260),
    }

    font = ImageFont.truetype('Hebar.ttf', size=12)
    ticket = Image.open('images/ticket_template.png')
    draw = ImageDraw.Draw(ticket)
    for text, xy in data.items():
        draw.text(xy=xy, text=text, font=font, fill=ImageColor.colormap['black'])
    ticket.show()
    save_ticket = input('Сохранить билет (y/n)? ')
    if save_ticket.lower() in ['yes', 'y', 'да']:
        ticket.save('ticket.png')
        print(f'Билет сохранен!')
    else:
        print('Билет не сохранен.')


make_ticket(fio='Константин', from_='Moscow', to='Perm', date='19.04')




# TODO: можно доп.часть
# Усложненное задание (делать по желанию).
# Написать консольный скрипт c помощью встроенного python-модуля argparse.
# Скрипт должен принимать параметры:
#   --fio - обязательный, фамилия.
#   --from - обязательный, откуда летим.
#   --to - обязательный, куда летим.
#   --date - обязательный, когда летим.
#   --save_to - необязательный, путь для сохранения заполненнего билета.
# и заполнять билет.
