__author__ = 'Pradyumn Vikram'


# imports
import pygame
import random
import os

# setting window dimensions
WIN_WIDTH = 600
WIN_HEIGHT = 300

# initializing pygame, loading images and declaring some variables
pygame.init()

STAT_FONT = pygame.font.SysFont('pixelmix', 30)
END_GAME = pygame.font.SysFont('pixelmix_bold', 40)

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Dino Game')

root = os.path.dirname(__file__)

dinoRun = [pygame.image.load((os.path.join(root, 'imgs\\run' + str(x) + '.png')))
           for x in range(1, 3)]
dinoJump = pygame.image.load(os.path.join(root, 'imgs\\jump.png'))
cactusImgs = [pygame.image.load(os.path.join(
    root, 'imgs\\CACTUS' + str(j) + '.png')) for j in range(1, 6)]
baseImg = pygame.image.load(os.path.join(root, 'imgs\\floor-1.png'))
cloudImg = pygame.image.load(os.path.join(root, 'imgs\\1x-cloud.png'))
deadDino = pygame.image.load(os.path.join(root, 'imgs\\death.png'))
birds = [pygame.image.load(os.path.join(root, 'imgs\\enemy'+str(i)+'.png')) for i in range(1, 3)]
duckDino = [pygame.image.load(os.path.join(root, 'imgs\\low'+str(k)+'.png')) for k in range(1, 3)]

# main player class


class Dino:
    img_count = 0

    def __init__(self, x, y):
        self.imgs = dinoRun
        self.tick_count = 0
        self.img = self.imgs[0]
        self.x = x
        self.y = y
        self.jumpImg = False
        self.duckImg = False
        self.duck = duckDino

    def draw(self, win):
        if not self.jumpImg:
            if not self.duckImg:
                self.img_count += 1
                if self.img_count % 4 != 0:
                    self.img = self.imgs[0]
                else:
                    self.img = self.imgs[1]
            else:
                self.img_count += 1
                if self.img_count % 4 != 0:
                    self.img = self.duck[0]
                else:
                    self.img = self.duck[1]
                self.img = pygame.transform.scale(
                    self.img, (self.img.get_width()//2, self.img.get_height()//2))
        win.blit(self.img, (self.x, self.y))

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

# floor class


class Base:
    def __init__(self, y):
        self.base_width = baseImg.get_width()
        self.img = baseImg
        self.vel = 15
        self.x1 = 0
        self.x2 = self.base_width
        self.y = y

    def move(self):
        self.x1 -= self.vel
        self.x2 -= self.vel

        if self.x1 + self.base_width < 0:
            self.x1 = self.x2 + self.base_width

        if self.x2 + self.base_width < 0:
            self.x2 = self.x1 + self.base_width

    def draw(self, win):
        win.blit(self.img, (self.x1, self.y))
        win.blit(self.img, (self.x2, self.y))

# Enemy parent class


class Enemy:
    def collide(self, dino):
        dino_mask = dino.get_mask()
        mask = pygame.mask.from_surface(self.img)
        offset = (self.x - dino.x, self.y - round(dino.y))
        point = dino_mask.overlap(mask, offset)

        if point:
            return True
        return False

    def passed(self, dude):
        if dude.x > self.x + self.img.get_width():
            return True
        return False

# Cactus obstacle class


class Cactus(Enemy):
    def __init__(self, x):
        super().__init__()
        self.y = 200
        self.vel = 10
        self.x = x
        self.imgs = cactusImgs
        self.img = random.choice(self.imgs)

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def move(self):

        self.x -= self.vel

# bird parent class


class Bird(Enemy):
    def __init__(self):
        super().__init__()
        self.imgs = birds
        self.img_count = 0
        self.x = 600
        self.y = WIN_HEIGHT - random.choice([150, 175, 125])
        self.vel = 15
        self.img = self.imgs[0]
        self.img = pygame.transform.scale(
            self.img, (self.img.get_width()//2, self.img.get_height()//2))

    def draw(self, win):
        self.img_count += 1
        if self.img_count % 4 != 0:
            self.img = self.imgs[0]
        else:
            self.img = self.imgs[1]
        self.img = pygame.transform.scale(
            self.img, (self.img.get_width()//2, self.img.get_height()//2))
        win.blit(self.img, (self.x, self.y))

    def move(self):
        self.x -= self.vel

# function to draw window for every frame


def redraw_window(dino, base, cactii, score):
    win.fill((220, 220, 220))
    dino.draw(win)
    base.draw(win)
    for cactus in cactii:
        cactus.draw(win)
    text = STAT_FONT.render('Score:  ' + str(score), 1, (10, 10, 10))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    if dino.duckImg:
        dino.duckImg = False
        dino.y = 200
    pygame.display.update()

# main loop


def main():
    # decalring variables and class instances
    isJump = False
    jumpCount = 8
    clock = pygame.time.Clock()
    base = Base(245)
    run = True
    cactii = [Cactus(600)]
    dino = Dino(20, 200)
    score = 0
    while run:
        dino.jumpImg = isJump
        score += 1
        base.move()
        for cactus in cactii:
            cactus.move()
            if cactus.collide(dino):
                run = False
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        redraw_window(dino, base, cactii, score)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            isJump = True
        if keys[pygame.K_DOWN]:
            dino.y += 10
            dino.duckImg = True

        if isJump:
            if jumpCount >= -8:
                dino.img = dinoJump
                #Force = 1/2*m*v^2
                #v = jumpCount
                #dino.y -= Force
                dino.y -= (jumpCount * abs(jumpCount))/2
                # decreasing velocty to simulate realsitic jum
                jumpCount -= 1
            else:
                # resetting the velocity variable for next jump
                jumpCount = 8
                isJump = False
        # adding new enemies if old ones have left the screen
        for enemy in cactii:
            if enemy.passed(dino):
                cactii.remove(enemy)
                choose = random.choice(['bird', 'cactus'])
                if choose == 'bird':
                    cactii.append(Bird())
                else:
                    cactii.append(Cactus(600))
    # adding some after game clean-up code
    if not run:
        while True:
            endGame = END_GAME.render('GAME OVER!', 1, (10, 10, 10))
            win.fill((220, 220, 220))
            text = STAT_FONT.render('Score: ' + str(score), 1, (10, 10, 10))
            win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
            win.blit(deadDino, (dino.x, dino.y))
            win.blit(endGame, (220, WIN_HEIGHT//2 - 20))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    break


# running the whole thing!
main()
