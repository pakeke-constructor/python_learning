
import arcade
import random
import math
import time



WIDTH = 1200
HEIGHT = 800

ROOT_2 = 2**0.5


def get_vector(x1, y1, x2, y2):
    return math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))


class Evolution:
    def __init__(self, generation, name, speed, colour, border_view_radius, border_stop_running_radius, wandering_vector,
                 enemy_view_radius, enemy_stop_running_radius, radius_difference_to_escape, eat_view_radius, radius_difference_to_eat,
                 node_view_radius, genetic_shift):
        self.genetic_shift = genetic_shift
        self.generation = generation+1
        self.parent = name
        self.name = None
        self.colour = colour
        self.border_view_radius = border_view_radius
        self.border_stop_running_radius = border_stop_running_radius

        self.wandering_vector = wandering_vector

        self.enemy_view_radius = enemy_view_radius
        self.enemy_stop_running_radius = enemy_stop_running_radius

        self.radius_difference_to_escape = radius_difference_to_escape

        self.eat_view_radius = eat_view_radius
        self.radius_difference_to_eat = radius_difference_to_eat

        self.node_view_radius = node_view_radius

        self.speed = speed
        self.wandering_vector = None

    def create_cell(self, number):
        sel = self
        game.cell_dict[game.cell_number] = Cell(2, "random_location")

        def create_new(cell, number):
            game.cell_dict[game.cell_number] = Cell(2, "random_location")
            cell.name = "F{}-{}".format(sel.generation, number)
            cell.parent = sel.parent
            cell.colour = (sel.colour[0]+random.randint(-10, 10), sel.colour[1]+random.randint(-10, 10), sel.colour[2]+random.randint(-10, 10))
            cell.wandering_vector = [cell.wandering_vector[0]+random.randint(-20, 20), cell.wandering_vector[1]+random.uniform(-20*sel.genetic_shift, 20*sel.genetic_shift)]

            cell.border_view_radius = sel.border_view_radius + random.uniform(-2*sel.genetic_shift, 2*sel.genetic_shift)
            cell.border_stop_running_radius = sel.border_stop_running_radius + random.uniform(-2*sel.genetic_shift, 2*sel.genetic_shift)

            cell.speed = sel.speed + random.uniform(-0.05*sel.genetic_shift, 0.05*sel.genetic_shift)

            cell.radius_difference_to_escape = sel.radius_difference_to_escape + random.uniform(-0.1*sel.genetic_shift, 0.1*sel.genetic_shift)
            cell.radius_difference_to_eat = sel.radius_difference_to_eat + random.uniform(-0.1*sel.genetic_shift, 0.1*sel.genetic_shift)

            cell.eat_view_radius = sel.eat_view_radius + random.uniform(-2*sel.genetic_shift, 2*sel.genetic_shift)
            cell.enemy_view_radius = sel.enemy_view_radius + random.uniform(-2*sel.genetic_shift, 2*sel.genetic_shift)
            cell.enemy_stop_running_radius = sel.enemy_view_radius + random.uniform(-2*sel.genetic_shift, 2*sel.genetic_shift)

            cell.node_view_radius = sel.node_view_radius + random.randint(-2*sel.genetic_shift, 2*sel.genetic_shift)

            cell.genetic_shift = sel.genetic_shift + random.uniform(-0.01, 0.01)

        create_new(game.cell_dict[game.cell_number], number)


