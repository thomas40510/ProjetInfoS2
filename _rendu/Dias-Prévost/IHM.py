# ----------------------------------------------------------------------------
# Created By  : DIAS, PREVOST
# Created Date: 2022-04-02
# version ='1.0'
# ---------------------------------------------------------------------------
# Description : Module implémentant l'IHM du tarot africain
# Main author : Prévost Thomas

import pygame
import time
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog

WHITE = (255, 255, 255)
mains = [5, 5, 5]
POSITIONS_MAINS = [(50, 200), (325, 20), (600, 200)]

main_joueur_humain = []  # Cartes du joueur humain

f = open('règles.txt', 'r', encoding='utf-8')
règles = f.read()
f.close()


def save_main_joueur(cartes):
    """
    Sauvegarde les cartes du joueur humain dans une variable globale.
    Cette variable servira à l'affichage des tours des bots.
    """
    global main_joueur_humain
    main_joueur_humain = cartes


def prompt_welcome():
    """ Message de bienvenue. Propose de lire les règles du jeu.

    :return: False si l'utilisateur souhaite commencer la partie.
    """
    win = Tk()
    win2 = Tk()
    win2.geometry('0x0')
    win.geometry('0x0')
    win.tk.eval(f'tk::PlaceWindow {win._w} center')
    win.wm_withdraw()
    win.update_idletasks()
    msg = messagebox.askquestion('Bienvenue !', 'Bienvenue dans le jeu Tarot Africain.\n '
                                                'Souhaitez-vous lire les règles ?',
                                 parent=win, type='yesno', icon='question')
    if msg == 'yes':
        # display rules
        win2.geometry('0x0')
        win2.tk.eval(f'tk::PlaceWindow {win._w} center')
        win2.wm_withdraw()
        win2.update_idletasks()
        messagebox.showinfo('Règles', règles)
        win.destroy()
        return False
    else:
        win.destroy()
        win2.destroy()
        return True


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

    win.destroy()
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
    messagebox.showinfo(f"Fin de la manche",
                        f"La manche est terminée. Vous avez perdu {perte_vies} vie{'s' if perte_vies > 1 else ''}.")


