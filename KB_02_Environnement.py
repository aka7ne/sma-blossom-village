"""
Auteur : Bouguima Kawthar 22303487
Création : 03/10/2025
Contenu : Classe Environnement
"""
#Modification le .... : Ajout du système de phéromones
#Modification le 09/11/2025 : Ajout d'une méthode permettant un rayon de vision
#Modification le 15/11/2025 : Ajout d'une méthode retournant les positions non occupée pour generer les positions libre
import time

class Environnement:
    def __init__(self, width, height):
        """
        width (int) : largeur
        height (int) : hauteur
        """
        self.width = width
        self.height = height
        self.agents = []
        self.obstacles = [] 
        self.places = []
        self.pheromones = {
            'happy': [[0.0 for _ in range(self.width)] for _ in range(self.height)],
            'sad':   [[0.0 for _ in range(self.width)] for _ in range(self.height)]
        }

    def add_agent(self, agent):
        """
        Rôle : Ajoute un agent à l'environnement
        Données : agent (Agent) : un objet de type Agent
        Préconditions : agent doit être une instance valide de Agent
        Résultat : agent est ajouté a self.agents
        """
        self.agents.append(agent)

    def add_obstacle(self, x, y):
        """
        Rôle : Ajoute un obstacle à la grille.
        Données :
            x, y : coordonnées de l'obstacle dans la grille logique (entiers).
        Préconditions :
            0 <= x < self.width, 0 <= y < self.height
        Résultat :
            (x, y) est ajouté à self.obstacles.
        """
        col = int(x)
        row = int(y)
        if 0 <= col < self.width and 0 <= row < self.height:
            if (col, row) not in self.obstacles:
                self.obstacles.append((col, row))

        
    def is_obstacle(self, x, y):
        """
        Rôle : renvoie True si (x,y) correspond à un obstacle.
        IMPORTANT : arrondi pour supporter le A* continu.
        """
        col = int(round(x))
        row = int(round(y))

        if 0 <= col < self.width and 0 <= row < self.height:
            return (col, row) in self.obstacles

        return True

    def position_valide(self, x, y, positions_occupees=None):
        """
        Rôle : Vérifie si un agent peut occuper la position (x, y).

        Données :
            x, y : coordonnées continues
            positions_occupees : liste de couples (x,y) d'autres agents (floats)

        Résultat :
            True si la case n'est pas un obstacle et n'est pas déjà occupée.
        """
        col = int(round(x))
        row = int(round(y))

        # vérifier occupation par d'autres agents
        if positions_occupees:
            for (px, py) in positions_occupees:
                pc = int(round(px))
                pr = int(round(py))
                if pc == col and pr == row:
                    return False

        # vérifier obstacle
        if self.is_obstacle(col, row):
            return False

        return True


    def add_place(self, x, y):
        """
        Rôle : Ajoute un lieu (maison, parc, magasin) à l'environnement
        Données : x (float), y (float) : coordonnées du lieu
        Préconditions : (x, y) doit être dans les dimensions de la grille
        Résultat : la position (x, y) est ajoutée à self.places
        """
        self.places.append((float(x), float(y)))

    def display(self, step=0):
        """
        Rôle : Affiche les positions des agents
        Résultat : affichage console 
        """
        print(f"\n--- Étape {step} ---")
        for a in self.agents:
            print(f"{a.name} ({a.etat}, {a.humeur}) → ({a.x:.2f}, {a.y:.2f})")

    def add_pheromone(self, kind, x, y, amount=0.5):
        """
        Rôle : Ajoute de la phéromone d'un type à la cellule correspondante.
        Données : kind (str) : 'happy' ou 'sad'
                  x, y (float) : coordonnées continues
                  amount (float) : quantité ajoutée
        Préconditions : kind doit être géré ('happy'/'sad')
        Résultat : la grille pheromones[kind][row][col] est augmentée
        """
        if kind not in self.pheromones:
            return
        col = int(round(x))
        row = int(round(y))
        if 0 <= row < self.height and 0 <= col < self.width:
            self.pheromones[kind][row][col] += float(amount)
  

    def evaporate_pheromones(self, rate=0.9, threshold=0.01):
        """
        Rôle : Evapore (diminue) les phéromones de toutes les cellules.
        Données : rate (float) coefficient multiplicatif <1, threshold (float) valeur min
        Préconditions : les grilles de pheromones sont initialisées
        Résultat : mise à jour en place des grilles
        """
        for kind in self.pheromones:
            grid = self.pheromones[kind]
            for r in range(self.height):
                for c in range(self.width):
                    grid[r][c] *= rate
                    if grid[r][c] < threshold:
                        grid[r][c] = 0.0

    def tour_complet(self):
        """
        Rôle : Attend que tous les agents aient joué leur tour, effectue nettoyage/évaporation et réinitialise les flags.
        Données : utilise self.agents
        Préconditions : self.agents contient les threads Agent en cours d'exécution
        Résultat : retourne quand tous ont joué ; réinitialise a_joue à False pour le next tour
        """
        while not all(a.a_joue for a in self.agents):
            time.sleep(0.02)
        self.evaporate_pheromones(rate=0.92)
        for a in self.agents:
            a.a_joue = False