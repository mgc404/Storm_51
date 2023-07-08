


'''
Fer que el personatge pugui tenir mes d'un estat es a dir corre i disparar
o star parat i disparat...

fer una funcio que et canv la imatge segosn que esta fent el prota
'''


from bala import Bala
from sprite_sheets import crea_llista_imatges
import pygame
import os
from conf import mides_pantalla

#------------------------load player image-----------------------------------
llista_im_dreta = crea_llista_imatges(pygame.image.load(os.path.join("imatges","player","player_walk_right.png")), 6)
llista_im_esquerra = crea_llista_imatges(pygame.image.load(os.path.join("imatges","player","player_walk_left.png")), 6)
llista_im_abaix = crea_llista_imatges(pygame.image.load(os.path.join("imatges","player","player_walk_down.png")), 6)
llista_im_adalt = crea_llista_imatges(pygame.image.load(os.path.join("imatges","player","player_walk_up.png")), 6)

llista_im_run_dreta = crea_llista_imatges(pygame.image.load(os.path.join("imatges","player","player_run_right.png")), 6)
llista_im_run_esquerra = crea_llista_imatges(pygame.image.load(os.path.join("imatges","player","player_run_left.png")), 6)
llista_im_run_abaix = crea_llista_imatges(pygame.image.load(os.path.join("imatges","player","player_run_down.png")), 6)
llista_im_run_adalt = crea_llista_imatges(pygame.image.load(os.path.join("imatges","player","player_run_up.png")), 6)

im_escopeta_up = pygame.image.load(os.path.join("imatges","player","player_pumpgun_up.png"))
im_escopeta_down = pygame.image.load(os.path.join("imatges","player","player_pumpgun_down.png"))
im_escopeta_left = pygame.image.load(os.path.join("imatges","player","player_pumpgun_left.png"))
im_escopeta_right = pygame.image.load(os.path.join("imatges","player","player_pumpgun_right.png"))

#-----------------------------Player class-----------------------------------

