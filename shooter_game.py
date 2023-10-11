#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer
window = display.set_mode((1000, 700))
display.set_caption('Danger space')
clock = time.Clock()
fon = transform.scale(image.load('galaxy.jpg'),(1000,700))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_music = mixer.Sound('fire.ogg')
font.init()
font = font.SysFont('Arial',35)
score = 0
miss = 0
magazin = 0
r = False
class igroki(sprite.Sprite):
    def __init__(self,igrok_image,igrok_x,igrok_y,size_x,size_y,igrok_step):
        super().__init__()
        self.image = transform.scale(image.load(igrok_image),(size_x,size_y))
        self.rect = self.image.get_rect()
        self.rect.x = igrok_x
        self.rect.y = igrok_y
        self.step = igrok_step
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
class player(igroki):
    def control(self):
        buttons = key.get_pressed()
        if buttons[K_LEFT] and self.rect.x>0:
            self.rect.x-= self.step
        if buttons[K_RIGHT] and self.rect.x<920:
            self.rect.x+= self.step
    def fire(self):
        billet = Billet('bullet.png',self.rect.x+50,self.rect.y,15,20,17)
        billets.add(billet)

class Enemy(igroki):
    def update(self):
        self.rect.y += self.step
        global miss
        if self.rect.y>700:
            miss += 1
            self.rect.y = 0
            self.rect.x = randint(0,920)
class Enemy_1(igroki):
    def update(self):
        self.rect.y += self.step
        global miss
        if self.rect.y>700:
            self.rect.y = 0
            self.rect.x = randint(0,920)
class Billet(igroki):
    def update(self):
        self.rect.y -= self.step
        if self.rect.y < 0:
            self.kill()
game = True
finish = False
provaider = player('rocket.png',460,600,80,100,20)
asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Enemy_1('asteroid.png',randint(80,920),0,80,80,randint(1,3))
    asteroids.add(asteroid)
billets = sprite.Group()
monsters = sprite.Group()
for i in range(2,5):
    monster = Enemy('ufo.png',randint(0,920),0,80,80,randint(1,4))
    monsters.add(monster)
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if magazin <= 15 and r == False:
                    magazin += 1 
                    fire_music.play()
                    provaider.fire()
                if magazin > 15 and r == False:
                    start_t = timer()
                    r = True
    if finish != True:
        window.blit(fon,(0,0))
        score_text = font.render('Счёт:'+str(score),True,(111,111,233))
        miss_text = font.render('Пропущено:'+str(miss),True,(222,244,000))
        window.blit(score_text,(10,10))
        window.blit(miss_text,(10,55))
        provaider.reset()
        provaider.control()
        monsters.draw(window)
        monsters.update()
        billets.draw(window)
        billets.update()
        asteroids.draw(window)
        asteroids.update()
        if r == True:
            end_t = timer()
            if end_t-start_t < 2:
                text_r = font.render('Перезарядка!',True,(255,155,55))
                window.blit(text_r,(500,350))
            else:
                r = False
                magazin = 0
        if sprite.spritecollide(provaider,monsters,False) or sprite.spritecollide(provaider,asteroids,False) or miss>=15:
            finish = True
            text_lose = font.render('Вы продули!!!',True,(255,255,255))
            window.blit(text_lose,(500,350))
        cocos = sprite.groupcollide(billets,monsters,True,True)
        for i in cocos:
            score +=1
            monster = Enemy('ufo.png',randint(80,920),0,80,80,randint(1,4))
            monsters.add(monster)
        if score >=50:
            finish = True
            text_win = font.render('вы выиграли...может слишком просто?.',True,(255,255,255))
            window.blit(text_win,(500,350))
    display.update()
    clock.tick(60)