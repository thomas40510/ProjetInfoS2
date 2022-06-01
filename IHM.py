import sys

import pygame
import time
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog


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


def prompt_welcome():
    """ Message de bienvenue. Propose de lire les règles du jeu.
    :return: False si l'utilisateur souhaite commencer la partie.
    """
    win = Tk()
    win.geometry('800x600')
    win.tk.eval(f'tk::PlaceWindow {win._w} center')
    win.wm_withdraw()
    win.update_idletasks()
    msg = messagebox.askquestion('Bienvenue !', 'Bienvenue dans le jeu Tarot Africain.\n '
                                                'Souhaitez-vous lire les règles ?',
                                 parent=win, type='yesno', icon='question')
    if msg == 'yes':
        # display rules
        return True
    else:
        return False


def prompt_name():
    """ Demande son nom au joueur humain
    :return: le nom du joueur
    """
    win = Tk()
    win.geometry('800x600')
    win.tk.eval(f'tk::PlaceWindow {win._w} center')
    win.wm_withdraw()
    win.update_idletasks()
    name = simpledialog.askstring("Bienvenue !", "Entrez votre nom:", parent=win)

    return name

def alert_pari():
    """Indique au joueur qu'il souhaite placer un pari illégal"""
    win = Tk()
    win.geometry('800x600')
    win.tk.eval(f'tk::PlaceWindow {win._w} center')
    win.wm_withdraw()
    win.update_idletasks()
    messagebox.showinfo("Pari illégal", "Vous ne pouvez pas placer ce pari", icon='warning')

def info_fin_manche(perte_vies):
    """ Écran de fin de manche
    :param perte_vies: vies perdues par le joueur humain
    :type perte_vies: int
    """
    win = Tk()
    win.geometry('800x600')
    win.tk.eval(f'tk::PlaceWindow {win._w} center')
    win.wm_withdraw()
    win.update_idletasks()
    messagebox.showinfo(f"Fin de la manche", f"La manche est terminée. Vous avez perdu {perte_vies} vie{'s' if perte_vies > 1 else ''}.")


def info_fin_partie(vainqueur, playerName):
    """ Message de fin de partie
    :param vainqueur: vainqueur de la partie
    :type vainqueur: str
    :param playerName: nom du joueur humain
    :type playerName: str
    :return: True si l'utilisateur souhaite rejouer, False sinon
    """
    win = Tk()
    win.geometry('800x600')
    win.tk.eval(f'tk::PlaceWindow {win._w} center')
    win.wm_withdraw()
    win.update_idletasks()
    if vainqueur == playerName:
        msg = f"Bravo {playerName}, vous avez gagné la partie !"
    elif vainqueur == 'égalité':
        msg = "Et c'est une égalité !"
    else:
        msg = f"Dommage {playerName}, vous avez perdu la partie."
    msg += "\nVoulez-vous rejouer ?"
    res = messagebox.askquestion('Fin de la partie', msg, parent=win, type='yesno', icon='question')

    return res == 'yes'


def init_game_ui():
    """
    Initialisation de la fenêtre de jeu
    """
    # WINDOW SIZE
    WIDTH = 800
    HEIGHT = 600

    # Initializing PyGame
    pygame.init()

    # Setting up the screen and background
    global screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(GRAY)
    fond = pygame.image.load('fond.jpg')
    fond = pygame.transform.scale(fond, (600, 800))
    screen.blit(fond, (0, 0))

    # Setting up caption
    pygame.display.set_caption("Tarot Africain")

    # Loading image for the icon
    icon = pygame.image.load('22.jpeg')

    # Setting the game icon
    pygame.display.set_icon(icon)

    # Types of fonts to be used
    small_font = pygame.font.Font(None, 32)
    large_font = pygame.font.Font(None, 50)


