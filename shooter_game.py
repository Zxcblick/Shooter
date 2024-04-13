import pygame
pygame.init()
pygame.mixer.init()
pygame.font.init()
from random import randint
from time import time as t

vid_info = pygame.display.Info()
k = 0.8
width = int(vid_info.current_w * k)
height = int(vid_info.current_h * k)
size = int(min(width, height) * 0.2 * k)

#Classes
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(player_image), (size, size))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 
    def reset(self):
        main_win.blit(self.image, (self.rect.x, self.rect.y))

class Hero(GameSprite):
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < width - size:
            self.rect.x += self.speed
    def shot(self):
        global bullets, fire_timer
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and fire_timer <= 0:
            fire_sound.play()
            bullet = Bullet('bullet.png', self.rect.centerx-12, self.rect.top, 10)
            bullet.resized()
            bullets.add(bullet)
            fire_timer = 10

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > height:
            self.rect.y = randint(-100, 0)
            self.rect.x = randint(50, width-50)
            lost_sound.play()
            lost += 1

class SpriteSleep(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > height:
            self.rect.y = randint(-100, 0)
            self.rect.x = randint(50, width-50)

class Bullet(GameSprite):
    def resized(self):
        self.image = pygame.transform.scale(self.image, (int(size/4),int(size/4)))
        #self.rect = self.image.get_rect()
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

def getGFrame():
    global fire_timer, score, finish, res, enemyFreezFlag, playerFreezFlag, player_start_time, enemy_start_time
    fire_timer -= 1
    main_win.blit(bg, (0, 0))
    if not(finish):
        if not playerFreezFlag:
            hero.move()
            hero.shot()
            bullets.update()
        if not enemyFreezFlag:
            enemies.update()
        enemyFreez.update()
        playerFreez.update()
        enemyFreez.reset()
        playerFreez.reset()
        
    sprites_list = pygame.sprite.groupcollide(enemies, bullets, True, True)
    if len(sprites_list) > 0:
        score += len(sprites_list)
        for i in range(len(sprites_list)):
            enemy = Enemy('asteroid.png', randint(50, width-50), randint(-100, 0), 3)
            enemies.add(enemy)

    sprites_list = pygame.sprite.spritecollide(hero, enemies, False)
    if len(sprites_list) > 0:
        finish = True
        res = "You LOSER"
    
    if pygame.sprite.collide_rect(hero, enemyFreez):
        enemyFreezFlag = True
        enemy_start_time = t()
        enemyFreez.rect.y = randint(-100, 0)
        enemyFreez.rect.x = randint(50, width-50)

    if pygame.sprite.collide_rect(hero, playerFreez):
        playerFreezFlag = True
        player_start_time = t()
        playerFreez.rect.y = randint(-100, 0)
        playerFreez.rect.x = randint(50, width-50)

    if not(finish) and score == 10:
        finish = True
        res = "You WINER"

    if not(finish) and lost == 3:
        finish = True
        res = "You LOSER"

    if not(finish):
        hero.reset()
        enemies.draw(main_win)
        bullets.draw(main_win)

    if enemyFreezFlag:
        if t() - enemy_start_time > 3:
            enemyFreezFlag = False

    if playerFreezFlag:
        if t() - player_start_time > 3:
            playerFreezFlag = False


    lost_label = pygame.font.SysFont('arial', 25).render('Lost: ' + str(lost), True, (255,255,255))
    score_label = pygame.font.SysFont('arial', 25).render('Score: ' + str(score), True, (255,255,255))
    main_win.blit(lost_label, (10,10))
    main_win.blit(score_label, (10,35))
    if finish:
        res_img = pygame.font.SysFont('arial', size).render(res, True, (255,255,0))
        main_win.blit(res_img, (300, 250))

def getCrossClick():
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            return False
    return True

#window
main_win = pygame.display.set_mode((width, height))
pygame.display.set_caption('<<__SpaceShooter__>>')
bg = pygame.transform.scale(pygame.image.load("galaxy.jpg"), (width, height))

#var
clock = pygame.time.Clock()
run = True
finish = False
pygame.mixer.music.load('space.ogg')
lost = 0
score = 0
bullets = pygame.sprite.Group()
fire_timer = 10
res = None
enemyFreezFlag = False
playerFreezFlag = False
enemy_start_time = 0
player_start_time = 0

#pygame.mixer.music.play()
lost_sound = pygame.mixer.Sound('damage.ogg')
fire_sound = pygame.mixer.Sound('fire.ogg')

#sprites
hero = Hero('hero.png', height, (width-size)/2, 5)
enemies = pygame.sprite.Group()
for i in range(5):
    enemy = Enemy('asteroid.png', randint(50, width-50), randint(-100, 0), 3)
    #enemy = pygame.transform.rotate(enemy, randint(0, 360))
    enemies.add(enemy)
enemyFreez = SpriteSleep('greeen.png', randint(50, width-50), randint(-100, 0), 5)
playerFreez = SpriteSleep('red.png', randint(50, width-50), randint(-100, 0), 5)

#main loop
while run:
    run = getCrossClick()
    getGFrame()
    pygame.display.update()
    clock.tick(60)