class Player(pygame.sprite.Sprite):
    '''
        Aquesta clase crea l'animacio de caminar a partir d'una sprite_sheet.
        El nombre_imatges_spritesheet es el numero de fotogramas en el que
        s'ha de dividir la sprite_sheet i en aquest cas sempre es 6
    '''

    def __init__(self, grup_sprites, all_enemics, grup_sp_mov, pos, grup_obs):
        super().__init__()
        # Llistes
        self.ll_estats = ['caminant','parat']
        self.all_sp = grup_sprites
        self.grup_sp_mov = grup_sp_mov
        self.grup_obs = grup_obs
        self.all_enemics = all_enemics
        # Stats del jugador
        self.vidas = 20  # Pot canviar si es troba curas per las salas
        self.vidas_ini = 20
        self.dps = 5    # Pot canviar segons l'arma que porta
        self.arma = ''  # Un str amb el nom de l'arma. Si no te o simplement camina es el str buit
        self.estat = 'parat'
        self.corrent = False
        self.fps = 500     # Velocitat de l'animació. Com més petit més ràpid
        self.disparant = False
        self.faceing = 'RIGHT'
        self.vel = 3    # Velocitat real del personatge
        self.cadencia = 500 # Els milisegons entre bala i bala
        # Direccio inicial
        self.llista_im = llista_im_dreta    
        self.direccio_str = 'RIGHT'
        self.direccio = [1, 0]
        # Imatge
        self.count = 0
        self.image = self.llista_im[0]
        # Atributs rect
        self.rect = pygame.Rect((0,0),(70,60))
        self.rect.center = pos
        self.minx = 0
        self.miny = 0
        self.maxx = 0
        self.maxy = 0
        self.radius = 30
        # Atributs de temps
        self.temps_dispara = 0
        # Atributs de so
        self.laser = pygame.mixer.Sound('so/laser_player.wav')
        self.laser.set_volume(0.3)

    def avança(self):
        # Avanç en les x
        oldx = self.rect.x
        self.rect.x = self.rect.x + self.direccio[0]*self.vel
        num_col_sp = pygame.sprite.spritecollide(self, self.grup_sp_mov, False, pygame.sprite.collide_rect_ratio(0.6))
        if len(num_col_sp)> 1:
            self.rect.x = oldx
        num_col_obs = pygame.sprite.spritecollide(self, self.grup_obs, False, pygame.sprite.collide_rect_ratio(1))
        if len(num_col_obs)> 0:
            self.rect.x = oldx
        # Avanç en les y
        oldy = self.rect.y
        self.rect.y = self.rect.y + self.direccio[1]*self.vel
        num_col_sp = pygame.sprite.spritecollide(self, self.grup_sp_mov, False, pygame.sprite.collide_rect_ratio(0.6))
        if len(num_col_sp)> 1:
            self.rect.y = oldy
        num_col_obs = pygame.sprite.spritecollide(self, self.grup_obs, False, pygame.sprite.collide_rect_ratio(1))
        if len(num_col_obs)> 0:
            self.rect.y = oldy

    def corre(self, bol):
        if bol and not (self.disparant):
            self.vel = 5
            self.corrent = True
            self.disparant = False
        else:
            self.vel = 3
            self.corrent = False
        self.canvia_direccio(self.direccio_str)
        
    def dispara(self, direccio):
        self.corre(False)
        self.faceing = direccio
        self.disparant = True
        delta = pygame.time.get_ticks() - self.temps_dispara
        if delta > self.cadencia:
            self.laser.play()
            if direccio == 'RIGHT':
                x = self.rect.bottomright[0] + 28
                y = self.rect.bottomright[1] - 37
                posicio = (x, y)
            elif direccio == 'UP':
                x = self.rect.topright[0] - 15
                y = self.rect.topright[1] - 5
                posicio = (x, y)
            elif direccio == 'LEFT':
                x = self.rect.topleft[0]
                y = self.rect.topleft[1] + 18
                posicio = (x, y)
            elif direccio == 'DOWN':
                x = self.rect.bottomleft[0] + 20
                y = self.rect.bottomleft[1] + 5
                posicio = (x, y)
            self.temps_dispara = pygame.time.get_ticks()
            bala = Bala( posicio, self.faceing, self.dps, 'blue',grup_zombies=self.all_enemics)
            self.all_sp.add(bala)
            
    def canvia_direccio(self, direccio):
        '''
        Direccio ha de ser un str amb majusculas
        entre: UP, DOWN, LEFT, RIGHT
        '''
        if direccio == 'RIGHT':
            self.direccio = [1,0]
            self.direccio_str = 'RIGHT'
            if self.corrent:
                self.llista_im = llista_im_run_dreta
            else:
                self.llista_im = llista_im_dreta
        elif direccio == 'LEFT':
            self.direccio = [-1,0]
            self.direccio_str = 'LEFT'
            if self.corrent:
                self.llista_im = llista_im_run_esquerra
            else:
                self.llista_im = llista_im_esquerra
        elif direccio == 'UP':
            self.direccio = [0,-1]
            self.direccio_str = 'UP'
            if self.corrent:
                self.llista_im = llista_im_run_adalt
            else:
                self.llista_im = llista_im_adalt
        elif direccio == 'DOWN':
            self.direccio = [0,1]
            self.direccio_str = 'DOWN'
            if self.corrent:
                self.llista_im = llista_im_run_abaix
            else:
                self.llista_im = llista_im_abaix
            

    def update(self):
        
        # fa caminar el personatge dintre dels limits
        if self.estat == 'parat':
            self.image = self.llista_im[0]
        elif self.estat == 'caminant':

            if self.direccio_str == 'RIGHT' and self.rect.right >= self.maxx-15:
                self.image = self.llista_im[0] 
            elif self.direccio_str == 'LEFT' and self.rect.left <= self.minx:
                self.image = self.llista_im[0]
            elif self.direccio_str == 'UP' and self.rect.top < self.miny:
                self.image = self.llista_im[0]
            elif self.direccio_str == 'DOWN' and self.rect.bottom > self.maxy:
                self.image = self.llista_im[0]
            else:
                self.avança()
                
        # actualitza el fotograma del personatge a la velocitat de self.fps
        if self.disparant:
            if self.faceing == 'UP':
                self.image =  im_escopeta_up
            elif self.faceing == 'DOWN':
                self.image =  im_escopeta_down
            elif self.faceing == 'LEFT':
                self.image =  im_escopeta_left
            elif self.faceing == 'RIGHT':
                self.image =  im_escopeta_right
            self.dispara(self.faceing)
        elif self.estat == 'caminant':
            self.count = self.count + 1
            t = pygame.time.get_ticks()
            ta = t % self.fps
            idx = (ta * len(self.llista_im)) // self.fps
            self.image = self.llista_im[idx]
            if self.count == len(self.llista_im):
                self.count = 0
        