def terrain(LL, carterrain, pari, pointsterrain, vies):
    """
    Dessin du tapis de jeu
    :param LL: cartes des joueurs
    :param carterrain: cartes posées sur le tapis
    :param pari: pari du joueur
    :param pointsterrain: paris des joueurs
    :param vies: vies des joueurs
    :return:
    """
    L = LL[0]
    L0 = []
    for k in L:
        if type(k) != type(0):
            L0.append(22)
        else:
            L0.append(k)
    n = len(L0)
    Im = [str(k) for k in range(0, 23)]
    T = []
    for k in carterrain:
        if k != 0 and type(k) == type(0):
            T.append(k)
        elif type(k) != type(0):
            T.append(22)
    for k in range(0, 23):
        Im[k] = pygame.image.load(Im[k] + '.jpeg')
        Im[k] = pygame.transform.scale(Im[k], (50, 80))
    large_font = pygame.font.Font(None, 50)
    while True:
        fond = pygame.image.load('fond.jpg')
        fond = pygame.transform.scale(fond, (800, 600))
        screen.blit(fond, (0, 0))
        for k in range(n):
            screen.blit(Im[L0[k]], (400 - (50 / 2 * n) + 50 * k, 450))
        for k in range(len(T)):
            screen.blit(Im[T[k]], (400 - (50 / 2 * len(T)) + 50 * k, 300))
        botvivant=0

        paris0 = large_font.render("pari: " + str(pari[0]) + ", points: " + str(pointsterrain[0]), True, WHITE)
        paris0_rect = paris0.get_rect()
        paris0_rect.center = (400, 565)
        screen.blit(paris0, paris0_rect)
        vies0 = large_font.render("vies: " + str(vies[0]), True, WHITE)
        vies0_rect = vies0.get_rect()
        vies0_rect.center = (590, 500)
        screen.blit(vies0, vies0_rect)

        if vies[1]>0:
            botvivant+=1
            paris1 = large_font.render("pari: " + str(pari[botvivant]), True, WHITE)
            paris1_rect = paris1.get_rect()
            paris1_rect.center = (120, 375)
            screen.blit(paris1, paris1_rect)
            points1 = large_font.render("points: " + str(pointsterrain[botvivant]), True, WHITE)
            points1_rect = points1.get_rect()
            points1_rect.center = (120, 405)
            screen.blit(points1, points1_rect)
            vies1 = large_font.render("vies: " + str(vies[1]), True, WHITE)
            vies1_rect = vies1.get_rect()
            vies1_rect.center = (120, 170)
            screen.blit(vies1, vies1_rect)

        if vies[2]>0:
            botvivant+=1
            paris2 = large_font.render("pari: " + str(pari[botvivant]), True, WHITE)
            paris2_rect = paris2.get_rect()
            paris2_rect.center = (400, 195)
            screen.blit(paris2, paris2_rect)
            points2 = large_font.render("points: " + str(pointsterrain[botvivant]), True, WHITE)
            points2_rect = points2.get_rect()
            points2_rect.center = (400, 225)
            screen.blit(points2, points2_rect)
            vies2 = large_font.render("vies: " + str(vies[2]), True, WHITE)
            vies2_rect = vies2.get_rect()
            vies2_rect.center = (550, 50)
            screen.blit(vies2, vies2_rect)

        if vies[3]>0:
            botvivant+=1
            paris3 = large_font.render("pari: " + str(pari[botvivant]), True, WHITE)
            paris3_rect = paris3.get_rect()
            paris3_rect.center = (685, 375)
            screen.blit(paris3, paris3_rect)
            points3 = large_font.render("points: " + str(pointsterrain[botvivant]), True, WHITE)
            points3_rect = points3.get_rect()
            points3_rect.center = (685, 405)
            screen.blit(points3, points3_rect)
            vies3 = large_font.render("vies: " + str(vies[3]), True, WHITE)
            vies3_rect = vies3.get_rect()
            vies3_rect.center = (685, 170)
            screen.blit(vies3, vies3_rect)

        main = pygame.image.load('main' + str(n) + ".png")
        main = pygame.transform.scale(main, (150, 150))
        screen.blit(main, (50, 200))
        screen.blit(main, (600, 200))
        screen.blit(main, (325, 20))

        pygame.display.update()
        over = False
        mouse = pygame.mouse.get_pos()

        # Loop events occuring inside the game window
        for event in pygame.event.get():

            # Qutting event
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Left-mouse clicked event
            if not over and event.type == pygame.MOUSEBUTTONDOWN:
                # détection de la carte cliquée
                for k in range(n):
                    if 400 - (50 / 2 * n) + 50 * k < mouse[0] < 400 - (50 / 2 * n) + 50 * k + 50 \
                            and 450 < mouse[1] < 530:
                        return L0[k]


