from pyglet.window import Window
from pyglet.window import key
from pyglet.text import Label
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


    def move(self,dt):
        if self.right:
            self._ship_spr.x +=3+dt
        if self.left:
            self._ship_spr.x -=3+dt


    def key_press(self,symbol,modifiers):
        if symbol==key.LEFT or symbol==key.NUM_4:
            self.left=True
        if symbol==key.RIGHT or symbol==key.NUM_6:
            self.right=True
        if (symbol==key.RIGHT and symbol==key.LEFT) or (symbol==key.NUM_4 and symbol==key.NUM_6):
            self.left=False
            self.right=False



class GameWindow(Window):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_caption("Xavier's Game")
        self.set_location(300,200)
#background objects
        self.bg_list=[]

        self.bg_list.append(pyglet.sprite.Sprite(img=pyglet.image.load("maxresdefault.jpg"),x=0,y=0))
        self.bg_list.append(pyglet.sprite.Sprite(img=pyglet.image.load("maxresdefault.jpg"),x=0,y=700))
#player object
        self.player=PlayerShip()
#game window properties
        self.move_state=1
        self.game_states=['',True,False]
        self.pause_lbl=Label(text="Paused",font_size=25,bold=True,x=400,color=(255,0,0,200),y=400,anchor_x='center',anchor_y='center')
#laser animation
        self.laser_list=[]
        self._laser_rate=10
        self.laser_speed=5
        self.laser_state=False

#stats
        self.stats=pyglet.sprite.Sprite(img=pyglet.image.load("stats.png"),x=800,y=200)

    def laser_draw(self):
        for laser in self.laser_list:
            laser.draw()
    
    def laser_bound(self):
        for laser in self.laser_list:
            if laser.x >= 780:
                self.laser_list.remove(laser)

    def laser_move(self,dt):
        for laser in self.laser_list:
            laser.y+=self.laser_speed +dt

    def laser_update(self,dt):
        if self.laser_state:
            self.laser_list.append(pyglet.sprite.Sprite(img=pyglet.image.load("laser.png"),x=(self.player._ship_spr.x+107),y=(self.player._ship_spr.y+200)))

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
        self.stats.draw()
        self.player.draw()
        self.laser_draw()
        if not self.game_states[self.move_state]:
            self.pause_lbl.draw()

    def on_key_press(self,symbol,modifiers):
        if symbol==key.ENTER :
            self.move_state*=-1
        self.player.key_press(symbol,modifiers)
        if symbol==key.SPACE or symbol==key.NUM_5 :
            self.laser_state=True
            

    def on_key_release(self,symbol,modifiers):
        if symbol==key.LEFT or symbol==key.NUM_4:
            self.player.left=False
        if symbol==key.RIGHT or symbol==key.NUM_6:
            self.player.right=False
        if symbol==key.SPACE or symbol==key.NUM_5 :
            self.laser_state=False
    def update(self,dt):
        if self.game_states[self.move_state]:
            self.spr_update()
            self.player.move(dt)
            self.player.set_bound()
            self.laser_move(dt)
            self.laser_bound()
            self.clear()

if __name__=="__main__":
    win=GameWindow(1020,800,resizable=False)
    pyglet.clock.schedule_interval(win.update,1/60)
    pyglet.clock.schedule_interval(win.laser_update,1/5)
    pyglet.app.run()


