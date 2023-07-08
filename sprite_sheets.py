"""
Funcions per crear llistes o matrius d'imatges a partir d'un sprite
sheet.
"""

import pygame
    
def crea_llista_imatges(spritesheet, nims):
    """Retorna una llista de subsurfaces obtinguda a partir de l'sprite
    sheet de `nims` imatges.

    """
    if spritesheet.get_width()>spritesheet.get_height():
        mides = ( spritesheet.get_width() // nims,
                  spritesheet.get_height() )
        llista = []
        for columna in range(nims):
            tros = pygame.Rect( (mides[0] * columna, 0), mides )
            llista.append(spritesheet.subsurface(tros))
        return llista
    else:
        mides = ( spritesheet.get_width(),
                  spritesheet.get_height() // nims )
        llista = []
        for fila in range(nims):
            tros = pygame.Rect( (0, mides[1] * fila), mides )
            llista.append(spritesheet.subsurface(tros))
        return llista


def crea_matriu_imatges(spritesheet, nfils, ncols):
    """Retorna una matriu de subsurfaces obtinguda a partir de l'sprite
    sheet de `nfils`x`ncols` imatges.

    """
    llista = []
    if spritesheet.get_width()>spritesheet.get_height():
        mides = ( spritesheet.get_width() // ncols,
                  spritesheet.get_height() // nfils )
        matriu = [[] for i in range(nfils)]
        for fila in range(nfils):
            for columna in range(ncols):
                tros = pygame.Rect( (mides[0] * columna, mides[1] * fila), mides )
                matriu[fila].append(spritesheet.subsurface(tros))
        for fila in matriu:
            for column in fila:
                llista.append(column)
        return llista
    else:
        ncols, nfils = nfils, ncols
        mides = ( spritesheet.get_width() // ncols,
                  spritesheet.get_height() // nfils )
        matriu = [[] for i in range(nfils)]
        for fila in range(nfils):
            for columna in range(ncols):
                tros = pygame.Rect( (mides[0] * columna, mides[1] * fila), mides )
                matriu[fila].append(spritesheet.subsurface(tros))
        for fila in matriu:
            llista.append(fila[1])
        for fila in matriu:
            llista.append(fila[0])
        return llista
        







