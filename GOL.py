

import random
import pyglet
from pyglet import graphics,gl

from copy import deepcopy

"""
g = [1,2,3,4,5,6]

t = enumerate(g)

d = {'0':1,'1':2,'2':3,'3':4,'4':5,'5':6}

print([k for v,k in d.items()])
"""







# Data as a list. [X : int, Y : int, Counter : int]
#  [x, y, counter]
# So, there will be lists of points inside the alive_cells list.

gospers_glider_gun = [[1,5],[1,6],[2,5],[2,6],
                      [11,6],[11,5],[11,4],[12,3],[12,7],[13,2],[13,8],[14,2],[14,8],
                      [15,5],
                      [16,3], [16,7], [17,4], [17,5],[17,6],[17,7],[18,5],
                       [21,6],[21,7],[21,8],[22,6],[22,7],[22,8],[23,5],[23,9],
                      [25,4],[25,5],
                      [25,9],[25,10],
                      [35,7],[35,8],[36,7],[36,8]]

for x in gospers_glider_gun:
    x.append(0)

config = gl.Config(double_buffer=False)

window = pyglet.window.Window(640, 480, config=config, resizable=True)

class Holder:
    def __init__(self):
        self.alive_cells = [[40,40,0],[41,41,0],[42,40,0],[39,41,0]]



h=Holder()

chunks = []

def in_range(a,b): return abs(a[0]-b[0])<2 and abs(a[1]-b[1])<2 and a[0] != b[0] and a[1]!=b[1]

def points_around_cell(cell):
    x,y = cell[0],cell[1]
    return [[x-1,y,0],[x+1,y,0],[x-1,y+1,0],[x+1,y-1,0],[x-1,y-1,0],[x+1,y+1,0],[x,y+1,0],[x,y-1,0]]

@window.event
def on_draw():
    window.clear()
    for p in h.alive_cells:
        graphics.draw(1, pyglet.gl.GL_POINTS, ('v2i', (p[0], p[1])))

def this_update(x,y):
    around_p=[]
    no_dupe_around_p = []
    for cell in h.alive_cells:
        cell[2] = 0
        for p in points_around_cell(cell):
            around_p.append(p)
    for point in around_p:
        if point not in no_dupe_around_p: no_dupe_around_p.append(point)
        if point in h.alive_cells:
            around_p.pop(around_p.index(point))
    for cell in h.alive_cells:
        for x in no_dupe_around_p:
            if in_range(cell,x):
                x[2]+=1
        for llec in h.alive_cells:
            if in_range(cell, llec) and cell != llec:
                cell[2] +=1

        if cell[2]<2 or cell[2]>3:
            h.alive_cells.pop(h.alive_cells.index(cell))
    for p in no_dupe_around_p:
        if p[2]==3:
            h.alive_cells.append(p)
    checked = []
    for e in h.alive_cells:
        if e not in checked:
            checked.append(e)
    h.alive_cells = checked



key = pyglet.window.key

@window.event
def on_key_press(key_,modifiers):
    if key_ == key.ENTER:
        for x in range(100):
            h.alive_cells.append([random.randint(80,560), random.randint(80,400), 0])

    if key_ == key.G:

        gosper = deepcopy(gospers_glider_gun)

        x=random.randint(80,560)
        y=random.randint(80,400)

        for cell in gosper:
            cell[0] += x
            cell[1] += y

        h.alive_cells += gosper


pyglet.clock.schedule(this_update,1/60)

pyglet.app.run()
