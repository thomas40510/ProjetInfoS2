import copy
import random


def closers(x):
    X = int(x)
    if x == X:
        return ([x, x - 1, x + 1])
    else:
        if x - X > 0.5:
            return (X + 1, X, X + 2)
        else:
            return (X, X + 1, X - 1)


def possibilitésretirepoints(L):
    A = [copy.deepcopy(L) for k in range(len(L))]
    for k in range(len(L)):
        A[k][k] -= 1
    return (A)


def maxi(L):
    LL = copy.deepcopy(L)
    pos = 0
    for k in range(0, len(L)):
        if L[k] == ['atout', 'maxi']:
            LL[k] = 22
        if L[k] == ['atout', 'mini']:
            LL[k] = 1
    for k in range(1, len(L)):
        if LL[k] > LL[pos]:
            pos = k
    return (pos)


def maxiTerrain(L):
    if ['atout', 'maxi'] in L:
        return (22)
    elif ['atout', 'mini'] in L:
        LL = copy.deepcopy(L)
        LL.remove(['atout', 'mini'])
        LL.append(1)
        return (maxiTerrain(LL))
    else:
        m = L[0]
        for k in L:
            if k > m:
                m = k
        return (m)


class Pari1Carte:
    def __init__(self, parisprécédents, cartesautresjoueurs):
        self.pariprécédents = parisprécédents
        self.cartesautresjoueurs = cartesautresjoueurs
        self.nbjoueurs = len(self.pariprécédents)

    def pari(self):
        choixautres = []
        for k in self.pariprécédents:
            if k != -1:
                choixautres.append(k)
        chgt = 0
        for k in choixautres:
            if k == 0:
                chgt += 1
            elif k == 1:
                chgt -= 1
        choix = 1
        for k in self.cartesautresjoueurs:
            if k[0] == 'atout' or k[0] > 13 + chgt * 2:
                choix = 0
        if self.pariprécédents.count(-1) == 1 and sum(self.pariprécédents) + choix == 0:
            choix = 1 - choix

        return (choix)


class Choix1Carte:
    def __init__(self, carte, pari):
        self.carte = carte
        self.pari = pari

    def choix(self):
        if self.carte != 'atout':
            return self.carte
        elif self.carte == 'atout' and self.pari == 0:
            return [self.carte, 'mini']
        elif self.carte == 'atout' and self.pari == 1:
            return [self.carte, 'maxi']


class PariMCartes:
    def __init__(self, parisprécédents, cartes):
        self.parisprécédents = parisprécédents
        self.cartes = cartes
        self.nbcartes = len(self.cartes)
        self.nbjoueurs = len(self.parisprécédents)
        self.nbjoueursdéjàparié = self.nbjoueurs - self.parisprécédents.count(-1)

    def pari(self):
        sumdéjàparié = 0
        for k in self.parisprécédents:
            if k != -1:
                sumdéjàparié += k
        if self.nbjoueursdéjàparié == 0:
            risque = -1
        elif sumdéjàparié / self.nbcartes > self.nbjoueursdéjàparié / self.nbjoueurs:
            risque = 1
        else:
            risque = -1

        volonté = 0
        for k in self.cartes:
            if k != 'atout' and k > 18:
                volonté += 1
            elif k != 'atout' and k > 15 and risque == 1:
                volonté += 0.3
            elif k != 'atout' and k > 15 and risque == -1:
                volonté += 0.6
            elif k != 'atout' and k > 8 and risque == 1:
                volonté += 0
            elif k != 'atout' and k > 8 and risque == -1:
                volonté += 0.24
            elif k != 'atout':
                volonté += 0

        a = closers(volonté)

        parisautorisés = [k for k in range(self.nbcartes + 1)]
        if self.nbjoueursdéjàparié == self.nbjoueurs - 1 and self.nbcartes - sumdéjàparié in parisautorisés:
            parisautorisés.remove(self.nbcartes - sumdéjàparié)

        for k in a:
            if k in parisautorisés:
                return k


