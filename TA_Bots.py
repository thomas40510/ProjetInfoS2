import copy
import random


def closers(x):
    """ Donne les 3 entiers les plus proches d'un flottant x
        :param x: un flottant
        :return: la liste des 3 entiers les plus proches"""
    X = int(x)
    if x == X:
        return [x, x - 1, x + 1]
    else:
        if x - X > 0.5:
            return X + 1, X, X + 2
        else:
            return X, X + 1, X - 1


def possibilitésretirepoints(L):
    """ Donne le nombre de plis manquants de chaque joueur en fonction de s'il gagne ou non ce tour
        :param L: Liste des plis manquants de chaque joueur
        :return: [L si joueur 0 gagne, L si joueur 1 gagne, ...]
        """
    A = [copy.deepcopy(L) for k in range(len(L))]
    for k in range(len(L)):
        A[k][k] -= 1
    return A


def maxi(L):
    """ Identifie l'indice de l'élément maximum d'une liste
        :param L: Liste de nombres
        :return: l'indice de l'élément maximal
        """
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
    return pos


def maxiTerrain(L):
    """ Identifie la carte la plus forte sur le terrain
        :param L: Liste de nombres
        :return: valeur de la carte la plus forte sur le terrain
        """
    if ['atout', 'maxi'] in L:
        return (22)
    elif ['atout', 'mini'] in L:
        LL = copy.deepcopy(L)
        LL.remove(['atout', 'mini'])
        LL.append(1)
        return maxiTerrain(LL)
    else:
        m = L[0]
        for k in L:
            if k > m:
                m = k
        return m


def pari1Carte(parisprécédents, cartesautresjoueurs):
    """ Fait le pari à 1 carte: on connait les cartes sur le front des autres joueurs, éventuellement les paris précédents
        :param parisprécédents: Liste des paris précédents
        :param cartesautresjoueurs: Liste des cartes vues sur le front des autres joueurs
        :return: le pari (0 ou 1) fait par le bot
        """
    choixautres = []  # récupère les paris déjà effectués
    for k in parisprécédents:
        if k != -1:
            choixautres.append(k)
    chgt = 0  # réaction aux paris des autres joueurs
    for k in choixautres:
        if k == 0:
            chgt += 1
        elif k == 1:
            chgt -= 1
    choix = 1  # parier 1 d'office
    for k in cartesautresjoueurs:
        if k[0] == 'atout' or k[0] > 13 + chgt * 2:  # parier 0 dans le cas: voir une carte trop forte chez les autres joueurs
            choix = 0
    if parisprécédents.count(-1) == 1 and sum(
            parisprécédents) + choix == 0:  # si l'on est dernier à jouer, et que l'on a pas le choix
        choix = 1 - choix
    return choix


def Choix1Carte(carte, pari):
    """ pose la carte que l'on a main, en mini ou en maxi si l'on a l'atout selon le pari posé"""
    if carte != 'atout':
        return (carte)
    elif carte == 'atout' and pari == 0:
        return ([carte, 'mini'])
    elif carte == 'atout' and pari == 1:
        return ([carte, 'maxi'])


def PariMCartes(parisprécédents, cartes):
    """
        Fait le pari à plusieurs cartes: on connait les cartes que l'on a en main, éventuellement les paris précédents
        :param parisprécédents: Liste des paris précédents
        :param cartes: Liste des cartes en main
        :return: le pari, allant de 0 au nombre de cartes en main
        """
    nbcartes = len(cartes)
    nbjoueurs = len(parisprécédents)
    nbjoueursdéjàparié = nbjoueurs - parisprécédents.count(-1)
    sumdéjàparié = 0
    for k in parisprécédents:
        if k != -1:
            sumdéjàparié += k
    if nbjoueursdéjàparié == 0:
        risque = -1
    elif sumdéjàparié / nbcartes > nbjoueursdéjàparié / nbjoueurs:
        risque = 1
    else:
        risque = -1
    # risque évalue si les parieurs précédents ont parié haut ou bas, pour adapter ses propres paris

    volonté = 0  # évalue le nombre de plis que l'on pense remporter
    for k in cartes:
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

    a = closers(volonté)  # les 3 entiers les plus proches du nombre que l'on veut demander

    parisautorisés = [k for k in range(nbcartes + 1)]
    if nbjoueursdéjàparié == nbjoueurs - 1 and nbcartes - sumdéjàparié in parisautorisés:
        parisautorisés.remove(
            nbcartes - sumdéjàparié)  # si l'on est le dernier à jouer, on retire le pari interdit des paris possibles

    for k in a:
        if k in parisautorisés:
            return k  # on return l'entier le proche de ce que l'on veut parier, et que les règles autorisent


