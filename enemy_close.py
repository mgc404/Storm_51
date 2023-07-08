
import pygame
import random
from math import sqrt
import os
from conf import mides_pantalla
from bala import Bala
from sang import Gore

ll_run = []
ll_atac = []
ll_tocat = []
#-----------------------------------image load----------------------------------------------------------------------
#--------------------- ll_run
for ang in range(0,360,90):
    l=[]
    for i in range(21):
        num = str(i)
        if i < 10:
            num = "0" + num
        l.append(pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("imatges","enemyClose","run","armature_run_"+num+".png")),(140,140)),ang))
    ll_run.append(l)
#--------------------- ll_atac
for ang in range(0,360,90):
    l=[]
    for i in range(61):
        num = str(i)
        if i < 10:
            num = "0" + num
        l.append(pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("imatges","enemyClose","thrust","armature_thrust_"+num+".png")),(145,145)),ang))
    ll_atac.append(l)
#---------------------- ll_tocat
for ang in range(0,360,90):
    l=[]
    for i in range(13):
        num = str(i)
        if i < 10:
            num = "0" + num
        l.append(pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("imatges","enemyClose","hit","armature_hit_"+num+".png")),(145,145)),ang))
    ll_tocat.append(l)

#------------------------------------ EnemyRanged class ------------------------------------------------------------

class EnemyClose(pygame.sprite.Sprite):

    def __init__(self, grup_sang, grup_sp_mov, grup_obs, protagonista, pos, lvl):
        super().__init__()
        self.protagonista = protagonista
        self.grup_sp_mov = grup_sp_mov
        self.grup_obs = grup_obs
        # Listes
        self.direccions = [[0,1], [1,0], [0,-1], [-1,0]]
        self.ll_faceing = ['DOWN', 'RIGHT','UP', 'LEFT']
        self.ll_estats = ['wandering','persegueix','dead','atacant','tocat']
        self.velocitats = {'camina':2.25, 'corre':3, 'parat':0}
        self.grup_sang = grup_sang
        # Stats del zombie
        if lvl == 1:
            self.vida = 10 
            self.velocitats['corre'] = 3
            self.agro = 300
            self.range = 70
        elif lvl == 2:
            self.vida = 15
            self.velocitats['corre'] = 3.5
            self.agro = 400
            self.range = 80
        self.fps = 1500      # Velocitat de l'animació
        self.estat = 'wandering'
        self.vel = self.velocitats['parat']    # Velocitat real del personatge
        # Direccio inicial
        i = random.randint(0,3)
        self.direccio_vec = self.direccions[i]
        self.faceing = self.ll_faceing[i]
        # Imatge
        self.ll_generica = ll_run
        self.llista_im = ll_run[i]   #llista de imatges del persnatge
        self.count = 0
        self.voltes = 0
        self.image = self.llista_im[0]
        self.index = 0
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
        self.t_ataca = pygame.time.get_ticks()
        self.t_tocat = pygame.time.get_ticks()
        # Atributs de so
        self.atac = pygame.mixer.Sound('so/enemy_kick.wav')

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
        num_col_sp = pygame.sprite.spritecollide(self, self.grup_sp_mov, False, pygame.sprite.collide_circle_ratio(0.7))
        if len(num_col_sp)> 1:
            self.rect.x = oldx
        num_col_obs = pygame.sprite.spritecollide(self, self.grup_obs, False, pygame.sprite.collide_rect_ratio(1))
        if len(num_col_obs)> 0:
            self.rect.x = oldx
        # Avanç en les y
        oldy = self.rect.y
        self.rect.y = self.rect.y + self.direccio_vec[1]*self.vel
        num_col_sp = pygame.sprite.spritecollide(self, self.grup_sp_mov, False, pygame.sprite.collide_circle_ratio(0.6))
        if len(num_col_sp)> 1:
            self.rect.y = oldy
        num_col_obs = pygame.sprite.spritecollide(self, self.grup_obs, False, pygame.sprite.collide_rect_ratio(1))
        if len(num_col_obs)> 0:
            self.rect.y = oldy

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
                self.llista_im = self.ll_generica[1]
            elif faceing == 'LEFT':
                self.llista_im = self.ll_generica[3]
            elif faceing == 'UP':
                self.llista_im = self.ll_generica[2]
            elif faceing == 'DOWN':
                self.llista_im = self.ll_generica[0]
            else:
                raise ValueError("No saps angles i escrius malament la direccio")

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
            self.fps = 400
            self.ll_generica = ll_tocat
            self.vel = self.velocitats['parat']
            self.llista_im = ll_tocat[self.ll_faceing.index(self.faceing)]
            self.index = 0
            self.voltes = 0
            self.image = self.llista_im[0]
        elif estat == 'atacant':
            self.fps = 1000
            self.protagonista.vidas -= 1
            self.ll_generica = ll_atac                                            
            self.temps_ataca = pygame.time.get_ticks()
            self.vel = self.velocitats['parat']
            self.llista_im = ll_atac[self.ll_faceing.index(self.faceing)]
            self.image = self.llista_im[0]
            self.index = 0
            self.voltes = 0
        elif estat == 'persegueix':
            self.fps = 1500
            self.ll_generica = ll_run
            self.vel = self.velocitats['corre']
            self.llista_im = self.ll_generica[self.ll_faceing.index(self.faceing)]
            self.image = self.llista_im[0]
            self.index = 0
            self.voltes = 0
        elif estat == 'wandering':
            self.fps = 1500
            self.ll_generica = ll_run
            self.vel = self.velocitats['camina']
            i = random.randint(0,3)
            self.direccio_vec = self.direccions[i]
            self.faceing = self.ll_faceing[i]
            self.llista_im = ll_run[i]
            self.index = 0
            self.voltes = 0
            self.image = self.llista_im[0]
        else:
            raise ValueError("Escriu be l'estat capullo!")
    
    def update_estat(self):
        '''
        Actualitza l'estat del zombie
        '''
        if self.vida <= 0:
            self.canvia_estat('dead')
        elif self.estat == 'atacant':
            if abs(29-self.index)<2:
                self.atac.play()
            if abs(len(self.llista_im)-self.index)<2:
                self.canvia_estat('persegueix')
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
            elif self.dist<=self.range:
                self.canvia_estat('atacant')
        elif self.estat == 'tocat':
            if abs(len(self.llista_im)-self.index)<2:
                self.canvia_estat('wandering')

    def update(self):
        self.update_estat()
        self.count = self.count + 1
        self.dist = sqrt((self.rect.center[0]-self.protagonista.rect.center[0])**2 + (self.rect.center[1]-self.protagonista.rect.center[1])**2)
        self.update_direccio()
        # fa caminar el sprite dintre dels limits
        self.avança()            
        # Posa limits a la sprite
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
        
        # actualitza el fotograma del sprite a la velocitat de self.fps
        # el self.count esta a dalt
        t = pygame.time.get_ticks()
        ta = t % self.fps
        idx = (ta * len(self.llista_im)) // self.fps
        self.image = self.llista_im[idx]
        self.index = self.llista_im.index(self.image)
        if self.count == len(self.llista_im):
            self.voltes += 1
            self.count = 0
        self.image.convert_alpha()

