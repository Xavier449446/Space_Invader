from pyglet.window import Window
from pyglet.window import key
from pyglet.text import Label
import random
import pyglet

#Koster Xmas Special
class Laser:
    def __init__(self,image,x_pos,y_pos,speed):
        self.image=image
        self.x=x_pos
        self.y=y_pos
        self.spr=pyglet.sprite.Sprite(img=self.image, x= self.x , y= self.y)
        self.laser_speed=speed
    def move(self):
        self.spr.y+=self.laser_speed
    def draw(self):
        self.spr.draw()

class Xplosion:
    def __init__(self,x_pos=0,y_pos=0):
        self.x=x_pos
        self.y=y_pos
        self.image_grid=pyglet.image.ImageGrid(pyglet.image.load("explosion.png"),4,5,96,96)
        self.texture=pyglet.image.TextureGrid(self.image_grid)
        self.anim=pyglet.image.Animation.from_image_sequence(self.texture[0:],0.1,loop=False)
        self.spr=pyglet.sprite.Sprite(self.anim,x=self.x,y=self.y)
    def draw(self):
        self.spr.draw()

class Enemy:
    def __init__(self,image):
        self.image_name=image
        self.image=pyglet.image.load(self.image_name)
        if self.image_name=='enem2.png':
            self.image_grid=pyglet.image.ImageGrid(self.image,1,8,100,100)
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
        self.hit=False
    def draw(self):
        if not self.hit:
            self.sprite.draw()
        else:
            pass

    def move(self,dt):
        self.sprite.x += (self.speed * self.dire )+dt
    def bound(self):
        if self.sprite.x<=0 or self.sprite.x >=680:
            self.dire *= -1



class PlayerShip:
    def __init__(self):
        self._ship_spr=pyglet.sprite.Sprite(img=pyglet.image.load("index.png"),x=400,y=10)
        self.left=False
        self.right=False
        self.health=200

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
        self.lbl_batch=pyglet.graphics.Batch()
#background objects
        self.bg_list=[]
        self.bg_list.append(pyglet.sprite.Sprite(img=pyglet.image.load("bg.jpg"),x=0,y=0))
        self.bg_list.append(pyglet.sprite.Sprite(img=pyglet.image.load("bg.jpg"),x=0,y=700))
#player object
        self.player=PlayerShip()
#game window properties
        self.move_state=1
        self.pause_state=['',True,False]
        self.pause_lbl=Label(text="Paused",font_size=25,bold=True,x=400,color=(255,0,0,200),y=400,anchor_x='center',anchor_y='center')
        self.game_over=False
#laser animation
        self.laser_list=[]
        self.player_laser=pyglet.image.load("laser.png")
        self.laser_state=False
#stats
        self.stats=pyglet.sprite.Sprite(img=pyglet.image.load("stats.png"),x=800,y=200)
        self.enemy_kill=0
        self.score=0
        self.high_score=0
        self.level=1
        self.enemy_kill_lbl=Label(text=str(self.enemy_kill),font_size=12,bold=False, x=600,color=(255,255,0,255),y=900,anchor_x='center',anchor_y='center',batch=self.lbl_batch)
        self.score_lbl=Label(text=str(self.score),font_size=12,bold=False, x=500,color=(255,255,0,255),y=700,anchor_x='center',anchor_y='center',batch=self.lbl_batch)
        self.high_score_lbl=Label(text=str(self.high_score),font_size=12,bold=False, x=600,color=(255,255,0,255),y=900,anchor_x='center',anchor_y='center',batch=self.lbl_batch)
        self.level_lbl=Label(text=str(self.level),font_size=12,bold=False, x=600,color=(255,255,0,255),y=900,anchor_x='center',anchor_y='center',batch=self.lbl_batch)
# enemies list
        self.enemies=["enem1.png","enem2.png","enem1.png","enem1.png",'enem1.png']
        self.enemies_list=[]
        self.enemy_laser_list=[]
        self.enemy_laser=pyglet.image.load("enemy_laser.png")
        self.enemies_list.append(Enemy(image=random.choice(self.enemies)))
        
    def laser_draw(self):
        for laser in self.enemy_laser_list:
            laser.draw()
        for laser in self.laser_list:
            laser.draw()
    def exp_draw(self):
        for exp in self.exp_list:
            exp.draw()
    def enemy_hit(self):
        for enemy in self.enemies_list:
            for laser in self.laser_list:
                if laser.spr.x >= enemy.sprite.x and laser.spr.x <= enemy.sprite.x+100 and laser.spr.y +20 >=enemy.sprite.y and laser.spr.y <= enemy.sprite.y:
                    enemy.health-=50
                    self.laser_list.remove(laser)
                    if enemy.health <=0 :
                        self.enemies_list.remove(enemy)
                        self.score += 100
                        print(self.score)

    def laser_bound(self):
        for laser in self.enemy_laser_list:
            if laser.spr.y <= 10:
                self.enemy_laser_list.remove(laser)
        for laser in self.laser_list:
            if laser.spr.y >= 780:
                self.laser_list.remove(laser)

    def laser_move(self):
        for laser in self.enemy_laser_list:
            laser.move()

        for laser in self.laser_list:
            laser.move()

    def enemy_laser_update(self,dt):
        if self.pause_state[self.move_state]:
            for enemy in self.enemies_list:
                self.enemy_laser_list.append(Laser(image=self.enemy_laser,x_pos=(enemy.sprite.x+50),y_pos=(enemy.sprite.y),speed=-7))
    def laser_update(self,dt):
        if self.laser_state:
            self.laser_list.append(Laser(image=self.player_laser,x_pos=(self.player._ship_spr.x+107),y_pos=(self.player._ship_spr.y+200),speed=5))

    def spr_update(self):
        for spr in self.bg_list:
            spr.y-=4
            if spr.y <=-700:
                spr.y=700

    def bg_draw(self):
        for spr in self.bg_list:
            spr.draw()

    def enemy_update(self,dt):
        for enemy in self.enemies_list:
            enemy.move(dt)
            enemy.bound()

    def enemy_draw(self):
        for enemy in self.enemies_list:
            enemy.draw()
    def on_draw(self):
        self.bg_draw()
        self.laser_draw()
        self.stats.draw()
        self.enemy_draw()
        self.player.draw()

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
            self.enemy_update(dt)
            self.enemy_hit()
            self.player.set_bound()
            self.laser_move()
            self.laser_bound()
            self.clear()

if __name__=="__main__":
    win=GameWindow(1020,800,resizable=False)
    pyglet.clock.schedule_interval(win.update,1/60)
    pyglet.clock.schedule_interval(win.laser_update,1/5)
    pyglet.clock.schedule_interval(win.enemy_laser_update,2.96)
    pyglet.app.run()
