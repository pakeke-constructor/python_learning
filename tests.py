
import arcade
import time
import math
import random

# GEOMETRY

WIDTH = 500
HEIGHT = 500

PI_2 = math.pi/2
PI_4 = math.pi/4
THREE_PI_4 = math.pi + PI_4


class Cube:
    def __init__(self):

        self.x_rot = 0
        self.y_rot = 0

        self.line_length = 40
        self.width = 2
        self.colour = (255, 0, 0)
        self.x1 = 40
        self.y1 = 40

        self.fbl = ((WIDTH/2-(self.line_length/2))+(math.cos(self.x_rot+THREE_PI_4)*self.line_length/2), (HEIGHT/2-(self.line_length/2))+self.line_length*(math.sin(self.x_rot+PI_4))/2, 0)
        self.fbr = ((WIDTH/2+(self.line_length/2))-(math.cos(self.x_rot+PI_2)*self.line_length/2), (HEIGHT/2-(self.line_length/2))-self.line_length*(math.sin(self.x_rot+PI_4))/2, 0)
        self.ftr = ((WIDTH/2+(self.line_length/2))-(math.cos(self.x_rot+PI_2)*self.line_length/2), (HEIGHT/2+(self.line_length/2))-self.line_length*(math.sin(self.x_rot+PI_4))/2, 0)
        self.ftl = ((WIDTH/2-(self.line_length/2))+(math.cos(self.x_rot+THREE_PI_4)*self.line_length/2), (HEIGHT/2+(self.line_length/2))+self.line_length*(math.sin(self.x_rot+PI_4))/2, 0)

        self.bbl = ((WIDTH/2-(self.line_length/2))+(math.cos(self.x_rot+THREE_PI_4)*self.line_length/2), (HEIGHT/2-(self.line_length/2))+self.line_length*(math.sin(self.x_rot+THREE_PI_4))/2, +self.line_length)
        self.bbr = ((WIDTH/2+(self.line_length/2))-(math.cos(self.x_rot+PI_2)*self.line_length/2), (HEIGHT/2-(self.line_length/2))-self.line_length*(math.sin(self.x_rot+THREE_PI_4))/2, +self.line_length)
        self.btr = ((WIDTH/2+(self.line_length/2))-(math.cos(self.x_rot+PI_2)*self.line_length/2), (HEIGHT/2+(self.line_length/2))-self.line_length*(math.sin(self.x_rot+THREE_PI_4))/2, +self.line_length)
        self.btl = ((WIDTH/2-(self.line_length/2))+(math.cos(self.x_rot+THREE_PI_4)*self.line_length/2), (HEIGHT/2+(self.line_length/2))+self.line_length*(math.sin(self.x_rot+THREE_PI_4))/2, +self.line_length)

        self.point_list = [self.fbl,self.fbr,self.ftr,self.ftl]
        self.b_p_l = [self.bbl, self.bbr, self.btr, self.btl]


    def draw(self, x, y, colour):
        arcade.draw_line(x[0], x[1], y[0], y[1], colour, border_width=self.width)


cube = Cube()


