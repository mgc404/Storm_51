

import pygame
import os
from random import randint

ll_im = []
xy = 30
for i in range(20):
    if i<=10:
        xy+=1
        ll_im.append(pygame.transform.scale(pygame.image.load(os.path.join("imatges","player","vida+.png")),(xy,xy)))
    else:
        xy-=1
        ll_im.append(pygame.transform.scale(pygame.image.load(os.path.join("imatges","player","vida+.png")),(xy,xy)))


class Life_up(pygame.sprite.Sprite):

    def __init__(self, pos, prota):
        super().__init__()
        self.vidas_inicials = prota.vidas_ini
        self.pos = pos
        self.prota = prota
        self.vida = randint(1,3)
        self.llista_im = ll_im
        self.count = 0
        self.image = ll_im[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.fps = 100
        self.t = pygame.time.get_ticks()

    def update(self):
        delta = pygame.time.get_ticks() - self.t
        if delta >= self.fps:
            self.t = pygame.time.get_ticks()
            self.count += 1
            if self.count== len(self.llista_im):
                self.count = 0
            self.image = self.llista_im[self.count].convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
        colisio = pygame.sprite.collide_rect(self,self.prota)
        if colisio:
            print('botiquin: ' + str(self.vida))
            print('vida prota avans: ' +str(self.prota.vidas))
            self.prota.vidas+=self.vida
            print('vida prota despres: ' +str(self.prota.vidas))
            print('vida max: ' +str(self.vidas_inicials))
            if self.prota.vidas > self.vidas_inicials:
                self.prota.vidas = self.vidas_inicials
            self.kill()
