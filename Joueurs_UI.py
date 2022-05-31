# -*- coding: utf-8 -*- Line 2
# ----------------------------------------------------------------------------
# Created By  : DIAS, PREVOST
# Created Date: 2022-04-02
# version ='1.0'
# ---------------------------------------------------------------------------
# Description : Module implémentant les joueurs de tarot africain

import TA_Bots as bot
import random
import copy
import abc
from IHM import *


class Joueur(metaclass=abc.ABCMeta):
    """
    Classe générique définissant un joueur
    """

    def __init__(self, cartes, nbjoueurs, nom,vies):
        """ Joueur générique de tarot africain. Il joue aléatoirement.
        :param cartes: cartes du joueur
        :param nbjoueurs: nombre de joueurs
        :param nom: nom du joueur et son type (humain / bot)
        """
        self.statut = nom[1]
        self.cartes = cartes
        self.nbjoueurs = nbjoueurs
        self.nom = nom[0]
        self.nbcartes = len(self.cartes)
        self.vies=vies

    @abc.abstractmethod
    def pari2(self, parisprécédents, cartesjoueurs, indice):
        pass

    @abc.abstractmethod
    def choixcartes2(self, dejapresent, paris, pointsterrains, cartesautresjoueurs, indice, nombredecartes, pari,
                     debut):
        pass


class JoueurHumain(Joueur):
    """ Joueur Humain de tarot africain. Il demande chaque pari et chaque coup à l'utilisateur.
        Attributs:
            - cartes: main courante du joueur
            - nbjoueurs: nombre de joueurs
            - nom: nom du joueur
        """

    def __init__(self, cartes, nbjoueurs, nom,vies):
        """ Joueur humain
        :param cartes: Cartes du joueur
        :param nbjoueurs: nombre de joueurs
        :param nom: nom du joueur
        """
        super().__init__(cartes, nbjoueurs, nom,vies)

    def pari2(self, parisprécédents, cartesjoueurs, indice=None):
        """ Pari du joueur humain
        :param parisprécédents: paris déjà placés par les joueurs
        :param cartesjoueurs:
        :return: pari du joueur
        """

        nbcartes = len(cartesjoueurs[0])
        if nbcartes != 1:
            bet=-1
            while bet==-1:
                bet=pari(cartesjoueurs,parisprécédents,self.vies)

                if parisprécédents.count(-1) == 1:  # conditions seulement si dernier joueur
                    if bet + sum(parisprécédents) + 1 == nbcartes or bet < 0 or bet > len(cartesjoueurs[0]):
                        bet=-1
            return int(bet)


        else:
            bet = -1
            while bet == -1:
                print(cartesjoueurs)
                bet = pari1carte(cartesjoueurs, parisprécédents, self.vies)

                if parisprécédents.count(-1) == 1:  # conditions seulement si dernier joueur
                    while bet + sum(parisprécédents) + 1 == nbcartes or bet < 0 or bet > len(cartesjoueurs[0]):
                        bet = -1

            return int(bet)


    def choixcartes2(self, dejapresent, paris, pointsterrains, cartesautresjoueurs, indice, nombredecartes, pari,
                     debut):
        """ Choix des cartes du joueur humain
        :param dejapresent: cartes déjà posées
        :param paris: paris placés par les joueurs
        :param pointsterrains: points sur le terrain
        :type dejapresent: list
        :type paris: list
        :type pointsterrains: list
        :return: la carte choisie par le joueur
        """

        if self.nbcartes != 1:

            selection=terrain([self.cartes],dejapresent,paris,pointsterrains,self.vies)

            if selection == 22:
                choix = minmax()
                print(self.cartes)
                self.cartes.remove("atout")
                return ['atout', choix]

            else:
                self.cartes.remove(int(selection))
                return int(selection)

        else:
            if self.cartes[0] == "atout":
                choix = minmax()
                print(self.cartes)
                self.cartes.remove("atout")
                return ['atout', choix]
            return self.cartes[0]




class JoueurBot(Joueur):
    """ Joueur machine calculant ses coups récursivement
       Attributs :
           - cartes : liste des cartes du bot
           - nbjoueurs : nombre de joueurs
           - nom : nom du bot
       """

    def __init__(self, cartes, nbjoueurs, nom,vies):
        super().__init__(cartes, nbjoueurs, nom,vies)

    def pari2(self, parisprécédents, cartesautrejoueurs, indice):
        """ Pari du joueur bot
        :param parisprécédents: Paris déjà placés par les joueurs
        :param cartesautrejoueurs: Cartes des autres joueurs (jeu à une carte)
        :param indice: position du bot dans la manche
        :type parisprécédents: list
        :type cartesautrejoueurs: list
        :type indice: int
        :return: Pari du bot
        """
        if len(self.cartes) == 1:
            c = copy.deepcopy(cartesautrejoueurs)
            c.remove(c[indice])
            P = bot.pari1Carte(parisprécédents, c)
        else:
            P = bot.PariMCartes(parisprécédents, self.cartes)
        return(P)


    def choixcartes2(self, dejapresent, paris, pointsterrains, cartesautresjoueurs, indice, nombredecartes, pari,
                     debut):
        """Choix des cartes du joueur bot
        :param dejapresent: Cartes déjà posées
        :param paris: Paris placés par les joueurs
        :param pointsterrains: Points sur le terrain
        :param cartesautresjoueurs: Cartes des autres joueurs (jeu 1 carte)
        :param indice: Position du bot dans la manche
        :param nombredecartes: Nombre de cartes en main
        :param pari: Pari du bot
        :param debut: Position du joueur qui parie en premier
        :type dejapresent: list
        :type paris: list
        :type pointsterrains: list
        :type cartesautresjoueurs: list
        :type indice: int
        :type nombredecartes: int
        :type pari: int
        :type debut: int
        :return: Carte jouée par le bot
        """
        if nombredecartes == 1:
            choix = bot.Choix1Carte(self.cartes[0], pari)
        else:
            choix = bot.ChoixMCartes(self.cartes, paris, dejapresent, pointsterrains, indice, debut)
        print(choix)
        if choix == ['atout', 'maxi'] or choix == ['atout', 'mini']:
            self.cartes.remove('atout')
        else:
            self.cartes.remove(choix)
        return choix
