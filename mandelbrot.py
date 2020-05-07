

import arcade

col_dict = {
    0 : (0,0,0),
    1 : (0,0,200),
    2 : (0,0,255),
    3 : (10,10,250),
    4 : (30,20,240),
    5 : (255,0,0),
    6 : (100,20,200),
    7 : (0,0,255),
    8 : (200,20,100),
    9 : (0,255,0),
    10 : (255,20,20)
}

m = lambda x : x**2



def mandelbrotter(num, ori_num, n):
    if abs(ori_num) < abs(num): # if num become big
        return col_dict[round(min(n,10))]
    if abs(num) < 0.01:
        return (0,0,0)
    try: return mandelbrotter(m(num),ori_num,n+1)
    except: return mandelbrotter(m(num),ori_num,n+1)

def default(num):
    return mandelbrotter(num, num, 0)

w=400
h=300

class t(arcade.Window):
    def __init__(self):
        self.scale = 0.0001
        self.offset = 300
        super().__init__(w,h,'mandeloraian',False)

    def dr(self):
        for x in range(w):
            for y in range(h):
                arcade.draw_point(x,y, default(complex((2*(x-(w/2))/w)+(w/2) + (2j*(y-(h/2))/h)))+(h/2),1)


def main():

    e=t()
    arcade.run()
    arcade.set_background_color((255,255,255))
    e.dr()
    arcade.finish_render()
    print('finished-')

main()




