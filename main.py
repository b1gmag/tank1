#подключение библиотек*
from pygame import*

#написание классов
class Tank(sprite.Sprite):
    def __init__(self,player_image, health, armor, damage,speed,x,y):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(80,80))
        self.rect = self.image.get_rect()
        self.health = health
        self.armor = armor 
        self.damage = damage
        self.speed = speed
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        global direction
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x>10:
            self.rect.x -= self.speed
            direction = 'left'
            self.image = transform.scale(image.load('tankA.png'),(80,80))

        if keys[K_d] and self.rect.x<long_window-90:
            self.rect.x += self.speed
            direction = 'right'
            self.image = transform.scale(image.load('tankD.png'),(80,80))

        if keys[K_w] and self.rect.y>10:
            self.rect.y -= self.speed
            direction = 'up'
            self.image = transform.scale(image.load('tankW.png'),(80,80))

        if keys[K_s] and self.rect.y<wide_window-90:
            self.rect.y += self.speed
            direction = 'down'
            self.image = transform.scale(image.load('tankS.png'),(80,80))


    def fire(self):
        if direction == 'up':
            bullet1 = Bullet('bulletW.png',self.rect.centerx,self.rect.y,15,30,10,direction) 
            bullets_player.add(bullet1)
            fire.play()

        if direction == 'down':
            bullet1 = Bullet('bulletS.png',self.rect.centerx,self.rect.bottom,15,30,10,direction) 
            bullets_player.add(bullet1)
            fire.play()

        if direction == 'left':
            bullet1 = Bullet('bulletA.png',self.rect.x,self.rect.centery,30,15,10,direction) 
            bullets_player.add(bullet1)
            fire.play()

        if direction == 'right':
            bullet1 = Bullet('bulletD.png',self.rect.right,self.rect.centery,30,15,10,direction) 
            bullets_player.add(bullet1)
            fire.play()

    def reset(self):
        main_window.blit(self.image,(self.rect.x, self.rect.y))    


class Walls(sprite.Sprite):
    def __init__(self,wall_image,wall_x,wall_y,wall_long,wall_wide):
        super().__init__()
        self.long = wall_long
        self.wide = wall_wide
        self.image = transform.scale(image.load(wall_image),(self.long,self.wide))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
        
        
    def draw(self):
        main_window.blit(self.image,(self.rect.x, self.rect.y))


class Bullet(sprite.Sprite):
    def __init__(self, bullet_image, bullet_x, bullet_y,bullet_long,bullet_wide, bullet_speed,bullet_direction):
        super().__init__()
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(bullet_image), (bullet_long, bullet_wide))
        self.speed =bullet_speed
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = bullet_x
        self.rect.y =bullet_y
        self.direction = bullet_direction

    def update(self):
        if self.direction == 'left':
            self.rect.x -= self.speed
            if self.rect.x<=0:
                self.kill()

        if self.direction == 'right':
            self.rect.x += self.speed
            if self.rect.x>1920:
                self.kill()

        if self.direction == 'up':
            self.rect.y -= self.speed
            if self.rect.y<=0:
                self.kill()
        
        if self.direction == 'down':
            self.rect.y += self.speed
            if self.rect.y>1080:
                self.kill()

    def draw(self):
        main_window.blit(self.image,(self.rect.x, self.rect.y))


