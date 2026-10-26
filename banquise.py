import pygame
from conf import *

class Banquise(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_o = pygame.image.load("banquise.png").convert_alpha()
        tmp = self.image_o.get_size()
        self.image_o = pygame.transform.scale(self.image_o,(int(WIDTH*5/6),tmp[1]))

        self.image = self.image_o
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH//2 - self.rect.w//2
        self.rect.y = HEIGHT//1.1 - self.rect.h//2

        self.rotation = 0

        self.les_image = [pygame.transform.rotate(self.image_o,r) for r in range(-MAX_ANGLE-1,MAX_ANGLE+2)]

    def bascule(self,sens):
        self.rotation += sens
        if abs(self.rotation) >= MAX_ANGLE:
            self.rotation = MAX_ANGLE * abs(self.rotation)//self.rotation

    def tourne(self):
        self.image = self.les_image[self.rotation + MAX_ANGLE]
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 - self.rect.w // 2
        self.rect.y = HEIGHT // 1.1 - self.rect.h // 2

    def update(self):
        self.tourne()

    def draw(self,screen):
        screen.blit(self.image,self.rect)
