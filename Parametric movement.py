import arcade

from math import *
import math

class Holder:
    t=0  # value of parametric input for x and y
    scale = 5
    pos_x = 0  # x,y displacement of functions on screen by mouse drag
    pos_y = 0


class Param:
    param_list = []

    def __init__(self, eqx, eqy, colour : tuple):
        self.eqx = eqx
        self.eqy = eqy
        self.colour = colour

        self.prev_x = 0
        self.prev_y = 0

        self.x = 0
        self.y = 0
        Param.param_list.append(self)

    def draw(self):
        arcade.draw_line(((self.x/Holder.scale)+400)+Holder.pos_x, ((self.y/Holder.scale)+300)+Holder.pos_y, ((self.prev_x/Holder.scale)+400)+Holder.pos_x,
                         ((self.prev_y/Holder.scale)+300)+Holder.pos_y,  self.colour, border_width=2)

    def update(self):
        self.prev_x = self.x
        self.prev_y = self.y

        self.x += self.eqx(Holder.t)
        self.y += self.eqy(Holder.t)


s1 = lambda x : x*sin(x)
c1 = lambda x : x*cos(x)

s = lambda x : 10*sin(x)
c = lambda x : 10*cos(x)
u = lambda x : tan(x)/10
new_s = lambda x : sin(x)*x

sq = lambda x : 10*sin(x**2)
sw = lambda x : 10*sin(x**0.5)
cw = lambda x : x**3

f = lambda x : 10*sin(x**3)

green = Param(s1,c1,(0,255,0))
white = Param(c,new_s, (255, 255, 255,120))
red = Param(c, f, (255, 0, 0,120))
blue = Param(sw,c, (0,0,255,120))

key = arcade.key

class Game(arcade.Window):
    def __init__(self):
        self.fllscrn = False
        super().__init__(800,600,"parametric movement", fullscreen=self.fllscrn,resizable=True)

    def on_draw(self):
        for x in Param.param_list:
            x.draw()

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        Holder.scale -= scroll_y/20
        arcade.start_render()

    def on_mouse_drag(self, x: float, y: float, dx: float, dy: float, buttons: int, modifiers: int):
        Holder.pos_x += dx; Holder.pos_y += dy; arcade.start_render()

    def on_key_press(self, symbol : int, modifiers: int):
        if symbol == key.F:
            self.fllscrn = not self.fllscrn
            self.set_fullscreen(self.fllscrn)
        if symbol == key.ENTER:
            Holder.t = 0
            arcade.start_render()
            arcade.start_render()
            arcade.start_render()

    def update(self,d):
        for x in Param.param_list:
            x.update()
            Holder.t+=0.01

game = Game()
def main():
    arcade.run()

if __name__ == '__main__':
    main()