def ChoixMCartes(carte, paris, carteterrain, points, indice, debut):
    """
        Choisit la carte à jouer lors d'un jeu à plusieurs cartes
        :param carte: les cartes en main
        :param paris: les paris effectués par les joueurs
        :param carteterrain: les cartes éventuellement déjà posées sur le terrain pendant ce tour
        :param points: les points déjà obtenus lors des tours précédents
        :param indice: entier représentant le joueur qui effectue ce choix (0 à 3)
        :param debut: entier représentant le joueur posant ses cartes en premier (0 à 3)
        :return: la carte choisie
        """

    pointàavoir = paris[indice]
    pointdéjàeu = points[indice]
    reste = pointàavoir - pointdéjàeu
    risque = 0
    if sum(paris) > len(carte) + sum(points):
        risque = 'sup'
    elif sum(paris) < len(carte) + sum(points):
        risque = 'inf'
    restegroupe = [paris[k] - points[k] for k in range(len(paris))]
    # risque évalue si l'on joue au supérieur (les paris ont été plus hauts que le nombre de cartes, donc les joueurs
    # vont se battre pour récupérer assez de plis), ou à l'inférieur (les paris ont été plus bas que le nombre de
    # cartes, donc les joueurs vont se battre pour ne pas récupérer trop de plis) Les stratégies dans ces deux cas
    # sont très différentes

    # si l'on joue à l'inférieur: le but est de forcer les autres joueurs à récupérer des plis
    if risque == 'inf':
        CC = copy.deepcopy(carte)
        if 'atout' in CC:
            A = 1
            CC.remove('atout')
        else:
            A = 0
        CC.sort()
        TT = copy.deepcopy(carteterrain)
        if ['atout', 'mini'] in TT:
            TT.remove(['atout', 'mini'])
        if (TT == [0, 0] or TT == [0, 0, 0] or TT == [0, 0, 0,
                                                      0]) and reste != 0 and CC != []:  # si l'on joue en premier, et que l'on a encore des plis à gagner, on pose la carte la plus forte
            return CC[-1]
        elif (TT == [0, 0] or TT == [0, 0, 0] or TT == [0, 0, 0,
                                                        0]) and reste == 0 and CC != []:  # si l'on joue en premier, et que l'on ne doit plus gagner de plis, on pose la carte la plus faible
            return CC[0]
        elif CC == []:
            if reste > 0:
                return ['atout', 'maxi']
            else:
                return ['atout', 'mini']
        elif (reste == len(CC) and A == 0) or (
                reste == len(CC) + 1 and A == 1):  # si on doit gagner des plis, on pose la carte la plus forte
            return CC[-1]
        elif reste > 0:  # si possible, on se débarrasse des cartes fortes pour ne pas avoir à prendre de plis excédents avec
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
        elif reste < 1:  # si on ne doit plus prendre de plis, on place la carte nécessaire pour ne pas gagner le pli actuel
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

    # si l'on joue au supérieur, et que l'on doit se battre pour récupérer assez de plis
    # l'ordre de jeu est essentiel; le dernier joueur à poser sa carte est fortement favorisé
    # on va estimer les probabilités de chaque joueur de gagner le tour, et estimer les situations
    # (points encore à gagner, joueur jouant en premier) les plus favorables avec la fonction récursive Proba
    # pour décider quelle carte il est préférable de poser
    if risque == 'sup':
        P = possibilitésretirepoints(restegroupe)
        TT = copy.deepcopy(carteterrain)

        if indice == debut:  # si le bot joue en premier
            L = [[] for k in carte]
            for c in range(len(carte)):  # pour chaque carte
                S = copy.deepcopy(carte)
                S.remove(carte[c])
                for joueur in range(len(paris)):
                    Prob = Proba(S, P[joueur], joueur, indice)
                    L[c].append(
                        Prob * restegroupe[joueur])  # les estimations des situations selon la victoire de chaque joueur
            M = [max(L[k] for k in range(len(L)))]
            C = carte[maxi(M)]  # choisit la carte la plus favorable
            if C == 'atout':
                return ['atout', 'maxi']
            else:
                return C

        elif indice == (debut - 1) % len(points):  # si le bot joue en dernier
            m = maxiTerrain(TT)
            L = [[] for k in carte]
            for c in range(len(carte)):
                S = copy.deepcopy(carte)
                S.remove(carte[c])
                if carte[c] == 'atout' or carte[c] > m:  # si la carte posée lui fait gagner le pli
                    Prob = Proba(S, P[indice], indice, indice)
                    L[c] = Prob
                else:  # si la carte posée ne lui fait pas gagner le pli
                    m = maxi(TT)
                    Prob = Proba(S, P[m], m, indice)
                    L[c] = Prob
            M = [max(L[k] for k in range(len(L)))]  # choisit la carte la plus favorablee
            C = carte[maxi(M)]
            if C == 'atout':
                return ['atout', 'maxi']
            else:
                return C

        else:
            if indice == (debut + 1) % len(points):  # si l'on joue en deuxième
                m = maxiTerrain(TT)
                L = [[] for k in carte]
                for c in range(len(carte)):
                    S = copy.deepcopy(carte)
                    S.remove(carte[c])
                    if carte[c] == 'atout':  # atout en maxi: on est sûr de gagner le pli
                        Prob = Proba(S, P[indice], indice, indice)
                        L[c].append(Prob)
                    elif carte[c] > m:  # carte plus forte que celle du premier : on peut gagner le pli
                        for joueur in range(len(paris)):
                            if joueur != (indice - 1) % len(points):
                                Prob = Proba(S, P[joueur], joueur, indice)
                                L[c].append(Prob * restegroupe[joueur])
                    elif carte[c] < m:  # carte plus faible que celle du premier : impossible de gagner le pli
                        for joueur in range(len(paris)):
                            if joueur != indice:
                                Prob = Proba(S, P[joueur], joueur, indice)
                                L[c].append(Prob * restegroupe[joueur])
                M = [max(L[k] for k in range(len(L)))]
                C = carte[maxi(M)]
                if C == 'atout':
                    return ['atout', 'maxi']
                else:
                    return C

            elif indice == (debut + 2) % len(points):  # le bot joue en troisième
                m = maxiTerrain(TT)
                L = [[] for k in carte]
                for c in range(len(carte)):
                    S = copy.deepcopy(carte)
                    S.remove(carte[c])
                    if carte[c] == 'atout':  # atout -> sûr de gagner
                        Prob = Proba(S, P[indice], indice, indice)
                        L[c].append(Prob)
                    elif carte[c] > m:  # carte plus forte que celle des 2 premiers
                        for joueur in range(len(paris)):
                            if joueur != (indice - 1) % len(points) and joueur != (indice - 2) % len(points):
                                Prob = Proba(S, P[joueur], joueur, indice)
                                L[c].append(Prob * restegroupe[joueur])
                    elif carte[c] < m:  # carte plus faible que la plus forte des deux premiers
                        g = maxi(TT)
                        for joueur in range(len(paris)):
                            if joueur == (indice + 1) % len(points) or joueur == g:
                                Prob = Proba(S, P[joueur], joueur, indice)
                                L[c].append(Prob * restegroupe[joueur])
                M = [max(L[k] for k in range(len(L)))]
                C = carte[maxi(M)]
                if C == 'atout':
                    return ['atout', 'maxi']
                else:
                    return C


