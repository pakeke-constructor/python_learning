import arcade
import random
import math

WIDTH = 1300
HEIGHT = 800
G_CONST = 0


def get_vector(x1, y1, x2, y2):
    return math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))


class qqq:
    def __init__(self):
        self.scale = 1
        self.screen_center = (WIDTH/2, HEIGHT/2)
        self.com_x = 0
        self.com_y = 0


yyy = qqq()


class Balls:
    def __init__(self, radius, colour, preset_x, preset_y, preset_velx, preset_vely, name):
        self.radius = radius
        self.mass = (((radius**3)*4)/3)*math.pi

        if preset_x == 0:
            self.x = random.randint(radius, WIDTH-radius)*yyy.scale
        else: self.x = preset_x

        if preset_y == 0:
            self.y = random.randint(radius, HEIGHT-radius)*yyy.scale
        else: self.y = preset_y

        if preset_velx == 0:
            self.velx = random.randint(-4, 4)/4
        else: self.velx = preset_velx

        if preset_vely == 0:
            self.vely = random.randint(-4, 4)/4
        else: self.vely = preset_vely

        self.colour = colour
        self.name = name

    def draw(self):
        arcade.draw_circle_filled((self.x-yyy.com_x)/yyy.scale, (self.y-yyy.com_y)/yyy.scale, round(self.radius/yyy.scale),
                                  self.colour)
        arcade.draw_text("{}".format(self.name), (self.x-yyy.com_y)/yyy.scale - 6, (self.y-yyy.com_y)/yyy.scale + 8,
                         self.colour)


ball = Balls(100, (255, 255, 255), 0, 0, 10, 10, "earth")
b1 = Balls(100, (255, 100, 10), 0, 0, 10, 10, "akjrfn")


class Game(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT)
        self.ball_list = [ball]
        self.ticker = 0
        self.border_sin = 0
        self.delta_time = 1/360

    def on_draw(self):
        arcade.start_render()
        for b in self.ball_list:
            b.draw()

    def update(self, delta_time):
        tempx = (ball.x-yyy.com_x) / (WIDTH/2)
        tempy = (ball.y-yyy.com_y) / (HEIGHT/2)
        if tempx > tempy:
            yyy.scale = tempx
        else:
            yyy.scale = tempy

        for q in self.ball_list:
            q.x += q.velx
            q.y += q.vely


def main():
    arcade.run()


game = Game()

main()


"""

        mass_x = 0
        mass_y = 0
        length_x = 0
        length_y = 0

        for b in self.ball_list:
            mass_x += b.mass * b.x
            mass_y += b.mass * b.y
            length_x += b.x
            length_y += b.y
        yyy.com_x = mass_x / length_x
        yyy.com_y = mass_y / length_y

        self.ticker += 0.01
        self.border_sin = yyy.scale/5 * math.sin(self.ticker) + yyy.scale/5
        tempx = 0
        tempy = 0
        bx = None
        by = None
        for b in self.ball_list:
            if tempx < abs(WIDTH/2-(b.x/yyy.scale)):
                tempx = abs(WIDTH/2-b.x/yyy.scale)
                bx = b
            if tempy < abs(HEIGHT/2-b.y/yyy.scale):
                tempy = abs(HEIGHT/2-b.y/yyy.scale)
                by = b
            b.x += b.velx
            b.y += b.vely
            for o in self.ball_list:
                if b != o:
                    a = G_CONST*o.mass / (get_vector(b.x, b.y, o.x, o.y))**2
                    b.velx = a * ((b.x-o.x)/(b.y-o.y))
                    b.vely = a * ((b.y-o.y)/(b.x-o.x))
                    if get_vector(b.x, b.y, o.x, o.y) < b.radius + o.radius:
                        if b.mass > o.mass:
                            b.velx = b.velx + o.velx * (o.mass/b.mass)
                            b.vely = b.vely + o.vely * (o.mass/b.mass)
                            b.mass = b.mass + o.mass
                            self.ball_list.remove(o)
                        elif b.mass < o.mass:
                            o.velx = o.velx + b.velx * (b.mass / o.mass)
                            o.vely = o.vely + b.vely * (b.mass / o.mass)
                            o.mass = o.mass + b.mass
                            self.ball_list.remove(b)
        if tempy > tempx:
            yyy.scale = abs((WIDTH/2)-(by.y/yyy.scale)-30)/WIDTH
        else: yyy.scale = abs(HEIGHT-(bx.x/yyy.scale)-30)/HEIGHT
        if yyy.scale < 1:
            yyy.scale = 1
        print("X pos of earth: {}".format(ball.x/yyy.scale))
        print(" Y of earth: {}".format(ball.y/yyy.scale))

"""