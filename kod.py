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
            bullets.add(bullet1)
            fire.play()

        if direction == 'down':
            bullet1 = Bullet('bulletS.png',self.rect.centerx,self.rect.bottom,15,30,10,direction) 
            bullets.add(bullet1)
            fire.play()

        if direction == 'left':
            bullet1 = Bullet('bulletA.png',self.rect.x,self.rect.centery,30,15,10,direction) 
            bullets.add(bullet1)
            fire.play()

        if direction == 'right':
            bullet1 = Bullet('bulletD.png',self.rect.right,self.rect.centery,30,15,10,direction) 
            bullets.add(bullet1)
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
    def __init__(self, enemy_image, health, damage, speed, x, y):
        super().__init__()
        self.image = transform.scale(image.load(enemy_image),(80,80))
        self.rect = self.image.get_rect()
        self.health = health
        self.damage = damage
        self.speed = speed
        self.rect.x = x
        self.rect.y = y
        self.begin_x = x

    def reset(self):
        main_window.blit(self.image,(self.rect.x, self.rect.y))  

    def fire(self):
        bullet1 = Bullet('bulletD.png',self.rect.right,self.rect.centery,30,15,10,direction) 
        bullets.add(bullet1)
        fire.play()

    def update(self):
        self.rect.x  -= self.speed 
        if abs(self.begin_x - self.rect.x) > 100:
            self.speed *= -1

        if sprite.spritecollide(self, walls_group, False):
            self.speed *= -1
        
        if (abs(self.rect.x - player.rect.x) or (self.rect.y - player.rect.y)) < 2:
            self.fire()
        


#создание игровой сцены
long_window = 1920
wide_window = 1080
main_window = display.set_mode((long_window,wide_window))
display.set_caption('Tank_mission')
background = transform.scale(image.load('texture_scene.png'),(long_window,wide_window))

#персонажи
player = Tank('tankW.png',10,3,4,3,950,500)
enemy1 = Enemies('enemy_type1S.png',2,1,3,900,100)
#health_wall = 25
a = 0
b =100
#стены
walls_group = sprite.Group()

wall1 = Walls('wall_turfH.png',1100,-20,50,750)
walls_group.add(wall1)

wall2 = Walls('wall_stoneH.png',700,150,50,950)
walls_group.add(wall2)

wall3 = Walls('wall_turfV.png',1100,710,600,50)
walls_group.add(wall3)

wall4 = Walls('wall_turfH.png',1680,150,50,605)
walls_group.add(wall4)

wall5 = Walls('wall_turfH.png',1450,-20,50,600)
walls_group.add(wall5)

wall6 = Walls('wall_turfH.png',1680,900,50,150)
walls_group.add(wall6)

#стрельба
mixer.init()
direction = 'up'
bullets = sprite.Group()
fire = mixer.Sound('fire.ogg')




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

            if i.key == K_a:
                player.rect.x -= player.speed
                direction = 'left'
                player.image = transform.scale(image.load('tankA.png'),(80,80))

            if i.key == K_w:
                player.rect.y -= player.speed
                direction = 'up'
                player.image = transform.scale(image.load('tankW.png'),(80,80))

    if end == False:
        main_window.blit(background,(0,0))
        player.update()
        player.reset()
        walls_group.draw(main_window)
        bullets.update()
        bullets.draw(main_window)
        enemy1.reset()
        
        enemy1.update()
        

        '''if sprite.spritecollide(player,walls_group,False):
            health_wall-=1
            if health_wall == 0:
                end =True'''

        if sprite.groupcollide(bullets, walls_group, True, False):   
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

    display.update()
    clock.tick(FPS)