def info_fin_partie(vainqueur, playerName):
    """ Message de fin de partie.
    Permet d'obtenir le souhait de l'utilisateur de rejouer ou non.

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
    "Author : Prévost Thomas"
    WIDTH = 800
    HEIGHT = 600
    pygame.init()
    global screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    fond = pygame.image.load('cartes/fond.png')
    fond = pygame.transform.scale(fond, (600, 800))
    screen.blit(fond, (0, 0))
    pygame.display.set_caption("Tarot Africain")
    icon = pygame.image.load('cartes/22.jpeg')
    pygame.display.set_icon(icon)


def affiche_tour_joueur(LL, carterrain, pari, pointsterrain, vies):
    """
    Affiche le jeu et récupère la carte choisie par l'utilisateur.

    :param LL: cartes du joueur
    :param carterrain: cartes posées sur le tapis
    :param pari: pari du joueur
    :param pointsterrain: paris des joueurs
    :param vies: vies des joueurs
    :return:
    """
    "Author : Prévost Thomas"
    L = LL[0]
    L0 = []
    for k in L:
        if type(k) != int:
            L0.append(22)
        else:
            L0.append(k)
    n = len(L0)
    Im = [str(k) for k in range(0, 23)]
    T = []
    for k in carterrain:
        if k != 0 and type(k) == int:
            T.append(k)
        elif type(k) != int:  # on associe une valeur numérique à l'excuse
            T.append(22)
    for k in range(0, 23):  # on associe les cartes à leurs images
        Im[k] = pygame.image.load('cartes/' + Im[k] + '.jpeg')
        Im[k] = pygame.transform.scale(Im[k], (50, 80))
    large_font = pygame.font.Font(None, 50)
    while True:
        # affichage du fond
        fond = pygame.image.load('cartes/fond.png')
        fond = pygame.transform.scale(fond, (800, 600))
        screen.blit(fond, (0, 0))

        for k in range(n):  # affichage des cartes du joueur
            screen.blit(Im[L0[k]], (400 - (50 / 2 * n) + 50 * k, 450))

        for k in range(len(T)):  # affichage des cartes sur le terrain
            screen.blit(Im[T[k]], (400 - (50 / 2 * len(T)) + 50 * k, 300))
        botvivant = 0

        # paris, points et vies du joueur humain
        paris0 = large_font.render("pari: " + str(pari[0]) + ", points: " + str(pointsterrain[0]), True, WHITE)
        paris0_rect = paris0.get_rect()
        paris0_rect.center = (400, 565)
        screen.blit(paris0, paris0_rect)
        vies0 = large_font.render("vies: " + str(vies[0]), True, WHITE)
        vies0_rect = vies0.get_rect()
        vies0_rect.center = (590, 500)
        screen.blit(vies0, vies0_rect)

        # paris, points et vies du joueur bot 1 si vivant
        if vies[1] > 0:
            botvivant += 1
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

        # idem pour le bot 2
        if vies[2] > 0:
            botvivant += 1
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

        # idem pour le bot 3
        if vies[3] > 0:
            botvivant += 1
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

        if mains == [0, 0, 0]:  # actualisation du nombre de carte dans chaque main pour l'affichage
            for pos in range(len(mains)):
                mains[pos] = len(L0)

        for i in range(len(mains)):  # affichage du nombre de carte de chaque joueur
            if mains[i] > 1:
                main = pygame.transform.scale(pygame.image.load(f"cartes/main{mains[i]}.png"), (150, 150))
                screen.blit(main, POSITIONS_MAINS[i])
            elif mains[i] == 1:
                main = pygame.transform.scale(pygame.image.load(f"cartes/main{mains[i]}.png"), (85, 150))
                screen.blit(main, POSITIONS_MAINS[i])

        pygame.display.update()
        mouse = pygame.mouse.get_pos()

        # écoute les événements se produisant sur l'interface
        for event in pygame.event.get():

            # Quitter le jeu
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # clic de la souris
            if event.type == pygame.MOUSEBUTTONDOWN:
                for k in range(n):  # détection de la carte cliquée
                    if 400 - (50 / 2 * n) + 50 * k < mouse[0] < 400 - (50 / 2 * n) + 50 * k + 50 \
                            and 450 < mouse[1] < 530:
                        return L0[k]


def affiche_tour_bot(carte_bot, carterrain, pari, pointsterrain, vies, position):
    """
    Affichage simple du tour d'un joueur bot.

    :param carte_bot: carte jouée par le bot
    :param carterrain: cartes posée sur le terrain
    :param pari: paris des joueurs
    :param pointsterrain: points remportés sur le tour
    :param vies: vies des joueurs
    :param position: numéro du bot
    """
    "Author : Prévost Thomas"

    L = main_joueur_humain
    L0 = []
    for k in L:  # cartes du joueur
        if type(k) != int:
            L0.append(22)
        else:
            L0.append(k)
    n = len(L0)
    Im = [str(k) for k in range(0, 23)]
    T = []
    for k in carterrain:  # cartes du terrain
        if k != 0 and type(k) == int:
            T.append(k)
        elif type(k) != int:  # on associe une valeur numérique à l'excuse
            T.append(22)
    if type(carte_bot) == int:
        T.append(carte_bot)
    else:
        T.append(22)
    for k in range(0, 23):  # on associe les cartes à leurs images
        Im[k] = pygame.image.load('cartes/' + Im[k] + '.jpeg')
        Im[k] = pygame.transform.scale(Im[k], (50, 80))
    large_font = pygame.font.Font(None, 50)

    fond = pygame.image.load('cartes/fond.png')
    fond = pygame.transform.scale(fond, (800, 600))
    screen.blit(fond, (0, 0))
    for k in range(n):  # affichage des cartes du joueur
        screen.blit(Im[L0[k]], (400 - (50 / 2 * n) + 50 * k, 450))
    for k in range(len(T)):  # affichage des cartes du terrain
        screen.blit(Im[T[k]], (400 - (50 / 2 * len(T)) + 50 * k, 300))
        time.sleep(.5)
    botvivant = 0

    # affichage des paris, points, vies : idem que pour le joueur humain

    paris0 = large_font.render("pari: " + str(pari[0]) + ", points: " + str(pointsterrain[0]), True, WHITE)
    paris0_rect = paris0.get_rect()
    paris0_rect.center = (400, 565)
    screen.blit(paris0, paris0_rect)
    vies0 = large_font.render("vies: " + str(vies[0]), True, WHITE)
    vies0_rect = vies0.get_rect()
    vies0_rect.center = (590, 500)
    screen.blit(vies0, vies0_rect)

    if vies[1] > 0:
        botvivant += 1
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

    if vies[2] > 0:
        botvivant += 1
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

    if vies[3] > 0:
        botvivant += 1
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

    if mains == [0, 0, 0]:
        for pos in range(len(mains)):
            mains[pos] = len(L0)

    mains[position - 1] -= 1

    for i in range(len(mains)):  # affichage des mains des bots avec le bon nombre de cartes
        if mains[i] > 1:
            main = pygame.transform.scale(pygame.image.load(f"cartes/main{mains[i]}.png"), (150, 150))
            screen.blit(main, POSITIONS_MAINS[i])
        elif mains[i] == 1:
            main = pygame.transform.scale(pygame.image.load(f"cartes/main{mains[i]}.png"), (85, 150))
            screen.blit(main, POSITIONS_MAINS[i])

    pygame.display.update()


def affiche_pari_joueur(LL, pariprécédents, vies):
    """
    Gestion graphique de la prise de pari du joueur humain.
    Affiche les paris possibles et renvoie le choix de l'utilisateur

    :param LL: joueurs
    :param pariprécédents: paris déjà posés
    :param vies: vies des joueurs
    :return: valeur du pari du joueur humain
    """
    "Author : Prévost Thomas"

    # partie d'affichage du plateau
    # même fonctionnement que dans les autres fonctions
    L = LL[0]
    L0 = []
    for k in L:
        if type(k) != int:
            L0.append(22)
        else:
            L0.append(k)

    n = len(L0)
    Im = [str(k) for k in range(0, 23)]
    # chargement des cartes
    for k in range(0, 23):
        Im[k] = pygame.image.load('cartes/' + Im[k] + '.jpeg')
        Im[k] = pygame.transform.scale(Im[k], (50, 80))
    large_font = pygame.font.Font(None, 50)
    while True:
        fond = pygame.image.load('cartes/fond.png')
        fond = pygame.transform.scale(fond, (800, 600))
        screen.blit(fond, (0, 0))
        for k in range(n):
            screen.blit(Im[L0[k]], (400 - (50 / 2 * n) + 50 * k, 450))

        button = [None for k in range(len(L0) + 1)]
        button_rect = [None for k in range(len(L0) + 1)]
        # proposition des paris
        for k in range(len(button)):
            button[k] = large_font.render(str(k), True, WHITE)
            button_rect[k] = button[k].get_rect()
            button_rect[k].center = (400 - (50 / 2 * n) + 50 * k, 415)
            screen.blit(button[k], button_rect[k])
        # compte le nombre de bots vivants
        botvivant = 0
        # affiche les cartes en main
        main = pygame.image.load('cartes/main' + str(n) + ".png")
        main = pygame.transform.scale(main, (150, 150))
        screen.blit(main, (50, 200))
        screen.blit(main, (600, 200))
        screen.blit(main, (325, 20))

        vies0 = large_font.render("vies: " + str(vies[0]), True, WHITE)
        vies0_rect = vies0.get_rect()
        vies0_rect.center = (590, 500)
        screen.blit(vies0, vies0_rect)

        # idem affichage fonctions précédentes. Subtilité : tous les paris ne sont pas forcément encore faits
        if vies[1] > 0:
            botvivant += 1
            if pariprécédents[botvivant] != -1:
                paris1 = large_font.render("pari: " + str(pariprécédents[botvivant]), True, WHITE)
            else:
                paris1 = large_font.render("pas parié", True, WHITE)
            paris1_rect = paris1.get_rect()
            paris1_rect.center = (120, 375)
            screen.blit(paris1, paris1_rect)
            vies1 = large_font.render("vies: " + str(vies[1]), True, WHITE)
            vies1_rect = vies1.get_rect()
            vies1_rect.center = (120, 170)
            screen.blit(vies1, vies1_rect)

        if vies[2] > 0:
            botvivant += 1
            if pariprécédents[botvivant] != -1:
                paris2 = large_font.render("pari: " + str(pariprécédents[botvivant]), True, WHITE)
            else:
                paris2 = large_font.render("pas parié", True, WHITE)
            paris2_rect = paris2.get_rect()
            paris2_rect.center = (400, 195)
            screen.blit(paris2, paris2_rect)
            vies2 = large_font.render("vies: " + str(vies[2]), True, WHITE)
            vies2_rect = vies2.get_rect()
            vies2_rect.center = (550, 50)
            screen.blit(vies2, vies2_rect)

        if vies[3] > 0:
            botvivant += 1
            if pariprécédents[botvivant] != -1:
                paris3 = large_font.render("pari: " + str(pariprécédents[botvivant]), True, WHITE)
            else:
                paris3 = large_font.render("pas parié", True, WHITE)
            paris3_rect = paris3.get_rect()
            paris3_rect.center = (685, 375)
            screen.blit(paris3, paris3_rect)
            vies3 = large_font.render("vies: " + str(vies[3]), True, WHITE)
            vies3_rect = vies3.get_rect()
            vies3_rect.center = (685, 170)
            screen.blit(vies3, vies3_rect)

        # détection du choix
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
    Gestion graphique du jeu à une carte. L'utilisateur voit les cartes des autres, mais pas la sienne.

    :param cartes: cartes visibles (celles des joueurs bots)
    :param pariprécédents: paris déjà posés
    :param vies: vies des joueurs
    :return: pari du joueur humain
    """
    "Author : Prévost Thomas"

    # affichage : même fonctionnement que pour les autres fonctions
    # spécificité : affiche les cartes des bots, mais pas celle du joueur
    for k in range(len(cartes)):
        if type(cartes[k][0]) != int:
            cartes[k] = [22]
    n = len(cartes)
    Im = [str(k) for k in range(0, 23)]
    for k in range(0, 23):
        Im[k] = pygame.image.load('cartes/' + Im[k] + '.jpeg')
        Im[k] = pygame.transform.scale(Im[k], (50, 80))
    large_font = pygame.font.Font(None, 50)
    while True:
        fond = pygame.image.load('cartes/fond.png')
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

        # subtile différence avec les précédents : 1 carte -> on voit la carte des autres, pas la sienne
        if vies[1] > 0:
            screen.blit(Im[cartes[1][0]], (50, 200))
            paris1 = large_font.render("pari: " + str(pariprécédents[1]), True, WHITE)
            paris1_rect = paris1.get_rect()
            paris1_rect.center = (120, 375)
            screen.blit(paris1, paris1_rect)
            vies1 = large_font.render("vies: " + str(vies[1]), True, WHITE)
            vies1_rect = vies1.get_rect()
            vies1_rect.center = (120, 170)
            screen.blit(vies1, vies1_rect)

        if vies[2] > 0:
            screen.blit(Im[cartes[2][0]], (600, 200))
            paris2 = large_font.render("pari: " + str(pariprécédents[2]), True, WHITE)
            paris2_rect = paris2.get_rect()
            paris2_rect.center = (400, 195)
            screen.blit(paris2, paris2_rect)
            vies2 = large_font.render("vies: " + str(vies[2]), True, WHITE)
            vies2_rect = vies2.get_rect()
            vies2_rect.center = (550, 50)
            screen.blit(vies2, vies2_rect)

        if vies[3] > 0:
            screen.blit(Im[cartes[3][0]], (325, 20))
            paris3 = large_font.render("pari: " + str(pariprécédents[3]), True, WHITE)
            paris3_rect = paris3.get_rect()
            paris3_rect.center = (685, 375)
            screen.blit(paris3, paris3_rect)
            vies3 = large_font.render("vies: " + str(vies[3]), True, WHITE)
            vies3_rect = vies3.get_rect()
            vies3_rect.center = (685, 170)
            screen.blit(vies3, vies3_rect)

        # détection du pari
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
