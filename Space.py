# Not Completed Yet So The performance totally depend on your CPU
# For further assistance and suggestions contact me
# Press Space for shooting
# Enter To pause
# ESC to Quit



from pyglet.window import Window
from pyglet.window import key
from pyglet.text import Label
import random
import threading
import pyglet
import sys
def write(score):
    with open("Scores.txt",'a') as fwrite:
        fwrite.write(str(score)+"\n")

def score_get():
    try :
        with open("Scores.txt",'r') as fread:
            scores=[int(a) for a in fread.read()]
            high_score=max(scores)
            return high_score
    except:
        return 0

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
        self.state=False
    def draw(self):
        self.spr.draw()


class Enemy:
    def __init__(self,image):
        self.image_name=image
        self.image=pyglet.image.load(self.image_name)
        if self.image_name=='enem2.png':
            self.image_grid=pyglet.image.ImageGrid(self.image,1,8,100,100)
            self.health=200
            self.speed=6
            self.score=150
            self.laser_speed=-9
        else :
            self.image_grid=pyglet.image.ImageGrid(self.image,1,15,100,100)
            self.health=100
            self.score=50
            self.speed=4
            self.laser_speed=-6
        self.texture=pyglet.image.TextureGrid(self.image_grid)
        self.anim=pyglet.image.Animation.from_image_sequence(self.texture[0:],0.1,loop=True)
        self.dir=[-1,1]
        self.sprite=pyglet.sprite.Sprite(self.anim,x=random.randrange(0,700,3),y=random.randrange(300,700,5))
        self.dire=random.choice(self.dir)
    def draw(self):
        if not self.hit:
            self.sprite.draw()

    def move(self,dt):
        self.sprite.x += (self.speed * self.dire )+dt
    def bound(self):
        if self.sprite.x<=0 or self.sprite.x >=680:
            self.dire *= -1



class PlayerShip:
    def __init__(self):
        self.spr=pyglet.sprite.Sprite(img=pyglet.image.load("index.png"),x=400,y=10)
        self.left=False
        self.right=False
        self.health=200

    def draw(self):
        self.spr.draw()
    def set_bound(self):
        if self.spr.x <=-80 :
            self.spr.x=-80
        if self.spr.x >= 800-135:
            self.spr.x =800-135


    def move(self,dt):
        if self.right:
            self.spr.x +=3+dt
        if self.left:
            self.spr.x -=3+dt


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
        self.pause_lbl=Label(text="Paused",font_name="Koster Xmas Special",font_size=25,bold=True,x=400,color=(255,0,0,200),y=400,anchor_x='center',anchor_y='center')
        self.game_over=False
        self.game_over_lbl=Label(text='Game Over',font_name="Koster Xmas Special",font_size=25,bold=True,x=400,y=400,color=(255,0,0,200),anchor_x='center',anchor_y='center')
        
#laser animation
        self.laser_list=[]
        self.player_laser=pyglet.image.load("laser.png")
        self.laser_state=False
#stats
        self.stats=pyglet.sprite.Sprite(img=pyglet.image.load("stats.png"),x=800,y=200)
        self.enemy_kill=0
        self.score=0
        self.high_score=score_get()
        self.level=1
        self.enemy_kill_lbl=Label(text=str(self.enemy_kill),font_size=12,bold=False,font_name="Koster Xmas Special", x=900,color=(255,0,0,255),y=570,anchor_x='center',anchor_y='center',batch=self.lbl_batch)
        self.score_lbl=Label(text=str(self.score),font_size=12,bold=False, x=900,color=(255,0,0,255),font_name="Koster Xmas Special",y=420,anchor_x='center',anchor_y='center',batch=self.lbl_batch)
        self.high_score_lbl=Label(text=str(self.high_score),font_size=12,font_name="Koster Xmas Special",bold=False, x=900,color=(255,0,0,255),y=680,anchor_x='center',anchor_y='center',batch=self.lbl_batch)
        self.level_lbl=Label(text=str(self.level),font_name="Koster Xmas Special",font_size=12,bold=False, x=900,color=(255,0,0,255),y=300,anchor_x='center',anchor_y='center',batch=self.lbl_batch)
# enemies list
        self.enemies=["enem1.png","enem2.png","enem1.png","enem1.png",'enem1.png']
        self.enemies_list=[]
        self.enemy_laser_list=[]
        self.enemy_laser=pyglet.image.load("enemy_laser.png")
        self.enemies_list.append(Enemy(image=random.choice(self.enemies)))

