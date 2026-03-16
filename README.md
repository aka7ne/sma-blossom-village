ReadMe Projet SMA
Auteur : Bouguima Kawthar 22303486

Ce fichier documente la partie modélisation et threads en .py du développement du projet

03/10/2025 :
Création du fichier .py de la partie modélisation
* Description : - Création d'une classe Agent avec les attributs (positions, etat_sante, humeur et destination)
                - Création des méthodes (choix des destinations, deplacement et interaction)
                - Environnement (stocke les obstacles, les lieux et gere la liste des agents)
                - Affichage console

* Objectif : Avoir une interface console avec 2,3 agents marqué avec des lettres, les obstacles les objets etc...


10/10/2025 :
Implémentation du système Multi-threading
* Description : - Chaque agent hérite d’un thread (class Agent(threading.Thread)), lui permettant d’évoluer indépendamment
                - Chaque thread exécute sa boucle d’actions : choisir destination --> se déplacer --> interagir
                - Le moteur principal (main) se contente d’afficher l’environnement à intervalles réguliers

* Objectif : Permettre une simulation parallèle réaliste, où les agents agissent simultanément, sans dépendre d’un tour global


12/10/2025 :
Ajout des 3 scénario émergent/trivial
* Description : - Scénario trivial : déplacement libre et propagation simple
                - Scénario émergent 1 : contagion épidémique
                - Scénario émergent 2 : regroupement social dynamique
Chaque scénario est défini par un ensemble de règles locales différentes (choix de destination, interaction, humeur)

* Objectif : Observer l’apparition de comportements collectifs non programmés explicitement

Partie Affichage :

27/10/2025 :
* Description :
Cette partie du projet correspond à l’interface graphique réalisée en JavaFX.
Elle contient un menu principal permettant de choisir entre trois scénarios différents, chacun ouvrant une fenêtre explicative avant d’accéder à la simulation.
