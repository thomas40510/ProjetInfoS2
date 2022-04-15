import unittest

from Tarot_Africain import *


class Test_Tarot_Africain(unittest.TestCase):
    def testcohérenceattributioncartes(self):
        for nombredejoueurs in range(2,5):
            for nombredecartes in range(1,5):
                for nombredetests in range(20):
                    N=[[str(k),str(k)] for k in range(nombredejoueurs)]
                    M=Manche(N,nombredecartes,0,False)
                    L=[]
                    for joueur in M.joueurs:
                        for k in joueur.cartes:
                            L.append(k)
                    coh=True
                    LP=[]
                    for k in L:
                        if k not in LP:
                            LP.append(k)
                        elif k in LP:
                            coh=False
                    self.assertTrue(coh)

    def testcohérencespari(self):
        for nombredejoueurs in range(2,5):
            for nombredecartes in range(1,5):
                for nombredetests in range(20):
                    N = [[str(k), str(k)] for k in range(nombredejoueurs)]
                    M = Manche(N, nombredecartes, 0, False)
                    L=M.paris()
                    self.assertNotEqual(sum(L),nombredecartes)
                    for k in L:
                        self.assertTrue(k >= 0)
                        self.assertTrue(k<=nombredecartes)


    def testpertespoints(self):
        for nombredejoueurs in range(2,5):
            for nombredecartes in range(1,5):
                for nombredetests in range(20):
                    N = [[str(k), str(k)] for k in range(nombredejoueurs)]
                    M = Manche(N, nombredecartes, 0, False)
                    P=M.jeu
                    self.assertNotEqual(P,[0 for k in range((nombredejoueurs))])




unittest.main()