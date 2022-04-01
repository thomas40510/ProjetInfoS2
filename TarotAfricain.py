import random
import copy


def maxi(L):
    pos = 0
    for k in range(1, len(L)):
        if L[k] > L[pos]:
            pos = k
    return (pos)


def nonnull(nomJ, joueurmorts):
    for k in range((len(nomJ))):
        if nomJ[k][1] == 'vivant' and nomJ[k][2] <= 0 and joueurmorts[k] == False:
            return False
    return True


class Joueur:
    def __init__(self, cartes, nbjoueurs, nom):
        self.cartes = cartes
        self.nbjoueurs = nbjoueurs
        self.nom = nom

    def pari(self, parisprécédents, nombrecartes):
        volonté = int(sum(self.cartes) / (10 * nombrecartes))
        if len(parisprécédents) == self.nbjoueurs - 1 and sum(parisprécédents) + volonté == nombrecartes:
            volonté += [-1, 1][random.randint(0, 1)]
        return (volonté)

    def choixcartes(self, dejapresent, paris, pointsterrains):
        n = len(self.cartes)
        cartechoisi = self.cartes[random.randint(0, n - 1)]
        self.cartes.remove(cartechoisi)
        return (cartechoisi)


class Manche:
    def __init__(self, Listejoueur, nombredecartes, joueurdebut):
        L = [k for k in range(2, 23)]
        random.shuffle(L)  # Lrandomisé est juste un shuffle de L, inutile de travailler sur 2 listes
        self.joueurs = []
        self.listejoueur = Listejoueur
        self.nombredecartes = nombredecartes
        self.joueurdebut = joueurdebut
        self.nbjoueurs = len(self.listejoueur)
        self.cartestour = []
        for k in range(self.nbjoueurs):
            Listejoueur[k] = Joueur(L[nombredecartes * k:nombredecartes * (k + 1)], self.nbjoueurs,
                                    Listejoueur[k])
            self.joueurs.append(Listejoueur[k])

    def paris(self):
        L = []
        for k in range(self.nbjoueurs):
            L.append(self.joueurs[k].pari(L, self.nombredecartes))
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
            self.__str__()
            # print("\n")
            vainqueur = maxi(cartesposées)
            Points[vainqueur] += 1
            debut = vainqueur
        Perte = [0 for k in range(self.nbjoueurs)]
        for k in range(self.nbjoueurs):
            Perte[k] += abs(Points[k] - paris[k])
        print(Perte)
        return Perte

    def afftour(self, cartesposées, debut):
        if self.nbjoueurs == 4:
            return (str(debut) + "\n" + "1:" + str(cartesposées[0]) + "  2:" + str(cartesposées[1]) + "  3:" + str(
                cartesposées[2]) + "  4:" + str(cartesposées[3]))
        elif self.nbjoueurs == 3:
            return (str(debut) + "\n" + "1:" + str(cartesposées[0]) + "  2:" + str(cartesposées[1]) + "  3:" + str(
                cartesposées[2]))
        elif self.nbjoueurs == 2:
            return (str(debut) + "\n" + "1:" + str(cartesposées[0]) + "  2:" + str(cartesposées[1]))

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
    def __init__(self, nomJoueurs, nbPoints=20):
        self.nomJoueurs = [[nomJoueurs[k], 'vivant', nbPoints, False] for k in range(len(nomJoueurs))]
        self.nomJoueurs[0][3] = True
        self.memoire = []
        self.joueurmort = [False for k in range(len(nomJoueurs))]

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
                print(joueurdebut, self.nomJoueurs)
                self.nbjoueurs = compt
                a = Manche(joueurvivant, nbcartes, joueurdebut)  # pb joueurdebut
                perte = a.jeu()
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
                        return (a, self.memoire)
                    else:
                        break
                self.__str__()

            for k in range(len(self.nomJoueurs)):
                if self.nomJoueurs[k][3]:
                    c = k
            self.nomJoueurs[c][3] = False
            self.nomJoueurs[(c + 1) % len(self.nomJoueurs)][3] = True
            c = (c + 1) % len(self.nomJoueurs)  # gestion du premier joueur à refaire
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

    def affvainqueur(self):
        nbJoueurs = 0
        for k in self.nomJoueurs:
            if k[1] == 'vivant':
                nbJoueurs += 1
        if nbJoueurs != 1:
            # print('égalité!')
            return 4
        else:
            for k in self.nomJoueurs:
                if k[1] == 'vivant':
                    a = k[0]
            # print('Vainqueur:'+a)
            return int(a)

    def __str__(self):
        pts = [self.nomJoueurs[k][2] for k in range(len(self.nomJoueurs))]
        print(pts)


L = [0, 0, 0, 0, 0]
for a in range(100):
    t = Tarot([str(k) for k in range(4)], nbPoints=100)
    v, l = t.exe()
    L[v] += 1
    print(t.nomJoueurs)
print(L)
