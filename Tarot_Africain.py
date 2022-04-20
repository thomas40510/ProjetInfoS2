import random
import copy
from Joueurs import *


def maxi(L: list):
    """ Identifie l'indice de l'élément maximum d'une liste

    :param L: Liste de nombres
    :return: l'indice de l'élément maximal
    """
    pos = 0
    for k in range(1, len(L)):
        if L[k] > L[pos]:
            pos = k
    return pos


def nonnull(nomJ, joueurmorts):
    """ Vérifie si le joueur n'est pas mort

    :param nomJ: Nom du joueur
    :param joueurmorts: liste des joueurs morts
    :return: True si le joueur n'est pas mort, False sinon
    """
    for k in range((len(nomJ))):
        if nomJ[k][1] == 'vivant' and nomJ[k][2] <= 0 and joueurmorts[k] is False:
            return False
    return True


def compacartesposées(cartesposées):
    """ Compare les cartes posées pour savoir si le joueur a gagné

    :param cartesposées: liste des cartes posées
    :return: l'indice de la carte gagnante
    """
    L = []
    for k in cartesposées:
        if k == ['atout', 'maxi']:
            L.append(22)
        elif k == ['atout', 'mini']:
            L.append(1)
        else:
            L.append(k)
    # pos = 0
    # for k in range(len(L)):
    #     if L[k] > L[pos]:
    #         pos = k
    # return pos
    return maxi(L)


def verifremontée(perte):
    ind = -1
    nb = 0
    for k in range(len(perte)):
        if perte[k] == 0:
            nb += 1
            ind = k
    if nb == 1:
        return True, ind
    else:
        return False, -1


class Manche:
    """
    Classe représentant une manche de Tarot Africain
    """
    def __init__(self, Listejoueur, nombredecartes, joueurdebut, log, aff):
        """ Initialisation de la manche

        :param Listejoueur: liste des joueurs
        :param nombredecartes: nombre de cartes par joueur
        :param joueurdebut: joueur qui commence
        :param log: log de la partie
        :param aff: affichage de messages
        :type Listejoueur: list
        :type nombredecartes: int
        :type joueurdebut: int
        :type log: Log
        :type aff: bool
        """
        L = [k for k in range(2, 22)] + ['atout']
        Lrandomisé = []
        for k in range(len(L)):
            a = random.randint(0, len(L) - 1)
            Lrandomisé.append(L[a])
            L.remove(L[a])
        self.joueurs = []
        self.listejoueur = Listejoueur
        self.nombredecartes = nombredecartes
        self.joueurdebut = joueurdebut
        self.nbjoueurs = len(self.listejoueur)
        self.cartestour = []
        self.aff = aff
        for k in range(self.nbjoueurs):
            if 'bot' in self.listejoueur[k]:
                Listejoueur[k] = JoueurBot(Lrandomisé[nombredecartes * k:nombredecartes * (k + 1)], self.nbjoueurs,
                                           Listejoueur[k])
            else:
                Listejoueur[k] = JoueurHumain(Lrandomisé[nombredecartes * k:nombredecartes * (k + 1)], self.nbjoueurs,
                                              Listejoueur[k])
            self.joueurs.append(Listejoueur[k])
        self.cartesjoueurs = []
        for joueur in self.joueurs:
            self.cartesjoueurs.append(joueur.cartes)
        self.log = log

    def paris(self):
        """ Récolte les paris des joueurs

        :return: la liste des paris des joueurs
        """
        paris = [-1 for k in range(self.nbjoueurs)]
        for k in range(self.nbjoueurs):
            paris[(k + self.joueurdebut) % self.nbjoueurs] = self.joueurs[
                (k + self.joueurdebut) % self.nbjoueurs].pari2(paris, self.cartesjoueurs,
                                                               (k + self.joueurdebut) % self.nbjoueurs)
        if self.aff:
            print(self.joueurdebut, [self.joueurs[k].cartes for k in range(self.nbjoueurs)], paris)
        self.log[-1].append(paris)
        return paris

    def jeu(self):
        """ Joue une manche

        :return: Le joueur ayant perdu la manche
        """
        Points = [0 for k in range(4)]
        debut = self.joueurdebut
        paris = self.paris()
        print('Les paris sont:', paris)
        self.log[-1].append([])
        for tour in range(self.nombredecartes):
            cartesposées = [0 for k in range(self.nbjoueurs)]
            for joueur in range(self.nbjoueurs):
                cartesposées[(joueur + debut) % self.nbjoueurs] = (
                    self.joueurs[(joueur + debut) % self.nbjoueurs].choixcartes2(cartesposées, paris, Points,
                                                                                 self.cartesjoueurs,
                                                                                 (joueur + debut) % self.nbjoueurs,
                                                                                 self.nombredecartes, paris[joueur],
                                                                                 debut))
            self.cartestour.append([debut, cartesposées])
            if self.aff:
                self.__str__()
            self.log[-1][-1].append(cartesposées)
            # print("\n")
            vainqueur = compacartesposées(cartesposées)
            Points[vainqueur] += 1
            print('Le nombre de pli gagné est', Points)
            print('\n' * 3)
            debut = vainqueur
        Perte = [0 for k in range(self.nbjoueurs)]
        for k in range(self.nbjoueurs):
            Perte[k] += abs(Points[k] - paris[k])
        if self.aff:
            print("Perte :", Perte, "Points :", Points, "Paris :", paris)
            print('\n')
        return Perte

    def afftour(self, cartesposées, debut):
        """ Formate les cartes posées pour l'affichage

        :param cartesposées: liste des cartes posées
        :param debut: joueur ayant débuté le tour
        :type cartesposées: list
        :type debut: int
        :return: la liste des cartes posées
        """
        s = f"{debut} \n"
        for i in range(self.nbjoueurs):
            s += f"{i + 1}: {cartesposées[i]} "
        return s

    def __str__(self):
        """ Affichage de la manche"""
        debut = self.cartestour[-1][0]
        cartesposées = self.cartestour[-1][1]
        aff = ""
        for k in range(self.nbjoueurs):
            m = ""
            m += self.joueurs[k].nom + " "
            if debut == k:
                m += " leader "
            m += " " + str(cartesposées[k])
            m += '\n'
            aff += m
        print(aff)


