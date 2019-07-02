from pyglet.gl import *
from pyglet.window import Window
from pyglet.window import key
import random
import pyglet

class PlayerShip:
    def __init__(self):
        self._ship_spr=pyglet.sprite.Sprite(img=pyglet.image.load("index_burned.png"),x=400,y=10)
        self.left=False
        self.right=False
    def draw(self):
        self._ship_spr.draw()
    def set_bound(self):
        if self._ship_spr.x <=0 :
            self._ship_spr.x=0
        if self._ship_spr.x >= 800-215:
            self._ship_spr.x =800-215
    def move(self):
        if self.right:
            self._ship_spr.x +=3
        if self.left:
            self._ship_spr.x -=3
    def key_press(self,symbol,modifiers):
        if symbol==key.LEFT or symbol==key.NUM_4:
            self.left=True
        if symbol==key.RIGHT or symbol==key.NUM_6:
            self.right=True
        if (symbol==key.RIGHT and symbol==key.LEFT) or (symbol==key.NUM_4 and symbol==key.NUM_6):
            self.left=False
            self.right=False
        self.set_bound()
        self.move()


class GameWindow(Window):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_caption("Xavier's Game")
        self.set_location(300,200)
#bg
        self.bg_list=[]

        self.bg_list.append(pyglet.sprite.Sprite(img=pyglet.image.load("maxresdefault.jpg"),x=0,y=0))
        self.bg_list.append(pyglet.sprite.Sprite(img=pyglet.image.load("maxresdefault.jpg"),x=0,y=700))
#player
        self.player=PlayerShip()

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
        self.player.draw()

    def on_key_press(self,symbol,modifiers):
        self.player.key_press(symbol,modifiers)

    def update(self,dt):
        self.spr_update()

        self.clear()

if __name__=="__main__":
    win=GameWindow(800,800,resizable=False)
    pyglet.clock.schedule_interval(win.update,1/60)
    pyglet.app.run()
