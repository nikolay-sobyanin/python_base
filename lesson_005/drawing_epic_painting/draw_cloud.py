import simple_draw as sd


def draw_cloud(center_x, center_y):
    for _ in range(0, 100):
        x = sd.random_number(center_x - 100, center_x + 100)
        y = sd.random_number(center_y - 25, center_y + 25)
        radius = sd.random_number(30, 50)
        sd.circle(center_position=sd.get_point(x, y), radius=radius, color=(255, 255, 255), width=0)