def pari(LL, pariprécédents, vies):
    """
    Gestion graphique de la prise de pari du joueur humain.
    Affiche les paris possibles et donne le résultat
    :param LL: joueurs
    :param pariprécédents: paris déjà posés
    :param vies: vies des joueurs
    :return: valeur du pari du joueur humain
    """
    L = LL[0]
    L0 = []
    for k in L:
        if type(k) != type(0):
            L0.append(22)
        else:
            L0.append(k)

    n = len(L0)
    Im = [str(k) for k in range(0, 23)]
    for k in range(0, 23):
        Im[k] = pygame.image.load(Im[k] + '.jpeg')
        Im[k] = pygame.transform.scale(Im[k], (50, 80))
    large_font = pygame.font.Font(None, 50)
    while True:
        fond = pygame.image.load('fond.jpg')
        fond = pygame.transform.scale(fond, (800, 600))
        screen.blit(fond, (0, 0))
        for k in range(n):
            screen.blit(Im[L0[k]], (400 - (50 / 2 * n) + 50 * k, 450))

        button = [None for k in range(len(L0) + 1)]
        button_rect = [None for k in range(len(L0) + 1)]
        for k in range(len(button)):
            button[k] = large_font.render(str(k), True, WHITE)
            button_rect[k] = button[k].get_rect()
            button_rect[k].center = (400 - (50 / 2 * n) + 50 * k, 415)
            screen.blit(button[k], button_rect[k])
        botvivant=0
        main = pygame.image.load('main' + str(n) + ".png")
        main = pygame.transform.scale(main, (150, 150))
        screen.blit(main, (50, 200))
        screen.blit(main, (600, 200))
        screen.blit(main, (325, 20))

        vies0 = large_font.render("vies: " + str(vies[0]), True, WHITE)
        vies0_rect = vies0.get_rect()
        vies0_rect.center = (590, 500)
        screen.blit(vies0, vies0_rect)

        if vies[1]>0:
            botvivant+=1
            paris1 = large_font.render("pari: " + str(pariprécédents[botvivant]), True, WHITE)
            paris1_rect = paris1.get_rect()
            paris1_rect.center = (120, 375)
            screen.blit(paris1, paris1_rect)
            vies1 = large_font.render("vies: " + str(vies[1]), True, WHITE)
            vies1_rect = vies1.get_rect()
            vies1_rect.center = (120, 170)
            screen.blit(vies1, vies1_rect)

        if vies[2]>0:
            botvivant+=1
            paris2 = large_font.render("pari: " + str(pariprécédents[botvivant]), True, WHITE)
            paris2_rect = paris2.get_rect()
            paris2_rect.center = (400, 195)
            screen.blit(paris2, paris2_rect)
            vies2 = large_font.render("vies: " + str(vies[2]), True, WHITE)
            vies2_rect = vies2.get_rect()
            vies2_rect.center = (550, 50)
            screen.blit(vies2, vies2_rect)

        if vies[3]>0:
            botvivant+=1
            paris3 = large_font.render("pari: " + str(pariprécédents[botvivant]), True, WHITE)
            paris3_rect = paris3.get_rect()
            paris3_rect.center = (685, 375)
            screen.blit(paris3, paris3_rect)
            vies3 = large_font.render("vies: " + str(vies[3]), True, WHITE)
            vies3_rect = vies3.get_rect()
            vies3_rect.center = (685, 170)
            screen.blit(vies3, vies3_rect)

        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:

                for k in range(n + 1):
                    if 400 - (50 / 2 * n) + 50 * k - 25 < mouse[0] < 400 - (50 / 2 * n) + 50 * k + 25 and 415 - 25 < \
                            mouse[1] < 415 + 25:
                        return k

        pygame.display.update()


