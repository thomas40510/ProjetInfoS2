# -*- coding: utf-8 -*- Line 2
# ----------------------------------------------------------------------------
# Created By  : DIAS, PREVOST
# Created Date: 2022-04-02
# version ='1.0'
# ---------------------------------------------------------------------------
# Description : Module implémentant les joueurs de tarot africain
# Main author : Prévost Thomas

import TA_Bots as bot
import copy
import abc


class Joueur(metaclass=abc.ABCMeta):
    """
    Classe générique définissant un joueur
    """
    "Author : Prévost Thomas"
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
    "Author : Prévost Thomas"

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
            print("Vos cartes sont:", self.cartes)
            print("Les autres joueurs ont parié (-1= pas encore parié):", parisprécédents)
            bet = -1
            while bet < 0 or bet > len(cartesjoueurs[0]):
                msg = f"Votre pari (0 à {len(cartesjoueurs[0])}) ? >> "
                val = input(msg)
                try:
                    bet = int(val)
                except ValueError:
                    if val == 'quitter':
                        print("Merci d'avoir joué.")
                        exit(0)
                    else:
                        print("Mauvaise valeur. Merci d'entrer un pari valide.")
                        bet = -1
            if parisprécédents.count(-1) == 1:  # conditions seulement si dernier joueur
                while bet + sum(parisprécédents) + 1 == nbcartes or bet < 0 or bet > len(cartesjoueurs[0]):
                    print("Vous ne pouvez pas placer ce pari.")
                    bet = int(input(msg))
            return int(bet)


        else:
            print('Les cartes que vous voyez sur le front des autres joueurs sont:',
                  [cartesjoueurs[k] for k in range(1, len(cartesjoueurs))])
            msg = f"Votre pari (0 à {len(cartesjoueurs[0])}) ? >> "
            bet = int(input(msg))
            if parisprécédents.count(-1) == 1:  # conditions seulement si dernier joueur
                while bet + sum(parisprécédents) + 1 == nbcartes:
                    print("Vous ne pouvez pas placer ce pari.")
                    bet = input(msg)

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
                self.cartes.remove('atout')
                return ['atout', choix]
            print(self.cartes[0])
            return self.cartes[0]



class JoueurBot(Joueur):
    """ Joueur machine calculant ses coups récursivement
       Attributs :
           - cartes : liste des cartes du bot
           - nbjoueurs : nombre de joueurs
           - nom : nom du bot
       """
    "Author : Prévost Thomas"

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
