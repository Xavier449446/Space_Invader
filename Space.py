from pyglet.gl import *
from pyglet.window import *
import random
import pyglet

class GameWindow(Window):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
#bg
        self.bg_list=[]

        self.bg_list.append(pyglet.sprite.Sprite(img=pyglet.image.load("maxresdefault.jpg"),x=0,y=0))
        self.bg_list.append(pyglet.sprite.Sprite(img=pyglet.image.load("maxresdefault.jpg"),x=0,y=700))
#player
        self.player_sprite=pyglet.sprite.Sprite(img=pyglet.image.load("index_burned.png"),x=0,y=0)

    def spr_update(self):
        for spr in self.bg_list:
            spr.y-=4
            if spr.y <=-700:
                spr.y=700

    def bg_draw(self):
        for spr in self.bg_list:
            spr.draw()

    def on_draw(self):
        self.bg_draw()
        self.player_sprite.draw()

    def update(self,dt):
        self.spr_update()

        self.clear()

if __name__=="__main__":
    win=GameWindow(800,800,resizable=False)
    pyglet.clock.schedule_interval(win.update,1/60)
    pyglet.app.run()

