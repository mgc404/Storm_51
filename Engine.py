'''
Fer el final del joc (you win)
'''
import os
from pgu import engine, gui
import pygame
from porta import Porta
from pygame.locals import *
from player import Player
from zombie import Zombie
import random
import conf
from sala import Sala, Transicio
from trans import Trans
from random import randint
import networkx as nx
from enemy_ranged import EnemyRanged
from enemy_close import EnemyClose
from life_up import Life_up
from barra import Health_bar
from boss import BOSS
global win
win = False

#---------------- carga d'imatges de fons----------
im_menu = pygame.image.load(os.path.join('imatges','imatges fons','ima_menu.png'))
sala_ini = pygame.image.load(os.path.join("imatges",'salas','Sala_ini.png'))
S1_1 = pygame.image.load(os.path.join("imatges",'salas','S1_1.png'))
S1_2 = pygame.image.load(os.path.join("imatges",'salas','S1_2.png'))
S1_3 = pygame.image.load(os.path.join("imatges",'salas','S1_3.png'))
S2_1 = pygame.image.load(os.path.join("imatges",'salas','S2_1.png'))
S2_2 = pygame.image.load(os.path.join("imatges",'salas','S2_2.png'))
S2_3 = pygame.image.load(os.path.join("imatges",'salas','S2_3.png'))
S2_4 = pygame.image.load(os.path.join("imatges",'salas','S2_4.png'))


#------------------------------------------Storm_51-------------------------------------------------------------------
class Storm_51(engine.Game):

    def __init__(self):
        super().__init__()
        pygame.font.init()
        self.screen = pygame.display.set_mode(conf.mides_pantalla, SWSURFACE)
        pygame.display.set_caption('Storm 51')
        self.screen.fill(conf.color_fons_menu)
        self.fons = 1
        self.crono = pygame.time.Clock()
        self._init_state_machine()
        pygame.mixer.init()

    def _init_state_machine(self):
        # All states must be initialized and stored as attributes
        self.menu_state = Menu(self)
        self.playing_state = Play(self)
        self.paused_state = Pause(self)
        self.game_over = Game_over(self)
        self.quit_state = engine.Quit(self)

    def run(self): 
        # Calls the main loop with the initial state
        # (self.menu, in this case)
        super().run(self.menu_state, self.screen)
    
    def change_state(self, transition=None):
        """
        Implements the state machine of the game.
        Given self.state and an optional parameter indicating 
        the kind of transition, computes and returns the new state
        """
        if self.state is self.menu_state:   # MENU
            if transition == 'PLAY':
                self.playing_state = Play(self)
                new_state = self.playing_state
            elif transition == 'EXIT':
                new_state = self.quit_state
            else:
                raise ValueError('Unknown transition indicator')
            
        elif self.state is self.playing_state:  # Play
            if transition == 'PAUSE':
                new_state = self.paused_state
            elif transition == 'GAME OVER':
                new_state = self.game_over
            elif transition == 'MENU':
                self.menu_state = Menu(self)
                new_state = self.menu_state
            else:
                raise ValueError('Unknown transition indicator')
            
        elif self.state is self.paused_state:   # Pausa
            if transition == 'PLAY':
                new_state = self.playing_state
            elif transition == 'MENU':
                self.menu_state = Menu(self)
                new_state = self.menu_state
            elif transition == 'EXIT':
                new_state = self.quit_state
            else:
                raise ValueError('Unknown transition indicator')
            
        elif self.state is self.game_over:  # GAME OVER
            if transition == 'MENU':
                self.menu_state = Menu(self)
                new_state = self.menu_state
            elif transition == 'EXIT':
                new_state = self.quit_state
            else:
                raise ValueError('Unknown transition indicator')
            
        else:
            raise ValueError('Unknown game state value')
        
        return new_state

    ##
    ##Tick is called once per frame. It shoud control de timing.
    ##::
    def tick(self):
        self.crono.tick(conf.fps)   # Limits the maximum FPS

#------------------------------------------Pausa----------------------------------------------------------------------
        
