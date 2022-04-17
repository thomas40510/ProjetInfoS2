# from Tarot_Africain import *
import TA_Bots as bot
import random
import copy


class Joueur:
    # def __init__(self, cartes, nbjoueurs, nom):
    #     self.isBot = nom[1] == 'bot'
    #     self.cartes = cartes
    #     self.nbjoueurs = nbjoueurs
    #     self.nom = nom[0]
    #     self.nbcartes = len(self.cartes)
    #
    def __init__(self, cartes, nbjoueurs, nom):
        self.statut = nom[1]
        self.cartes = cartes
        self.nbjoueurs = nbjoueurs
        self.nom = nom[0]
        self.nbcartes = len(self.cartes)

    def pari2(self, parisprécédents, nbcartes, paris):
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
    def __init__(self, cartes, nbjoueurs, nom):
        super().__init__(cartes, nbjoueurs, nom)

    def choixcartes2(self, dejapresent, paris, pointsterrains):
        n = len(self.cartes)
        print(f"État du jeu : {self.nbjoueurs} joueurs, {len(dejapresent)} cartes déjà présentes, {paris} paris, "
              f"pour un total de {pointsterrains} points.")
        selection = input(f"Votre main : {self.cartes}. Que voulez-vous jouer ?")
        if self.nbcartes != 1:
            print(f"Cartes posées : {dejapresent}")
            if max(self.cartes) >= max(dejapresent + [selection]) and 'atout' not in self.cartes:
                while selection != max(dejapresent + [selection]) or selection != 'atout':
                    print("Vous ne pouvez pas jouer cette carte. Vous devez jouer une carte plus forte "
                          "que celles posées, ou l'excuse.")
                    selection = input(f"Votre main : {self.cartes}. Que voulez-vous jouer ?")
                self.cartes.remove(selection)
        return selection

    def pari2(self, parisprécédents, nbcartes, paris):
        msg = f"Votre pari (0 à {nbcartes}) ? >> "
        bet = input(msg)
        if self.nbjoueurs - 1 == len(parisprécédents):  # conditions seulement si dernier joueur
            while bet + sum(paris) == nbcartes:
                print("Vous ne pouvez pas placer ce pari.")
                bet = input(msg)


class JoueurBot(Joueur):
    def __init__(self, cartes, nbjoueurs, nom):
        super().__init__(cartes, nbjoueurs, nom)

    def choixcartes2(self, dejapresent, paris, pointsterrains, cartesautresjoueurs, indice, nombredecartes, pari,
                     debut):
        if nombredecartes == 1:
            C = bot.Choix1Carte(self.cartes[0], pari)
            choix = C.choix()
        else:
            C = bot.ChoixMCartes(self.cartes, paris, dejapresent, pointsterrains, indice, debut)
            choix = C.choix()
        print(self.cartes, choix)
        if choix == ['atout', 'maxi'] or choix == ['atout', 'mini']:
            self.cartes.remove('atout')
        else:
            self.cartes.remove(choix)
        return choix

    def pari2(self, parisprécédents, cartesautrejoueurs, indice):
        if len(self.cartes) == 1:
            c = copy.deepcopy(cartesautrejoueurs)
            c.remove(c[indice])
            P = bot.Pari1Carte(parisprécédents, c)
            return P.pari()
        else:
            P = bot.PariMCartes(parisprécédents, self.cartes)
            return P.pari()
        # else:
        #     if len(self.cartes) == 1:
        #         c = copy.deepcopy(cartesautrejoueurs)
        #         c.remove(c[indice])
        #         J = joueurs.JoueurHumain(self.cartes, self.nbjoueurs, self.nom)
        #         return J.pari(parisprécédents, c)
        #     else:
        #         J = joueurs.JoueurHumain(self.cartes, self.nbjoueurs, self.nom)
        #         return J.pari(parisprécédents, cartesautrejoueurs)