class ChoixMCartes:
    def __init__(self, carte, paris, carteterrain, points, indice, debut):
        self.carte = carte
        self.paris = paris
        self.carteterrain = carteterrain
        self.points = points
        self.indice = indice
        self.pointàavoir = self.paris[indice]
        self.pointdéjàeu = self.points[indice]
        self.reste = self.pointàavoir - self.pointdéjàeu
        self.risque = 0
        if sum(paris) > len(carte) + sum(points):
            self.risque = 'sup'
        elif sum(paris) < len(carte):
            self.risque = 'min'
        self.debut = debut
        self.restegroupe = [self.paris[k] - self.points[k] for k in range(len(self.paris))]

    def choix(self):
        if self.risque == 'sup':
            return self.choixmax()
        else:
            return self.choixmin()

    def choixmin(self):
        CC = copy.deepcopy(self.carte)
        if 'atout' in CC:
            A = 1
            CC.remove('atout')
        else:
            A = 0
        CC.sort()
        TT = copy.deepcopy(self.carteterrain)
        if ['atout', 'mini'] in TT:
            TT.remove(['atout', 'mini'])
        if (TT == [0, 0] or TT == [0, 0, 0] or TT == [0, 0, 0, 0]) and self.reste != 0 and CC != []:
            return CC[-1]
        elif (TT == [0, 0] or TT == [0, 0, 0] or TT == [0, 0, 0, 0]) and self.reste == 0 and CC != []:
            return CC[0]
        elif CC == []:
            if self.reste > 0:
                return ['atout', 'maxi']
            else:
                return ['atout', 'mini']
        elif (self.reste == len(CC) and A == 0) or (self.reste == len(CC) + 1 and A == 1):
            return CC[-1]
        elif self.reste > 0:
            if ['atout', 'maxi'] in TT:
                return CC[-1]
            else:
                M = max(TT)
                if CC[0] < M < CC[-1]:
                    k = 0
                    while CC[k] < M:
                        k += 1
                    return CC[k - 1]
                elif M > CC[-1]:
                    return CC[-1]
                elif CC[0] > M:
                    return CC[-1]
        elif self.reste < 1:
            if ['atout', 'maxi'] in TT:
                return CC[-1]
            else:
                M = max(TT)
                if CC[0] < M < CC[-1]:
                    k = 0
                    while CC[k] < M:
                        k += 1
                    return CC[k - 1]
                elif M > CC[-1]:
                    return CC[-1]
                elif CC[0] > M and A == 1:
                    return ['atout', 'mini']
                elif CC[0] > M and A == 0:
                    return CC[-1]

    def choixmax(self):

        P = possibilitésretirepoints(self.restegroupe)
        TT = copy.deepcopy(self.carteterrain)
        if self.indice == self.debut:
            L = [[] for carte in self.carte]
            for carte in range(len(self.carte)):
                S = copy.deepcopy(self.carte)
                S.remove(self.carte[carte])
                for joueur in range(len(self.paris)):
                    Prob = Proba(S, P[joueur], joueur, self.indice)
                    L[carte].append(Prob.pointsmax() * self.restegroupe[joueur])
            M = [max(L[k] for k in range(len(L)))]
            C = self.carte[maxi(M)]
            if C == 'atout':
                return ['atout', 'maxi']
            else:
                return C

        elif self.indice == (self.debut - 1) % len(self.points):
            m = maxiTerrain(TT)
            L = [[] for carte in self.carte]
            for carte in range(len(self.carte)):
                S = copy.deepcopy(self.carte)
                S.remove(self.carte[carte])
                if self.carte[carte] == 'atout' or self.carte[carte] > m:
                    Prob = Proba(S, P[self.indice], self.indice, self.indice)
                    L[carte] = Prob.pointsmax()
                else:
                    m = maxi(TT)
                    Prob = Proba(S, P[m], m, self.indice)
                    L[carte] = Prob.pointsmax()
            M = [max(L[k] for k in range(len(L)))]
            C = self.carte[maxi(M)]
            if C == 'atout':
                return ['atout', 'maxi']
            else:
                return C

        else:
            if self.indice == (self.debut + 1) % len(self.points):
                m = maxiTerrain(TT)
                L = [[] for carte in self.carte]
                for carte in range(len(self.carte)):
                    S = copy.deepcopy(self.carte)
                    S.remove(self.carte[carte])
                    if self.carte[carte] == 'atout':
                        Prob = Proba(S, P[self.indice], self.indice, self.indice)
                        L[carte].append(Prob.pointsmax())
                    elif self.carte[carte] > m:
                        for joueur in range(len(self.paris)):
                            if joueur != (self.indice - 1) % len(self.points):
                                Prob = Proba(S, P[joueur], joueur, self.indice)
                                L[carte].append(Prob.pointsmax() * self.restegroupe[joueur])
                    elif self.carte[carte] < m:
                        for joueur in range(len(self.paris)):
                            if joueur != self.indice:
                                Prob = Proba(S, P[joueur], joueur, self.indice)
                                L[carte].append(Prob.pointsmax() * self.restegroupe[joueur])
                M = [max(L[k] for k in range(len(L)))]
                C = self.carte[maxi(M)]
                if C == 'atout':
                    return ['atout', 'maxi']
                else:
                    return C

            elif self.indice == (self.debut + 2) % len(self.points):
                m = maxiTerrain(TT)
                L = [[] for carte in self.carte]
                for carte in range(len(self.carte)):
                    S = copy.deepcopy(self.carte)
                    S.remove(self.carte[carte])
                    if self.carte[carte] == 'atout':
                        Prob = Proba(S, P[self.indice], self.indice, self.indice)
                        L[carte].append(Prob.pointsmax())
                    elif self.carte[carte] > m:
                        for joueur in range(len(self.paris)):
                            if joueur != (self.indice - 1) % len(self.points) and joueur != (self.indice - 2) % len(
                                    self.points):
                                Prob = Proba(S, P[joueur], joueur, self.indice)
                                L[carte].append(Prob.pointsmax() * self.restegroupe[joueur])
                    elif self.carte[carte] < m:
                        g = maxi(TT)
                        for joueur in range(len(self.paris)):
                            if joueur == (self.indice + 1) % len(self.points) or joueur == g:
                                Prob = Proba(S, P[joueur], joueur, self.indice)
                                L[carte].append(Prob.pointsmax() * self.restegroupe[joueur])
                M = [max(L[k] for k in range(len(L)))]
                C = self.carte[maxi(M)]
                if C == 'atout':
                    return ['atout', 'maxi']
                else:
                    return C