class Pause(engine.State):
    """
    Pauses the actual state, darkening the screen.
    Exits when SPACE is released.
    """
    def paint(self, s):
        s.fill((100, 100, 100), special_flags=BLEND_MULT)
        # set the font
        font = pygame.font.Font('freesansbold.ttf', 42)
        # Blocs amb text
        r = font.render('[R] --- > RESUME', True, (0, 255, 0))
        r_Rect = r.get_rect()
        r_Rect.center = (920 // 2 , (800 // 5))
        s.blit(r, r_Rect)
        esc = font.render('[ESC] --- > MENU', True, (0, 255, 0))
        esc_Rect = esc.get_rect()
        esc_Rect.center = (920 // 2 , (800 // 5)*2)
        s.blit(esc, esc_Rect)
        q = font.render('[Q] --- > EXIT', True, (0, 255, 0))
        q_Rect = q.get_rect()
        q_Rect.center = (920 // 2 , (800 // 5)*3)
        s.blit(q, q_Rect)
        # Actuelitza la pantalla
        pygame.display.flip()
        
    def event(self,e): 
        if e.type == KEYDOWN and e.key == K_r:
            return self.game.change_state('PLAY')
        elif e.type == KEYDOWN and e.key == K_ESCAPE:
            return self.game.change_state('MENU')
        elif e.type == KEYDOWN and e.key == K_q:
            return self.game.change_state('EXIT')

        
#--------------------------------------- Game over ------------------------------

class Game_over(engine.State):
    """
    Ends the actual game and show the score
    Exits when ESC is down.
    """
    def paint(self, s):
        # pinto el fons de la pantalla
        s.fill((100, 100, 100), special_flags=BLEND_MULT)
        if win:
            # blocs amb text
            font = pygame.font.Font('freesansbold.ttf', 42)
            
            title = font.render('G A M E  O V E R', True, (0, 255, 0))
            titleRect = title.get_rect()
            titleRect.center = (920 // 2, 800 // 4)
            s.blit(title, titleRect)
            
            yw = font.render('Y O U  W I N !', True, (0, 255, 0))
            ywRect = yw.get_rect()
            ywRect.center = (920 // 2, (800 // 4) + 70)
            s.blit(yw, ywRect)

        else:
            # blocs amb text
            font = pygame.font.Font('freesansbold.ttf', 42)
            title = font.render('G A M E  O V E R', True, (0, 255, 0))
            titleRect = title.get_rect()
            titleRect.center = (920 // 2, 800 // 4)
            s.blit(title, titleRect)
        # Blocs amb text
        esc = font.render('[ESC] --- > MENU', True, (0, 255, 0))
        esc_Rect = esc.get_rect()
        esc_Rect.center = (920 // 4 , (800 // 5)*3)
        s.blit(esc, esc_Rect)
        q = font.render('[Q] --- > EXIT', True, (0, 255, 0))
        q_Rect = q.get_rect()
        q_Rect.center = (3*920 // 4 , (800 // 5)*3)
        s.blit(q, q_Rect)
        # Actualitzo la pantalla
        pygame.display.flip()
        
    def event(self,e): 
        if e.type == KEYDOWN and e.key == K_ESCAPE:
            return self.game.change_state('MENU')
        elif e.type == KEYDOWN and e.key == K_q:
            return self.game.change_state('EXIT')
        

#------------------------------------------Play----------------------------------------------------------------------
        
class Play(engine.State):
    """
    L'estat del joc en realment es juga.
    Per moure el personatge s'utilitzen les tecles a, s, w, d.
    Per disparar s'utilitzen les fletxes de direcció.
    Si es prem la p es para el joc
    Si es prem la tecla ESC s'acava el joc
    """
    
    def init(self):
        # Inicia el mixer
        pygame.mixer.music.stop()
        pygame.mixer.music.load('so/s_p1.ogg')
        pygame.mixer.music.play()
        self.s_portes = pygame.mixer.Sound('so/Doors.wav')
        self.s_portes.set_volume(0.8)
        self.p = 0
        # Llista amb les sales
        self.grup_salas = []
        # Atributs de canvi de sala
        self.transicio = False
        self.t_trans = pygame.time.get_ticks()
        self.activat = False
        self.sp_trans = Transicio()
        self.c = 0
        # Inicialització grups sprites
        self.all_sprites =  pygame.sprite.Group()
        self.grup_obs = pygame.sprite.Group()
        self.grup_sp_mov = pygame.sprite.Group()
        self.all_portes = pygame.sprite.Group()
        self.all_enemics = pygame.sprite.Group()
        # Inicialització Protagonista
        self.protagonista = Player(self.all_sprites ,self.all_enemics ,self.grup_sp_mov ,(-50,-50), self.grup_obs)
        # Barra de salud
        self.barra = Health_bar(self.protagonista)
        # Inicialització de la sala
        self.grup_salas.append(Sala('inicial',sala_ini.convert_alpha(),0,2,0,self.grup_sp_mov,self.grup_obs,1)) # 0
        self.grup_salas.append(Sala(1,S1_1.convert_alpha(),2,2,3,self.grup_sp_mov,self.grup_obs,1)) # 1
        self.grup_salas.append(Sala(2,S1_2.convert_alpha(),2,2,1,self.grup_sp_mov,self.grup_obs,1)) # 2
        self.grup_salas.append(Sala(3,S1_3.convert_alpha(),2,0,2,self.grup_sp_mov,self.grup_obs,1)) # 3
        self.grup_salas.append(Sala(1,S2_1.convert_alpha(),1,2,2,self.grup_sp_mov,self.grup_obs,2)) # 4
        self.grup_salas.append(Sala(2,S2_2.convert_alpha(),2,2,0,self.grup_sp_mov,self.grup_obs,2)) # 5
        self.grup_salas.append(Sala(3,S2_3.convert_alpha(),0,0,0,self.grup_sp_mov,self.grup_obs,2)) # 6
        self.grup_salas.append(Sala(4,S2_4.convert_alpha(),0,0,0,self.grup_sp_mov,self.grup_obs,2)) # 7
        self.sala =self.grup_salas[0]
        # El graf de las salas
        self.G = nx.DiGraph()
        self.G.add_nodes_from(self.grup_salas)
        self.G.add_edge(self.grup_salas[0],self.grup_salas[1],direccio='U')
        self.G.add_edge(self.grup_salas[1],self.grup_salas[0],direccio='D')
        self.G.add_edge(self.grup_salas[1],self.grup_salas[2],direccio='L')
        self.G.add_edge(self.grup_salas[2],self.grup_salas[1],direccio='R')
        self.G.add_edge(self.grup_salas[1],self.grup_salas[3],direccio='U')
        self.G.add_edge(self.grup_salas[3],self.grup_salas[1],direccio='D')
        self.G.add_edge(self.grup_salas[1],self.grup_salas[4], direccio='DOWN')
        self.G.add_edge(self.grup_salas[4],self.grup_salas[5], direccio='L')
        self.G.add_edge(self.grup_salas[5],self.grup_salas[4], direccio='R')
        self.G.add_edge(self.grup_salas[4],self.grup_salas[6], direccio='U')
        self.G.add_edge(self.grup_salas[6],self.grup_salas[4], direccio='D')
        self.G.add_edge(self.grup_salas[6],self.grup_salas[7], direccio='U')
        self.G.add_edge(self.grup_salas[7],self.grup_salas[6], direccio='D')

        # S'omplen els grups de sprites
        self.all_sprites.add(self.protagonista)
        self.grup_sp_mov.add(self.protagonista)
        # Variables útils
        self.lvl = 1
        self.ll_dispara = [False]*4
        self.ll_mov = [False]*4
        # Colocar sprites
        self.sala.posa_obs()
        coloca_spritees(self.all_enemics, self.lvl, self.grup_obs, self.grup_sp_mov, self.protagonista, self.all_sprites, self.sala, orientacio_porta='U')
        
    def event(self,event):
        
        #---------------------KEYDOWN----------------------
        if event.type == pygame.KEYDOWN and not self.transicio:
            # Activar el ascensor
            if self.activat and event.key == pygame.K_LSHIFT:
                self.sala.grup_portes.add(self.sala.ascensor)
                ll_colisio = pygame.sprite.spritecollide(self.protagonista, self.grup_obs, False, pygame.sprite.collide_rect_ratio(1.25))
                if len(ll_colisio)>0 and ll_colisio[0] is self.sala.panel:
                    self.lvl = 2
                    self.transicio = True
                    self.t_trans = pygame.time.get_ticks()
            # Pause and exit
            if event.key == pygame.K_p:
                return self.game.change_state('PAUSE')
            elif event.key == pygame.K_ESCAPE:
                return self.game.change_state('MENU')
            
            # Moving events
            if event.key == pygame.K_SPACE:
                self.protagonista.corre(True)
            elif event.key == pygame.K_d:
                self.ll_mov[0] = True
                self.protagonista.estat = 'caminant'
                self.protagonista.canvia_direccio('RIGHT')
            elif event.key == pygame.K_a:
                self.ll_mov[1] = True
                self.protagonista.estat = 'caminant'
                self.protagonista.canvia_direccio('LEFT')
            elif event.key == pygame.K_w:
                self.ll_mov[2] = True
                self.protagonista.estat = 'caminant'
                self.protagonista.canvia_direccio('UP')
            elif event.key == pygame.K_s:
                self.ll_mov[3] = True
                self.protagonista.estat = 'caminant'
                self.protagonista.canvia_direccio('DOWN')
            # Shooting events
            if event.key == pygame.K_RIGHT:
                self.ll_dispara[0] = True
                self.protagonista.dispara('RIGHT')
            elif event.key == pygame.K_LEFT:
                self.ll_dispara[1] = True
                self.protagonista.dispara('LEFT')
            elif event.key == pygame.K_UP:
                self.ll_dispara[2] = True
                self.protagonista.dispara('UP')
            elif event.key == pygame.K_DOWN:
                self.ll_dispara[3] = True
                self.protagonista.dispara('DOWN')
            
        #---------------------KEYUP----------------------    
        if event.type == pygame.KEYUP and not self.transicio:
            # Run
            if event.key == pygame.K_SPACE:
                self.protagonista.corre(False)

            # Moving events
            if event.key == pygame.K_d or event.key == pygame.K_a or\
                 event.key == pygame.K_w or event.key == pygame.K_s:
                
                if event.key == pygame.K_d:
                    self.ll_mov[0] = False
                elif event.key == pygame.K_a:
                    self.ll_mov[1] = False
                elif event.key == pygame.K_w:
                    self.ll_mov[2] = False
                elif event.key == pygame.K_s:
                    self.ll_mov[3] = False
                    
                if self.ll_mov[0]:
                    self.protagonista.canvia_direccio('RIGHT')
                elif self.ll_mov[1]:
                    self.protagonista.canvia_direccio('LEFT')
                elif self.ll_mov[2]:
                    self.protagonista.canvia_direccio('UP')
                elif self.ll_mov[3]:
                    self.protagonista.canvia_direccio('DOWN')
                else:
                    self.protagonista.estat = 'parat'
                    
            # Shoot
            elif event.key == pygame.K_UP or event.key == pygame.K_LEFT or\
                 event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:
                
                if event.key == pygame.K_RIGHT:
                    self.ll_dispara[0] = False
                elif event.key == pygame.K_LEFT:
                    self.ll_dispara[1] = False
                elif event.key == pygame.K_UP:
                    self.ll_dispara[2] = False
                elif event.key == pygame.K_DOWN:
                    self.ll_dispara[3] = False
                    
                if self.ll_dispara[0]:
                    self.protagonista.dispara('RIGHT')
                elif self.ll_dispara[1]:
                    self.protagonista.dispara('LEFT')
                elif self.ll_dispara[2]:
                    self.protagonista.dispara('UP')
                elif self.ll_dispara[3]:
                    self.protagonista.dispara('DOWN')
                else:
                    self.protagonista.disparant = False
        return
    
    def paint(self, s):
        s.fill(conf.color_fons_play)
        pygame.display.flip()
        
    def loop(self):
        if self.transicio:
            # Actualitzar les imatges
            self.sala.ascensor.update()
        else:
            if self.sala.tipus == 4 and len(self.grup_sp_mov)-1==0:
                global win
                win = True
                return self.game.change_state('GAME OVER')
            self.sala.grup_sang.update()
            self.sala.grup_vida.update()
            self.all_sprites.update()
            if len(self.grup_sp_mov)-1==0:
                self.sala.empty = True
                self.sala.grup_portes.update()
                if self.p==0:
                    self.s_portes.play()
                    self.p=1
                p1 = 0
                p2 = 0
                for sala in self.G.nodes:
                    if sala.lvl == 1 and not(sala.empty):
                        p1 = 1
                    if sala.lvl == 2 and not(sala.empty):
                        p2 = 1
                if self.lvl == 1 and p1 == 0 and self.sala.tipus == 1:
                    self.activat = True
                if self.lvl == 2 and p2 == 0 and self.c != 1 and self.sala.tipus == 1:
                    self.c = 1
                    self.sala.grup_portes.add(self.sala.porta)
            self.barra.update()
            
    def canvia_sala(self,porta):
        self.p = 0
        for sp in self.sala.grup_sang:
            sp.kill()
        self.sala.treu_obs()
        self.sala = find_sala(self.sala,porta.orientacio,self.G)
        self.sala.posa_obs()
        # Colocar sprites
        coloca_spritees(self.all_enemics, self.lvl, self.grup_obs, self.grup_sp_mov, self.protagonista,self.all_sprites, self.sala, porta=porta)
        if self.transicio:
            pygame.mixer.music.stop()
            pygame.mixer.music.load('so/s_p2.ogg')
            pygame.mixer.music.play()
            
        self.transicio = False
        self.activat = False
            
            
        
    def update(self,s):
        s.fill(conf.color_fons_play)
        # Pinto el que toca si no estem en transicio
        if not self.transicio:
            # Primer es pinta la sala de sota
            self.sala.update(s)
            # Pinto la sang si hi ha
            self.sala.grup_sang.draw(s)
            # Pinto els botiquins
            self.sala.grup_vida.draw(s)
            #comprovo si hi han zombies
            if len(self.grup_sp_mov)-1==0:
                # Animacio de les portes
                self.sala.grup_portes.draw(s)
                # Mirar les colisions amb les portes
                ll_colisio = pygame.sprite.spritecollide(self.protagonista, self.sala.grup_portes, False, pygame.sprite.collide_rect_ratio(1.15))
                if len(ll_colisio)==1 and ll_colisio[0].orientacio == self.protagonista.direccio_str[0]:# el [0] es per pillar la primera lletra
                    self.canvia_sala(ll_colisio[0])
            self.barra.draw(s)
            # Animacio spritees
            self.all_sprites.draw(s)
            # Dibuixa quadrats per veure les hitbox
##            for obs in self.sala.ll_obs:
##                pygame.draw.rect(s, (255,0,0), obs)
##            pygame.draw.rect(s, (255,255,0), self.protagonista.rect)
##            for sp in self.all_sprites:
##                pygame.draw.rect(s, (255,0,0), sp)
            # GAME OVER si el prota no te vidas
            if self.protagonista.vidas == 0:
                return self.game.change_state('GAME OVER')
        else:
            delta = pygame.time.get_ticks() - self.t_trans
            if delta>=2000:
                if len(self.sp_trans.ll_image)==self.sp_trans.index:
                    self.canvia_sala(self.sala.ascensor)
                self.sp_trans.update(s)
            else:
                # Primer es pinta la sala de sota
                self.sala.update(s)
                self.all_sprites.draw(s)
                # Pintar el ascensor
                self.sala.grup_portes.draw(s)
        pygame.display.flip()

            
#------------------------------------------Menu----------------------------------------------------------------------

class Menu(engine.State):

    def __init__(self, *args):
        super().__init__(*args)
        self.imfons = im_menu.convert_alpha()
        # gui
        self.app = gui.App()
        

    #
    # Creem un menú amb un botó per a cada opció
    # en un taula vertical
    # i la lliguem al mètode que ha de retornar el valor
    #

    def init(self):
        pygame.mixer.music.load('so/s_menu.ogg')
        pygame.mixer.music.play()
        self.transicio = ''
        t = gui.Table()
        for text in ['PLAY', 'EXIT']:
            b = gui.Button(text)
            b.connect(gui.CLICK, self.canvia_etapa, text)
            t.td(b)
            t.tr()
        self.app.init(widget=t)
        
    def paint(self, screen):
        screen.fill(conf.color_fons_menu)
        screen.blit(self.imfons, (2, 10))
        self.update(screen)
        
    #
    # Redefinim el mètode event per cridar distribuir l'esdeveniment
    # tant a l'etapa com a la gui
    #
    def event(self, event):
        self.app.event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return self.game.change_state('EXIT')

    #
    # Redefinim el mètode loop per canviar d'etapa quan s'hagi premut
    # algun botó
    #
    def loop(self):
        if self.transicio != '':
            self.app.quit()
            return self.game.change_state(self.transicio)

    #
    # Redefinim el mètode update per cridar update tant de l'etapa com
    # de la gui
    #
    def update(self, screen):
        super().update(screen)
        self.app.update(screen)
        pygame.display.flip()

    def canvia_etapa(self, text):
        self.transicio = text

#----------------------------------------Funcions diversas---------------------------------------------------------

def find_sala(sala_actual,direccio,graph):
    for sala in graph[sala_actual]:
        if graph[sala_actual][sala]['direccio'] == direccio:
            return sala

def coloca_spritees(all_enemics, lvl, grup_obs, grup_sp_mov, prota ,grup_sp, sala, orientacio_porta=0, porta=0):
    
    # Porta per on surt el player
    if porta == 0:
        if orientacio_porta == 'U': # 'D'
            prota.rect.center = (sala.limits[0]+70, sala.limits[3]-70)
        else:
            raise ValueError('posicio del player no vlida')
        
    else:
        orientacio_porta = porta.orientacio
        if orientacio_porta == 'U': # 'D' En realitat es la que esta a DOWN
            prota.rect.center = (sala.d_portes['D'].rect.centerx ,sala.d_portes['D'].rect.centery-40)
        elif orientacio_porta == 'D': # 'U' En realitat es la que esta a UP
            prota.rect.center = (sala.d_portes['U'].rect.centerx, sala.d_portes['U'].rect.centery+40)
        elif orientacio_porta == 'L': # 'R' En realitat es la que esta a Right
            prota.rect.center = (sala.d_portes['R'].rect.centerx-40, sala.d_portes['R'].rect.centery)
        elif orientacio_porta == 'R': # 'L' En realitat es la que esta a Left
            prota.rect.center = (sala.d_portes['L'].rect.centerx+40, sala.d_portes['L'].rect.centery)
        elif orientacio_porta == 'DOWN':
            prota.rect.center = (75+70*2.5,75+70*3.5)

        else:
            raise ValueError('Orientacio desconeguda')
        
    if sala.tipus == 4:
        pos = (200, 200)
        boss = BOSS(prota, grup_sp_mov, grup_obs)
        boss.rect.center = pos
        grup_sp_mov.add(boss)
        grup_sp.add(boss)
        all_enemics.add(boss)
    
    elif not(sala.empty):
        grup_sp_mov.add(grup_obs)
        # Creo els zombies (Zombie)
        for i in range(sala.num_zombies):
            
            pos = (randint(sala.limits[0]+30,sala.limits[2]-30), randint(sala.limits[1]+30,sala.limits[3]-30))
            zomb = Zombie(sala.grup_sang, prota, grup_sp_mov, grup_obs, pos, lvl)
            num_colx = pygame.sprite.spritecollide(zomb, grup_sp_mov, False, pygame.sprite.collide_rect_ratio(1))
            c = 0
            while len(num_colx) > 0:
                c += 1
                if c>50:
                    print('No hi ha espai per mes sprites!')
                    zomb.kill()
                    break
                pos = (randint(sala.limits[0]+30,sala.limits[2]-30), randint(sala.limits[1]+30,sala.limits[3]-30))
                zomb.rect.center = pos
                num_colx = pygame.sprite.spritecollide(zomb, grup_sp_mov, False, pygame.sprite.collide_rect_ratio(1))
            grup_sp_mov.add(zomb)
            grup_sp.add(zomb)
            all_enemics.add(zomb)
            
        # creo els enemics a distancia (EnemyRanged)
        for i in range(sala.num_enemyrange):
            pos = (randint(sala.limits[0]+40,sala.limits[2]-40), randint(sala.limits[1]+40,sala.limits[3]-40))
            enemic = EnemyRanged(grup_sp,sala.grup_sang,  grup_sp_mov, grup_obs, prota, pos, lvl)
            num_colx = pygame.sprite.spritecollide(enemic, grup_sp_mov, False, pygame.sprite.collide_rect_ratio(1))
            c = 0
            while len(num_colx) > 0:
                c += 1
                if c>50:
                    print('No hi ha espai per mes sprites!')
                    enemic.kill()
                    break
                pos = (randint(sala.limits[0]+40,sala.limits[2]-40), randint(sala.limits[1]+40,sala.limits[3]-40))
                enemic.rect.center = pos
                num_colx = pygame.sprite.spritecollide(enemic, grup_sp_mov, False, pygame.sprite.collide_rect_ratio(1))
            grup_sp_mov.add(enemic)
            grup_sp.add(enemic)
            all_enemics.add(enemic)
            
        # creo els enemics cos a cos (EnemyClose)
        for i in range(sala.num_enemyclose):
            pos = (randint(sala.limits[0]+40,sala.limits[2]-40), randint(sala.limits[1]+40,sala.limits[3]-40))
            enemic = EnemyClose(sala.grup_sang,  grup_sp_mov, grup_obs, prota, pos, lvl)
            num_colx = pygame.sprite.spritecollide(enemic, grup_sp_mov, False, pygame.sprite.collide_rect_ratio(1))
            c = 0
            while len(num_colx) > 0:
                c += 1
                if c>50:
                    print('No hi ha espai per mes sprites!')
                    enemic.kill()
                    break
                pos = (randint(sala.limits[0]+40,sala.limits[2]-40), randint(sala.limits[1]+40,sala.limits[3]-40))
                enemic.rect.center = pos
                num_colx = pygame.sprite.spritecollide(enemic, grup_sp_mov, False, pygame.sprite.collide_rect_ratio(1))
            grup_sp_mov.add(enemic)
            grup_sp.add(enemic)
            all_enemics.add(enemic)

        # Creacio de botiquins (Life_up)
        if sala.tipus != 'inicial' and sala.tipus != 3:
            t = random.choice([True,True])
            if t:
                pos = (randint(sala.limits[0]+20,sala.limits[2]-20), randint(sala.limits[1]+20,sala.limits[3]-20))
                vida_up = Life_up(pos, prota)
                num_colx = pygame.sprite.spritecollide(vida_up, grup_obs, False, pygame.sprite.collide_rect_ratio(1))
                c = 0
                while len(num_colx) > 0:
                    c += 1
                    if c>50:
                        print('No hi ha espai per mes sprites!')
                        vida_up.kill()
                        break
                    pos = (randint(sala.limits[0],sala.limits[2]), randint(sala.limits[1],sala.limits[3]))
                    vida_up.rect.center = pos
                    num_colx = pygame.sprite.spritecollide(vida_up, grup_obs, False, pygame.sprite.collide_rect_ratio(0.75))
                sala.grup_vida.add(vida_up)
        grup_sp_mov.remove(grup_obs)
    update_limits(grup_sp_mov,sala)
    
def update_limits(sp,sala):
    for sprite in sp:
        sprite.minx = sala.limits[0]
        sprite.miny = sala.limits[1]
        sprite.maxx = sala.limits[2]
        sprite.maxy = sala.limits[3]


def main():
    game = Storm_51()
    game.run()

if __name__ == "__main__":
    main()
    pygame.quit()
