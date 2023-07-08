import pygame
from zombie import Zombie
from random import randint, choice
import pygame
import os
from conf import mides_pantalla, limits
import porta
from obstacles import Obs
from sprite_sheets import crea_llista_imatges


ll = crea_llista_imatges(pygame.image.load(os.path.join("imatges","salas","Elevator.png")), 22)


class Sala:
    def __init__(self, tipus, imatge, enemyclose, num_zombies, enemyrange, grup_sp_mov, grup_obs, lvl):
        '''
        inputs:
            num_monstres = numero de monstres a l'habitació
            imatge = imtge de fons
            portes = llista amb les portes
            all_sprites = grups de totes les sprites
            all_zombies = grups de tots els zombies
        metodes:
            update = pinta la imatge de fons 
        '''
        self.lvl = lvl
        self.ll_obs = []
        self.grup_sp_mov = grup_sp_mov
        self.grup_obs = grup_obs
        self.grup_vida = pygame.sprite.Group()
        self.grup_sang = pygame.sprite.Group()
        # Stats de les portes
        self.d_portes = {'U':0,'R':0, 'D':0, 'L':0}
        self.grup_portes = pygame.sprite.Group()
        # Bool per saber si ha passat per la sala
        if enemyclose + num_zombies + enemyrange == 0:
            self.empty = True
        else:
            self.empty = False
        # posicio de la sala a la imatge
        self.llarg = (mides_pantalla[0] - imatge.get_width())//2
        self.curt = 0
        
        # ---------------------------- Sala inicial --------------------------
        if tipus =='inicial':
            # Limits de la sala
            miny = 75
            minx = self.llarg
            maxx = self.llarg + imatge.get_width()
            maxy = imatge.get_height()
            self.limits = [minx,miny,maxx,maxy]
            # Portes
            topleft = (minx+70,0)
            port = porta.Porta('U', 'Enter', self.lvl, topleft=topleft)
            self.d_portes['U'] = port
            self.grup_portes.add(port)
            #---------Controls
            self.grup_blit = []
            #   moviment
            font = pygame.font.Font('freesansbold.ttf', 30)
            moviment = font.render('MOVE:', True, (0, 255, 0))
            moviment_Rect = moviment.get_rect()
            moviment_Rect.center = (150 , 300)
            self.grup_blit.append((moviment,moviment_Rect))
            for lletra in ['W','A','S','D','RUN ---> [SPACE]']:
                text = font.render('['+lletra+']', True, (0, 255, 0))
                text_Rect = text.get_rect()
                if lletra == 'W':
                    text_Rect.center = (150,350)
                elif lletra == 'A':
                    text_Rect.center = (100,390)
                elif lletra == 'S':
                    text_Rect.center = (150,390)
                elif lletra == 'D':
                    text_Rect.center = (200,390)
                elif lletra == 'RUN ---> [SPACE]':
                    text = font.render(lletra, True, (0, 255, 0))
                    text_Rect = text.get_rect()
                    text_Rect.center = (150,500)
                self.grup_blit.append((text,text_Rect))
            disparar = font.render('SHOOT:', True, (0, 255, 0))
            disparar_Rect = disparar.get_rect()
            disparar_Rect.center = (920-150 , 300)
            self.grup_blit.append((disparar,disparar_Rect))
            for lletra in ['^','<','v','>','PAUSE ---> [P]']:
                text = font.render('['+lletra+']', True, (0, 255, 0))
                text_Rect = text.get_rect()
                if lletra == '^':
                    text_Rect.center = (920-150,350)
                elif lletra == '>':
                    text_Rect.center = (920-100,390)
                elif lletra == 'v':
                    text_Rect.center = (920-150,390)
                elif lletra == '<':
                    text_Rect.center = (920-200,390)
                elif lletra == 'PAUSE ---> [P]':
                    text = font.render(lletra, True, (0, 255, 0))
                    text_Rect = text.get_rect()
                    text_Rect.center = (920-150,500)
                self.grup_blit.append((text,text_Rect))
            # Creacio d'obstacles
            #       balla horitzontal
            topleft = (minx, miny+70*1.5+12)
            longx = 70*3
            balla1 = Obs(topleft,width=longx)
            self.ll_obs.append(balla1)
            #       balla vertical
            leftup = (minx+70*3-5, miny+70*1.5+12)
            longy = 70*2.5
            balla2 = Obs(leftup, height=longy)
            self.ll_obs.append(balla2)
            
        # ---------------------------- Sala 1 --------------------------
        elif tipus == 1:
            # Limits de la sala
            self.limits = [75,85,845,712]
            #--------------Creacio d'obstacles
            # PANEL DE CONTROL
            topleft = (self.limits[0]+4*70+8, self.limits[1]+70*2-8)
            panel = Obs(topleft,width=50,height=50)
            self.panel = panel
            self.ll_obs.append(panel)
            # Portes
            if lvl == 1:
                # Porta de abaix
                topleft = (self.limits[0]+70*8,self.limits[3])
                port = porta.Porta('D', 'Exit', self.lvl, topleft=topleft)
                self.d_portes['D'] = port
                self.grup_portes.add(port)
                # Porta de adalt
                topleft = (self.limits[0]+70*6,0)
                port = porta.Porta('U', 'Door', self.lvl, topleft=topleft)
                self.d_portes['U'] = port
                self.grup_portes.add(port)
                # Porta de l'esquerra
                topleft = (-10,self.limits[1]+70*6)
                port = porta.Porta('L', 'Door', self.lvl, topleft=topleft)
                self.d_portes['L'] = port
                self.grup_portes.add(port)
                # Ascensor
                topleft = (self.limits[0]+70,self.limits[1]+70*2)
                ascensor = porta.Porta('DOWN', 'ascensor', 1, topleft=topleft)
                self.d_portes['DOWN'] = ascensor
                self.ascensor = ascensor
                
            elif lvl == 2:
                # Porta de adalt
                topleft = (self.limits[0]+70*6,0)
                port = porta.Porta('U', 'Enter', self.lvl, topleft=topleft)
                self.d_portes['U'] = port
                self.porta = port
