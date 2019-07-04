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
        self.enemy_kill_lbl=Label(text=str(self.enemy_kill),font_size=12,bold=False, x=600,color(255,255,255,255),y=900,anchor_x='center',anchor_y='center')
        self.score_lbl=Label(text=str(self.enemy_kill),font_size=12,bold=False, x=500,color(255,255,255,255),y=700,anchor_x='center',anchor_y='center')
        self.high_score_lbl=
        self.level=


# enemies list
        self.enemies=["enem1.png","enem2.png"]
        self.enemies_list=[]
        self.enemies_list.append(Enemy("enem2.png"))
# enemy laser_animation
        self.enemy_laser=pyglet.image.load("enemy_laser.png")
        self.enemy_laser_list=[]


    def laser_draw(self):
        for laser in self.enemy_laser_list:
            laser.draw()
        for laser in self.laser_list:
            laser.draw()

    def laser_bound(self):
        for laser in self.enemy_laser_list:
            if laser.spr.y <= 10:
                self.enemy_laser_list.remove(laser)
        for laser in self.laser_list:
            if laser.spr.y >= 780:
                self.laser_list.remove(laser)
"Space.py" 252L, 7941C                                                                                                                                 137,0-1       55%