class Proba:
    def __init__(self, carte, resteglobal, debut, indice):
        self.carte = carte
        self.resteglobal = resteglobal
        self.indice = indice
        self.debut = debut
        self.resteperso = None

    def pointsmax(self):
        if len(self.carte) == 1:
            self.resteperso = self.resteglobal[self.indice]
            if self.resteperso < 0 or self.resteperso > 1:
                return 0
            elif (self.resteperso == 0 or self.resteperso == 1) and self.carte[0] == 'atout':
                return 1
            elif self.resteperso == 1:
                return max(0, 1 - (22 - self.carte[0]) * 0.15)
            elif self.resteperso == 0:
                if self.carte[0] < 17:
                    return 1
                else:
                    return 0
        else:
            Possibilités = possibilitésretirepoints(self.resteglobal)
            Chances = [0 for k in range(len(self.carte))]
            for c in range(len(self.carte)):
                if self.carte[c] == 'atout':
                    L = copy.deepcopy(self.carte)
                    L.remove('atout')
                    V = Proba(L, Possibilités[self.indice], self.debut, self.indice)
                    Chances[c] = (V.pointsmax())
                else:
                    L = copy.deepcopy(self.carte)
                    L.remove(self.carte[c])
                    resteglob = [max(0, k) for k in self.resteglobal]
                    Coef = [0.1, 0.2, 0.3, 0.4]
                    ptg = [1 - resteglob[k] * Coef[(self.debut - k - 1) % len(self.resteglobal)] for k in
                           range(len(self.resteglobal))]
                    ptg[self.indice] *= max(5 - (22 - self.carte[c]) * 0.7, 0)
                    ptg = [k ** 2 for k in ptg]
                    ptg = [k / sum(ptg) for k in ptg]
                    Prb = [(Proba(L, Possibilités[k], k, self.indice)).pointsmax() * ptg[k] for k in
                           range(len(self.resteglobal))]
                    Chances[c] = sum(Prb)
            return sum(Chances)
