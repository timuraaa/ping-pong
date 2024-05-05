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
        if keys[K_UP] and self.rect.y >= 5:
            self.rect.y -= self.speed
        elif keys[K_DOWN] and self.rect.y <= WIN_HEIGHT - 5:
            self.rect.y += self.speed

    def update_r(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y >= 5:
            self.rect.y -= self.speed
        elif keys[K_s] and self.rect.y <= WIN_HEIGHT - 5:
            self.rect.y += self.speed
    


player1 = Player('racket.png', 50, 175, 10, 50, 150)
player2 = Player('racket.png', 600, 175, 10, 50, 150)

game = True
finish = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    window.fill(BG)

    if not finish:
        pass

        player1.reset()
        player1.update()

        player2.reset()
        player2.update()

    display.update()
    clock.tick(FPS)