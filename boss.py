
import pygame
import random
from math import sqrt
import os
from conf import mides_pantalla
from bala import Bala
from sang import Gore
from sprite_sheets import crea_llista_imatges


#------------------------load player image-----------------------------------
#--------------------- ll_walk
ll_run = []
for ang in range(0,360,90):
    l = crea_llista_imatges(pygame.transform.rotate(pygame.image.load(os.path.join("imatges","boss","walk.png")),ang), 7)
    ll_run.append(l)

#-------------------- ll_fire_atack
ll_fire_atack = []
for ang in range(0,360,90):
    l = crea_llista_imatges(pygame.transform.rotate(pygame.image.load(os.path.join("imatges","boss","fire_attack.png")),ang), 8)
    ll_fire_atack.append(l)

#-------------------- ll_mele
ll_mele = []
for ang in range(0,360,90):
    l = crea_llista_imatges(pygame.transform.rotate(pygame.image.load(os.path.join("imatges","boss","close_attack.png")),ang), 9)
    ll_mele.append(l)

#-------------------- ll_dead
ll_dead = []

#-------------------- ll_shoot
ll_shoot = []


class BOSS(pygame.sprite.Sprite):

    def __init__(self, prota, grup_sp_mov, grup_obs):
        super().__init__()
        self.grup_sp_mov = grup_sp_mov
        self.protagonista = prota
        self.grup_obs = grup_obs
        # Listes
        self.direccions = [[1,0], [0,-1], [-1,0], [0,1]]
        self.ll_faceing = ['RIGHT','UP', 'LEFT', 'DOWN']
        self.ll_estats = ['mele', 'fire','persegueix','dead']
        self.velocitats = {'camina':2.5, 'parat':0}
        self.ll_atacs = ['mele','fire']
        # Stats del BOSS
        self.fps = 1500
        self.vida = 65
        self.range = 120
        self.cadencia = 1000
        self.estat = 'persegueix'
        self.vel = self.velocitats['camina']
        self.damage = 0
        # Direccio inicial
        i = 0
        self.direccio_vec = self.direccions[i]
        self.faceing = self.ll_faceing[i]
        # Imatge
        self.ll_generica = ll_run
        self.llista_im = ll_run[i]   #llista de imatges del persnatge
        self.image = self.llista_im[0]
        self.index = 0
        # Atributs rect
        self.rect = self.image.get_rect()
        self.rect.center = (0,0)
        self.minx = 0
        self.miny = 0
        self.maxx = 0
        self.maxy = 0
        self.radius = 35
        # Variables de temps
        self.t_dispara = pygame.time.get_ticks()
        self.t_tocat = pygame.time.get_ticks()

    def canvia_direccio(self, direccio):
        '''
        Direccio ha de ser un vector o una direccio
        '''
        if direccio == [1,0] or direccio == 'RIGHT':
            self.direccio_vec = [1,0]
        elif direccio == [-1,0] or direccio == 'LEFT':
            self.direccio_vec = [-1,0]
        elif direccio == [0,-1] or direccio == 'UP':
            self.direccio_vec = [0,-1]
        elif direccio == [0,1] or direccio == 'DOWN':
            self.direccio_vec = [0,1]

    def avança(self):
        # Avanç en les x
        oldx = self.rect.x
        self.rect.x = self.rect.x + self.direccio_vec[0]*self.vel
        num_col_sp = pygame.sprite.spritecollide(self, self.grup_sp_mov, False, pygame.sprite.collide_rect_ratio(0.6))
        if len(num_col_sp)> 1:
            self.rect.x = oldx
        num_col_obs = pygame.sprite.spritecollide(self, self.grup_obs, False, pygame.sprite.collide_rect_ratio(1))
        if len(num_col_obs)> 0:
            self.rect.x = oldx
        # Avanç en les y
        oldy = self.rect.y
        self.rect.y = self.rect.y + self.direccio_vec[1]*self.vel
        num_col_sp = pygame.sprite.spritecollide(self, self.grup_sp_mov, False, pygame.sprite.collide_rect_ratio(0.6))
        if len(num_col_sp)> 1:
            self.rect.y = oldy
        num_col_obs = pygame.sprite.spritecollide(self, self.grup_obs, False, pygame.sprite.collide_rect_ratio(1))
        if len(num_col_obs)> 0:
            self.rect.y = oldy

    def update_direccio(self):
        '''
        Actualitza el faceing
        '''
        x = self.direccio_vec[0]
        y = self.direccio_vec[1]
        if abs(x) > abs(y):
            if x > 0:
                faceing = 'RIGHT'
            else:
                faceing = 'LEFT'
        else:
            if y > 0:
                faceing = 'DOWN'
            else:
                faceing = 'UP'
        if faceing != self.faceing:
            self.faceing = faceing
            if faceing == 'RIGHT':
                self.llista_im = self.ll_generica[0]
            elif faceing == 'LEFT':
                self.llista_im = self.ll_generica[2]
            elif faceing == 'UP':
                self.llista_im = self.ll_generica[1]
            elif faceing == 'DOWN':
                self.llista_im = self.ll_generica[3]
            else:
                raise ValueError("No saps angles i escrius malament la direccio")

    def canvia_estat(self, estat):
        '''
        Fa els canvis necessaris quan es canvia d'estat
        ['mele', 'fire','persegueix','dispara','dead']
        '''
        self.estat = estat
        if estat == 'dead':
            self.vel = self.velocitats['parat']
            self.kill()
        elif estat == 'tocat':
            # Se li treu la vida a la calse bala
            pass
        elif estat == 'mele':
            self.damage = 0
            self.fps = 1000
            self.temps_ataca = pygame.time.get_ticks()
            self.vel = self.velocitats['camina']
            self.ll_generica = ll_mele
            self.llista_im = ll_mele[self.ll_faceing.index(self.faceing)]
            self.image = self.llista_im[0]
            self.index = 0
        elif estat == 'fire':
            self.damage = 0
            self.fps =  1000
            self.temps_ataca = pygame.time.get_ticks()
            self.vel = self.velocitats['camina']
            self.ll_generica = ll_fire_atack
            self.llista_im = ll_fire_atack[self.ll_faceing.index(self.faceing)]
            self.image = self.llista_im[0]
            self.index = 0
        elif estat == 'disparant':
            self.damage = 0
            self.fps = 1000
            self.vel = self.velocitats['parat']
            self.ll_generica = ll_shoot                                            
            self.llista_im = ll_shoot[self.ll_faceing.index(self.faceing)]
            self.image = self.llista_im[0]
            self.index = 0
        elif estat == 'persegueix':
            self.damage = 0
            self.fps = 1500
            self.vel = self.velocitats['camina']
            self.ll_generica = ll_run
            self.llista_im = self.ll_generica[self.ll_faceing.index(self.faceing)]
            self.image = self.llista_im[0]
            self.index = 0
 
        else:
            raise ValueError("Escriu be l'estat capullo!")

    def update_estat(self):
        '''
        Actualitza l'estat del zombie
        '''
        # Si el zombie (self) esta aprop del protagonista es canvia el estat a
        # perseguir fent que el zombie tri la direccio cap al protagonista
        if self.vida <= 0:
            self.canvia_estat('dead')
            
        elif self.estat == 'persegueix':
            self.direccio_vec = [(1/self.dist)*(self.protagonista.rect.center[0]-self.rect.center[0]),(1/self.dist)*(self.protagonista.rect.center[1]-self.rect.center[1])]                
            if self.dist<self.range:
                atac = random.choice(self.ll_atacs)
                self.canvia_estat(atac)
                
        elif self.estat == 'mele':
            if len(self.llista_im)-1==self.index:
                if self.dist < self.range:
                    atac = random.choice(self.ll_atacs)
                    self.canvia_estat(atac)
                else:
                    self.canvia_estat('persegueix')
                
            elif self.index == 2 and self.dist < self.range and self.damage == 0:
                self.protagonista.vidas -= 1
                self.damage += 1
            elif self.index == 6 and self.dist < self.range+5 and self.damage <= 1:
                self.protagonista.vidas -= 1
                self.damage += 1
                
        elif self.estat == 'fire':
            if len(self.llista_im)-1==self.index:
                if self.dist < self.range:
                    atac = random.choice(self.ll_atacs)
                    self.canvia_estat(atac)
                else:
                    self.canvia_estat('persegueix')
            elif abs(5-self.index) < 1 and self.dist < self.range+20 and self.damage <= 1:
                self.damage += 1
                self.protagonista.vidas -= 1

        elif self.estat == 'tocat':
            self.canvia_estat('persegueix')
                
        elif self.estat == 'disparant':
            if abs(len(self.llista_im)-self.index)<1:
                self.canvia_estat('persegueix')
            elif abs(5-self.index) < 1:
                pass

    def update(self):
        self.dist = sqrt((self.rect.centerx-self.protagonista.rect.centerx)**2 + (self.rect.centery-self.protagonista.rect.centery)**2)
        self.update_estat()
        self.update_direccio()
        # fa caminar el personatge dintre dels limits
        self.avança()            
        # Posa limits al zombie
        if self.faceing == 'RIGHT' or self.faceing == 'LEFT':
            if self.rect.left < self.minx:
                self.canvia_direccio('RIGHT')
            elif self.rect.right > self.maxx:
                self.canvia_direccio('LEFT')
        elif self.faceing == 'UP' or self.faceing == 'DOWN':
            if self.rect.top < self.miny:
                self.canvia_direccio('DOWN')
            elif self.rect.bottom > self.maxy:
                self.canvia_direccio('UP')
        
        # actualitza el fotograma del personatge a la velocitat de self.fps
        t = pygame.time.get_ticks()
        ta = t % self.fps
        self.index = (ta * len(self.llista_im)) // self.fps
        self.image = self.llista_im[self.index]
        self.image.convert_alpha()
        if abs(len(self.llista_im)-self.index)<1:
            self.index = 0











        
