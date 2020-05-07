
import arcade
import random
import math

WIDTH = 1280
HEIGHT = 800
G_CONST = 10


class Balls:

    camera_pos_x = 0
    camera_pos_y = 0

    scale = 1

    def __init__(self, radius, colour, mass):
        self.ori_rad = radius
        self.radius = radius

        if mass is not None:
            self.ori_mass = mass
            self.mass = mass
        else:
            self.ori_mass = (self.radius+4)**3
            self.mass = (self.radius + 4) ** 3

        self.ori_colour = colour
        self.ballx = random.uniform(-(WIDTH*Balls.scale)/2, (WIDTH*Balls.scale)/2)
        self.bally = random.uniform(-(HEIGHT*Balls.scale)/2, (HEIGHT*Balls.scale)/2)
        self.velx = random.randint(-4, 4)/4
        self.vely = random.randint(-4, 4)/4
        self.colour = colour

        self.display_x = 0
        self.display_y = 0

    def update(self):
        self.display_x = ((self.ballx-Balls.camera_pos_x)/Balls.scale)+WIDTH/2
        self.display_y = ((self.bally-Balls.camera_pos_y)/Balls.scale)+HEIGHT/2

    def draw(self):
        #arcade.draw_rectangle_filled(self.display_x, self.display_y, (self.radius/Balls.scale)+15, (self.radius/Balls.scale)+15,self.colour)
        arcade.draw_circle_filled(self.display_x, self.display_y, self.radius/Balls.scale + 3, self.colour)


one_3 = Balls(0, (255, 255, 0), None)
one_2 = Balls(0, (255, 255, 0), None)
one = Balls(0, (255, 255, 0), None)
two = Balls(5, (0, 255, 0), 169)
qerteng = Balls(4, (255, 0, 0), 100)
three = Balls(6, (50, 100, 50), 225)
ei = Balls(4, (0, 0, 255), 10000)
anti_mass = Balls(1, (255, 255, 255), -100)
anti_mass2 = Balls(1, (255, 255, 255), -100)
anti_mass3 = Balls(1, (255, 255, 255), -100)
anti_mega = Balls(4, (255, 255, 255), -10000)
half_big = Balls(9, (255, 80, 0), None)
bigg = Balls(120, (10, 50, 50), 800000)
quite_big = Balls(6, (30, 30, 60), 2500)

dist = lambda x1,y1,x2,y2 : math.sqrt((x1-x2)**2 + (y1-y2)**2)

