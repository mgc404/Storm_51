
import pygame
import os

ll_im = []
for i in range(0,40,5):
    if i <= 15:
        ll_im.append(pygame.transform.scale(pygame.image.load(os.path.join("imatges","sang","sang_01.png")),(50+i,50+i)))
    elif 15<i<30:
        ll_im.append(pygame.transform.scale(pygame.image.load(os.path.join("imatges","sang","sang_02.png")),(50+i,50+i)))
    else:
        ll_im.append(pygame.transform.scale(pygame.image.load(os.path.join("imatges","sang","sang_03.png")),(50+i,50+i)))

class Gore(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.llista_im = ll_im
        self.count = 0
        self.image = ll_im[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self):
        if self.count == len(self.llista_im):
            self.image = self.llista_im[len(self.llista_im)-1]
        else:
            self.image = self.llista_im[self.count]
            self.count = self.count + 1
