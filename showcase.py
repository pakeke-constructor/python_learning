
import arcade
import math

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

r_s = 10
r_p = 5
r_m1 = 3

center_y = SCREEN_HEIGHT // 4 * 3

center_x = SCREEN_WIDTH // 4 * 3

def draw_planet(a, b, c):
    arcade.draw_ellipse_outline(center_x, center_y, ampli_p_x, (ampli_p_y//2), (40, 40, 40), 1, 0)
    arcade.draw_circle_filled(a, b, c, (255, 100, 150))


def draw_moon(a, b, c):
    arcade.draw_ellipse_outline(planet_x, planet_y, ampli_m_x, (ampli_m_y//2), (30, 30, 30), 1, 0)
    arcade.draw_circle_filled(a, b, c, (100, 200, 100))




x = 0
y = 0

ampli_p_x = 200
ampli_p_y = 200

ampli_m_x = 50
ampli_m_y = 50


def on_draw(delta_time):
    global x  # x ticker (controls period of x orbit)
    global y  # y ticker (controls period of y orbit)
    global center_x  # center of window
    global center_y  # center of window
    global r_p  # radius of planet
    global r_m1  # radius of moon
    global r_m2
    global r_s  # radius of star
    global ampli_p_x  # Amplitude of sin function that determines length of planet's X coordinate in orbit
    global ampli_p_y  # Amplitude of cos function that determines height of planet's Y coordinate in orbit
    global ampli_m_x  # Amplitude of sin function that determines length of moon's X coordinate in orbit
    global ampli_m_y  # Amplitude of cos function that determines height of moon's Y coordinate in orbit
    global planet_x  # X position of planet
    global planet_y  # Y position of planet

    planet_x = (ampli_p_x * math.sin(x) + center_x)
    planet_y = ((ampli_p_y//2) * math.cos(y) + center_y)

    moon_x = (ampli_m_x * math.cos(x) + planet_x)
    moon_y = (ampli_m_y//2 * math.sin(y) + planet_y)

    arcade.start_render()

    draw_planet(planet_x, planet_y, r_p)
    draw_moon(moon_x, moon_y, r_m1)
    arcade.draw_circle_filled(center_x, center_y, r_s, (255, 255, 0))
    arcade.draw_rectangle_outline(center_x, center_y, (SCREEN_WIDTH//2), (SCREEN_HEIGHT//2), (255, 255, 200), 3)

    x += 0.01
    y += 0.01

def main():
    arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Orbitals")
    arcade.set_background_color((0, 0, 0))
    arcade.schedule(on_draw, 1/60)
    arcade.run()


main()


