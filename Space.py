from pyglet.gl import *
from pyglet.window import *
import random
import pyglet

class GameWindow(Window):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.bg_img=pyglet.image.load("maxresdefault.jpg")
        self.bg_sprite=pyglet.sprite.Sprite(img=self.bg_img,x=0,y=0)
    def on_draw(self):
        self.bg_sprite.draw()
    def update(self,dt):
        self.bg_sprite.y-=0.5
        self.clear()

if __name__=="__main__":
    win=GameWindow(800,600,resizable=False)
    pyglet.clock.schedule_interval(win.update,1/60)
    pyglet.app.run()