##                self.grup_portes.add(port)
                # Porta de l'esquerra
                topleft = (0,self.limits[1]+70*6)
                port = porta.Porta('L', 'Door', self.lvl, topleft=topleft)
                self.d_portes['L'] = port
                self.grup_portes.add(port)
              
        # ---------------------------- Sala 2 --------------------------
        elif tipus == 2:   
            # Limits de la sala
            miny = 85
            minx = self.llarg + 85
            maxx = self.llarg + imatge.get_width()-60
            maxy = imatge.get_height() - 85
            self.limits = [minx,miny,maxx,maxy]
            # Porta de la dreta
            topleft = (self.limits[2]-15,self.limits[1]+70)
            port = porta.Porta('R', 'Door', self.lvl, topleft=topleft)
            self.d_portes['R'] = port
            self.grup_portes.add(port)
            # Creacio d'obstacles
            #       balla horitzontal
            topleft = (self.limits[0]+70*5, self.limits[1]+70*3)
            width = 70*4
            height = 70*2
            balla1 = Obs(topleft, width=width, height=height)
            self.ll_obs.append(balla1)
        # ---------------------------- Sala 3 --------------------------
        elif tipus == 3:
            if lvl == 1:
                self.curt = 85
                # Limits de la sala
                miny = self.curt
                minx = self.llarg + 85
                maxx = imatge.get_width()-60
                maxy = self.curt + imatge.get_height() - 85
                self.limits = [minx,miny,maxx,maxy]
                # Porta de abaix
                topleft = (self.limits[0]+70*4.5-10,self.limits[3]+2)
                port = porta.Porta('D', 'Door', self.lvl, topleft=topleft)
                self.d_portes['D'] = port
                self.grup_portes.add(port)
                # Creacio d'obstacles
                #       balla horitzontal
                topleft = (self.limits[0]-5, self.limits[1]+70*4+2)
                width = 70*3.5
                height = 70*5
                balla1 = Obs(topleft, width=width, height=height)
                self.ll_obs.append(balla1)
                #       balla horitzontal
                topleft = (self.limits[0]+70*7.5-10, self.limits[1]+70*4+2)
                width = 70*3.5
                height = 70*5
                balla1 = Obs(topleft, width=width, height=height)
                self.ll_obs.append(balla1)
            if lvl == 2:
                # Limits de la sala
                miny = 75
                minx = self.llarg
                maxx = self.llarg + imatge.get_width()+30
                maxy = imatge.get_height()-75
                self.limits = [minx,miny,maxx,maxy]
                # Portes U
                topleft = (minx+70,0)
                port = porta.Porta('U', 'Enter', self.lvl, topleft=topleft)
                self.d_portes['U'] = port
                self.grup_portes.add(port)
                # Portes D
                topleft = (minx+70,maxy)
                port = porta.Porta('D', 'Enter', self.lvl, topleft=topleft)
                self.d_portes['D'] = port
                self.grup_portes.add(port)
        # ---------------------------- Sala BOSS --------------------------
        elif tipus == 4:
            # Limits de la sala
            self.limits = [75,85,845,712]
            # Porta de abaix
            topleft = (self.limits[0]+70*8,self.limits[3])
            port = porta.Porta('D', 'Enter', self.lvl, topleft=topleft)
            self.d_portes['D'] = port
            self.grup_portes.add(port)
        
        # Stats de la sala
        self.tipus = tipus
        self.num_zombies = num_zombies
        self.num_enemyrange = enemyrange
        self.num_enemyclose = enemyclose
        self.imfons = imatge

    def treu_obs(self):
        for obs in self.ll_obs:
            self.grup_obs.remove(obs)
    def posa_obs(self):
        for obs in self.ll_obs:
            self.grup_obs.add(obs)

    def update(self,screen):
        screen.blit(self.imfons.convert_alpha(), (self.llarg, self.curt))
        if self.tipus == 'inicial':
            for b in self.grup_blit:
                screen.blit(b[0],b[1])


class Transicio:
    def __init__(self):
        self.u = 0
        self.ll_image = ll
        self.image = ll[0]
        self.index = 0
        self.pos = ( (mides_pantalla[0] - self.image.get_width())//2, (mides_pantalla[1] - self.image.get_height())//2)
        self.t = pygame.time.get_ticks()
        self.fps = 250

    def update(self,s):
        if self.u == 0:
            self.u=1
            pygame.mixer.music.load('so/song_elevator.ogg')
            pygame.mixer.music.play()
        delta = pygame.time.get_ticks() - self.t
        if delta >= self.fps:
            self.u += 2
            self.t = pygame.time.get_ticks()
            self.image = self.ll_image[self.index]
            self.index = self.index + 1
            if len(self.ll_image)==self.index:
                self.index = len(self.ll_image)
        s.blit(self.image.convert_alpha(), self.pos)
















        