class Game(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "GEometry")
        self.a_key = False
        self.d_key = False

    def on_draw(self):
        r = (255, 0, 0)
        b = (255, 0, 0)
        w = (255, 255, 255)

        arcade.start_render()
        cube.draw(cube.fbl, cube.fbr, r)
        cube.draw(cube.fbl, cube.ftl,r)
        cube.draw(cube.fbl, cube.bbl, w)

        cube.draw(cube.fbr, cube.bbr, w)
        cube.draw(cube.fbr, cube.ftr, r)

        cube.draw(cube.ftl, cube.ftr, r)
        cube.draw(cube.ftl, cube.fbl, r)
        cube.draw(cube.ftl, cube.fbl, r)

        cube.draw(cube.ftr, cube.fbr, r)
        # cube.draw(cube.ftr, cube.fbr)

        cube.draw(cube.bbl, cube.bbr, b)
        cube.draw(cube.bbl, cube.btl, b)
        cube.draw(cube.bbl, cube.fbl, b)

        # cube.draw(cube.bbr, cube.bbl)
        cube.draw(cube.bbr, cube.btr, b)
        # cube.draw(cube.bbr, cube.bbl)

        cube.draw(cube.btl, cube.btr, b)
        cube.draw(cube.btl, cube.ftl, w)
        cube.draw(cube.btl, cube.bbl, b)

        cube.draw(cube.bbr, cube.bbl, b)
        cube.draw(cube.bbr, cube.fbr,w )
        cube.draw(cube.bbr, cube.btr, b)

        for x in cube.point_list:
            arcade.draw_circle_filled(x[0], x[1], 4, (255, 255, 0))

        for x in cube.b_p_l:
            arcade.draw_circle_filled(x[0], x[1], 4,(255, 0, 255))

    def update(self, delta_time: float):
        if self.d_key:
            cube.x_rot += 0.01
        if self.a_key:
            cube.x_rot -= 0.01

        cube.fbl = ((WIDTH / 2 - (cube.line_length / 2)) + (math.sin(cube.x_rot) * cube.line_length), # <
                    (HEIGHT / 2 - (cube.line_length / 2)) + cube.line_length * (-math.cos(cube.x_rot)) / 2) # <
        cube.fbr = ((WIDTH / 2 + (cube.line_length / 2)) - (math.cos(cube.x_rot) * cube.line_length), # <
                    (HEIGHT / 2 - (cube.line_length / 2)) - cube.line_length * (math.sin(cube.x_rot)) / 2) # <
        cube.ftr = ((WIDTH / 2 + (cube.line_length / 2)) - (math.cos(cube.x_rot) * cube.line_length), # <
                    (HEIGHT / 2 + (cube.line_length / 2)) - cube.line_length * (math.sin(cube.x_rot)) / 2) # <
        cube.ftl = ((WIDTH / 2 - (cube.line_length / 2)) + (math.sin(cube.x_rot) * cube.line_length), # <
                    (HEIGHT / 2 + (cube.line_length / 2)) + cube.line_length * (-math.cos(cube.x_rot)) / 2) # <

        cube.bbl = ((WIDTH / 2 - (cube.line_length / 2)) + (-math.cos(cube.x_rot) * cube.line_length), # <
                    (HEIGHT / 2 - (cube.line_length / 2)) + cube.line_length * (math.sin(cube.x_rot)) / 2) # <
        cube.bbr = ((WIDTH / 2 + (cube.line_length / 2)) + (math.sin(cube.x_rot) * cube.line_length), # <
                    (HEIGHT / 2 - (cube.line_length / 2)) - cube.line_length * (math.cos(cube.x_rot)) / 2) # <
        cube.btr = ((WIDTH / 2 + (cube.line_length / 2)) - (math.sin(cube.x_rot) * cube.line_length), # <
                    (HEIGHT / 2 + (cube.line_length / 2)) - cube.line_length * (math.cos(cube.x_rot)) / 2)
        cube.btl = ((WIDTH / 2 - (cube.line_length / 2)) + (-math.cos(cube.x_rot) * cube.line_length),  # <
                        (HEIGHT / 2 + (cube.line_length / 2)) + cube.line_length * (math.sin(cube.x_rot)) / 2) # <

        cube.point_list = [cube.fbl, cube.fbr, cube.ftr, cube.ftl]
        cube.b_p_l = [cube.bbl, cube.bbr, cube.btr, cube.btl]

    def on_key_press(self, key, modifiers: int):
        if key == arcade.key.D:
            self.d_key = True
        if key == arcade.key.A:
            self.a_key = True

    def on_key_release(self, key, modifiers: int):
        if key == arcade.key.D:
            self.d_key = False
        if key == arcade.key.A:
            self.a_key = False

def main():
    game = Game()
    arcade.run()

main()



