# from Tarot_Africain import *
import TA_Bots as bot
import random
import copy


class Joueur:
    """
    Classe Joueur
    =====================
    Attributs:
        nom: string
        cartes: list
        points: int
    """

    def __init__(self, cartes, nbjoueurs, nom):
        """
        Constructeur de la classe Joueur
        =====================
        :param cartes: cartes du joueur
        :param nbjoueurs: nombre de joueurs
        :param nom: nom du joueur et son type (humain / bot)
        """
        self.statut = nom[1]
        self.cartes = cartes
        self.nbjoueurs = nbjoueurs
        self.nom = nom[0]
        self.nbcartes = len(self.cartes)

    def pari2(self, parisprécédents, nbcartes, indice=None):
        nbparis = 0
        for k in parisprécédents:
            if k != -1:
                nbparis += 1
        volonté = 0
        for k in range(self.nbcartes):
            if self.cartes[k] == 'atout':
                volonté += 14
            else:
                volonté += self.cartes[k]
        volonté = int(volonté / (10 * self.nbcartes))
        volonté = min(max(0, volonté), self.nbcartes)
        if nbparis == self.nbjoueurs - 1 and sum(parisprécédents) + volonté + 1 == self.nbcartes:
            volonté += [-1, 1][random.randint(0, 1)]
            if volonté == -1:
                volonté += 2
            if volonté > self.nbcartes:
                volonté -= 2
        return volonté

    def choixcartes2(self, dejapresent, paris, pointsterrains, cartesautresjoueurs, indice, nombredecartes, pari,
                     debut):
        n = len(self.cartes)
        cartechoisi = self.cartes[random.randint(0, n - 1)]
        self.cartes.remove(cartechoisi)
        if cartechoisi == 'atout':
            cartechoisi = ['atout', 'maxi']
        return cartechoisi


class JoueurHumain(Joueur):
    """
    Joueur Humain
    =====================
    Attributs:
        - cartes: main courante du joueur
        - nbjoueurs: nombre de joueurs
        - nom: nom du joueur
    """

    def __init__(self, cartes, nbjoueurs, nom):
        """ Joueur humain
        :param cartes: Cartes du joueur
        :param nbjoueurs: nombre de joueurs
        :param nom: nom du joueur
        """
        super().__init__(cartes, nbjoueurs, nom)

    def pari2(self, parisprécédents, cartesjoueurs, indice=None):
        """ Pari du joueur humain
        :param parisprécédents: paris déjà placés par les joueurs
        :param cartesjoueurs:
        :return: pari du joueur
        """
        nbcartes = len(cartesjoueurs[0])
        if nbcartes != 1:
            print("Vos cartes sont:", self.cartes)
            print("Les autres joueurs ont parié (-1= pas encore parié):", parisprécédents)
            bet = -1
            while bet < 0 or bet > len(cartesjoueurs[0]):
                msg = f"Votre pari (0 à {len(cartesjoueurs[0])}) ? >> "
                bet = int(input(msg))
            if parisprécédents.count(-1) == 1:  # conditions seulement si dernier joueur
                while bet + sum(parisprécédents) + 1 == nbcartes or bet < 0 or bet > len(cartesjoueurs[0]):
                    print("Vous ne pouvez pas placer ce pari.")
                    bet = int(input(msg))
            return int(bet)
        else:
            print('Les cartes que vous voyez sur le front des autres joueurs sont:',
                  [cartesjoueurs[k] for k in range(1, len(cartesjoueurs))])
            msg = f"Votre pari (0 à {len(cartesjoueurs[0])}) ? >> "
            bet = input(msg)
            if parisprécédents.count(-1) == 1:  # conditions seulement si dernier joueur
                while bet + sum(parisprécédents) + 1 == nbcartes:
                    print("Vous ne pouvez pas placer ce pari.")
                    bet = input(msg)
            return int(bet)

    def choixcartes2(self, dejapresent, paris, pointsterrains, cartesautresjoueurs, indice, nombredecartes, pari,
                     debut):
        """
        Choix des cartes du joueur humain
        =====================
        :param dejapresent: cartes déjà posées
        :type dejapresent: list
        :param paris: paris placés par les joueurs
        :type paris: list
        :param pointsterrains: points sur le terrain
        :type pointsterrains: int
        :return: la carte choisie par le joueur
        """
        n = len(self.cartes)
        if self.nbcartes != 1:
            # print(f"Cartes posées : {dejapresent}")
            selection = input(f"Votre main : {self.cartes}. Que voulez-vous jouer ? >> ")
            if selection == 'atout':
                choix = ''
                while choix not in ['mini', 'maxi']:
                    choix = input("Vous posez l'excuse. Quelle est sa valeur ? (mini ou maxi) >> ")
                self.cartes.remove(selection)
                return ['atout', choix]

            if int(selection) in self.cartes or selection == 'atout' and 'atout' in self.cartes:

                self.cartes.remove(int(selection))
                return int(selection)
            else:
                print("Vous ne pouvez pas jouer cette carte.")
                return self.choixcartes2(dejapresent, paris, pointsterrains, cartesautresjoueurs, indice,
                                         nombredecartes, pari,
                                         debut)

        else:
            if self.cartes[0] == 'atout':
                choix = ''
                while choix not in ['mini', 'maxi']:
                    choix = input("Vous posez l'excuse. Quelle est sa valeur ? (mini ou maxi) >> ")
                self.cartes.remove(choix)
                return ['atout', choix]
            print(self.cartes[0])
            return self.cartes[0]


