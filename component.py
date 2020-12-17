import pygame


class Plat:
    def __init__(self) -> None:
        super().__init__()
        self.body = pygame.image.load('sprites/Plat.png').convert()
        self.nomor = ""
        self.speed = 1
        self.pos = self.body.get_rect().move(0, 20)

    def move(self):
        self.pos = self.pos.move(0, self.speed)
        if self.pos.right > 600:
            self.pos.left = 0


class Conveyor(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super(Conveyor, self).__init__()
        self.images = [pygame.image.load("sprites/conv"+str(i)+".png")
                       for i in [0, 60, 120, 180]]
        self.rect = pygame.Rect(, 400, 605, 60)
        self.index = 0
        self.image = self.images[self.index]

    def update(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
