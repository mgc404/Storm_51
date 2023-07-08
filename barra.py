
import pygame
import os

bar_empty_1 = pygame.transform.scale(pygame.image.load(os.path.join("imatges","player","bar_empty_1.png")),(20,20))
bar_empty_2 = pygame.transform.scale(pygame.image.load(os.path.join("imatges","player","bar_empty_2.png")),(20,20))
bar_empty_3 = pygame.transform.scale(pygame.image.load(os.path.join("imatges","player","bar_empty_3.png")),(20,20))

bar_full_1 = pygame.transform.scale(pygame.image.load(os.path.join("imatges","player","bar_full_1.png")),(20,20))
bar_full_2 = pygame.transform.scale(pygame.image.load(os.path.join("imatges","player","bar_full_2.png")),(20,20))
bar_full_3 = pygame.transform.scale(pygame.image.load(os.path.join("imatges","player","bar_full_3.png")),(20,20))
class Health_bar:
    def __init__(self,prota):
        self.prota = prota
        self.vidas = prota.vidas
        self.ll_barras = []
        self.ll_barras.append(Barra_vida(prota,1))
        self.grup_barras = pygame.sprite.Group()
        for i in range(self.vidas-2):
            self.ll_barras.append(Barra_vida(prota,2,numero=i))
        self.ll_barras.append(Barra_vida(prota,3))
        for barra in self.ll_barras:
            self.grup_barras.add(barra)
            
    def draw(self,s):
        self.grup_barras.draw(s)
        
    def update(self):
        dif =self.vidas-self.prota.vidas
        if dif>0:
            for i in range(dif):
                self.ll_barras[self.vidas-1-i].switch()
        else:
            for i in range(abs(dif)):
                self.ll_barras[self.vidas+i].switch()
        self.vidas = self.prota.vidas
            
        
class Barra_vida(pygame.sprite.Sprite):

    def __init__(self, prota,tipus,numero=0):
        super().__init__()
        self.full = True
        self.tipus = tipus
        if tipus == 1:
            self.image = bar_full_1.convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.center = (60,40)
        elif tipus == 2:
            self.image = bar_full_2.convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.center = (80+20*numero,40)
        else:
            self.image = bar_full_3.convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.center = (80+20*(prota.vidas-2),40)
            
    def switch(self):
        self.full = not(self.full)
        if self.full:
            if self.tipus == 1:
                self.image = bar_full_1
            elif self.tipus == 2:
                self.image = bar_full_2
            elif self.tipus == 3:
                self.image = bar_full_3
        else:
            if self.tipus == 1:
                self.image = bar_empty_1
            elif self.tipus == 2:
                self.image = bar_empty_2
            elif self.tipus == 3:
                self.image = bar_empty_3
