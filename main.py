from random import randint


class Jeu:
    """
    Liste des attributs :
        -nb_carte int()-> nombre de carte dans la partie ( 32 ou 52 )
        -template list()-> contient le jeu de carte sans mélange
        -jeu_melange list()-> on mélange le paquet principale de Carte
        -joueur_1_in list()-> liste contenant les cartes du joueur 1
        -joueur_1_out list()-> liste contenant les cartes gagnées du joueur 1, ces cartes s'ajoute à la liste "in" quand celle ci est vide
        -joueur_2_in list()-> liste contenant les cartes du joueur 2
        -joueur_2_out list()-> liste contenant les cartes gagnées du joueur 2, ces cartes s'ajoute à la liste "in" quand celle ci est vide
        -stockage_temporaire list()-> liste dans laquelle sont mises les cartes joué, qui sont comparé ou gardé lors d'une "bataille"
        -end bool()-> False si la partie est en cours, True si la partie est finie
        -manches int()-> nombre de manches actuelles
        -max_manches int()-> nombre maximal de manches avant la declaration du match nul



    Liste des méthodes :
        -genlist() -> permet de générer un jeu de carte en fonction du nombre de cartes définit par l'utilisateur ( 32 ou 52 )
        -shuffle_liste() -> permet de mélanger le jeu de carte et de creer une liste de carte mélangée
        -verifj1() -> permet de vérifier si il y a des cartes dans la main du joueur 1
        -verifj2() -> permet de vérifier si il y a des cartes dans la main du joueur 2
        -reffil_j1() -> permet de remplir la liste "main" du joueur 1 avec les éléments de sa liste de cartes gagnées ("in")
        -reffil_j2() -> permet de remplir la liste "main" du joueur 2 avec les éléments de sa liste de cartes gagnées ("in")
        -fight1v1octogone() -> permet de comparer les cartes en première position du joueur 1 et 2 afin de définir qui remporte la manche
        -bataille() -> permet de s'occuper de l'instant où une "bataille" à lieu et de poursuivre la partie
        -verif_loose() -> permet de tester si un des 2 joueurs ne possède plus aucune carte
        -verifwin() -> permet de déclarer un vainqueur et mettre fin à la partie
        -match_nul() -> permet de stopper la partie si celle ci n'aboutit pas au bout d'un certain nombre de manches
        -clean() -> permet de nettoyer le stockage temporaire
    """

    def __init__(self, nb, nb_manches=10000):

        self.nb_carte = nb
        self.template = self.genlist()
        self.jeu_melange = self.shuffle_liste()
        self.joueur_1_out = self.jeu_melange[:int(len(self.jeu_melange) / 2)]
        self.joueur_1_in = []
        self.joueur_2_out = self.jeu_melange[int(len(self.jeu_melange) / 2):]
        self.joueur_2_in = []
        self.stockage_temporaire = []
        self.end = False
        self.manche = 0
        self.max_manches = nb_manches

    def genlist(self):
        if self.nb_carte == 52:
            default = 15
        elif self.nb_carte == 32:
            default = 10
        liste = []
        for symb in ["carreau", "trefle", "coeur", "pique"]:
            for val in range(2, default):
                liste.append(Carte(val, symb, self.nb_carte))
        return liste

    def shuffle_liste(self):
        liste = self.template.copy()
        liste_random = []
        for heboi in range(len(liste)):
            _rand = randint(0, len(liste) - 1)
            liste_random.append(liste[_rand]), liste.pop(_rand)
        return liste_random

    def verifj1(self):
        if self.joueur_1_out:
            return True
        return False

    def verifj2(self):
        if self.joueur_2_out:
            return True
        return False

    def reffil_j1(self):
        self.joueur_1_out += self.joueur_1_in
        self.joueur_1_in = []
        print("Le joueur 1 ajoute les cartes gagnées à sa pile de carte à jouer")

    def reffil_j2(self):
        self.joueur_2_out += self.joueur_2_in
        self.joueur_2_in = []
        print("Le joueur 2 ajoute les cartes gagnées à sa pile de carte à jouer")

    def fight1v1octogone(self):
        if self.verif_loose():
            self.verifwin()
        else:
            self.manche += 1
            if not self.verifj1(): self.reffil_j1()
            if not self.verifj2(): self.reffil_j2()
            Carte_j1 = self.joueur_1_out[0]
            Carte_j2 = self.joueur_2_out[0]
            print("{} contre {}".format(Carte_j1, Carte_j2))
            if Carte_j1 == Carte_j2:
                self.stockage_temporaire += Carte_j1, Carte_j2
                self.joueur_1_out.pop(0), self.joueur_2_out.pop(0)
                self.bataille()
                self.fight1v1octogone()

            elif Carte_j1 > Carte_j2:
                self.stockage_temporaire.append(Carte_j1), self.stockage_temporaire.append(Carte_j2)
                self.joueur_1_in += self.stockage_temporaire
                self.joueur_1_out.pop(0), self.joueur_2_out.pop(0)
                self.clean()

            elif Carte_j1 < Carte_j2:
                self.stockage_temporaire.append(Carte_j2), self.stockage_temporaire.append(Carte_j1)
                self.joueur_2_in += self.stockage_temporaire
                self.joueur_1_out.pop(0), self.joueur_2_out.pop(0)
                self.clean()

    def bataille(self):
        if self.verif_loose():
            self.verifwin()
        else:
            print("BATAILLE !!!")
            if not self.verifj1(): self.reffil_j1()
            if not self.verifj2(): self.reffil_j2()
            self.stockage_temporaire += self.joueur_1_out[0], self.joueur_2_out[0]
            self.joueur_1_out.pop(0), self.joueur_2_out.pop(0)

    def verif_loose(self):
        return (self.joueur_1_in == self.joueur_1_out) or (self.joueur_2_in == self.joueur_2_out)

    def verifwin(self):
        if not self.joueur_1_in and not self.joueur_1_out:
            with open("resulats.txt", "a") as fi:
                fi.write("le joueur 2 remporte la partie!\n")
            print("le joueur 2 remporte la partie car le le joueur 1 n'a plus de cartes !")
        elif not self.joueur_2_in and not self.joueur_2_out:
            with open("resulats.txt", "a") as fi:
                fi.write("le joueur 1 remporte la partie!\n")
            print("le joueur 1 remporte la partie car le le joueur 2 n'a plus de cartes !")
        self.end = True

    def match_nul(self):
        self.end = True
        with open("resulats.txt", "a") as fi:
            fi.write("Match nul, aucun vainqueur\n")
        print("Match nul, aucun vainqueur")

    def clean(self):
        self.stockage_temporaire = []