class Cell:
    def __init__(self, speed, location):

        self.temp_target_x = None
        self.temp_target_y = None
        self.temp_closest_node = 1
        self.running_from_edge = False
        self.running_from_enemy = False

        self.acc = speed
        self.mass = 16

        if location == "random_location":
            self.radius = 4
        else:
            self.radius = 0.000001
        if location == "random_location":
            self.cellx = random.randint(0+self.radius, WIDTH-self.radius)
            self.celly = random.randint(0+self.radius, HEIGHT-self.radius)
        else:
            self.cellx = 0
            self.celly = 1000000
        self.x_velocity = 0
        self.y_velocity = 0
        self.colour = (random.randint(50,255), random.randint(50,255),random.randint(50,255))
        self.tilt = 0
        names = ["A", "B", "C", "D", "E", "F", "G", "Q", "H", "I", "j", "K", "L", "M", "N", "O", "P", "Q",
                 "R", "s", "T", "U", "V", "W", "x", "Y", "Z", "0", "ETC", "OBV", "T9", "G9", "F7", "VV", "T6", "UJP",
                 "FE8", "DD1", "DO2","LO5", "VXX", "PXX", "DXX", "L88", "Q22", "P83", "DLF", "8DJ", "LL7", "44X", "W3",
                 "IO", "IO2", "IO3", "O4", "7U", "8V", "9Q", "R6", "R4", "R8", "R9", "RQ", "Q1", "::C", "C-7", ":H:",
                 "?F", "P0X", "44I", "@B", "@Q", "@I", "@KD", "33^D", "R5", "MC%", "$Y", "::Y", "::N", "N1", "N2", "N2",
                 "N3", "N10", "U45", "33X", "XJ", "**U", "**G", "T8", "T-5", "T-4", "T-3", "T-2", "T-1", "T-0", "T-6",
                 "T-8"]
        self.name = random.choice(names)

        # AI:
        self.speed = 1  # Greater the speed, the faster rate the cell will lost mass. speed also scales opposite mass.
        self.speed_mod = 1

        self.border_view_radius = 10
        self.border_stop_running_radius = 20

        self.wandering_vector = [random.randint(0, WIDTH), random.randint(0, HEIGHT)]
        # This is the location the cell will travel to if there is nothing else to do. WIDTH/2 and HEIGHT/2 are optimal.

        self.target_x = WIDTH/2
        self.target_y = HEIGHT/2

        self.enemy_view_radius = 100
        self.enemy_stop_running_radius = 120
        self.radius_difference_to_escape = 0.2

        self.eat_view_radius = 100
        self.radius_difference_to_eat = 0.3

        self.node_view_radius = 250
        self.current_view_radius = self.border_view_radius
        self.current_view_radius_colour = (0, 0, 0)
        self.generation = 1

        self.genetic_shift = 1

    def draw(self):
        arcade.draw_circle_filled(self.cellx, self.celly, round(self.radius, 0), self.colour)
        arcade.draw_circle_outline(self.cellx, self.celly, self.current_view_radius, self.current_view_radius_colour)
        arcade.draw_line(self.cellx, self.celly, game.nodes[self.temp_closest_node].nodex, game.nodes[self.temp_closest_node].nodey, (0, 50, 0))
        arcade.draw_line(self.cellx, self.celly, self.target_x, self.target_y, (0, 0, 255))
        if self.running_from_edge:
            arcade.draw_circle_outline(self.cellx,self.celly, 10, (200, 0, 0))
            arcade.draw_text("!", self.cellx-20, self.celly-5, (255, 0, 0), bold=True)
        arcade.draw_text("{}".format(self.name), self.cellx - 15, self.celly + 8, (255, 255, 255))


