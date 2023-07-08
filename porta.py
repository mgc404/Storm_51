
import pygame
from pygame import Rect
import os
from sprite_sheets import crea_llista_imatges
from conf import mides_pantalla

ll_im_Door_U1 = crea_llista_imatges(pygame.image.load(os.path.join("imatges","portes","Door_U.png")), 4)
ll_im_Door_D1 = crea_llista_imatges(pygame.image.load(os.path.join("imatges","portes","Door_D.png")), 4)
ll_im_Door_R1 = crea_llista_imatges(pygame.image.load(os.path.join("imatges","portes","Door_R.png")), 4)
ll_im_Door_L1 = crea_llista_imatges(pygame.image.load(os.path.join("imatges","portes","Door_L.png")), 4)

ll_im_Enter_door_U1 = crea_llista_imatges(pygame.image.load(os.path.join("imatges","portes",'Enter_door_U.png')),10)
ll_im_Enter_door_D1 = crea_llista_imatges(pygame.image.load(os.path.join("imatges","portes","Enter_door_D.png")), 10)

ll_im_Exit_door_U1 = crea_llista_imatges(pygame.image.load(os.path.join("imatges","portes","Exit_door_U.png")), 9)
ll_im_Exit_door_D1 = crea_llista_imatges(pygame.image.load(os.path.join("imatges","portes","Exit_door_D.png")), 9)

ll_im_Door_U2 = crea_llista_imatges(pygame.image.load(os.path.join("imatges","portes","Door_U_2.png")), 4)
ll_im_Door_D2 = crea_llista_imatges(pygame.image.load(os.path.join("imatges","portes","Door_D_2.png")), 4)
ll_im_Door_R2 = crea_llista_imatges(pygame.image.load(os.path.join("imatges","portes","Door_R_2.png")), 4)
ll_im_Door_L2 = crea_llista_imatges(pygame.image.load(os.path.join("imatges","portes","Door_L_2.png")), 4)

ll_im_Enter_door_U2 = crea_llista_imatges(pygame.image.load(os.path.join("imatges","portes",'Enter_door_U_2.png')),10)
ll_im_Enter_door_D2 = crea_llista_imatges(pygame.image.load(os.path.join("imatges","portes","Enter_door_D_2.png")), 10)

ll_ascensor = crea_llista_imatges(pygame.image.load(os.path.join("imatges","portes","Elevator.png")), 4)


ll_im_Door_D1.reverse()
ll_im_Door_D2.reverse()
ll_im_Door_R1.reverse()
ll_im_Door_R2.reverse()
ll_im_Enter_door_D1.reverse()
ll_im_Enter_door_D2.reverse()
ll_im_Exit_door_D1.reverse()

ll_orient = ['U', 'R', 'D', 'L']
d_portes1 = {'Door':{'U':ll_im_Door_U1,'D':ll_im_Door_D1,'R':ll_im_Door_R1,'L':ll_im_Door_L1},\
            'Enter':{'U':ll_im_Enter_door_U1,'D':ll_im_Enter_door_D1},\
            'Exit':{'D':ll_im_Exit_door_D1,'U':ll_im_Exit_door_U1}}
d_portes2 = {'Door':{'U':ll_im_Door_U2,'D':ll_im_Door_D2,'R':ll_im_Door_R2,'L':ll_im_Door_L2},\
            'Enter':{'U':ll_im_Enter_door_U2,'D':ll_im_Enter_door_D2},\
            'Exit':{}}
class Porta(pygame.sprite.Sprite):
    '''
    Tipus Door = canvi de sala
    Tipus Exit = sortida exterior
    tipus Enter = entrada interior
    tipus Elevator = ascensor
    estats = [tancada, oberta, animacio]
    
    '''
    def __init__(self, orientacio, tipus, lvl, topleft=0, panel=0):
        super().__init__()
        if tipus == 'ascensor':
            # Animacio
            self.fps = 500
            self.llista_im = ll_ascensor
            self.image = self.llista_im[0]
            self.rect = topleft
            
        else:
            # Asignacio d'imatges segons tipus
            if lvl == 1:
                try:
                    self.llista_im = d_portes1[tipus][orientacio]
                except KeyError:
                    raise ValueError('Falta posar al diccionari del modul portas la llista amb els frames de la porta')
            elif lvl == 2:
                try:
                    self.llista_im = d_portes2[tipus][orientacio]
                except KeyError:
                    raise ValueError('Falta posar al diccionari del modul portas la llista amb els frames de la porta')            
            # Animacio
            if tipus == 'Door':
                self.fps = 100
            elif tipus == 'Enter' or tipus == 'Exit':
                self.fps = 50
            # Atributs rects
            self.image = self.llista_im[0]
            self.rect = self.image.get_rect()
            self.rect.topleft = topleft #per a la sala principal = (75+6*70,0)
        self.tipus = tipus
        self.estat = 'tancada'
        self.orientacio = orientacio
        # Imatge (la image esta amb el rect)
        self.count = 0
        # Atributs de temps
        self.t_animacio = pygame.time.get_ticks()

    def update(self):
        delta = pygame.time.get_ticks() - self.t_animacio
        if self.count == len(self.llista_im)-1:
            self.image = self.llista_im[len(self.llista_im)-1]
        elif delta >= self.fps:
            self.t_animacio = pygame.time.get_ticks()
            self.count = self.count + 1
            self.image = self.llista_im[self.count]
            
            
class Mando_de_control(pygame.sprite.Sprite):
    def __init__(self, porta):
        super().__init__()
        self.porta = porta
        self.rect = Rect(porta.rect.right+1, porta.rect.top, porta.rect.width, porta.rect.height)
