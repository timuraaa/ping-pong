from pygame import *

WIN_WIDTH = 700
WIN_HEIGHT = 500
FPS = 40
BG = (33, 133, 108)

window = display.set_mode((WIN_WIDTH, WIN_HEIGHT))
display.set_caption('ping-pong')

clock = time.Clock()

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
    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y >= 5:
            self.rect.y -= self.speed
        elif keys[K_s] and self.rect.y <= WIN_HEIGHT - 5:
            self.rect.y += self.speed

    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y >= 5:
            self.rect.y -= self.speed
        elif keys[K_DOWN] and self.rect.y <= WIN_HEIGHT - 5:
            self.rect.y += self.speed

class Ball(GameSprite):
    def __init__(self, player_image, player_x, player_y, speed, size_x, size_y):
        super().__init__(player_image, player_x, player_y, speed, size_x, size_y)
        self.speed_x = speed
        self.speed_y = speed

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.y >= WIN_HEIGHT:
            self.speed_y *= -1
        
        if self.rect.y <= 0:
            self.speed_y *= -1
    
    def collide_rect(self, player):
        if self.rect.colliderect(player):
            self.speed_x *= -1

speed_x = 3
speed_y = 3

player1 = Player('racket.png', 50, 175, 10, 50, 150)
player2 = Player('racket.png', 600, 175, 10, 50, 150)
ball = Ball('tenis_ball.png', 320, 220, 10, 50, 50)

game = True
finish = False

font.init()
font_win = font.SysFont('Arial', 50)
win_r = font_win.render('WIN RIGHT PLAYER', True, (255, 255, 255))
win_l= font_win.render('WIN LEFT PLAYER', True, (255, 255, 255))

winner = None

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    window.fill(BG)

    if not finish:
        
        player1.reset()
        player1.update_l()

        player2.reset()
        player2.update_r()

        ball.reset()
        ball.update()

        ball.collide_rect(player1)
        ball.collide_rect(player2)

        if ball.rect.x < 50:
            winner = win_r
            finish = True
        
        if ball.rect.x > WIN_WIDTH - 50:
            winner = win_l
            finish = True
    
    elif finish:
        window.blit(winner, (50, 200))

    display.update()
    clock.tick(FPS)
