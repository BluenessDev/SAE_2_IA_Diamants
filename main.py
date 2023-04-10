##############################################################################
# main                                                                       #
##############################################################################

# Dans ce fichier que vous pouvez compléter vous lancez vos expérimentations

from moteur_diamant import partie_diamant


def testNormal(nbPartie, joueur):
    """
    Renvoie un pourcentage selon le nombre de partie gagnee par joueur
    Parametres : 'nbPartie' un int, 'joueur' une liste
    Renvoi : Pourcentage de victoire par joueur, un str
    """
    nbPartiesGagnees = {x: 0 for x in joueur}

    for i in range(nbPartie):
        score = partie_diamant(5, joueur)
        gagnant = score.index(max(score))
        nbPartiesGagnees[joueur[gagnant]] += 1

    for i in range(len(joueur)):
        disScore = str(round(((nbPartiesGagnees[joueur[i]] / nbPartie) * 100), 2)) + "%"
        print(joueur[i], ":", disScore)

    print("Le score de tous les joueurs :", nbPartiesGagnees)

if __name__ == '__main__':
    testNormal(2000,['IA_BossV2', 'IA_temeraire', 'IA_aleatoire', 'IA_trouillarde'])