class Node:
    def __init__(self, border):
        border = border
        a = (int(round((3-border)+WIDTH//2)))
        b = int((round((border-3)+WIDTH//2)))
        c = int(round((3-border)+HEIGHT//2))
        d = int((round((border-3)+HEIGHT//2)))
        self.nodex = random.randint(a, b)
        self.nodey = random.randint(c, d)
        self.colour = (random.randint(0,255),random.randint(0, 255), random.randint(0,255))

    def draw(self):
        arcade.draw_rectangle_filled(self.nodex, self.nodey, 4, 4, (255, 0,0))


cel_1 = Cell(2, "random location")
cel_2 = Cell(2, "random location")
cel_3 = Cell(2, "random location")
cel_4 = Cell(2, "random location")
cel_5 = Cell(2, "random location")
cel_6 = Cell(2, "random location")
cel_7 = Cell(2, "random location")
cel_8 = Cell(2, "random location")
cel_9 = Cell(2, "random location")
cel_10 = Cell(2, "random location")
cel_11 = Cell(2, "random location")
cel_12 = Cell(2, "random location")
cel_13 = Cell(2, "random location")
cel_14 = Cell(2, "random location")
cel_15 = Cell(2, "random location")
cel_16 = Cell(2, "random location")
cel_17 = Cell(2, "random location")
cel_18 = Cell(2, "random location")
cel_19 = Cell(2, "random location")
cel_20 = Cell(2, "random location")
cel_21 = Cell(2, "random location")
cel_22 = Cell(2, "random location")
cel_23 = Cell(2, "random location")
cel_24 = Cell(2, "random location")

dead_cell = Cell(0, "")

node_1 = Node(math.sqrt((WIDTH/2)**2 + (HEIGHT/2)**2))
node_2 = Node(math.sqrt((WIDTH/2)**2 + (HEIGHT/2)**2))
node_3 = Node(math.sqrt((WIDTH/2)**2 + (HEIGHT/2)**2))
node_4 = Node(math.sqrt((WIDTH/2)**2 + (HEIGHT/2)**2))
node_5 = Node(math.sqrt((WIDTH/2)**2 + (HEIGHT/2)**2))
node_6 = Node(math.sqrt((WIDTH/2)**2 + (HEIGHT/2)**2))
node_7 = Node(math.sqrt((WIDTH/2)**2 + (HEIGHT/2)**2))
node_8 = Node(math.sqrt((WIDTH/2)**2 + (HEIGHT/2)**2))
n = Node(math.sqrt((WIDTH/2)**2 + (HEIGHT/2)**2))
q = Node(math.sqrt((WIDTH/2)**2 + (HEIGHT/2)**2))
w= Node(math.sqrt((WIDTH/2)**2 + (HEIGHT/2)**2))
e= Node(math.sqrt((WIDTH/2)**2 + (HEIGHT/2)**2))
r= Node(math.sqrt((WIDTH/2)**2 + (HEIGHT/2)**2))
t= Node(math.sqrt((WIDTH/2)**2 + (HEIGHT/2)**2))
y= Node(math.sqrt((WIDTH/2)**2 + (HEIGHT/2)**2))
u= Node(math.sqrt((WIDTH/2)**2 + (HEIGHT/2)**2))


class Game(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "the battle of agar")
        self.delta_border = 0.1

        self.winner = None
        self.round_over = False

        self.speed_modifier = 1

        self.cell_number = 1
        self.cell_dict = {}

        self.unpaused = True

        self.node_dict = {}
        self.node_number = 1

        self.border = math.sqrt((WIDTH/2)**2 + (HEIGHT/2)**2)

        self.cells = [cel_1, cel_2, cel_3, cel_4, cel_5, cel_6, cel_7, cel_8, cel_9, cel_10, cel_11, cel_12, cel_13, cel_14, cel_15, cel_16, cel_17, cel_18, cel_19, cel_20, cel_21,
                      cel_22, cel_23, cel_24]
        self.nodes = [node_1, node_2, node_3, node_4, node_5, node_6, node_7, node_8, n, q, w, e, r, t, y, u]

    def spawn_cells(self):
        for i in range(len(self.cells)):
            this_cell = self.cells[i]
            this_cell.cellx = random.randint(30, WIDTH-30)
            this_cell.celly = random.randint(30, HEIGHT-30)
            this_cell.radius = 4
            this_cell.mass = 16

    def new_node(self, n):
        self.node_dict[self.node_number] = Node(self.border)
        self.nodes[n] = (self.node_dict[self.node_number])
        self.node_number += 1

    def get_cell_vector(self, x, y):
        return math.sqrt((x.cellx - y.cellx)**2 + (x.celly - y.celly)**2)

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color((40, 40, 40))
        arcade.draw_text("TARGET CELL", cel_1.cellx, cel_1.celly, (255, 0, 0), font_size=20)
        arcade.draw_text("Border = {}".format(round(self.border)), WIDTH - (WIDTH - 70), HEIGHT - 50, (255, 0, 0))
        arcade.draw_rectangle_outline(WIDTH/2, HEIGHT/2, self.border*ROOT_2, self.border*ROOT_2, (0, 70, 0))
        arcade.draw_line(WIDTH/2, 0, WIDTH/2, HEIGHT, (0, 80, 0))
        arcade.draw_line(0, HEIGHT/2, WIDTH, HEIGHT/2, (0, 80, 0))
        arcade.draw_circle_outline((WIDTH/2), (HEIGHT/2), self.border, (255, 255, 255))
        if self.round_over:
            arcade.draw_text(self.winner, WIDTH/2, HEIGHT-100, (255, 255, 255), bold=True, font_size=20)
        for cell in self.cells:
            if cell != dead_cell:
                cell.draw()
        for x in range(len(self.nodes)):
            self.nodes[x].draw()

    def update(self, delta_time: float):
        dead_cell_number = 0
        winner = None
        if self.border < 80:
            self.delta_border = 0
        for cell in self.cells:
            if cell == dead_cell:
                dead_cell_number += 1
                cell.name = "Dead cell"
        if len(self.cells)-dead_cell_number == 1:
            self.unpaused = False
            for x in self.cells:
                if x != dead_cell:
                    self.winner = "{} HAS WON, AND WILL PASS ON GENES".format(x.name)
                    winner = x
            self.new_cells(winner)
            #time.sleep(5/self.speed_modifier)

        if self.unpaused:
            self.border -= (self.delta_border * self.speed_modifier)
            for cell in self.cells:
                if cell == dead_cell:
                    dead_cell_number += 1

                if cell != dead_cell:
                    if cell.radius <= 0.1:
                        print("DELETED BY SIZE")
                        self.cells[self.cells.index(cell)] = dead_cell
                    cell.radius -= (0.0002 * (cell.speed ** 3))*self.speed_modifier
                    cell.target_x = cell.wandering_vector[0]
                    cell.target_y = cell.wandering_vector[1]
                    """ Engine: cells are deleted when they touch border """
                    if get_vector(cell.cellx, cell.celly, WIDTH/2, HEIGHT/2) > self.border:
                        cell.radius -= 0.1
                    if cell.radius > 0:
                        cell.speed_mod = (1 / cell.radius) ** 0.7
                    minimum = 1000
                    for m in range(len(self.nodes)):
                        if minimum > get_vector(self.nodes[m].nodex, self.nodes[m].nodey, cell.cellx, cell.celly):
                            minimum = get_vector(self.nodes[m].nodex, self.nodes[m].nodey, cell.cellx, cell.celly)
                            cell.temp_closest_node = m
                    if cell.node_view_radius > get_vector(cell.cellx, cell.celly,
                                                    self.nodes[cell.temp_closest_node].nodex, self.nodes[cell.temp_closest_node].nodey):
                        cell.current_view_radius_colour = (0, 0, 0, 60)
                        cell.current_view_radius = cell.node_view_radius
                        cell.target_x = self.nodes[cell.temp_closest_node].nodex
                        cell.target_y = self.nodes[cell.temp_closest_node].nodey
                    """ Engine: for cells consuming each other """
                    for oppo in self.cells:
                        if cell != oppo and get_vector(cell.cellx, cell.celly, oppo.cellx, oppo.celly) < 200:
                            if math.sqrt((cell.cellx-oppo.cellx)**2 + (cell.celly-oppo.celly)**2) < (cell.radius + oppo.radius):
                                if cell.radius-1 > oppo.radius:
                                    cell.cellx = (cell.cellx + cell.cellx) / 2
                                    cell.celly = (oppo.celly + cell.celly) / 2
                                    cell.radius += (oppo.radius/2)
                                    self.cells[self.cells.index(oppo)] = dead_cell
                                elif cell.radius < oppo.radius-1:
                                    oppo.cellx = (cell.cellx + oppo.cellx) / 2
                                    oppo.celly = (oppo.celly + cell.celly) / 2
                                    oppo.radius += (cell.radius/2)
                                    self.cells[self.cells.index(cell)] = dead_cell
                                """ Chasing other cells to eat:  """
                            if self.get_cell_vector(cell, oppo) < cell.eat_view_radius and (cell.radius -
                                cell.radius_difference_to_eat) > oppo.radius:
                                cell.target_x = oppo.cellx
                                cell.target_y = oppo.celly
                                cell.current_view_radius = cell.eat_view_radius
                                cell.current_view_radius_colour = (0, 100, 0)
                            """ Running away from other cells: """
                            if self.get_cell_vector(cell, oppo) < cell.enemy_view_radius and cell.radius < \
                                oppo.radius - cell.radius_difference_to_escape:
                                cell.running_from_enemy = True
                            elif self.get_cell_vector(cell, oppo) > cell.enemy_stop_running_radius:
                                cell.running_from_enemy = False
                            if cell.running_from_enemy:
                                m = (oppo.celly - cell.celly) / (oppo.cellx - cell.cellx)
                                c = cell.celly - (m * cell.cellx)
                                x = (cell.cellx - oppo.cellx) * 500
                                cell.target_x = x
                                cell.target_y = m * x + c
                                cell.temp_target_x = x
                                cell.temp_target_y = m * x + c
                                cell.current_view_radius = cell.enemy_view_radius
                                cell.current_view_radius_colour = (100, 0, 0)
                                """ Running away from border: """
                    if cell.border_view_radius + get_vector(WIDTH/2, HEIGHT/2, cell.cellx,
                                                                      cell.celly) > self.border:
                        cell.running_from_edge = True
                    elif cell.border_stop_running_radius + get_vector(WIDTH/2, HEIGHT/2, cell.cellx,
                                                                      cell.celly) < self.border:
                        cell.running_from_edge = False
                    if cell.running_from_edge:
                        cell.target_x = WIDTH / 2
                        cell.target_y = HEIGHT / 2

                    if cell.running_from_edge and cell.running_from_enemy:
                        x1mag = (cell.temp_target_x) / math.sqrt(cell.temp_target_x**2 + cell.temp_target_y**2)
                        y1mag = (cell.temp_target_y) / math.sqrt(cell.temp_target_x**2 + cell.temp_target_y**2)
                        x2mag = (cell.target_x) / math.sqrt(cell.target_x**2 + cell.target_y**2)
                        y2mag = (cell.target_y) / math.sqrt(cell.target_x**2 + cell.target_y**2)
                        cell.target_x = (x1mag + x2mag)
                        cell.target_y = (y2mag + y1mag)

                        """
                        theta = math.atan(cell.temp_target_y/cell.temp_target_x)
                        beta = math.atan(cell.target_y/cell.target_x)
                        angle = (theta + beta) / 2
                        cell.target_y = (math.pi/6) * math.tan(angle)
                        cell.target_x = cell.target_y / math.tan(angle)
                        """
                    vel_x = (cell.target_x - cell.cellx) / (
                        abs(cell.target_x - cell.cellx) + abs(cell.target_y - cell.celly))
                    vel_y = (cell.target_y - cell.celly) / (
                        abs(cell.target_x - cell.cellx) + abs(cell.target_y - cell.celly))

                    cell.cellx += (vel_x * cell.speed * cell.speed_mod * self.speed_modifier)
                    cell.celly += (vel_y * cell.speed * cell.speed_mod * self.speed_modifier)

                    for n in range(len(self.nodes)):
                        if get_vector(self.nodes[n].nodex, self.nodes[n].nodey, (WIDTH / 2),
                                       (HEIGHT / 2)) > self.border:
                            self.new_node(n)
                        if get_vector(cell.cellx, cell.celly, self.nodes[n].nodex,
                                       self.nodes[n].nodey) < cell.radius:
                            self.new_node(n)
                            if self.border > 80:
                                cell.radius += 0.35

    def on_key_press(self, key, modifiers: int):
        if key == arcade.key.ENTER:
            if self.unpaused:
                self.unpaused = False
            else:
                self.unpaused = True
        if key == arcade.key.S:
            self.spawn_cells()
        if key == arcade.key.BRACKETLEFT:
            self.speed_modifier -= 1
        if key == arcade.key.BRACKETRIGHT:
            self.speed_modifier\
                += 1

    def new_cells(self, cell):
        evolution = Evolution(cell.generation, cell.name, cell.speed, cell.colour, cell.border_view_radius,
                              cell.border_stop_running_radius, cell.wandering_vector,
                              cell.enemy_view_radius, cell.enemy_stop_running_radius, cell.radius_difference_to_escape,
                              cell.eat_view_radius, cell.radius_difference_to_eat,
                              cell.node_view_radius, cell.genetic_shift)
        self.cells.clear()
        self.cells.append(evolution.create_cell(1))
        self.cells.append(evolution.create_cell(2))
        self.cells.append(evolution.create_cell(3))
        self.cells.append(evolution.create_cell(4))
        self.cells.append(evolution.create_cell(5))
        self.cells.append(evolution.create_cell(6))

game = Game()


def main():
    arcade.run()

"""
game.new_cells(cel_1)
print(len(game.cells))
print(game.cells)
for cell in game.cells:
    print(cell.name)
"""
game.spawn_cells()


main()

"""


                if target_x > 0 and target_x_2 > 0:
                    cell.x_velocity = ((target_x - cell.cellx)/((target_x - cell.cellx)+(target_y - cell.celly)))
                    cell.y_velocity = ((target_y - cell.cellx)/((target_x - cell.cellx)+(target_y - cell.celly)))
                else:
                    theta = math.atan(target_y/target_x)
                    cell.x_velocity = math.sin(theta) * cell.speed
                    cell.y_velocity = math.cos(theta) * cell.speed


"""



"""

cell.x_velocity = (target_x - cell.cellx) / (
                                (target_x - cell.cellx) + (target_y - cell.celly))
                    cell.y_velocity = (target_y - cell.cellx) / (
                                (target_x - cell.cellx) + (target_y - cell.celly))
"""