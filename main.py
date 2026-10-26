import pygame
from conf import *
from banquise import Banquise
from pinguin import Pinguin
import lecture

pygame.init()

clock = pygame.time.Clock()

class App():
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.fond = pygame.image.load("fond.jpeg").convert_alpha()
        self.fond = pygame.transform.scale(self.fond, (WIDTH, HEIGHT))
        self.banquise = Banquise()
        self.pinguin = Pinguin(self.banquise)
        self.mannette = True
        tmp = lecture.init()
        if not tmp:
            self.mannette = False
            print("Pas de mannette")
        self.running = True
        self.timer = 0
        self.sum = 0

    def run(self):
        while self.running:
            self.inpu()
            self.draw()
            self.update()
            clock.tick(FPS)


    def update(self):
        self.banquise.update()
        self.pinguin.update()


    def draw(self):
        self.screen.blit(self.fond, (0, 0))
        self.banquise.draw(self.screen)
        self.pinguin.draw(self.screen)
        pygame.display.flip()

    def inpu(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            touches = pygame.key.get_pressed()

            # On bloque les contrôles si le pingouin est en train de réapparaître
            if self.pinguin.etat != "ATTENTE":
                if self.mannette:
                    tmp = lecture.get_info()
                    if tmp is not None:
                        tmp = int(70/1100 * tmp)
                        if abs(tmp) > MAX_ANGLE:
                            tmp = MAX_ANGLE * abs(tmp)//tmp

                        self.sum += tmp
                        self.timer += 1

                    if self.timer > MOY:
                        self.banquise.rotation = int(self.sum/MOY)
                        self.timer = 0
                        self.sum = 0
                        self.banquise.tourne()


                if touches[pygame.K_LEFT]:
                    self.banquise.bascule(2)
                if touches[pygame.K_RIGHT]:
                    self.banquise.bascule(-2)


App().run()