from Tarot_Africain import *


class Joueur:
    def __init__(self, cartes, nbjoueurs, nom):
        self.isBot = nom[1] == 'bot'
        self.cartes = cartes
        self.nbjoueurs = nbjoueurs
        self.nom = nom[0]
        self.nbcartes = len(self.cartes)

    def pari(self, parisprécédents):
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
        return (volonté)

    def choixcartes(self, dejapresent, paris, pointsterrains):
        n = len(self.cartes)
        cartechoisi = self.cartes[random.randint(0, n - 1)]
        self.cartes.remove(cartechoisi)
        if cartechoisi == 'atout':
            cartechoisi = ['atout', 'maxi']
        return (cartechoisi)


class JoueurHumain(Joueur):
    def __init__(self, carte, nbjoueurs, nom, cartes):
        super().__init__(carte, nbjoueurs, nom)

    def choixcartes(self, dejapresent, paris, pointsterrains):
        n = len(self.cartes)
        print(f"État du jeu : {self.nbjoueurs} joueurs, {len(dejapresent)} cartes deja présentes, {paris} pariés, "
              f"{pointsterrains} points de terrain")
        selection = ""
        while selection != maxi(dejapresent + [selection]) or selection != 'atout':
            selection = input(f"Votre main : {self.cartes}. Que voulez-vous jouer ?")
        self.cartes.remove(selection)
        return selection
