import pygame

class Trans(pygame.sprite.Sprite):
    def __init__(self, sala_antiga, joc):
        super().__init__()
        ll_estat = ['movent jugador','amagant','mostrant']
        self.protagonista = joc.protagonista
        self.sala = joc.sala
        self.sala_antiga = sala_antiga
        self.estat = ll_estat[0]
        self.image = sala_antiga.imfons
        self.rect = self.image.get_rect()
        self.alpha = self.image.get_alpha
        self.fase = 0

    def update(self,screen):
        
        # Fase 1: direccionar jugador
        if self.fase == 0:
            dist_x = self.sala.porta.rect.centerx - self.protagonista.rect.centerx
            dist_y = self.sala.porta.rect.centery - self.protagonista.rect.centery
            self.protagonista.estat = 'caminant'
            if self.sala.porta.orientacio == 'U' or self.sala.porta.orientacio == 'D':
                if dist_x < 0:
                    self.protagonista.canvia_direccio('LEFT')
                else:
                    self.protagonista.canvia_direccio('RIGHT')
            else:
                if dist_y < 0:
                    self.protagonista.canvia_direccio('DOWN')
                else:
                    self.protagonista.canvia_direccio('UP')
            self.fase = 1
            
        # moure el jugador 
        elif self.fase == 1:
            if abs(self.protagonista.rect.centerx - self.sala.porta.rect.centerx) < 10\
               or abs(self.protagonista.rect.centery - self.sala.porta.rect.centery) < 10:
                pass
                
            
        # Actualitza la imatge de fons o aixo crec...
        screen.blit(self.image, (0, 0))





        
