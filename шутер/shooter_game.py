from pygame import *
import time as timer
import random

WIN_WIDTH = 700
WIN_HEIGHT = 500
FPS = 40

life = 3
lost = 0
score = 0

window = display.set_mode((WIN_WIDTH, WIN_HEIGHT))
display.set_caption('Space Invader')

clock = time.Clock()

background = transform.scale(image.load('galaxy.jpg'), (WIN_WIDTH, WIN_HEIGHT))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y) )

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x >= 5:
            self.rect.x -= self.speed
        elif keys[K_RIGHT] and self.rect.x <= WIN_HEIGHT - 5:
            self.rect.x += self.speed
        
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 10, 15, 20)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        global lost 
        self.rect.y += self.speed
        if self.rect.y >= WIN_HEIGHT:
            lost += 1
            self.rect.y = -75
            self.rect.x = random.randint(5, WIN_WIDTH - 75)
            self.speed = random.randint(1, 5)

class Asteroid(GameSprite):
    def update(self):
        global lost 
        self.rect.y += self.speed
        if self.rect.y >= WIN_HEIGHT:
            self.rect.y = -75
            self.rect.x = random.randint(5, WIN_WIDTH - 75)
            self.speed = random.randint(1, 5)
        
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.x <= -20:
            self.kill 

class Button(sprite.Sprite):
    def __init__(self, reference_image, pos_x, pos_y, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(reference_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

    def click(self, function):
        pressed = mouse.get_pressed()
        pos = mouse.get_pos()
        if pressed[0]:
            if self.rect.collidepoint(pos):
                function()
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y) )

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

num_bullets = 0
rel_time = False
start_rel = None

fire_song = mixer.Sound('fire.ogg')

player = Player('rocket.png', 75, 420, 10, 50, 100)

bullets = sprite.Group()
monsters = sprite.Group()
asteroid = sprite.Group()

for i in range(6):
    x = random.randint(5, WIN_WIDTH - 75)
    speed = random.randint(1, 3)
    enemy = Enemy('ufo.png', x, -75, speed, 80, 50)
    monsters.add(enemy)

for i in range(2):
    x = random.randint(5, WIN_WIDTH - 75)
    speed = random.randint(1, 3)
    enemy = Enemy('asteroid.png', x, -75, speed, 80, 50)
    asteroid.add(enemy)

reset_button = Button('asteroid.png', 200, 200, 80, 50)
def restart_game():
    global lost, score, num_bullets, life, monsters, bullets, asteroids, player, finish
    for b in bullets:
        b.kill()
    for m in monsters:
        m.kill()
    player.rect.x = 5
    player.rect.y = WIN_HEIGHT - 100
    for a in asteroid:
        a.kill()
    for i in range(6):
        x = random.randint(5, WIN_WIDTH - 75)
        speed = random.randint(1, 5)
        enemy = Enemy('ufo.png', x, -75, speed, 80, 50)
        monsters.add(enemy)
    score = 0
    lost = 0
    life = 3
    num_bullets = 0
    finish = False

game = True
finish = False

font.init()
font_score = font.SysFont('Arial', 36)
font_end = font.SysFont('Arial', 70)
font2 = font.SysFont('Arial', 36)

win = font_end.render('YOU WIN!!!', True, (255, 255, 255))
lose = font_end.render('YOU LOSE!!!', True, (255, 255, 255))
reload_text = font_score.render('ПЕРЕЗАРЯДКА', True, (255, 255, 255))

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN and not finish:
                if e.key == K_SPACE:
                    if num_bullets < 5:
                        player.fire()
                        fire_song.play()
                        num_bullets += 1
                    else:
                        rel_time = True
                        start_rel = timer.time() 

        if e.type == ACTIVEEVENT:
            print('Окно свернуто')
        
    window.blit(background, (0, 0))



    if not finish:
        if rel_time:
            now_time = timer.time()
            window.blit(reload_text, (300, 450))
            if now_time - start_rel >= 3:
                rel_time = False
                num_bullets = 0

        text_skip = font_score.render('Пропущено:' + str(lost), True, (255, 255, 255))
        window.blit(text_skip, (10, 50))

        text_score = font_score.render('Счет' + str(score), True, (255, 255, 255))
        window.blit(text_score, (10, 30))

        monsters.draw(window)

        asteroid.draw(window)
        asteroid.update()

        bullets.draw(window)
        bullets.update()

        player.reset()
        player.update()

        monsters.update()
    
        collide_bullets_and_enemy = sprite.groupcollide(bullets, monsters, True, True)
        for _ in collide_bullets_and_enemy:
            score += 1
            x = random.randint(5, WIN_WIDTH - 75)
            speed = random.randint(1, 5)
            enemy = Enemy('ufo.png', x, -75, speed, 80, 50)
            monsters.add(enemy)

        if sprite.spritecollide(player, monsters, True):
            life -= 1
        if lost >= 3:
            finish = True
            draw_end_text = lose
        if score >= 10:
            finish = True
            draw_end_text = win

        if sprite.spritecollide(player, asteroid, True):
            life -= 1

        if life <= 0:
            finish = True
            draw_end_text = lose

    elif finish:
        window.blit(draw_end_text, (200, 200))
        reset_button.click(restart_game)
        reset_button.reset()
        
    display.update()
    clock.tick(FPS)