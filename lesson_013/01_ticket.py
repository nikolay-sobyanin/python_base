# -*- coding: utf-8 -*-


# Заполнить все поля в билете на самолет.
# Создать функцию, принимающую параметры: ФИО, откуда, куда, дата вылета,
# и заполняющую ими шаблон билета Skillbox Airline.
# Шаблон взять в файле lesson_013/images/ticket_template.png
# Пример заполнения lesson_013/images/ticket_sample.png
# Подходящий шрифт искать на сайте ofont.ru


import argparse
from PIL import Image, ImageDraw, ImageFont, ImageColor


def make_ticket(fio, from_, to, date, save_to):
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
        ticket.save(save_to)
        print(f'Билет сохранен!')
    else:
        print('Билет не сохранен.')


# make_ticket(fio='Константин', from_='Moscow', to='Perm', date='19.04', save_to='new_ticket.png')


# Усложненное задание (делать по желанию).
# Написать консольный скрипт c помощью встроенного python-модуля argparse.
# Скрипт должен принимать параметры:
#   --fio - обязательный, фамилия.
#   --from - обязательный, откуда летим.
#   --to - обязательный, куда летим.
#   --date - обязательный, когда летим.
#   --save_to - необязательный, путь для сохранения заполненнего билета.
# и заполнять билет.


parser = argparse.ArgumentParser(description="Make new ticket")
parser.add_argument('--fio', required=True, type=str, help='Name')
parser.add_argument('--from_', required=True, type=str, help='From')
parser.add_argument('--to', required=True, type=str, help='To')
parser.add_argument('--date', required=True, type=str, help='Date')
parser.add_argument('--save_to', default='new_ticket.png', type=str, help='Save to...')
args = vars(parser.parse_args())

make_ticket(**args)

# Для запуска скрипта.
# Нужно в cmd консоли перейти в папку где расположен скрипт (cd <path>), и выполнить команду:
# python 01_ticket.py --fio Nick --from Moscow --to Perm --date 19.04