
from sprite_sheets import crea_matriu_imatges
import pygame
import random
from math import sqrt
import os
from conf import mides_pantalla
from sang import Gore
#------------------------load player image-----------------------------------
llista_im_dreta = crea_matriu_imatges(pygame.image.load(os.path.join("imatges","zombie", "zombie_walk_right.png")), 2,3)
llista_im_esquerra = crea_matriu_imatges(pygame.image.load(os.path.join("imatges","zombie","zombie_walk_left.png")), 2,3)
llista_im_abaix = crea_matriu_imatges(pygame.image.load(os.path.join("imatges","zombie","zombie_walk_down.png")), 2,3)
llista_im_adalt = crea_matriu_imatges(pygame.image.load(os.path.join("imatges","zombie","zombie_walk_up.png")), 2,3)
ll_general_im = [llista_im_dreta,llista_im_esquerra,llista_im_adalt,llista_im_abaix]
#-----------------------------Player class-----------------------------------

class Zombie(pygame.sprite.Sprite):
    '''
    Aquesta clase crea l'animacio de caminar a partir d'una sprite_sheet.
    El nombre_imatges_spritesheet es el numero de fotogramas en el que
    s'ha de dividir la sprite_sheet i en aquest cas sempre es 6.
    
    Pos = la posicio del centre de la spite
    Direccio = llista amb vector normalitzat
    Limits = per on pot caminar el zombie
    Estats = ['wandering','persegueix','dead','atacant']
    '''

    def __init__(self, grup_sang, protagonista, grup_sp_mov, grup_obs, pos, lvl):
        super().__init__()
        self.protagonista = protagonista
        self.grup_sp_mov = grup_sp_mov
        self.grup_obs = grup_obs
        # Listes
        self.direccions = [[1,0],[-1,0],[0,-1],[0,1]]
        self.ll_faceing = ['RIGHT','LEFT','UP','DOWN']
        self.ll_estats = ['wandering','persegueix','dead','atacant','tocat']
        self.grup_sang = grup_sang
        self.velocitats = {'camina':2.25, 'corre':2.6, 'parat':0}
        # Stats del zombie
        if lvl == 1:
            self.vida = 10 
            self.velocitats['corre'] = 3.2
            self.agro = 300
            self.range = 50
            self.cadencia = 1500
        elif lvl == 2:
            self.vida = 15
            self.velocitats['corre'] = 3.7
            self.agro = 400
            self.range = 50
            self.cadencia = 1000
        self.fps = 1000      # Velocitat de l'animació
        self.estat = 'wandering'
        self.vel = self.velocitats['parat']    # Velocitat real del personatge
        # Direccio inicial
        i = random.randint(0,3)
        self.direccio_vec = self.direccions[i]
        self.faceing = self.ll_faceing[i]
        # Imatge
        self.llista_im = ll_general_im[i]   #llista de imatges del persnatge
        self.count = 0
        self.image = self.llista_im[0]
        # Atributs rect
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.minx = 0
        self.miny = 0
        self.maxx = 0
        self.maxy = 0
        self.radius = 35
        # Atributs de canvia la direccio
        self.temps_cambi_direc = pygame.time.get_ticks()
        self.dist = sqrt((self.rect.center[0]-self.protagonista.rect.center[0])**2 + (self.rect.center[1]-self.protagonista.rect.center[1])**2)
        # Variables de temps
        self.temps_ataca = pygame.time.get_ticks()
        self.t_tocat = pygame.time.get_ticks()
                
        

    def canvia_direccio(self, direccio):
        '''
        Direccio ha de ser un vector 
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
            
    def canvia_estat(self, estat):
        '''
        Fa els canvis necessaris quan es canvia d'estat
        '''
        self.estat = estat
        if estat == 'dead':
            self.vel = self.velocitats['parat']
            sang = Gore(self.rect.center)
            self.grup_sang.add(sang)
            self.kill()
        elif estat == 'tocat':
            # El so de mort i ferit tambe esta a la calsse bala
            # Aqui nomes es para el zombi el damage esta a la clase bala
            self.vel = self.velocitats['parat']
            self.t_tocat = pygame.time.get_ticks()
        elif estat == 'atacant':
            self.temps_ataca = pygame.time.get_ticks()
            self.vel = self.velocitats['parat']
            self.protagonista.vidas -= 1
        elif estat == 'persegueix':
            self.vel = self.velocitats['corre']
            self.direccio_vec = [(1/self.dist)*(self.protagonista.rect.center[0]-self.rect.center[0]),(1/self.dist)*(self.protagonista.rect.center[1]-self.rect.center[1])]                
        elif estat == 'wandering':
            self.vel = self.velocitats['camina']
            i = random.randint(0,3)
            self.direccio_vec = self.direccions[i]
            self.faceing = self.ll_faceing[i]
            self.llista_im = ll_general_im[i]
            self.count = 0
            self.image = self.llista_im[0]
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
        elif self.estat == 'atacant':
            delta_a = pygame.time.get_ticks() - self.temps_ataca
            if delta_a > self.cadencia:
                self.canvia_estat('wandering')
        elif self.estat == 'wandering':
            if self.dist<self.agro:
                self.canvia_estat('persegueix')
            else:
                delta = pygame.time.get_ticks() - self.temps_cambi_direc
                temps = random.randint(2000, 5000)
                if delta>temps:
                    self.canvia_direccio(random.choice(self.direccions))
                    self.vel = random.choice([self.velocitats['camina'],self.velocitats['parat']])
                    self.temps_cambi_direc = pygame.time.get_ticks()
        elif self.estat == 'persegueix':
            self.direccio_vec = [(1/self.dist)*(self.protagonista.rect.center[0]-self.rect.center[0]),(1/self.dist)*(self.protagonista.rect.center[1]-self.rect.center[1])]                
            if self.dist>=self.agro:
                self.canvia_estat('wandering')
            elif self.dist<self.range:
                self.canvia_estat('atacant')
        elif self.estat == 'tocat':
            delta = pygame.time.get_ticks() - self.t_tocat
            if delta >= 500:
                self.canvia_estat('wandering')
                
    def update_direccio(self):
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
                self.llista_im = llista_im_dreta
            elif faceing == 'LEFT':
                self.llista_im = llista_im_esquerra
            elif faceing == 'UP':
                self.llista_im = llista_im_adalt
            elif faceing == 'DOWN':
                self.llista_im = llista_im_abaix
            else:
                raise ValueError("No saps angles i escrius malament la direccio")
                        
    def update(self):
        self.dist = sqrt((self.rect.center[0]-self.protagonista.rect.center[0])**2 + (self.rect.center[1]-self.protagonista.rect.center[1])**2)
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
        if self.estat == 'atacant' or self.estat == 'tocat':
            self.image = self.llista_im[0]
        else:
            self.count = self.count + 1
            t = pygame.time.get_ticks()
            ta = t % self.fps
            idx = (ta * len(self.llista_im)) // self.fps
            self.image = self.llista_im[idx]
            if self.count == len(self.llista_im):
                self.count = 0