class Enemies(sprite.Sprite):
    def __init__(self, enemy_image, health, damage, speed, x, y,direction):
        super().__init__()
        self.image = transform.scale(image.load(enemy_image),(80,80))
        self.rect = self.image.get_rect()
        self.health = health
        self.damage = damage
        self.speed = speed
        self.rect.x = x
        self.rect.y = y
        self.begin_x = x
        self.begin_y = y
        self.direction = direction

    def reset(self):
        main_window.blit(self.image,(self.rect.x, self.rect.y))  

    def fire(self):
        if self.direction == 'down':
            bullet1 = Bullet('bulletS.png',self.rect.centerx,self.rect.bottom,15,30,15,self.direction)
            bullets_enemy.add(bullet1)
        if self.direction == 'up':
            bullet1 = Bullet('bulletW.png',self.rect.centerx,self.rect.y,15,30,15,self.direction)
            bullets_enemy.add(bullet1)
        if self.direction == 'right':
            bullet1 = Bullet('bulletD.png',self.rect.right,self.rect.centery,30,15,15,self.direction)
            bullets_enemy.add(bullet1)
        if self.direction == 'left':
            bullet1 = Bullet('bulletA.png',self.rect.x,self.rect.centery,30,15,15,self.direction)
            bullets_enemy.add(bullet1)

    def update(self):
        if self.direction == 'up' or self.direction == 'down':
            self.rect.x  -= self.speed 
            if abs(self.begin_x - self.rect.x) > 100:
                self.speed *= -1

            if sprite.spritecollide(self, walls_group, False):
                self.speed *= -1
            
            if abs(self.rect.x - player.rect.x) < 2:
                self.fire()
            
        if self.direction == 'left' or self.direction == 'right':
            self.rect.y  -= self.speed 
            if abs(self.begin_y - self.rect.y) > 100:
                self.speed *= -1

            if sprite.spritecollide(self, walls_group, False):
                self.speed *= -1
            
            if abs(self.rect.y - player.rect.y) < 2:
                self.fire()

class Stuff(sprite.Sprite):
    def __init__(self,stuff_image,x,y):
        super().__init__()
        self.image = transform.scale(image.load(stuff_image),(45,32))
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y

    def reset(self):
        main_window.blit(self.image,(self.rect.x, self.rect.y))    
#создание игровой сцены
long_window = 1920
wide_window = 1080
main_window = display.set_mode((long_window,wide_window))
display.set_caption('Tank_mission')
background = transform.scale(image.load('texture_scene.png'),(long_window,wide_window))

#персонажи
player = Tank('tankW.png',3,3,4,3,850,600)
enemy1 = Enemies('enemy_type1S.png',2,1,4,900,100,'down')
enemy2 = Enemies('enemy_type1A.png',2,1,4,1800,900,'left')
enemy3 = Enemies('enemy_type1S.png',2,1,4,1700,50,'down')
enemy4 = Enemies('enemy_type1W.png',2,1,4,1450,600,'up')
enemy5 = Enemies('enemy_type1S.png',2,1,4,1245,100,'down')
enemy6 = Enemies('enemy_type1S.png',2,1,4,1200,200,'down')
enemy7 = Enemies('enemy_type1W.png',2,1,4,600,600,'up')
enemy8 = Enemies('enemy_type1W.png',2,1,4,700,430,'up')
enemy9 = Enemies('enemy_type1W.png',2,1,4,300,600,'up')
enemy10 = Enemies('enemy_type1W.png',2,1,4,100,800,'up')
enemy11 = Enemies('enemy_type1A.png',2,1,4,500,800,'left')
enemy12 = Enemies('enemy_type1A.png',2,1,4,600,850,'left')

enemy_group = sprite.Group()

enemy_group.add(enemy1)
enemy_group.add(enemy2)
enemy_group.add(enemy3)
enemy_group.add(enemy4)
enemy_group.add(enemy5)
enemy_group.add(enemy6)
enemy_group.add(enemy7)
enemy_group.add(enemy8)
enemy_group.add(enemy9)
enemy_group.add(enemy10)
enemy_group.add(enemy11)
enemy_group.add(enemy12)


stuff_group = sprite.Group()
aid_kit = Stuff('aid_kit.png',1280, 50)
aid_kit2 = Stuff('aid_kit.png',700, 850)
stuff_group.add(aid_kit)
stuff_group.add(aid_kit2)

#стены
walls_group = sprite.Group()

wall1 = Walls('wall_turfH.png',1100,-20,50,750)
walls_group.add(wall1)

wall2 = Walls('wall_stoneH.png',800,150,30,950)
walls_group.add(wall2)

