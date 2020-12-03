import simple_draw as sd


def draw_sun(center_x, center_y):
    N = 7
    delta = 360 / N

    point_center = sd.get_point(center_x, center_y)
    sd.circle(center_position=point_center, radius=50, color=sd.COLOR_YELLOW, width=0)

    for i in range(0, N):
        v = sd.get_vector(start_point=point_center, angle=i * delta, length=75)
        v1 = sd.get_vector(start_point=v.end_point, angle=i * delta, length=50, width=8)
        v1.draw(color=sd.COLOR_YELLOW)
