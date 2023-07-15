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

        if keys[K_w] and self.rect.y>10:
            self.rect.y -= self.speed
            direction = 'up'

        if keys[K_s] and self.rect.y<wide_window-90:
            self.rect.y += self.speed
            direction = 'down'
        
        

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




#создание игровой сцены
long_window = 1920
wide_window = 1080
main_window = display.set_mode((long_window,wide_window))
display.set_caption('Tank_mission')
background = transform.scale(image.load('texture_scene.png'),(long_window,wide_window))
#персонажи
player = Tank('tankW.png',10,3,4,3,950,500)
health_wall = 25

#стены
walls_group = sprite.Group()

wall1 = Walls('wall_turfH.png',1100,-20,50,750)
walls_group.add(wall1)
wall2 = Walls('wall_stoneH.png',700,150,50,950)
walls_group.add(wall2)
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

    if end == False:
        main_window.blit(background,(0,0))
        wall1.draw()
        player.update()
        player.reset()
        wall1.draw()
        wall2.draw()
        bullets.update()
        bullets.draw(main_window)
        '''if i.type == KEYDOWN:
            if i.key == K_SPACE:
                bullets.draw(main_window)
                bullets.update()'''
        if sprite.spritecollide(player,walls_group,False):
            health_wall-=1
            if health_wall == 0:
                end =True
            


    display.update()
    clock.tick(FPS)

