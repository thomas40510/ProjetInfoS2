# coding=utf-8
import random


def maxi(L):
    pos = 0
    for k in range(1, len(L)):
        if L[k] > L[pos]:
            pos = k
    return pos


def nonNull(L):
    for k in range(len(L)):
        if L[k] <= 0:
            return False
    return True


class Joueur:
    def __init__(self, cartes):
        self.cartes = cartes

    def pari(self, parisprécédents, nombrecartes):
        volonté = int(sum(self.cartes) / (10 * nombrecartes))
        if len(parisprécédents) == 3 and sum(parisprécédents) + volonté == nombrecartes:
            volonté += [-1, 1][random.randint(0, 1)]
        return volonté

    def choixCartes(self, dejapresent, paris, pointsterrains):
        n = len(self.cartes)
        cartechoisie = self.cartes[random.randint(0, n - 1)]
        self.cartes.remove(cartechoisie)
        return cartechoisie


class Manche:
    def __init__(self, Listejoueur, nombredecartes, joueurdebut):
        L = [k for k in range(2, 23)]
        Lrandomisé = []
        for k in range(len(L)):
            a = random.randint(0, len(L) - 1)
            Lrandomisé.append(L[a])
            L.remove(L[a])
        self.joueurs = []
        self.listejoueur = Listejoueur
        self.nombredecartes = nombredecartes
        self.joueurdebut = joueurdebut
        for k in range(4):
            Listejoueur[k] = Joueur(Lrandomisé[nombredecartes * k:nombredecartes * (k + 1)])
            self.joueurs.append(Listejoueur[k])

    def paris(self):
        L = []
        for k in range(4):
            L.append(self.joueurs[k].pari(L, self.nombredecartes))
        return L

    def jeu(self):
        Points = [0 for k in range(4)]
        debut = self.joueurdebut
        paris = self.paris()
        for tour in range(self.nombredecartes):
            cartesposées = []
            for joueur in range(4):
                cartesposées.append(self.joueurs[(joueur + debut) % 4].choixcartes(cartesposées, paris, Points))
            vainqueur = maxi(cartesposées)
            Points[vainqueur] += 1
            debut = vainqueur
        Perte = [0 for k in range(4)]
        for k in range(4):
            Perte[k] += abs(Points[k] - paris[k])
        return Perte

    def __str__(self, cartesposées, debut):
        return f"{debut} \n 1: {cartesposées[0]}  2: {cartesposées[1]}  3: {cartesposées[2]}  4: {cartesposées[3]}"

    # def afftour(self, cartesposées, debut):
    #
    #     return (str(debut) + "\n" + "1:" + str(cartesposées[0]) + "  2:" + str(cartesposées[1]) + "  3:" + str(
    #         cartesposées[2]) + "  4:" + str(cartesposées[3]))


class Tarot:
    def __init__(self, nomJoueurs, nbPoints=20):
        self.nomJoueurs = nomJoueurs
        self.points = [nbPoints for k in range(4)]

    def exe(self):
        joueurdebut = 0
        while True:
            for k in range(5, 0, -1):
                a = Manche(self.nomJoueurs, k, joueurdebut % 4)
                perte = a.jeu()
                for p in range(4):
                    self.points[p] -= perte[p]
                if not nonNull(self.points):
                    return ()
                print(self.points)
            joueurdebut += 1


t = Tarot([str(k) for k in range(4)])
t.exe()
print(t.points)
