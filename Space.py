from pyglet.window import Window
from pyglet.window import key
from pyglet.text import Label
import random
import pyglet
#Koster Xmas Special
class Laser:
    def __init__(self,image,x_pos,y_pos):
        self.image=image
        self.x=x_pos
        self.y=y_pos
        self.spr=pyglet.sprite.Sprite(img=self.image, x= self.x , y= self.y)
        self._laser_rate=10
        self.laser_speed=5
    def move(self):
        self.spr.y+=self.laser_speed
    def draw(self):
        self.spr.draw()

class Enemy:
    def __init__(self,image):
        self.image_name=image
        self.image=pyglet.image.load(self.image_name)
        if image_name=='enem2.png':
            self.image_grid=pyglet.image.ImageGrid(self.image, row=1,column=8,item_width=100,item_height==100)
            self.health=200
            self.speed=5
        else :
            self.image_grid=pyglet.image.ImageGrid(self.image,1,15,100,100)
            self.health=100
            self.speed=4
       
        self.texture=pyglet.image.TextureGrid(self.image_grid)
        self.anim=pyglet.image.Animation.from_image_sequence(self.texture[0:],0.1,loop=True)
        self.dir=[-1,1]
        self.sprite=pyglet.sprite.Sprite(self.anim,x=random.randrange(0,700,3),y=random.randrange(300,700,5))
        self.dire=random.choice(self.dir)
    def draw(self):
        self.sprite.draw()
    def move(self):
        self.sprite.x += (self.speed * self.dire )



class PlayerShip:
    def __init__(self):
        self._ship_spr=pyglet.sprite.Sprite(img=pyglet.image.load("index_burned.png"),x=400,y=10)
        self.left=False
        self.right=False


    def draw(self):
        self._ship_spr.draw()
        


    def set_bound(self):
        if self._ship_spr.x <=-80 :
            self._ship_spr.x=-80
        if self._ship_spr.x >= 800-135:
            self._ship_spr.x =800-135


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
        self.pause_state=['',True,False]
        self.pause_lbl=Label(text="Paused",font_size=25,bold=True,x=400,color=(255,0,0,200),y=400,anchor_x='center',anchor_y='center')
#laser animation
        self.laser_list=[]
        self.player_laser=pyglet.image.load("laser.png")
        self.laser_state=False

#stats
        self.stats=pyglet.sprite.Sprite(img=pyglet.image.load("stats.png"),x=800,y=200)

# enemies list
        self.enemies=["enem1.png","enem2.png"]
    def laser_draw(self):
        for laser in self.laser_list:
            laser.draw()
    
    def laser_bound(self):
        for laser in self.laser_list:
            if laser.spr.x >= 780:
                self.laser_list.remove(laser)

    def laser_move(self):
        for laser in self.laser_list:
            laser.move()
            
    def laser_update(self,dt):
        if self.laser_state:
            self.laser_list.append(Laser(image=self.player_laser,x_pos=(self.player._ship_spr.x+107),y_pos=(self.player._ship_spr.y+200)))

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
        if not self.pause_state[self.move_state]:
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
        if self.pause_state[self.move_state]:
            self.spr_update()
            self.player.move(dt)
            self.player.set_bound()
            self.laser_move()
            self.laser_bound()
            self.clear()

if __name__=="__main__":
    win=GameWindow(1020,800,resizable=False)
    pyglet.clock.schedule_interval(win.update,1/60)
    pyglet.clock.schedule_interval(win.laser_update,1/5)
    pyglet.app.run()