class Game(arcade.Window):
    def __init__(self):
        self.delta_time = 1/30
        super().__init__(WIDTH, HEIGHT, "MY BALLS", fullscreen=False)
        arcade.set_background_color((0, 0, 0))
        self.ball_list = [one, one_2, one_3, bigg]
        self.grab_list = [one, two, qerteng, three, anti_mass, half_big, one, two, qerteng]
        self.timer = 0
        self.timer_max = 0
        self.n = 1
        self.keep_dict = {}
        self.friction = False
        self.gravity = False
        self.lines = False
        self.com_x = 0
        self.com_y = 0
        self.com = False
        self.unpaused = True
        self.view_fields = False
        self.collisions = False

        self.scale = 1
        self.frame_rate = 0



    def cheap_vect(self, x, y):
        return abs(x.ballx - y.ballx)+abs(x.bally - y.bally)

    def get_vectr(self, x, y):
        return self.cheap_vect(x,y)

    def on_draw(self):

        arcade.start_render()
        arcade.draw_text(f"Frames: {round(self.frame_rate)}", 50, HEIGHT-300, (255,255,255,100))
        arcade.draw_text("Balls: {}".format(len(self.ball_list)), 100, 620, (255, 0, 0))
        if self.com:
            for a in self.ball_list:
                arcade.draw_line(a.display_x, a.display_y, self.com_x, self.com_y, (150, 0, 220,120),0.7)

        for a in self.ball_list:
            a.draw()
        if self.view_fields:
            for a in self.ball_list:
                arcade.draw_circle_outline(a.display_x, a.display_y, (a.mass / 6)/Balls.scale,
                                           a.colour, border_width=0.1)

        if self.lines:
            for a in self.ball_list:
                for b in self.ball_list:
                    if a != b:
                        arcade.draw_line(a.display_x, a.display_y, b.display_x, b.display_y, (255, 255, 255,40), 0.1)
        if self.friction:
            arcade.draw_text("friction", WIDTH-100, 100, (255, 0, 0))
        if self.gravity:
            arcade.draw_text("Downwards force: ON", WIDTH-200, 130, (255, 0, 0))

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        Balls.scale -= scroll_y/6

    def on_mouse_drag(self, x: float, y: float, dx: float, dy: float, buttons: int, modifiers: int):
        Balls.camera_pos_x -=dx
        Balls.camera_pos_y -= dy

    def update(self, delta_time):
        self.frame_rate = 1/delta_time
        masses = []
        mass_distances_x = []
        mass_distances_y = []
        if self.unpaused:
            for b in self.ball_list:
                b.update()
                for o in self.ball_list:
                    if b != o:
                        b.velx += (b.ballx - o.ballx)/(100*(b.mass/10000))/(dist(b.ballx,b.bally,o.ballx,o.bally))
                        b.vely += (b.bally - o.bally)/(100*(b.mass/10000))/(dist(b.ballx,b.bally,o.ballx,o.bally))
                        if self.collisions:
                            if dist(b.ballx,b.bally,o.ballx,o.bally) < (b.radius + o.radius):
                                pre_x = b.velx
                                pre_y = b.vely
                                b.velx = ((-0.3*(b.ballx-o.ballx) + 0.7*pre_x)*(100/b.mass))
                                b.vely = ((-0.3*(b.bally-o.bally) + 0.7*pre_y)*(100/b.mass))
                                self.timer = 0

                if self.friction:
                    b.velx * 0.05
                    b.vely * 0.05
                if self.com:
                    masses.append(b.mass)
                    mass_distances_x.append(b.mass*b.display_x)
                    mass_distances_y.append(b.mass*b.display_y)
            for n in self.ball_list:
                n.ballx -= n.velx
                n.bally -= n.vely

            if self.com:
                self.com_x = sum(mass_distances_x)/sum(masses)
                self.com_y = sum(mass_distances_y)/sum(masses)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        for o in range(len(self.ball_list)):
            if self.ball_list[o].radius < math.sqrt((x-self.ball_list[o].ballx)**2+(y-self.ball_list[o].bally)**2) < 30:
                lx = (x - self.ball_list[o].ballx)
                ly = (y - self.ball_list[o].bally)
                self.ball_list[o].velx += 100/(lx+ly)
                self.ball_list[o].vely += 100/(ly+ly)

    def on_key_press(self, key, modifiers: int):
        if key == arcade.key.SPACE:
            self.unpaused = not self.unpaused

        elif key == arcade.key.V:
            self.view_fields = not self.view_fields
        elif key == arcade.key.ENTER:
            for o in range(len(self.ball_list)):
                self.ball_list[o].vely = 0
                self.ball_list[o].velx = 0
                self.timer = 0
        elif key == arcade.key.R:
            for o in range(len(self.ball_list)):
                self.ball_list[o].ballx = random.randint(500, 1100)
                self.ball_list[o].bally = random.randint(200, 600)
                self.ball_list[o].velx = random.randint(-10, 10)/4
                self.ball_list[o].vely = random.randint(-10, 10)/4
                self.ball_list[o].mass = self.ball_list[o].ori_mass
                self.ball_list[o].colour = self.ball_list[o].ori_colour
                self.ball_list[o].radius = self.ball_list[o].ori_rad
                self.timer = 0
        elif key == arcade.key.N:
            self.collisions = not self.collisions
        elif key == arcade.key.E:
            for o in range(len(self.ball_list)):
                self.ball_list[o].colour = (random.randint(0, 255), random.randint(0,255), random.randint(0,255))
                self.ball_list[o].radius = (random.randint(7, 20))
                self.ball_list[o].mass = self.ball_list[o].radius**2
        elif key == arcade.key.W:
            for o in range(len(self.ball_list)):
                self.ball_list[o].vely -= 6
                self.ball_list[o].velx -= 8

        elif key == arcade.key.Q:
            for o in range(len(self.ball_list)):
                self.ball_list[o].velx += 8
                self.ball_list[o].vely -= 6
        elif key == arcade.key.A:
            for o in range(len(self.ball_list)):
                self.ball_list[o].velx += 8
                self.ball_list[o].vely += 6
        elif key == arcade.key.S:
            for o in range(len(self.ball_list)):
                self.ball_list[o].velx -= 8
                self.ball_list[o].vely += 6
        elif key == arcade.key.Z:
            try:
                self.ball_list.pop()
            except:
                print("There are no more balls to remove!")

        elif key == arcade.key.X:
            print(len(self.ball_list))
            t = random.randint(2, 7)
            self.keep_dict[self.n] = Balls(t, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), (t+4)**3)
            self.ball_list.append(self.keep_dict[self.n])
            self.ball_list[len(self.ball_list) - 1].velx = random.random(-6, 6)
            self.ball_list[len(self.ball_list) - 1].vely = random.random(-6, 6)
            self.n += 1
        elif key == arcade.key.F:
            if self.friction:
                self.friction = False
            else:
                self.friction = True
        elif key == arcade.key.G:
            self.gravity = not self.gravity
        elif key == arcade.key.D:
            self.lines = not self.lines
        elif key == arcade.key.C:
            self.com = not self.com





game = Game()


def main():
    arcade.run()


main()




