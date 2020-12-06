import simple_draw as sd


def draw_sun(point_sun, ray_offset):
    N = 7
    step = 5
    offset = step * ray_offset
    delta = 360 / N
    sd.circle(center_position=point_sun, radius=50, color=sd.COLOR_YELLOW, width=0)
    for i in range(0, N):
        v1_old = sd.get_vector(start_point=point_sun, angle=i * delta + (offset - step), length=75)
        v2_old = sd.get_vector(start_point=v1_old.end_point, angle=i * delta + (offset - step), length=50, width=8)

        v1_new = sd.get_vector(start_point=point_sun, angle=i * delta + offset, length=75)
        v2_new = sd.get_vector(start_point=v1_new.end_point, angle=i * delta + offset, length=50, width=8)

        v2_old.draw(color=sd.background_color)
        v2_new.draw(color=sd.COLOR_YELLOW)
