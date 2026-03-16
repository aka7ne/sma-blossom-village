"""
Auteur : Bouguima Kawthar 22303487
Création : 03/10/2025
Contenu : Affichage console
"""
#Modification le 02/11/2025 par Younes Abbassi: Ajout serveur socket 
import time
import random
from KB_00_Agent import *
from KB_02_Environnement import *
from socket_server_thread import SocketServer


def afficher_menu():
    """
    Rôle : Affiche le menu principal de l'utilisateur
    """
    print("*** MENU UTILISATEUR ***")
    print("1 - Lancer la simulation")
    print("2 - Quitter")

    choix = input("Votre choix : ")
    return choix

def afficher_menu_scenario():
    """
    Rôle : Permet de choisir le scénario
    """
    print("*** Choix du scénario ***")
    print("1 - Scénario trivial : déplacement libre")
    print("2 - Scénario émergent : propagation d’une maladie")
    print("3 - Scénario émergent : propagation d’une rumeur")
    choix = input("Votre choix (1/2/3) : ")
    return int(choix) if choix in ["1", "2", "3"] else 1

def lancer_simulation():
    """
    Rôle : Monte l'environnement, démarre les threads agents et ainsi lance la boucle de tour
    Résultats : lance une simulation simple avec agents qui se déplacent et interagissent
    """

    env = Environnement(15, 12) #Environnement

    env.add_place(3, 2)   # maison 1
    env.add_place(10, 3)  # maison 2
    env.add_place(3, 9)   # magasin
    env.add_place(10, 9)  # place publique

    obstacles = [
        (5, 3), (6, 3),
        (5, 4), (6, 4),
        (7, 6), (8, 6), (9, 6),
        (3, 7), (3, 8)
    ]
    for x, y in obstacles:
        env.add_obstacle(x, y)
    
    noms = ["sakura", "midori", "akane", "yuna", "haru", "ryo", "mei", "miku", "hana"]
    agents = []

    for nom in noms:
        while True:
            x = random.randint(0, env.width - 1)
            y = random.randint(0, env.height - 1)
            if env.position_valide(x, y, positions_occupees=[(a.x, a.y) for a in env.agents]):
                break

        a = Agent(nom, x, y, env)
        env.add_agent(a)
        agents.append(a)

    # --- Création du serveur socket pour Java ---
    socket_server = SocketServer(env=env)
    socket_server.start()
    print("[MAIN] Serveur socket lancé.")

    scenario = afficher_menu_scenario()
    if scenario == 2:
        agents[0].etat = "malade"
    elif scenario == 3:
        agents[1].humeur = "triste"
  
    for a in env.agents:
        a.start()
        
    try:
        for step in range(100):
            env.tour_complet() 
            env.display(step)
            time.sleep(0.2)
    finally:
        for a in env.agents:
            a.running = False
        socket_server.stop()
        print("[MAIN] Serveur socket arrêté.")
        print("Simulation terminée")


if __name__ == "__main__":
    """
    Rôle : Main du programme permet de choisir entre exécuter la simulation ou quitter
    """
    while True:
        choix = afficher_menu()
        if choix == "1":
            lancer_simulation()
        elif choix == "2":
            print("Au revoir")
        else:
            print("Choix invalide, veuillez réessayer.")