def Proba(carte, resteglobal, debut, indice):
    """
        Evalue de manière récursive si la situation donnée est favorable au bot (indice de favorabilité)
        Initialisation : avec 0 cartes en main, l'indice vaut 1 point si l'on a le bon nombre de plis, 0 sinon
        Hérédité: on estime les probabilités de chaque joueur de gagner le tour en fonction:
        -des plis qu'il lui reste à gagner
        -de la carte que le bot peut poser
        -l'ordre de jeu
        que l'on multiplie par l'indice de favorabilité que donnerait la situation au tour suivant, avec donc 1 une
        carte de moins dans chaque main.
        :param carte: liste des cartes dans la main du bot
        :param resteglobal: liste des plis restants à gagner pour chaque joueur
        :param debut: entier donnant la position du joueur jouant en premier
        :param indice: entier donnant la position du bot
        :return: un flottant positif, l'indice de favorabilité
        """
    if carte == []:  # initialisation
        resteperso = resteglobal[indice]
        if resteperso != 0:
            return 0
        elif resteperso == 0:
            return 1
    else:  # hérédité
        Possibilités = possibilitésretirepoints(
            resteglobal)  # situation au tour suivant selon la victoire de chaque joueur
        Chances = [0 for k in range(len(carte))]  # indice de favorabilité pour chaque carte jouée
        for c in range(len(carte)):
            if carte[c] == 'atout':  # certitude de gagner (peu d'intérêt de jouer l'atout en mini)
                L = copy.deepcopy(carte)
                L.remove('atout')
                V = Proba(L, Possibilités[indice], debut, indice)
                Chances[c] = V
            else:
                L = copy.deepcopy(carte)
                L.remove(carte[c])
                resteglob = [max(0, k) for k in resteglobal]  # plis restants à gagner pour chaque joueur
                Coef = [0.1, 0.2, 0.3, 0.4]  # représente l'avantage du dernier joueur à jouer
                ptg = [1 - resteglob[k] * Coef[(debut - k - 1) % len(resteglobal)] for k in
                       range(len(resteglobal))]  # chance de gagner le pli de chaque joueur
                ptg[indice] *= max(5 - (22 - carte[c]) * 0.7,
                                   0)  # modification de cette chance pour le bot selon la carte qu'il pose
                ptg = [k ** 2 for k in ptg]
                ptg = [k / sum(ptg) for k in ptg]  # normalisation
                Prb = [(Proba(L, Possibilités[k], k, indice)) * ptg[k] for k in range(
                    len(resteglobal))]  # hérédité: produit de l'indice de favorabilité de chaque situation par la probabilité qu'elle arrive
                Chances[c] = sum(Prb)  # somme des indices
        return sum(Chances)
