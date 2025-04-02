from pygame import *
from random import randint
from time import time as timer
mixer.init()
font.init()
font2 = font.SysFont('Arial',35)
font1 = font.SysFont('Arial',70)
win = font1.render('YOU WON!!!',True,(0,255,0))
lose = font1.render('YOU LOST!',True,(255,0,0))
class GameSprite(sprite.Sprite):  
    def __init__(self,player_image,player_x,player_y,player_speed,size):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,self.rect)
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 700 - 50:
            self.rect.x += self.speed
    def fire(self):
            bullet = Bullet('bullet.png',self.rect.centerx-7,self.rect.top,5,(15,15))
            bullets.add(bullet)
lost = 0 
score = 0
lives = 3
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(0,620)
            lost += 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
bullets = sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png',randint(0,620),-40,randint(1,2),(80,50))   
    monsters.add(monster)
for i in range(3):
    asteroid = Enemy('asteroid.png',randint(0,620),-40,randint(1,2),(50,50))   
    asteroids.add(asteroid)
num_fire = 0
rel_time = False
window = display.set_mode((700,500))
display.set_caption('Шутер')
bg = transform.scale(image.load('galaxy.jpg'),(700,500))
player = Player('rocket.png',325,405,5,(50,90))

mixer.music.load('space.ogg')
fire_sound = mixer.Sound('fire.ogg')
mixer.music.play()
mixer.music.set_volume(0.05)
rect_x,rect_y,rect_width,rect_height = 250,300,200,100
rect_visible = True
game = True
clock = time.Clock()
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <10 and rel_time == False: 
                    num_fire += 1   
                    fire_sound.play()
                    player.fire()
                if num_fire >= 10 and rel_time == False:
                    last_time = timer()
                    rel_time = True
        if   score >9 or lives < 1 or lost > 4:
            if e.type == MOUSEBUTTONDOWN:
                mouse_x,mouse_y =  mouse.get_pos()
                if rect_visible and rect_x <= mouse_x <= rect_x + rect_width and rect_y <= mouse_y <= rect_y + rect_height:
                    rect_visible = False
                    finish = False
                    score = 0
                    lost = 0
                    lives = 3
                    bullets.empty()
                    monsters.empty()
                    asteroids.empty()
                    for i in range(5):
                        monster = Enemy('ufo.png',randint(0,620),-40,randint(1,2),(80,50))   
                        monsters.add(monster)
                    for i in range(3):
                        asteroid = Enemy('asteroid.png',randint(0,620),-40,randint(1,2),(50,50))   
                        asteroids.add(asteroid)
                    player = Player('rocket.png',325,405,5,(50,90))
                    rect_visible = True
        
    if not finish:
        window.blit(bg,(0,0))
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('Перезарядка',True,(255,255,255))
                window.blit(reload,(250,400))
            else:
                num_fire = 0
                rel_time =False

        player.reset()
        player.update()
        if sprite.groupcollide(monsters,bullets,True,True):
            score += 1
            monster = Enemy('ufo.png',randint(0,620),-40,randint(1,2),(80,50))   
            monsters.add(monster)
        if score > 9:
            finish = True
            window.blit(win,(200,200))
            if rect_visible:
                draw.rect(window,(0,0,255),(rect_x,rect_y,rect_width,rect_height))   
        if sprite.spritecollide(player,monsters,True):
            if lives > 0:
                lives -= 1
            else:
                window.blit(lose,(200,200))
                if rect_visible:
                    draw.rect(window,(0,0,255),(rect_x,rect_y,rect_width,rect_height))   
        if sprite.spritecollide(player,asteroids,True):
            if lives > 0:
                lives -= 1
            else:
                window.blit(lose,(200,200))
                if rect_visible:
                    draw.rect(window,(0,0,255),(rect_x,rect_y,rect_width,rect_height))   
        if lives < 1:
            window.blit(lose,(200,200))
            finish = True
            if rect_visible:
                draw.rect(window,(0,0,255),(rect_x,rect_y,rect_width,rect_height))
        
            

            
        monsters.draw(window)
        monsters.update()
        asteroids.draw(window)
        asteroids.update()
        bullets.draw(window)
        bullets.update()
        text_lose = font2.render('Пропущено:'+str(lost),True,(255,255,255))
        text_win = font2.render('Очки:'+ str(score),True,(255,255,255))
        HP = font2.render('HP:' + str(lives),True,(255,255,255))
        window.blit(text_lose,(10,20))
        window.blit(text_win,(10,60))
        window.blit(HP,(600,20))
    display.update()
    clock.tick(60)