def pari1carte(cartes, pariprécédents, vies):
    """
    Gestion graphique du pari à une carte.
    :param cartes: cartes visibles (celles des joueurs bots)
    :param pariprécédents: paris déjà posés
    :param vies: vies des joueurs
    :return: pari du joueur humain
    """
    for k in range(len(cartes)):
        if type(cartes[k][0]) != type(0):
            cartes[k] = [22]
    n = len(cartes)
    Im = [str(k) for k in range(0, 23)]
    for k in range(0, 23):
        Im[k] = pygame.image.load(Im[k] + '.jpeg')
        Im[k] = pygame.transform.scale(Im[k], (50, 80))
    large_font = pygame.font.Font(None, 50)
    while True:
        fond = pygame.image.load('fond.jpg')
        fond = pygame.transform.scale(fond, (800, 600))
        screen.blit(fond, (0, 0))

        L = [None, None]
        Lrect = [None, None]
        for k in range(2):
            L[k] = large_font.render(str(k), True, WHITE)
            Lrect[k] = L[k].get_rect()
            Lrect[k].center = (400 - (50) + 50 * k, 415)
            screen.blit(L[k], Lrect[k])

        screen.blit(Im[0], (375, 450))


        vies0 = large_font.render("vies: " + str(vies[0]), True, WHITE)
        vies0_rect = vies0.get_rect()
        vies0_rect.center = (590, 500)
        screen.blit(vies0, vies0_rect)

        if vies[1]>0:
            screen.blit(Im[cartes[1][0]], (50, 200))
            paris1 = large_font.render("pari: " + str(pariprécédents[1]), True, WHITE)
            paris1_rect = paris1.get_rect()
            paris1_rect.center = (120, 375)
            screen.blit(paris1, paris1_rect)
            vies1 = large_font.render("vies: " + str(vies[1]), True, WHITE)
            vies1_rect = vies1.get_rect()
            vies1_rect.center = (120, 170)
            screen.blit(vies1, vies1_rect)

        if vies[2]>0:
            screen.blit(Im[cartes[2][0]], (600, 200))
            paris2 = large_font.render("pari: " + str(pariprécédents[2]), True, WHITE)
            paris2_rect = paris2.get_rect()
            paris2_rect.center = (400, 195)
            screen.blit(paris2, paris2_rect)
            vies2 = large_font.render("vies: " + str(vies[2]), True, WHITE)
            vies2_rect = vies2.get_rect()
            vies2_rect.center = (550, 50)
            screen.blit(vies2, vies2_rect)

        if vies[3]>0:
            screen.blit(Im[cartes[3][0]], (325, 20))
            paris3 = large_font.render("pari: " + str(pariprécédents[3]), True, WHITE)
            paris3_rect = paris3.get_rect()
            paris3_rect.center = (685, 375)
            screen.blit(paris3, paris3_rect)
            vies3 = large_font.render("vies: " + str(vies[3]), True, WHITE)
            vies3_rect = vies3.get_rect()
            vies3_rect.center = (685, 170)
            screen.blit(vies3, vies3_rect)

        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for k in range(n + 1):
                    if 400 - (50 / 2 * n) + 50 * k - 25 < mouse[0] < 400 - (50 / 2 * n) + 50 * k + 25 and 415 - 25 < \
                            mouse[1] < 415 + 25:
                        return k

        pygame.display.update()


def minmax():
    """
    Gestion graphique du jeu de l'excuse (valeur mini ou maxi).
    :return: Valeur choisie par le joueur humain ("mini" ou "maxi")
    """
    large_font = pygame.font.Font(None, 50)

    while True:
        bmin = large_font.render("Min", True, WHITE)
        bmin_rect = bmin.get_rect()
        bmin_rect.center = (350, 400)
        screen.blit(bmin, bmin_rect)

        bmax = large_font.render("Max", True, WHITE)
        bmax_rect = bmax.get_rect()
        bmax_rect.center = (450, 400)
        screen.blit(bmax, bmax_rect)
        pygame.display.update()

        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 325 < mouse[0] < 375 and 400 - 25 < mouse[1] < 400 + 25:
                    return 'mini'
                elif 425 < mouse[0] < 475 and 400 - 25 < mouse[1] < 400 + 25:
                    return 'maxi'


if __name__ == "__main__":
    pass