class JoueurBot(Joueur):
    """
    Joueur machine
    =====================
    Attributs :
        - cartes : liste des cartes du bot
        - nbjoueurs : nombre de joueurs
        - nom : nom du bot
    """

    def __init__(self, cartes, nbjoueurs, nom):
        super().__init__(cartes, nbjoueurs, nom)

    def pari2(self, parisprécédents, cartesautrejoueurs, indice):
        """
        Pari du joueur bot
        =====================
        :param parisprécédents: Paris déjà placés par les joueurs
        :type parisprécédents: list
        :param cartesautrejoueurs: Cartes des autres joueurs
        :type cartesautrejoueurs: list
        :param indice:
        :return: Pari du bot
        """
        if len(self.cartes) == 1:
            c = copy.deepcopy(cartesautrejoueurs)
            c.remove(c[indice])
            P = bot.Pari1Carte(parisprécédents, c)
            return P.pari()
        else:
            P = bot.PariMCartes(parisprécédents, self.cartes)
            return P.pari()

    def choixcartes2(self, dejapresent, paris, pointsterrains, cartesautresjoueurs, indice, nombredecartes, pari,
                     debut):
        """
        Choix des cartes du joueur bot
        :param dejapresent: Cartes déjà posées
        :type dejapresent: list
        :param paris: Paris placés par les joueurs
        :type paris: list[int]
        :param pointsterrains: Points sur le terrain
        :type pointsterrains: int
        :param cartesautresjoueurs: Cartes des autres joueurs
        :type cartesautresjoueurs: list
        :param indice: ??
        :type indice: ?
        :param nombredecartes: Nombre de cartes en main
        :type nombredecartes: int
        :param pari: Pari du bot
        :type pari: int
        :param debut: ??
        :return: Carte jouée par le bot
        """
        if nombredecartes == 1:
            C = bot.Choix1Carte(self.cartes[0], pari)
            choix = C.choix()
        else:
            C = bot.ChoixMCartes(self.cartes, paris, dejapresent, pointsterrains, indice, debut)
            choix = C.choix()
        print(choix)
        if choix == ['atout', 'maxi'] or choix == ['atout', 'mini']:
            self.cartes.remove('atout')
        else:
            self.cartes.remove(choix)
        return choix
