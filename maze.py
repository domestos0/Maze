#создай игру "Лабиринт"!
from pygame import *

'''Классы'''

#Класс-родитель для спрайтов
class GameSprite(sprite.Sprite):
    #Конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        #Каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        #Каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    #Метод для отрисовки героя на экране
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#Класс самого игрока
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_width - 80:
            self.rect.y += self.speed

class Enemy(GameSprite): #Ходит по горизонтали
    direction = 'left' #Свойство направления врага
    def update(self):
        if self.rect.x <= 470:
            self.direction = 'right'
        if self.rect.x >= win_width - 85:
            self.direction = 'left'

        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, red, green, blue, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.red = red
        self.green = green
        self.blue = blue
        self.width = wall_width
        self.height = wall_height
        #Картинка стены - прямоугольник нужного размера и цвета
        self.image = Surface((self.width, self.height))
        self.image.fill((red, green, blue))
        #Каждый спрайт должен хранить свойство rect - прямоугольник
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#Игровая сцена
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Лабиринт')
background = transform.scale(image.load('background.jpg'), (win_width, win_height))

#Персонажи игры
player = Player('hero.png', 5, 400, 65, 65, 4)
enemy = Enemy('enemy.png', 620, 280, 65, 65, 2)
final = GameSprite('treasure.png', 580, 400, 15, 15, 0)
#Стены
w1 = Wall(143, 205, 50, 100, 20, 590, 10) #Сверху темно-зеленый
w2 = Wall(124, 43, 50, 100, 480, 590, 10) #Снизу бордовый
w3 = Wall(4, 205, 50, 100, 20, 10, 370) #Слево светло-зеленый
w4 = Wall(152, 180, 131, 210, 130, 10, 350) 
w5 = Wall(86, 255, 126, 320, 20, 10, 350)
w6 = Wall(34, 214, 187, 430, 130, 10, 350)
w7 = Wall(222, 199, 59, 430, 130, 50, 10)
w8 = Wall(46, 182, 26, 480, 130, 10, 350)
w9 = Wall(16, 102, 246, 590, 30, 10, 350)
w10 = Wall(50, 99, 111, 590, 370, 100, 10)

game = True
finish = False
clock = time.Clock()
FPS = 60

font.init()
font = font.SysFont('Verdana', 70)
win = font.render('YOU WIN =)', True, (105, 165, 254))
lose = font.render('YOU LOSE :(', False, (255, 150, 135))

#музыка
mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        window.blit(background, (0,0))
        player.update()
        enemy.update()
        player.reset()
        enemy.reset()
        final.reset()
        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        w4.draw_wall()
        w5.draw_wall()
        w6.draw_wall()
        w7.draw_wall()
        w8.draw_wall()
        w9.draw_wall()
        w10.draw_wall()

        #Ситуация "Проигрыш"
        if sprite.collide_rect(player, enemy) or sprite.collide_rect(player, w1) or sprite.collide_rect(player, w2) or sprite.collide_rect(player, w3) or sprite.collide_rect(player, w4) or sprite.collide_rect(player, w5) or sprite.collide_rect(player, w6) or sprite.collide_rect(player, w7) or sprite.collide_rect(player, w8) or sprite.collide_rect(player, w9) or sprite.collide_rect(player, w10):
            finish = True
            window.blit(lose, (200,200))
            kick.play()

        #Ситуация "Выигрыш"
        if sprite.collide_rect(player, final):
            finish = True
            window.blit(win, (200,200))
            money.play()

    display.update()
    clock.tick(FPS)