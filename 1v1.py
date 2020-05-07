
import arcade
import math
import random

class Holder:
    def __init__(self, tt):
        x = tt
        self.wid_th = 1000
        self.hei_ght = 800
        self.ticker = 0

def draw_crown(x,y, player):
    arcade.draw_triangle_filled(x-12, y+14, x-6, y+20, x, y+14, player.colour)
    arcade.draw_triangle_filled(x-6, y+14, x, y+20, x+6, y+14, player.colour)
    arcade.draw_triangle_filled(x+12, y+14, x+6, y+20, x, y+14, player.colour)


held = Holder(1)


class Platform:
    def __init__(self, amplitude_moving, start_x, end_x, y_level, colour):
        self.start_x = start_x
        self.end_x = end_x
        self.y_level = y_level
        self.colour = colour
        self.amplitude = amplitude_moving
        self.original_y_level = self.y_level

    def draw(self):
        arcade.draw_line(self.start_x, self.y_level, self.end_x, self.y_level, self.colour, border_width=4)


platform_1 = Platform(0, 40, held.wid_th/3, 90, (255, 255, 255))
platform_2 = Platform(0, held.wid_th/2, held.wid_th-30, 70, (255, 255, 255))
platform_3 = Platform(0, 100, held.wid_th/3, held.hei_ght/2, (255, 255, 255))
platform_4 = Platform(80, 200, 600, held.hei_ght/3, (255, 255, 255))

class Player:
    def __init__(self, up_key, down_key, left_key, right_key, agility, jump_boost, colour, mody, spawn_x, spawn_y):
        self.up = up_key
        self.down = down_key
        self.left = left_key
        self.right = right_key

        self.spawn_x = spawn_x
        self.spawn_y = spawn_y

        self.upq = False
        self.downq = False
        self.leftq = False
        self.rightq = False

        self.agility = agility
        self.jump = jump_boost
        self.colour = colour

        self.x = held.wid_th/2
        self.y = held.hei_ght/2

        self.dx = 0
        self.dy = 0
        self.wincount = 0
        self.crown = False

        self.text_mod_y = mody

    def draw_self(self):
        if game.middle_pull:
            arcade.draw_line(held.wid_th, held.hei_ght, self.x, self.y, (60, 60, 60))
        arcade.draw_rectangle_filled(self.x, self.y, 25, 25, self.colour)
        arcade.draw_text("Points ye boi: {}".format(round(self.wincount)), 50, held.hei_ght-50-self.text_mod_y, self.colour)
        if self.crown:
            draw_crown(self.x, self.y, self)


class Boost:
    def __init__(self, type):
        self.type = type


class Game(arcade.Window):

    def __init__(self, gamemode):
        super().__init__(held.wid_th, held.hei_ght, "Bounce", resizable=True)
        self.middle_pull = False

        self.gamemode = gamemode

        self.player_list = [p1, p2, p3]

        self.platform_list = [platform_1, platform_2, platform_3, platform_4]

    def on_draw(self):
        arcade.start_render()
        for pl in self.platform_list:
            pl.draw()
        for p in self.player_list:
            p.draw_self()

    def on_key_press(self, key: int, modifiers: int):
        for p in self.player_list:
            if key == p.up:
                p.upq = True
            if key == p.down:
                p.downq = True
            if key == p.left:
                p.leftq = True
            if key == p.right:
                p.rightq = True

    def on_key_release(self, key: int, modifiers: int):
        for p in self.player_list:
            if key == p.up:
                p.upq = False
            if key == p.down:
                p.downq = False
            if key == p.left:
                p.leftq = False
            if key == p.right:
                p.rightq = False

    def update(self, delta_time):
        held.ticker += 0.01
        for pl in self.platform_list:
            if pl.amplitude != 0:
                pl.y_level = math.sin(2*held.ticker)*pl.amplitude + pl.original_y_level
        for p in self.player_list:
            p.dx *= 0.9
            if p.leftq:
                p.dx -= p.agility
            if p.rightq:
                p.dx += p.agility
            if p.downq:
                p.dy -= p.agility*2
                p.y -= 16
            if p.upq and p.y < 18:
                p.dy = p.jump
                p.y += 1
            if p.x+15 > held.wid_th:
                p.dx *= -0.3
                p.x = held.wid_th-15
            if p.x-15 < 0:
                p.dx *= -0.3
                p.x = 15

            p.dy -= 1.5
            p.x += p.dx
            p.y += p.dy
            if p.crown:
                p.wincount += 0.05
            for o in self.player_list:
                if o != p:
                    if abs(o.x - p.x) < 30 and 20 > p.y - o.y > 1:
                        if self.gamemode == "deathmatch":
                            win(p)
                            for p in self.player_list:
                                p.crown = False
                        if self.gamemode == "crowns":
                            if not p1.crown and not p2.crown and not p3.crown:
                                random.choice(self.player_list).crown = True
                            o.x = o.spawn_x
                            o.y = o.spawn_y
                            if o.crown:
                                o.crown = False
                                p.crown = True

            if p.y < 15:
                p.y = 15.1
            for pl in self.platform_list:
                if pl.start_x < p.x < pl.end_x and abs((pl.y_level+4) - p.y) < 10 and p.dy < 0:
                    p.y = pl.y_level + 13
                    p.dy = 0
                    if p.upq:
                        p.dy = p.jump
                        p.y += 1


def win(player):
    for p in game.player_list:
        p.x = p.spawn_x
        p.y = p.spawn_y
    player.wincount += 1


p1 = Player(arcade.key.W, arcade.key.S, arcade.key.A, arcade.key.D, 1, 20, (50, 255, 255), 0, held.wid_th/4, held.hei_ght/2)

p2 = Player(arcade.key.UP, arcade.key.DOWN, arcade.key.LEFT, arcade.key.RIGHT, 1, 20, (50, 255, 100), 50, held.wid_th/4*3, held.hei_ght/2)

p3 = Player(arcade.key.U, arcade.key.J, arcade.key.H, arcade.key.K, 1, 20, (255, 50, 255), 100, held.wid_th/2, held.hei_ght/2)

#
#
#
#
#

game = Game("crowns")

""" 
Current gamemodes:wwaasa
    deathmatch
    crowns
"""
#
#
#
#
#


def main():
    arcade.run()


main()



