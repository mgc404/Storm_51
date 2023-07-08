
import pygame
from sprite_sheets import crea_llista_imatges
import os
from zombie import Zombie

#------------------------load player image-----------------------------------
llista_im_dreta = crea_llista_imatges(pygame.image.load(os.path.join("imatges","bala", "Laser_dreta.png")),4)
llista_im_esquerra = crea_llista_imatges(pygame.image.load(os.path.join("imatges","bala","Laser_esquerra.png")),4)
llista_im_abaix = crea_llista_imatges(pygame.image.load(os.path.join("imatges","bala","Laser_abaix.png")),4)
llista_im_adalt = crea_llista_imatges(pygame.image.load(os.path.join("imatges","bala","Laser_adalt.png")),4)
llista_im_adalt.reverse()
llista_im_esquerra.reverse()
ll_general_im = [llista_im_dreta,llista_im_esquerra,llista_im_adalt,llista_im_abaix]

#-----------------------------Player class-----------------------------------


class Bala(pygame.sprite.Sprite):
    def __init__(self, pos, direccio, damage, color, prota=0, grup_zombies=0):
        super().__init__()
        self.prota = prota
        # Stats de la bala
        self.fps = 175      # Velocitat de l'animació
        self.vel = 10    # Velocitat real del personatge
        self.dps = damage
        self.color = color
        # Llistes / diccionaris
        self.direccions = [[1,0],[-1,0],[0,-1],[0,1]]
        self.grup_zombies = grup_zombies
        d = {'RIGHT':[1,0], 'LEFT':[-1,0], 'UP':[0,-1], 'DOWN':[0,1]}
        # Direccio inicial
        i = self.direccions.index(d[direccio])
        self.direccio_vec = d[direccio]
        # Imatges
        self.llista_im = ll_general_im[i]   #llista de imatges del persnatge
        self.count = 0
        self.image = self.llista_im[0]
        # Atributs rect
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.maxy = 800
        self.maxx = 920
        self.radius = 5
        # Atributs de temps
        self.t_animacio = pygame.time.get_ticks()
        # Atributs so
        self.so_zomb_mort = pygame.mixer.Sound('so/zombi_morint.wav')
        self.so_zomb_hurt = pygame.mixer.Sound('so/zombie_ferit.wav')

    def move(self):
        self.rect.x = self.rect.x + self.direccio_vec[0]*self.vel
        self.rect.y = self.rect.y + self.direccio_vec[1]*self.vel

    def update(self):
        # Colisions
        if self.color == 'blue':
            ll_colisions = pygame.sprite.spritecollide(self, self.grup_zombies, False, pygame.sprite.collide_circle)
            for sp in ll_colisions:
                if sp is self.prota:
                    print('tocat')
                    t = pop(sp)
            if len(ll_colisions) > 0:
                self.kill()
                ll_colisions[0].canvia_estat('tocat')
                ll_colisions[0].vida -= self.dps
                if type(ll_colisions[0]) == Zombie:
                    if ll_colisions[0].vida<= 0:
                        self.so_zomb_mort.play()
                    else:
                        self.so_zomb_hurt.play()
        elif self.color == 'red':
            if pygame.sprite.collide_circle(self, self.prota):
                self.kill()
                self.prota.vidas -= 1
        # Elimina la sprite si surt del mapa
        if self.direccio_vec == [1,0] or self.direccio_vec == [-1,0]:
            if self.rect.right < 0:
                self.kill()
            elif self.rect.left > self.maxx:
                self.kill()
        elif self.direccio_vec == [0,-1] or self.direccio_vec == [0,1]:
            if self.rect.bottom < 0:
                self.kill()
            elif self.rect.top > self.maxy:
                self.kill()
        # Mou la bala
        self.move()
        # Animació
        delta = pygame.time.get_ticks() - self.t_animacio
        if self.count == 3:
            self.image = self.llista_im[3]
        elif delta >= self.fps:
            self.count = self.count + 1
            self.image = self.llista_im[self.count]
