import pygame
import pygame.freetype
import pygame.image


class Plat(pygame.sprite.Sprite):
    def __init__(self, Conveyor, Nomor, FONT) -> None:
        super().__init__()
        self.image = pygame.image.load('sprites/Plat.png')
        self.font = FONT
        self.nomor = Nomor
        self.teks, self.teksrect = self.font.render(
            "", pygame.Color("#FFFFFF"))
        self.speed = 11
        self.pos = self.image.get_rect().move(-300, 350)
        self.moving = Conveyor.working

    def switch(self):
        self.moving = not self.moving

    def setPlat(self):
        self.teks, self.teksrect = self.font.render(
            self.nomor, pygame.Color("#FFFFFF"))

    def move(self):
        if self.moving:
            self.pos = self.pos.move(self.speed, 0)
            if self.pos.left > 810:
                self.kill()


class Conveyor(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super(Conveyor, self).__init__()
        self.images = [pygame.image.load("sprites/conv"+str(i)+".png")
                       for i in [0, 60, 120, 180]]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect().move(-100, 450)
        self.working = False

    def switch(self):
        self.working = not self.working

    def update(self):
        if self.working:
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]


class Press(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load("sprites/press.png")
        self.rect = self.image.get_rect()
        self.pos = self.rect.move(220, -270)
        self.speed = 10
        self.working = False

    def switch(self):
        self.working = not self.working

    def update(self):
        if self.working:
            self.pos = self.pos.move(0, self.speed)
            if self.pos.top < -270:
                self.speed = -(self.speed)
                self.working = False
            elif self.pos.top > -90:
                self.speed = -(self.speed)
                return True
            return False
