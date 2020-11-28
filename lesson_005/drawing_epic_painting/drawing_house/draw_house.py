import simple_draw as sd
from drawing_house.draw_wall import draw_wall
from drawing_house.draw_smile import draw_smile


def draw_house(point_x, point_y, length, height):
    # Контур дома
    point_left_bottom_house = sd.get_point(point_x, point_y)
    point_right_top_house = sd.get_point(point_x + length, point_y + height)
    sd.rectangle(left_bottom=point_left_bottom_house, right_top=point_right_top_house,
                 color=sd.COLOR_DARK_ORANGE, width=0)
    sd.rectangle(left_bottom=point_left_bottom_house, right_top=point_right_top_house,
                 color=(169, 169, 169), width=2)
    # Стена дома
    draw_wall(point_x, point_y, length, height)
    # Крыша дома
    point_list_roof = [
        sd.get_point(point_x - 50, point_y + height),
        sd.get_point(point_x + length + 50, point_y + height),
        sd.get_point(point_x + length / 2, point_y + height + 100)
    ]
    sd.polygon(point_list=point_list_roof, color=(165, 42, 42), width=0)
    # Окно
    point_left_bottom_window = sd.get_point(point_x + length / 2 - 50, point_y + height / 2 - 50)
    point_right_top_window = sd.get_point(point_x + length / 2 + 50, point_y + height / 2 + 50)
    sd.rectangle(left_bottom=point_left_bottom_window, right_top=point_right_top_window,
                 color=(0, 191, 255), width=0)
    sd.rectangle(left_bottom=point_left_bottom_window, right_top=point_right_top_window,
                 color=sd.COLOR_WHITE, width=5)
    # Смайлик
    center_smile_x = point_x + length / 2
    center_smile_y = point_y + height / 2
    draw_smile(x=center_smile_x, y=center_smile_y)


draw_house(point_x=100, point_y=100, length=300, height=200)

sd.pause()
