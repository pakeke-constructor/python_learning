
import math
import pyglet
WIDTH = 640
HEIGHT = 480




class Handler:
    def __init__(self):
        self._fullscreen = True

        window = pyglet.window.Window(WIDTH, HEIGHT, fullscreen=False)

        handler = dict(a_pressed=False, q_pressed=False, w_pressed=False, s_pressed=False, d_pressed=False,
                            e_pressed=False,

                       xpos=WIDTH/2, ypos=HEIGHT/2, )



        @window.event
        def on_draw():
            window.clear()
            pyglet.text.Label(text="Test", font_size=22, x=handler['xpos'], y=handler['ypos']).draw()

        key = pyglet.window.key
        @window.event
        def on_key_press(_key, modifiers):
            if _key == key.F:
                if window.fullscreen:
                    window.set_fullscreen(fullscreen=False, width=WIDTH, height=HEIGHT)
                else:
                    window.set_fullscreen(fullscreen=True, width=WIDTH, height=HEIGHT)
            if _key == key.A:
                handler['a_pressed'] = True
        @window.event
        def on_key_release(_key, modifiers):
            if _key == key.A:
                handler['a_pressed'] = False


        def on_key_press_menu(_key, modifiers):
            if _key == key.ESCAPE:
                exit()
        def on_key_release_menu(_key, modifiers):
            if _key == key.A:
                pass


        def draw_menu(a,b):
            pass

        def update_menu(a,b):
            pass

        def draw_physic(a,b):
            pass

        def update_physics(x,y):
            if handler['a_pressed']:
                handler['xpos'] += 1
                handler['ypos'] += 1
            else:
                handler['xpos'] -=0
                handler['ypos'] -= 0
        on_update = update_physics
        draw = draw_physic

        pyglet.clock.schedule(on_update, 1/60)







def get_vector(x1, y1, x2, y2):
    return math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))




get_vector(1,1,2,2)

class Object:
    def __init__(self, mass, tags, red, blue, green, spin):
        self.mass = mass
        self.properties = tags

        self.spin = spin

        self.red = red
        self.true_red = 127.5*math.sin(self.red*((math.pi/2)/255)) + 127.5

        self.blue = blue
        self.true_blue = 127.5*math.sin(self.blue*((math.pi/2)/255)) + 127.5

        self.green = green
        self.true_green = 127.5*math.sin(self.green*((math.pi/2)/255)) + 127.5

        self.colour = (self.true_red, self.true_green, self.true_blue)
        self.velx = 0
        self.vely = 0

    def update_colours(self):
        self.true_green = 127.5*math.sin(self.green*((math.pi/2)/255)) + 127.5
        self.true_blue = 127.5*math.sin(self.blue*((math.pi/2)/255)) + 127.5
        self.true_red = 127.5*math.sin(self.red*((math.pi/2)/255)) + 127.5

    def draw_object(self):
        pass


objec = Object(1, None, 50, 50, 50, 0)

"""
How laws work:
destroy bool: If true, particle will be destroyed under certain conditions

Create bool: If true, particle will be created. The properties of the new particle will be 

particle property act - determines what aspect of the particle the law will affect. This will be in form of a list.

Colour red parameter - determines what colour range of red is required for particle to be under effect. 
For example: object A has red= 20, object B has red= 60. If range is 50, they will affect each other. If colour range
is negative, one will affect other
Colour green parameter - same as red, but green.
Colour blue parameter - same same.

direction (0 radians is towards other particle, PI radians is away from particle)


"""
#


class FabricLaw:
    def __init__(self, x

                 ):
        self.x = x


class InteractionLaw:
    def __init__(self, particle_property_act, colour_red_range,
                 colour_green_range, colour_blue_range, min_red, min_green, min_blue,
                 relative_angle_act, ):

        self.particle_property_act = particle_property_act

        self.red_parameter = colour_red_range
        self.green_parameter = colour_green_range
        self.blue_parameter = colour_blue_range

        self.min_red = min_red
        self.min_blue = min_blue
        self.min_green = min_green

        self.relative_angle_act = relative_angle_act


class CreationLaw:
    def __init__(self):
        x =1



def main():
    #  init all other classes here
    #  make sure to __init__ all other classes first!!! subclasses are defined in __init__ of handler.

    handler = Handler()
    pyglet.app.run()



main()
