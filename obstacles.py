
import pygame


class Obs(pygame.sprite.Sprite):

    def __init__(self, topleft, width=10, height=10, tipus='balla'):
        super().__init__()
        self.tipus = tipus
        if tipus == 'balla':
            self.rect = pygame.Rect((0,0),(width, height))
            self.rect.topleft = topleft
        elif tipus == 'comandament':
            self.rect = pygame.Rect((0,0),(width, height))
            self.rect.topleft = topleft
