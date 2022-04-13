import random
import copy
import matplotlib.pyplot as plt
from joueurs import *


def maxi(L):
    pos = 0
    for k in range(1, len(L)):
        if L[k] > L[pos]:
            pos = k
    return pos


def nonnull(nomJ, joueurmorts):
    for k in range((len(nomJ))):
        if nomJ[k][1] == 'vivant' and nomJ[k][2] <= 0 and not joueurmorts[k]:
            return False
    return True


def compacartesposees(cartesposées):
    L = []
    for k in cartesposées:
        if k == ['atout', 'maxi']:
            L.append(22)
        elif k == ['atout', 'mini']:
            L.append(1)
        else:
            L.append(k)
    pos = 0
    for k in range(len(L)):
        if L[k] > L[pos]:
            pos = k
    return pos


def verifremontee(perte):
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


# class Joueur:
#     def __init__(self, cartes, nbjoueurs, nom):
#         self.statut = nom[1]
#         self.cartes = cartes
#         self.nbjoueurs = nbjoueurs
#         self.nom = nom[0]
#         self.nbcartes = len(self.cartes)
#
#     def pari(self, parisprécédents):
#         nbparis = 0
#         for k in parisprécédents:
#             if k != -1:
#                 nbparis += 1
#         volonté = 0
#         for k in range(self.nbcartes):
#             if self.cartes[k] == 'atout':
#                 volonté += 14
#             else:
#                 volonté += self.cartes[k]
#         volonté = int(volonté / (10 * self.nbcartes))
#         volonté = min(max(0, volonté), self.nbcartes)
#         if nbparis == self.nbjoueurs - 1 and sum(parisprécédents) + volonté + 1 == self.nbcartes:
#             volonté += [-1, 1][random.randint(0, 1)]
#             if volonté == -1:
#                 volonté += 2
#             if volonté > self.nbcartes:
#                 volonté -= 2
#         return (volonté)
#
#     def choixcartes(self, dejapresent, paris, pointsterrains):
#         n = len(self.cartes)
#         cartechoisi = self.cartes[random.randint(0, n - 1)]
#         self.cartes.remove(cartechoisi)
#         if cartechoisi == 'atout':
#             cartechoisi = ['atout', 'maxi']
#         return (cartechoisi)


class Manche:
    def __init__(self, Listejoueur, nombredecartes, joueurdebut, aff):
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
            Listejoueur[k] = Joueur(Lrandomisé[nombredecartes * k:nombredecartes * (k + 1)], self.nbjoueurs,
                                    Listejoueur[k])
            self.joueurs.append(Listejoueur[k])

    def paris(self):
        L = [-1 for k in range(self.nbjoueurs)]
        for k in range(self.nbjoueurs):
            L[(k + self.joueurdebut) % self.nbjoueurs] = self.joueurs[(k + self.joueurdebut) % self.nbjoueurs].pari(L)
        if self.aff:
            print(self.joueurdebut, [self.joueurs[k].cartes for k in range(self.nbjoueurs)], L)
        return (L)

    def jeu(self):
        Points = [0 for k in range(4)]
        debut = self.joueurdebut
        paris = self.paris()
        for tour in range(self.nombredecartes):
            cartesposées = []
            for joueur in range(self.nbjoueurs):
                cartesposées.append(
                    self.joueurs[(joueur + debut) % self.nbjoueurs].choixcartes(cartesposées, paris, Points))
            self.cartestour.append([debut, cartesposées])
            if self.aff:
                self.__str__()
            # print("\n")
            vainqueur = compacartesposees(cartesposées)
            Points[vainqueur] += 1
            debut = vainqueur
        Perte = [0 for k in range(self.nbjoueurs)]
        for k in range(self.nbjoueurs):
            Perte[k] += abs(Points[k] - paris[k])
        if self.aff:
            print("Perte:", Perte, "Points:", Points, "Paris", paris)
            print('\n')
        return (Perte)

    def afftour(self, cartesposées, debut):
        if self.nbjoueurs == 4:
            return f"{debut} \n + 1 : {cartesposées[0]} 2 : {cartesposées[1]} " \
                   f"3 : {cartesposées[2]} 4 : {cartesposées[3]}"
            # return (str(debut) + "\n" + "1:" + str(cartesposées[0]) + "  2:" + str(cartesposées[1]) + "  3:" + str(
            #    cartesposées[2]) + "  4:" + str(cartesposées[3]))
        elif self.nbjoueurs == 3:
            return f"{debut} \n + 1 : {cartesposées[0]} 2 : {cartesposées[1]} 3 : {cartesposées[2]}"
            # return (str(debut) + "\n" + "1:" + str(cartesposées[0]) + "  2:" + str(cartesposées[1]) + "  3:" + str(
            #     cartesposées[2]))
        elif self.nbjoueurs == 2:
            return f"{debut} \n + 1 : {cartesposées[0]} 2 : {cartesposées[1]}"
            # return str(debut) + "\n" + "1:" + str(cartesposées[0]) + "  2:" + str(cartesposées[1])

    def __str__(self):
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
    def __init__(self, nomJoueurs, nbPoints=20, aff=True):
        self.nomJoueurs = [[nomJoueurs[k], 'vivant', nbPoints, False] for k in range(len(nomJoueurs))]
        if aff:
            print(self.nomJoueurs)
        self.nomJoueurs[0][3] = True
        self.memoire = []
        self.joueurmort = [False for k in range(len(nomJoueurs))]
        self.aff = aff

    def exe(self):
        while True:
            for nbcartes in range(5, 0, -1):
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
                a = Manche(joueurvivant, nbcartes, joueurdebut, aff=self.aff)
                perte = a.jeu()

                remontée, indice = verifremontee(perte)
                if remontée:
                    perte[indice] = -1

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
                        a = self.affvainqueur(self.aff)
                        return (a, self.memoire)
                    else:
                        break
                if self.aff:
                    self.__str__()

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
        V = []
        for k in range(len(self.nomJoueurs)):
            if self.nomJoueurs[k][2] <= 0 and self.nomJoueurs[k][1] == 'vivant':
                self.nomJoueurs[k][1] = 'mort'
                self.joueurmort[k] = True

    def affvainqueur(self, aff):
        if aff:
            print(self.nomJoueurs)
        nbJoueurs = 0
        for k in self.nomJoueurs:
            if k[1] == 'vivant':
                nbJoueurs += 1
        if nbJoueurs != 1:
            # print('égalité!')
            return ('égalité')
        else:
            for k in self.nomJoueurs:
                if k[1] == 'vivant':
                    a = k[0]
                    # print('Vainqueur:'+a)
                    return (k[0])

    def __str__(self):
        pts = [self.nomJoueurs[k][2] for k in range(len(self.nomJoueurs))]
        print(pts)


R = [0, 0, 0, 0]
for k in range(100):
    t = Tarot([['humain', 'humain']] + [['b1', 'bot']] + [['b2', 'bot']] + [['b3', 'bot']], nbPoints=200, aff=False)
    v, L = t.exe()
    if v[0] == 'humain':
        R[0] += 1
    if v[0] == 'b1':
        R[1] += 1
    if v[0] == 'b2':
        R[2] += 1
    if v[0] == 'b3':
        R[3] += 1
    print(k)
print(R)
# test unitaires:
# attribution cartes
# morts-vivants (vérification nombre joueur)
# paris déconnants
# pas de pertes de points