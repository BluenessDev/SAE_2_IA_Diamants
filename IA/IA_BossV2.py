##############################################################################
# votre IA : à vous de coder
# Rappel : ne pas changer les paramètres des méthodes
# vous pouvez ajouter librement méthodes, fonctions, champs, ...
##############################################################################

from random import *


class IA_Diamant:
    def __init__(self, match : str):
        """génère l'objet de la classe IA_Diamant

        Args:
            match (str): decriptif de la partie
        """
        description_partie = match.split('|')
        self.nom_IA = description_partie[2].split(',')
        description_partie.pop(2)
        self.nombre_IA = description_partie[1]
        description_partie.pop(1)
        place_de_notre_IA = description_partie[1]
        description_partie.pop(1)
        nombre_manches = description_partie[0]
        self.coffres_IA = [0] * int(self.nombre_IA)
        print(self.nom_IA)
        print(self.nombre_IA)
        print(place_de_notre_IA)
        print(nombre_manches)
        self.cartes_manche_en_cours_sans_y_toucher = []
        self.cartes_manche_en_cours = []
        self.numero_manche = 0
        self.rubis_manche_en_cours = 0
        self.pioche = [1, 2, 3, 4, 5, 5, 7, 7, 9, 11, 11, 13, 14, 15, 17, "P1", "P1", "P1", "P2",
                  "P2", "P2", "P3", "P3", "P3", "P4", "P4", "P4", "P5", "P5",
                  "P5", "R"]
        self.IA_rentre = 0

    def action(self, tour : str) -> str:
        """Appelé à chaque décision du joueur IA

        Args:
            tour (str): descriptif du dernier tour de jeu

        Returns:
            str: 'X' ou 'R'
        """
        action_carte = tour.split('|')
        action_IA = action_carte[0].split(',')
        carte_de_ce_tour = action_carte[1]
        print(action_IA)
        print(self.cartes_manche_en_cours)
        for i in action_IA:
            if i == "R":
                self.IA_rentre += 1
        if carte_de_ce_tour == "R":
            self.pioche.remove("R")
        if carte_de_ce_tour not in ["P1", "P2", "P3", "P4", "P5", "R"]:
            carte_de_ce_tour = int(carte_de_ce_tour)
            self.cartes_manche_en_cours_sans_y_toucher.append(carte_de_ce_tour)
            self.rubis_manche_en_cours += carte_de_ce_tour // int(self.nombre_IA)
            self.cartes_manche_en_cours.append(carte_de_ce_tour // int(self.nombre_IA))
        else:
            self.cartes_manche_en_cours_sans_y_toucher.append(carte_de_ce_tour)
            self.cartes_manche_en_cours.append(carte_de_ce_tour)
        if 'R' in action_IA:
            self.retour_IA(self.coffres_IA, action_IA.count('R'), action_IA, self.rubis_manche_en_cours, self.cartes_manche_en_cours, self.nombre_IA)

        if len(self.cartes_manche_en_cours_sans_y_toucher) <= 1:
            return "X"
        indice_dangerosite_tour = self.indice_dangerosite(self.cartes_manche_en_cours_sans_y_toucher)
        indice_rentabilite_a_rester_tour = self.indice_rentabilite_a_rester()
        indice_rentabilite_a_rentrer_tour = self.indice_rentabilite_a_rentrer()
        indice_total = ((indice_dangerosite_tour * 6 + indice_rentabilite_a_rentrer_tour * 2)// (62 - int(self.nombre_IA) * 7))
        # on fait un random number et si c'est supérieur on continue et si c'est inferieur, on rentre
        x = randint(0, 100)
        if x < indice_total :
            return "R"
        else:
            return "X"


    def indice_dangerosite(self, cartes_manche_en_cours_sans_y_toucher):
        """
        fonction qui renvoie un indice qui est un nombre entre 1 et 1000, selon la probabilité que la prochaine carte
        retournée soit un piège mettant fin à la manche.
        entrée: list
        sortie: int
        """
        nb_P1 = 0
        nb_P2 = 0
        nb_P3 = 0
        nb_P4 = 0
        nb_P5 = 0
        nb_P1_pioche = self.pioche.count("P1") - 1
        nb_P2_pioche = self.pioche.count("P2") - 1
        nb_P3_pioche = self.pioche.count("P3") - 1
        nb_P4_pioche = self.pioche.count("P4") - 1
        nb_P5_pioche = self.pioche.count("P5") - 1
        for i in range(len(cartes_manche_en_cours_sans_y_toucher)):
            if cartes_manche_en_cours_sans_y_toucher[i] == "P1":
                nb_P1 += 1
            elif cartes_manche_en_cours_sans_y_toucher[i] == "P2":
                nb_P2 += 1
            elif cartes_manche_en_cours_sans_y_toucher[i] == "P3":
                nb_P3 += 1
            elif cartes_manche_en_cours_sans_y_toucher[i] == "P4":
                nb_P4 += 1
            elif cartes_manche_en_cours_sans_y_toucher[i] == "P5":
                nb_P5 += 1
        calcul = (nb_P1 * nb_P1_pioche + nb_P2 * nb_P2_pioche + nb_P3 * nb_P3_pioche + nb_P4 * nb_P4_pioche + nb_P5 * nb_P5_pioche) / (len(self.pioche) - len(cartes_manche_en_cours_sans_y_toucher))
        proba = round(calcul * 1000)
        print("-------------------------------------")
        print(proba)
        return proba

    def indice_rentabilite_a_rester(self):
        """
        fonction qui determine la rentabilité de rester la manche suivante selon le nombre de rubis à gagner selon les cartes
        retournees.
        entree : list
        sortie : int(entre 1 et 1000)
        """
        nombre_total_rubis_pioche_restant = 0
        nombre_cartes_rubis_pioche_restant = 0
        for i in self.pioche:
            if type(i) == int:
                nombre_cartes_rubis_pioche_restant += 1
                nombre_total_rubis_pioche_restant += i
        for j in self.cartes_manche_en_cours_sans_y_toucher:
            if type(j) == int:
                nombre_total_rubis_pioche_restant -= j
                nombre_cartes_rubis_pioche_restant -= 1
        nombre_moyen_rubis_retournes_prochaine_manche = nombre_cartes_rubis_pioche_restant * nombre_total_rubis_pioche_restant / len(self.pioche)
        return round(nombre_moyen_rubis_retournes_prochaine_manche * 10) / (int(self.nombre_IA) - self.IA_rentre)

    def indice_rentabilite_a_rentrer(self):
        """
        fonction qui determine la rentabilité de rentrer la manche suivante selon le nombre de rubis a gagner selon les cartes
        retournees
        entree : list
        sortie : int(entre 1 et 1000)
        """
        nb_total_rubis_retour = 0
        nb_relique_retour = 0
        for i in self.cartes_manche_en_cours:
            if type(i) == int:
                nb_total_rubis_retour += i
            elif i == "R" and self.numero_manche < 4:
                nb_relique_retour += 1
            elif i == "R":
                nb_relique_retour += 1
        proba = nb_relique_retour * 100 + nb_total_rubis_retour * 20
        return proba

    def retour_IA(self, coffres_IA, nb_qui_rentre, action_IA, rubis_manche_en_cours, cartes_manche_en_cours, nombre_IA):
        """
        fonction qui simule le retour des IA du jeu, afin de savoir le nombre de rubis de chaque IA au cours de la partie
        entrée: list, int, list, int, list, int
        sortie: rien (la fonction modifie directement la liste coffres_IA)
        """
        if nb_qui_rentre == 1:
            coffres_IA[action_IA.index('R')] += rubis_manche_en_cours
            for i in range(len(cartes_manche_en_cours)):
                if cartes_manche_en_cours[i] not in ["P1", "P2", "P3", "P4", "P5", "R"]:
                    coffres_IA[action_IA.index('R')] += int(cartes_manche_en_cours[i])
                    cartes_manche_en_cours[i] = 0
                elif cartes_manche_en_cours[i] == 'R':
                    if self.numero_manche < 4:
                        coffres_IA[action_IA.index('R')] += 5
                    else:
                        coffres_IA[action_IA.index('R')] += 10
        else:
            for h in range(int(nombre_IA)):
                if action_IA[h] == 'R':
                    coffres_IA[h] += rubis_manche_en_cours
                    for i in range(len(cartes_manche_en_cours)):
                        if cartes_manche_en_cours[i] not in ["P1", "P2", "P3", "P4", "P5", "R"]:
                            coffres_IA[h] += int(cartes_manche_en_cours[i]) // action_IA.count('R')
            for k in range(len(cartes_manche_en_cours)):
                if type(cartes_manche_en_cours[k]) == int:
                    cartes_manche_en_cours[k] = cartes_manche_en_cours[k] % action_IA.count('R')

    def fin_de_manche(self, raison : str, dernier_tour : str) -> None:
        """Appelé à chaque fin de manche

        Args:
            raison (str): 'R' si tout le monde est un piège ou "P1","P2",... si un piège a été déclenché
            dernier_tour (str): descriptif du dernier tour de la manche
        """
        self.cartes_manche_en_cours = []
        self.cartes_manche_en_cours_sans_y_toucher = []
        self.numero_manche += 1
        self.rubis_manche_en_cours = 0
        self.pioche.append("R")
        self.IA_rentre = 0
        if raison in ["P1", "P2", "P3", "P4", "P5"]:
            self.pioche.remove(raison)

    def game_over(self, scores : str) -> None:
        """Appelé à la fin du jeu ; sert à ce que vous voulez

        Args:
            scores (str): descriptif des scores de fin de jeu
        """
        pass