#explosion
        self.explosion_list=[]

    def exp_remove(self):
        if self.explosion_list:
            for exp in self.explosion_list:
                if exp.state:
                    self.explosion_list.remove(exp)
        else:
            pass
    def exp_draw(self):
        if self.explosion_list:
            for exp in self.explosion_list:
                exp.draw()
                self.new_thread=threading.Timer(1.5,self.exp_remove())
                self.new_thread.start()
                self.new_thread.join()
                self.new_thread.cancel()
        else:
            pass

    def laser_draw(self):
        for laser in self.enemy_laser_list:
            laser.draw()
        for laser in self.laser_list:
            laser.draw()
    def enemy_hit(self):
        for enemy in self.enemies_list:
            for laser in self.laser_list:
                if laser.spr.x >= enemy.sprite.x and laser.spr.x <= enemy.sprite.x+100 and laser.spr.y +20 >=enemy.sprite.y and laser.spr.y <= enemy.sprite.y:
                    enemy.health-=50
                    self.laser_list.remove(laser)
                    if enemy.health <=0 :
                        self.score += enemy.score
                        self.explosion_list.append(Xplosion(enemy.sprite.x,enemy.sprite.y))
                        self.enemies_list.remove(enemy)
                        self.enemy_kill+=1
                        self.enemies_list.append(Enemy(image=random.choice(self.enemies)))
    def player_hit(self):
        for laser in self.enemy_laser_list:
            if laser.spr.x >= self.player.spr.x and laser.spr.x <=self.player.spr.x +214 and laser.spr.y >= self.player.spr.y and laser.spr.y <= self.player.spr.y +215:
                self.player.health-=100
                self.enemy_laser_list.remove(laser)
                if self.player.health <= 0:
                    self.explosion_list.append(Xplosion(enemy.sprite.x,enemy.sprite.y))
                    self.game_over=True
    def game_end(self):

        try:
            write(self.score)
            self.game_over_lbl.draw()
            self.end_game=threading.Timer(10,self.close())
            self.end_game_2=threading.Timer(10,sys.exit)
            self.end_game_2.start()
            self.end_game.start()
        except TypeError:
            write(self.score)
            sys.exit
            pass

    def label_update(self):
        self.score_lbl.text=str(self.score)
        self.enemy_kill_lbl.text=str(self.enemy_kill)
        self.high_score_lbl.text=str(self.high_score)
        self.level_lbl.text=str(self.level)

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
                self.enemy_laser_list.append(Laser(image=self.enemy_laser,x_pos=(enemy.sprite.x+50),y_pos=(enemy.sprite.y),speed=enemy.laser_speed))
    def laser_update(self,dt):
        if self.laser_state:
            self.laser_list.append(Laser(image=self.player_laser,x_pos=(self.player.spr.x+107),y_pos=(self.player.spr.y+200),speed=5))

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
        self.clear()
        if self.pause_state[self.move_state] and not self.game_over:
            self.bg_draw()
            self.exp_draw()
            self.laser_draw()
            self.enemy_draw()
            self.player.draw()
            self.stats.draw()
            self.lbl_batch.draw()
        if not self.pause_state[self.move_state]:
            self.pause_lbl.draw()
        if self.game_over:
            self.exp_draw()
            self.game_over_lbl.draw()

    def on_key_press(self,symbol,modifiers):
        if symbol==key.ENTER :
            self.move_state*=-1
        self.player.key_press(symbol,modifiers)
        if symbol==key.SPACE or symbol==key.NUM_5 :
            self.laser_state=True
        if symbol==key.ESC :
            self.game_over=True


    def on_key_release(self,symbol,modifiers):
        if symbol==key.LEFT or symbol==key.NUM_4:
            self.player.left=False
        if symbol==key.RIGHT or symbol==key.NUM_6:
            self.player.right=False
        if symbol==key.SPACE or symbol==key.NUM_5 :
            self.laser_state=False
    def update(self,dt):
        if self.pause_state[self.move_state] and not self.game_over:
            self.spr_update()
            self.player.move(dt)
            self.enemy_update(dt)
            self.player.set_bound()
            self.enemy_hit()
            self.player_hit()
            self.laser_move()
            self.laser_bound()
            self.label_update()
            self.clear()
        if self.game_over:
            self.game_end()

if __name__=="__main__":
    win=GameWindow(1020,800,resizable=False)
    pyglet.clock.schedule_interval(win.update,1/60)
    pyglet.clock.schedule_interval(win.laser_update,1/5)
    pyglet.clock.schedule_interval(win.enemy_laser_update,2.3)
    pyglet.app.run()
