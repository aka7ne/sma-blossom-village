"""
Auteur : Bouguima Kawthar 22303487
Création : 03/10/2025
Contenu : Classe agent
"""
#Modification le 10/10/2025: Ajout du multi-threading
#Modification le 18/10/2025 : Ajout d'un systéme de phéromones pour orienter le déplacement (humeurs)
#Modification le 24/10/2025 par Nawelle Abdelaziz 22301791 : Correction du multi-threading (Accès concurentiel) et ajout d'un deplacement progressif
#Modification le 09/11/2025 par Younes Abbassi : Ajout de mémoire pour les agents


import threading
import random
import time
import math
from NA_02_Astar_Final import astar_continu

class Agent(threading.Thread):
    def __init__(self,name ,x, y, env):
        """
        name : nom pour id l'agent (str)
        x, y : position initiale de l'agent (float)
        env : instance d’Environnement
        """
        super().__init__()
        self.name = name
        self.x = float(x)
        self.y = float(y)
        self.env = env
        self.path = []
        self.etat = "sain" # Etat de santé initial
        self.humeur = "neutre" #Humeur initiale
        self.destination = None
        self.a_joue = False
        self.running = True
        self.vitesse = 0.2
        self.memoire = set()
        print("[INIT] Agent", self.name, "initialisé avec position (", self.x, ",", self.y, ")")

    def choix_destination(self):
        """
        Rôle : Choisit une destination au hasard parmi les lieux de l'environnement.
        Données : env : objet de type environnement
        Préconditions : environnement doit contenir au moins une place.
        Résultat : self.destination prend la valeur d'une position (x, y) aléatoire parmi env.places
        """
        if not self.env.places:
            return

        self.destination = random.choice(self.env.places)
        print(f"[DEST] {self.name} choisit destination {self.destination}")

        start = (self.x, self.y)
        goal = self.destination

        self.path = astar_continu(
            start,
            goal,
            self.env,
            agent_memoire = self.memoire)
        
        print(f"[A*] {self.name} path = {self.path}")

        for pos in self.path:
            self.memoire.add(pos)
            print("[MEMO] Agent", self.name, "mémorise position chemin", pos)

    def deplacement_progressif(self, next_pos):
        """
        Rôle : Effectue un déplacement progressif vers next_pos
        Données : next_pos : position cible 
        Préconditions : next_pos est un tuple de 2 floats
        Résultat : met a jour self.x et self.y progressivement
        """
        dx = next_pos[0] - self.x
        dy = next_pos[1] - self.y
        distance = math.hypot(dx, dy)
        
        if distance == 0:
            return
        
        speed = self.vitesse  
        
        nx = dx / distance
        ny = dy / distance
        
        self.x += nx * speed
        self.y += ny * speed
        
        self.memoire.add((round(self.x,2), round(self.y,2)))
        print(f"[MOVE] {self.name} → ({self.x:.2f}, {self.y:.2f})")

       
    def eviter_agents(self, rayon=2.0):
        """
        Rôle : Évite les agents trop proches en modifiant légèrement la direction.
        Données : rayon (float) : distance à partir de laquelle on considère une collision imminente.
        Résultat : retourne une nouvelle position (x,y) légèrement décalée ou None.
        """
        for other in self.env.agents:
            if other is self:
                continue
            dx = other.x - self.x
            dy = other.y - self.y
            dist = math.hypot(dx, dy)

            if dist < rayon:  # collision imminente
                # petit changement de direction (10°)
                angle = math.radians(10)
                nx = dx * math.cos(angle) - dy * math.sin(angle)
                ny = dx * math.sin(angle) + dy * math.cos(angle)
                return (self.x - nx * 0.3, self.y - ny * 0.3)

        return None

    def run(self):
        """
        Rôle : Boucle principale de thread
        """
        while self.running:
            if not self.path or not self.destination:
                self.choix_destination()

            if self.path:
                evit = self.eviter_agents()
                next_pos = self.path.pop(0)

                if evit:
                    next_pos = evit

                self.deplacement_progressif(next_pos)

                for other in self.env.agents:
                    if other is not self:
                        if abs(self.x - other.x) < 0.5 and abs(self.y - other.y) < 0.5:
                            self.interaction(other)

            self.deposit_pheromone_from_humeur()
            self.a_joue = True

            time.sleep(0.05)

    def interaction(self, tiers):
        """
        Rôle : Simule une interaction entre deux agents (propagation maladie/rumeur)
        Données : tiers (Agent) un agent tier avec lequel l'agent est en contact
        Préconditions : les deux agents doivent être sur la même case 
        Résultat : - si un agent est "malade" et l’autre "sain", alors le sain peut devenir malade avec 60% de probabilité
                   - si un agent est heureux alors 
        """
        if self.etat == "malade" and tiers.etat == "sain":
            if random.random() < 0.6:
                tiers.etat = "malade"
        elif tiers.etat == "malade" and self.etat == "sain":
            if random.random() < 0.6:
                self.etat = "malade"

        if self.humeur == "heureux" and tiers.humeur != "heureux":
            if random.random() < 0.3:
                tiers.humeur = "heureux"
        if self.humeur == "triste" and tiers.humeur != "triste":
            if random.random() < 0.25:
                tiers.humeur = "triste"

    def deposit_pheromone_from_humeur(self):
        """
        Rôle : Dépose des phéromones locales selon l'humeur actuelle
        Données : self.humeur et self.env
        Préconditions : env contient add_pheromone
        Résultat : la grille de phéromones de l'environnement est mise à jour
        """
        if self.humeur == "heureux":
            self.env.add_pheromone('happy', self.x, self.y, amount=0.6)
        elif self.humeur == "triste":
            self.env.add_pheromone('sad', self.x, self.y, amount=0.6)
            