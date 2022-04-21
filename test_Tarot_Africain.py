import copy
import unittest

from Tarot_Africain import *


class Test_Tarot_Africain(unittest.TestCase):
    def testcohérenceattributioncartes(self):
        for nombredejoueurs in range(2, 5):
            for nombredecartes in range(1, 5):
                for nombredetests in range(20):
                    N = [[str(k), 'bot'] for k in range(nombredejoueurs)]
                    M = Manche(N, nombredecartes, 0, Log([]), False)
                    L = []
                    for joueur in M.joueurs:
                        for k in joueur.cartes:
                            L.append(k)
                    coh = True
                    LP = []
                    for k in L:
                        if k not in LP:
                            LP.append(k)
                        elif k in LP:
                            coh = False
                    self.assertTrue(coh)

    def testcohérencespari(self):
        for nombredejoueurs in range(2, 5):
            for nombredecartes in range(1, 5):
                for nombredetests in range(20):
                    N = [[str(k), 'bot'] for k in range(nombredejoueurs)]
                    M = Manche(N, nombredecartes, 0, [[]], False)
                    L = M.paris()
                    self.assertNotEqual(sum(L), nombredecartes)
                    for k in L:
                        self.assertTrue(k >= 0)
                        self.assertTrue(k <= nombredecartes)

    def testcohérencetour(self):
        for nombredejoueurs in range(2, 5):
            for nombredecartes in range(1, 5):
                for nombredetests in range(20):
                    N = [[str(k), 'bot'] for k in range(nombredejoueurs)]
                    M = Manche(N, nombredecartes, 0, [[0]], False)
                    cartes = copy.deepcopy(M.cartesjoueurs)
                    M.jeu()
                    a = M.log
                    for tour in a[0][2]:
                        for carte in range(len(tour)):
                            if tour[carte] == ['atout', 'maxi'] or tour[carte] == ['atout', 'mini']:
                                if not ('atout' in cartes[carte]):
                                    self.assertTrue('atout' in cartes[carte])
                            else:
                                if not tour[carte] in cartes[carte]:
                                    self.assertTrue(tour[carte] in cartes[carte])

    def testpertespoints(self):  # TODO: le faire marcher
        for nombredejoueurs in range(2, 5):
            for nombredecartes in range(1, 5):
                for nombredetests in range(20):
                    N = [[str(k), 'bot'] for k in range(nombredejoueurs)]
                    M = Manche(N, nombredecartes, 0, Log([[]]), False)
                    P = M.jeu()
                    self.assertNotEqual(P, [0] * len(P))


if __name__ == '__main__':
    unittest.main()