class Carte:
    """
    Liste des attributs :
        -valeur int()-> valeur en entier de la carte
        -symbole str()-> symbole de la carte, carreau, trefle, coeur, pique
        -nom str()-> ecrit en lettre si la carte est une dame, un roi, un as etc...

    Liste des méthodes :
        -__eq__ -> verifie si le self.valeur des deux cartes sont egales
        -__lt__ -> verifie si le self.valeur de la premiere carte est plus petit que la deuxième
        -__gt__ -> verifie si le self.valeur de la premiere carte est plus grand que la deuxième
    """

    def __init__(self, v, s, nb_carte, pregen=None):
        self.valeur = v
        self.symbole = s
        if nb_carte == 52:
            pregen = [
                "deux", "trois", "quatre", "cinq", "six", "sept", "huit",
                "neuf", "dix", "valet", "reine", "roi", "as"
            ]
        elif nb_carte == 32:
            pregen = [
                "sept", "huit", "neuf", "dix", "valet", "reine", "roi", "as"
            ]
        self.nom = pregen[self.valeur - 2]

    def __eq__(self, new):
        return self.valeur == new.valeur

    def __lt__(self, new):
        return self.valeur < new.valeur

    def __gt__(self, new):
        return self.valeur > new.valeur

    def __str__(self):
        return "{} de {}".format(self.nom, self.symbole)


nb_de_carte = input("52 ou 32 ? ")
if nb_de_carte not in ["32", "52"]:
    raise ValueError("Choissez 32 ou 52 cartes")
_Jeu = Jeu(int(nb_de_carte))
while not _Jeu.end:
    _Jeu.fight1v1octogone()
    if _Jeu.manche == _Jeu.max_manches: _Jeu.match_nul()

"""
la suite du programme permet de marquer les résultats dans un fichier resultats.txt pour sauvegarder les parties
"""
print("La partie s'est terminée en {} manches".format(_Jeu.manche))
with open("resulats.txt","a") as fi: fi.write("La partie s'est terminée en {} manches\n\n".format(_Jeu.manche))