class Tarot:
    """
    Classe qui gère une partie de tarot africain
    """
    def __init__(self, nomJoueurs, nbPoints=20, aff=True):
        """ Initialise la partie

        :param nomJoueurs: Noms des joueurs et leur type
        :param nbPoints: Nombre de vies des joueurs
        :param aff: Affichage des messages au cours de la partie
        :type nomJoueurs: list
        :type nbPoints: int
        :type aff: bool
        """
        self.nomJoueurs = [[nomJoueurs[k], 'vivant', nbPoints, False] for k in range(len(nomJoueurs))]
        if aff:
            print(self.nomJoueurs)
        self.nomJoueurs[0][3] = True
        self.memoire = []
        self.joueurmort = [False for k in range(len(nomJoueurs))]
        self.nbjoueurs = len(nomJoueurs)
        self.aff = aff
        self.log = Log()
        self.numManche = 0

    def exe(self):
        """ Exécute une partie

        :return: vainqueur et mémoire de la partie
        """
        print("Vous êtes le joueur en première position")
        while True:
            for nbcartes in range(5, 0, -1):
                print("Les points sont:", [self.nomJoueurs[k][2] for k in range(len(self.nomJoueurs))])
                compt = 0
                joueurvivant = []
                for a in range(len(self.nomJoueurs)):
                    if self.nomJoueurs[a][1] == 'vivant':
                        joueurvivant.append(self.nomJoueurs[a][0])
                        if self.nomJoueurs[a][3]:
                            joueurdebut = a
                if self.aff:
                    print(joueurdebut, self.nomJoueurs)
                self.nbjoueurs = compt
                self.log.append([])
                self.numManche += 1
                self.log[-1].append(copy.deepcopy(self.numManche))
                self.log[-1].append(copy.deepcopy(self.nomJoueurs))
                a = Manche(joueurvivant, nbcartes, joueurdebut, self.log, aff=self.aff)
                perte = a.jeu()

                remontée, indice = verifremontée(perte)
                if remontée:
                    perte[indice] = -1
                print('Les pertes sont:', perte)
                print('\n' * 2)
                ind = 0
                for k in self.nomJoueurs:
                    if k[1] == 'vivant':
                        k[2] -= perte[ind]
                        ind += 1
                points = [self.nomJoueurs[k][2] for k in range(len(self.nomJoueurs))]
                self.memoire.append(copy.deepcopy(points))
                if not nonnull(self.nomJoueurs, self.joueurmort):
                    self.enleve()
                    nbJoueurs = 0
                    for k in self.nomJoueurs:
                        if k[1] == 'vivant':
                            nbJoueurs += 1
                    if nbJoueurs <= 1:
                        a = self.affvainqueur()
                        print("Le vainqueur est ", a[0])
                        return a, self.memoire
                    else:
                        break
                if self.aff:
                    self.log.affder()

            for k in range(len(self.nomJoueurs)):
                if self.nomJoueurs[k][3]:
                    c = k
            self.nomJoueurs[c][3] = False
            self.nomJoueurs[(c + 1) % len(self.nomJoueurs)][3] = True
            c = (c + 1) % len(self.nomJoueurs)
            while self.nomJoueurs[c][1] == 'mort':
                self.nomJoueurs[c][3] = False
                self.nomJoueurs[(c + 1) % len(self.nomJoueurs)][3] = True
                c = (c + 1) % len(self.nomJoueurs)

    def enleve(self):
        """ Gestion des joueurs morts"""
        for k in range(len(self.nomJoueurs)):
            if self.nomJoueurs[k][2] <= 0 and self.nomJoueurs[k][1] == 'vivant':
                self.nomJoueurs[k][1] = 'mort'
                self.joueurmort[k] = True

    def affvainqueur(self):
        """ Identification du vainqueur pour affichage

        :return: vainqueur s'il existe, ou 'égalité' sinon
        """
        nbJoueurs = 0
        for k in self.nomJoueurs:
            if k[1] == 'vivant':
                nbJoueurs += 1
        if nbJoueurs != 1:
            return 'égalité'
        else:
            for k in self.nomJoueurs:
                if k[1] == 'vivant':
                    return k[0]

    def __str__(self):
        """ Affichage de la partie"""
        pts = [self.nomJoueurs[k][2] for k in range(len(self.nomJoueurs))]
        print(pts)


class Log(list):
    """
    Classe permettant de créer un log de la partie
    """
    def affder(self):
        return self[-1]

    def nbtour(self):
        return self[-1][0]

    def paris(self, nbcartes):
        L = []
        for k in self:
            if len(k[3]) == nbcartes:
                L.append(k[2])
        return L

# t = Tarot([['humain', 'humain']] + [['b1', 'bot']] + [['b2', 'bot']] + [['b3', 'bot']], nbPoints=2, aff=False)
# v, L = t.exe()
