import arcade
import math
import random
import time

WIDTH = 500
HEIGHT = 500

class Blah:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.colar = (250, 250, 250)
        self.t = 0

b = Blah()


class Game(arcade.Window):
    def __init__(self):
        self.drawing = False
        self.siz = 70
        self.colar = (250, 250, 250)
        self.t = 0
        self.x = 0
        self.y = 0
        super().__init__()
        self.dx = None
        self.dy = None

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button:
            arcade.start_render()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        b.x = x
        b.y = y
        self.dx = dx
        self.dy = dy

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        if button:
            self.drawing = False

    def update(self, delta_time: float):
        b.colar = (round(125*math.cos(b.t)+125), round(125*math.cos(b.t*0.8)+125), round(125*math.cos(1.2*b.t)+125))
        if self.dx == 0 and self.dy == 0:
            change = 0.01
        else:
            change = 0.05
        b.t += change

    def on_draw(self):
        arcade.draw_circle_filled(b.x, b.y, self.siz, b.colar)
        arcade.draw_circle_outline(b.x, b.y, self.siz, b.colar)


game = Game()


def main():
    arcade.run()


main()