wall3 = Walls('wall_turfV.png',1100,710,600,50)
walls_group.add(wall3)

wall4 = Walls('wall_turfH.png',1680,150,50,605)
walls_group.add(wall4)

wall5 = Walls('wall_turfH.png',1450,-20,50,600)
walls_group.add(wall5)

wall6 = Walls('wall_turfH.png',1680,900,50,150)
walls_group.add(wall6)

wall7 = Walls('wall_stoneV.png',200,710,600,30)
walls_group.add(wall7)

wall8 = Walls('wall_stoneV.png',600,530,350,30)
walls_group.add(wall8)

wall9 = Walls('wall_stoneH.png',600,150,30,390)
walls_group.add(wall9)

wall10 = Walls('wall_stoneH.png',400,150,30,590)
walls_group.add(wall10)

wall11 = Walls('wall_stoneH.png',200,150,30,590)
walls_group.add(wall11)

#стрельба
mixer.init()
direction = 'up'
bullets_player = sprite.Group()
bullets_enemy = sprite.Group()
fire = mixer.Sound('fire.ogg')
aid = mixer.Sound('aid_kit.ogg')
mixer.music.load('backgroung_mus.mp3')
mixer.music.play()

#надписи
font.init()
font = font.Font(None,100)
win = font.render('You WIN!', True, (0,255,0))
lose = font.render('mission failed!', True, (200,0,0))
mission = font.render('mission: kill all enemies!', True, (0,255,255))

#игровой цикл и все что к нему относится
game = True
end = False
FPS = 60
clock = time.Clock()

while game:
    for i in event.get():
        if i.type == QUIT:
            game = False
        elif i.type == KEYDOWN:
            if i.key == K_SPACE:
                player.fire()

            '''if i.key == K_a:
                player.rect.x -= player.speed
                direction = 'left'
                player.image = transform.scale(image.load('tankA.png'),(80,80))

            if i.key == K_w:
                player.rect.y -= player.speed
                direction = 'up'
                player.image = transform.scale(image.load('tankW.png'),(80,80))'''
    
        
    if end == False:
        main_window.blit(background,(0,0))
        player.update()
        player.reset()
        walls_group.draw(main_window)
        bullets_enemy.update()
        bullets_enemy.draw(main_window)
        bullets_player.draw(main_window)
        bullets_player.update()
        stuff_group.draw(main_window)
        
        
        #enemy1.reset()
        #enemy1.updateV()
        #enemy2.reset()
        #enemy2.updateH()
        #enemy3.reset()
        #enemy3.updateV()
        #enemy4.reset()
        #enemy4.updateV()
        
        enemy_group.draw(main_window)
        enemy_group.update()
        

        '''if sprite.spritecollide(player,walls_group,False):
            health_wall-=1
            if health_wall == 0:
                end =True'''

        if sprite.groupcollide(bullets_enemy, walls_group, True, False):   
            pass

        if sprite.groupcollide(bullets_player, walls_group, True, False):   
            pass

        if sprite.spritecollide(player,walls_group,False):
            if direction == 'left':
               player.rect.left += player.speed
            elif direction == 'right':
                player.rect.right -= player.speed
            elif direction == 'up':
                player.rect.top += player.speed
            elif direction == 'down':
                player.rect.bottom -= player.speed

        if sprite.groupcollide(enemy_group,bullets_player,True,True):
            if len(enemy_group) == 0:
                end = True
                main_window.blit(win,(800,100))

        if sprite.spritecollide(player,bullets_enemy,True):
            player.health -=1
            print(player.health)
            if player.health == 0:
                end = True
                main_window.blit(lose,(800,100))
                
        if sprite.spritecollide(player,enemy_group,False):
            player.health == 0
            end = True
            main_window.blit(lose,(800,100))

        if sprite.spritecollide(player,stuff_group,True):
            player.health = 3
            print(player.health)
            aid.play()
    display.update()
    clock.tick(FPS)