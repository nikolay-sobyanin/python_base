import os
import random
import cv2


class ImageMarker:

    def __init__(self, date, weather, temperature):
        self.date = date
        self.weather = weather
        self.temperature = temperature
        self.img = cv2.imread('WeatherEngine/image/base.jpg')
        # TODO Имена файлов надо присваивать константам и использовать в основном коде только их.
        #  Имена констант пишутся большими буквами. Располагают константы в начале модуля, сразу после
        #  импортов сторонних модулей.
        #  Может возникнуть необходимость изменить имя файла и через константу это делать удобнее - константа это
        #  единое место изменения, а примениться она может во многих местах. Поэтому вверху её легко найти для изменения
        #  без необходимости перелопачивания кода проекта.

    def create_card(self):
        self.draw_bg()
        self.insert_icon()
        self.insert_text_weather()
        # self.viewImage(f'{self.date}_card')
        self.save_card()

    def viewImage(self, name_of_window):   # Просмотр изображения
        # TODO имя метода пишется также как имя переменной - маленькими буквами и с подчёркиванием между словами
        cv2.namedWindow(name_of_window, cv2.WINDOW_NORMAL)
        cv2.imshow(name_of_window, self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def draw_bg(self):
        list_bg = [self.draw_bg_yellow, self.draw_bg_blue, self.draw_bg_grey]
        random_bg = random.choice(list_bg)
        random_bg()

    def draw_bg_yellow(self):    # Желтый фон
        img_width = self.img.shape[1]
        i = 0
        k = 0
        for _ in range(img_width):
            self.img[:, i:i + 2] = (k, 255, 255)
            i += 2
            k += 1

    def draw_bg_blue(self):  # Синий фон
        img_width = self.img.shape[1]
        i = 0
        k = 0
        for _ in range(img_width):
            self.img[:, i:i + 2] = (255, k, k)
            i += 2
            k += 1

    def draw_bg_grey(self):  # Серый фон
        img_width = self.img.shape[1]
        i = 0
        k = 0
        for _ in range(img_width):
            self.img[:, i:i + 2] = (128 + k, 128 + k, 128 + k)
            i += 2
            k += 0.5

    def insert_icon(self):
        icon_list = ['sun.jpg', 'cloud.jpg', 'rain.jpg', 'snow.jpg']
        random_icon = random.choice(icon_list)
        icon = cv2.imread(f'WeatherEngine/image/weather_img/{random_icon}')
        icon_height, icon_width, _ = icon.shape
        sx = 25
        sy = 25
        self.img[sx:sx + icon_width, sy: sy + icon_height] = icon

    def insert_text_weather(self):
        font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        size = 0.5
        color = (0, 0, 0)

        text_date = f'Дата {self.date}'
        cv2.putText(self.img, text_date, (150, 100), font, size, color, 1)

        text_weather = f'Погода {self.weather}'
        cv2.putText(self.img, text_weather, (150, 120), font, size, color, 1)

        text_temperature = f'Температура {self.temperature}'
        cv2.putText(self.img, text_temperature, (150, 140), font, size, color, 1)

    def save_card(self):
        if not os.path.isdir('WeatherEngine/weather_cards'):
            os.mkdir('WeatherEngine/weather_cards')
        path = f'WeatherEngine/weather_cards/{self.date}_card.jpg'
        cv2.imwrite(path, self.img)

