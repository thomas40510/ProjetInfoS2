import pygame
import time
# Margins
MARGIN_LEFT = 230
MARGIN_TOP = 150
# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (110, 110, 110)
GREEN = (0, 255, 0)
LIGHT_GREEN = (0, 120, 0)
RED = (255, 0, 0)
LIGHT_RED = (120, 0, 0)

def init_game_ui():


    # WINDOW SIZE
    WIDTH = 800
    HEIGHT = 600


    # Initializing PyGame
    pygame.init()

    # Setting up the screen and background
    global screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(GRAY)

    # Setting up caption
    pygame.display.set_caption("Tarot Africain")

    # Loading image for the icon
    icon = pygame.image.load('22.jpeg')

    # Setting the game icon
    pygame.display.set_icon(icon)

    # Types of fonts to be used
    small_font = pygame.font.Font(None, 32)
    large_font = pygame.font.Font(None, 50)

def terrain(L,dejapresent):
    L0=L[0]
    n=len(L0)
    Im=[str(k) for k in range(0,22)]
    for k in range(0,22):
        Im[k] = pygame.image.load(Im[k] + '.jpeg')
        Im[k] = pygame.transform.scale(Im[k], (50, 80))
    while True:
        screen.fill(GRAY)
        for k in range(n):
            screen.blit(Im[L0[k]], (400-(50/2*n)+50*k, 450))
        for k in range(len(dejapresent)):
            screen.blit(Im[dejapresent[k]], (400 - (50 / 2 * len(dejapresent)) + 50 * k, 350))
        pygame.display.update()
        over=False
        mouse = pygame.mouse.get_pos()

        # Loop events occuring inside the game window
        for event in pygame.event.get():

            # Qutting event
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Left-mouse clicked event
            if not over and event.type == pygame.MOUSEBUTTONDOWN:

                for k in range(n):
                    if 400-(50/2*n)+50*k<mouse[0]<400-(50/2*n)+50*k+50 and 450<mouse[1]<530:
                        return(L0[k])


def pari(L):
    L0=L[0]
    for k in range(len(L0)):
        if type(L0[k])!=type(0):
            L0[k]=0
    n=len(L0)
    Im=[str(k) for k in range(0,22)]
    large_font = pygame.font.Font(None, 50)
    for k in range(0,22):
        Im[k] = pygame.image.load(Im[k] + '.jpeg')
        Im[k] = pygame.transform.scale(Im[k], (50, 80))
    while True:
        screen.fill(GRAY)
        for k in range(n):
            screen.blit(Im[L0[k]], (400-(50/2*n)+50*k, 450))

        button=[None for k in range(len(L[0])+1)]
        button_rect=[None for k in range(len(L[0])+1)]
        for k in range(len(button)):
            button[k]=large_font.render(str(k), True, WHITE)
            button_rect[k]=button[k].get_rect()
            button_rect[k].center=(400-(50/2*n)+50*k, 415)
            screen.blit(button[k],button_rect[k])

        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:

                for k in range(n+1):
                    if 400-(50/2*n)+50*k-25<mouse[0]<400-(50/2*n)+50*k+50-25 and 375<mouse[1]<450:
                        return(k)

        pygame.display.update()



if __name__ == "__main__":

    init_game_ui()
    terrain([[17,21,14]])