import arcade
import time
import math

WIDTH = 500
HEIGHT = 500


PI8 = math.pi/8
PI = math.pi


def get_vector(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)


class Game(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "Bounce", resizable=True)
        self.dic = {}
        self.dic_n = 0
        self.bouncer_list = [b]

    def draw(self):
        arcade.start_render()
        for s in range(len(b.spoke_list)-1):
            arcade.draw_line(b.spoke_list[s].x, b.spoke_list[s].y, b.spoke_list[s-1].x, b.spoke_list[s-1].y, (255, 255, 0))

    def update(self, delta_time):
        for b in self.bouncer_list:
            for s in range(len(b.spoke_list)-1):
                b.spoke_list[s].dx = b.spoke_list[s].dx * 0.96
                b.spoke_list[s].dy = b.spoke_list[s].dy * 0.96
                b.spoke_list[s].dy -= 4
                grad_pos = ((b.spoke_list[s].y - b.spoke_list[s - 1].y) / (b.spoke_list[s].x - b.spoke_list[s - 1].x))
                if get_vector(b.spoke_list[s].x, b.spoke_list[s].y, b.spoke_list[s-1].x, b.spoke_list[s-1].y) > b.regulated_spoke_distance:
                    b.spoke_list[s].dx -= ((get_vector(b.spoke_list[s].x, b.spoke_list[s].y, b.spoke_list[s-1].x, b.spoke_list[s-1].y) - b.regulated_spoke_distance)*grad_pos)
                    b.spoke_list[s].dy -= ((get_vector(b.spoke_list[s].x, b.spoke_list[s].y, b.spoke_list[s-1].x, b.spoke_list[s-1].y) - b.regulated_spoke_distance)/grad_pos)

                if get_vector(b.spoke_list[s].x, b.spoke_list[s].y, b.spoke_list[s+1].x, b.spoke_list[s+1].y) > b.regulated_spoke_distance:
                    grad_pos = ((b.spoke_list[s].y-b.spoke_list[s+1].y)/(b.spoke_list[s].x-b.spoke_list[s+1].x))

                    b.spoke_list[s].dx -= ((get_vector(b.spoke_list[s].x, b.spoke_list[s].y, b.spoke_list[s+1].x, b.spoke_list[s+1].y) - b.regulated_spoke_distance)*grad_pos)
                    b.spoke_list[s].dy -= ((get_vector(b.spoke_list[s].x, b.spoke_list[s].y, b.spoke_list[s+1].x, b.spoke_list[s+1].y) - b.regulated_spoke_distance)/grad_pos)

                if get_vector(b.spoke_list[s].x, b.spoke_list[s].y, b.spoke_list[s-1].x, b.spoke_list[s-1].y) < b.regulated_spoke_distance:
                    grad_pos = ((b.spoke_list[s].y-b.spoke_list[s-1].y)/(b.spoke_list[s].x-b.spoke_list[s-1].x))

                    b.spoke_list[s].dx -= ((get_vector(b.spoke_list[s].x, b.spoke_list[s].y, b.spoke_list[s-1].x, b.spoke_list[s-1].y) - b.regulated_spoke_distance)*grad_pos)
                    b.spoke_list[s].dy -= ((get_vector(b.spoke_list[s].x, b.spoke_list[s].y, b.spoke_list[s-1].x, b.spoke_list[s-1].y) - b.regulated_spoke_distance)/grad_pos)

                if get_vector(b.spoke_list[s].x, b.spoke_list[s].y, b.spoke_list[s-1].x, b.spoke_list[s+1].y) < b.regulated_spoke_distance:
                    grad_pos = ((b.spoke_list[s].y-b.spoke_list[s+1].y)/(b.spoke_list[s].x-b.spoke_list[s+1].x))

                    b.spoke_list[s].dx -= ((get_vector(b.spoke_list[s].x, b.spoke_list[s].y, b.spoke_list[s+1].x, b.spoke_list[s-1].y) - b.regulated_spoke_distance)*grad_pos)
                    b.spoke_list[s].dy -= ((get_vector(b.spoke_list[s].x, b.spoke_list[s].y, b.spoke_list[s+1].x, b.spoke_list[s-1].y) - b.regulated_spoke_distance)/grad_pos)
        #
        #
        #
        #
                if get_vector()




class Spoke:
    def __init__(self, length, strength, spoke_number, total_spokes):
        self.length = length
        self.strength = strength
        self.spoke_number = spoke_number
        self.x = math.sin((math.pi/total_spokes) * spoke_number)
        self.y = math.cos((math.pi/total_spokes) * spoke_number)
        self.dx = 0
        self.dy = 0


class Bouncer:
    def __init__(self, spoke_length, spoke_strength, spoke_amount, mass):
        self.spoke_length = spoke_length
        self.spoke_strength = spoke_strength
        self.mass = mass
        self.center_x = WIDTH/2
        self.center_y = HEIGHT/2
        self.spoke_amount = spoke_amount

        self.spoke_dict = {}
        self.dict_n = 0

        self.spoke_list = []

        for x in range(spoke_amount):
            self.spoke_dict[self.dict_n] = Spoke(self.spoke_length, self.spoke_strength, x, self.spoke_amount)
            self.spoke_list.append(self.spoke_dict[self.dict_n])
            self.dict_n += 1

        self.regulated_spoke_distance = math.sqrt((self.spoke_dict[1].x-self.spoke_dict[2].x)**2 + (self.spoke_dict[1].y-self.spoke_dict[2].y)**2)


    def draw(self):

        arcade.draw_line(self.center_x, self.center_y, )




b = Bouncer(10, 1, 30, 10)

g = Game()


def main():

    arcade.run()

main()