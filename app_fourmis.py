import flet as ft
import random
import math
import time
import threading
from AntColony import AntColony


def main(page: ft.Page):
    page.title = "Algorithme de Colonie de Fourmis"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    
    # Variables globales pour stocker les données
    nodes = []  # Liste des positions (x, y) des nœuds
    distances = []
    pheromones = []
    best_path = []
    iteration = 0
    running = False
    stop_event = threading.Event()
    
    # Champs de saisie
    nodes_field = ft.TextField(label="Nombre de nœuds", value="20", width=150)
    ants_field = ft.TextField(label="Nombre de fourmis", value="15", width=150)
    iterations_field = ft.TextField(label="Itérations", value="100", width=150)
    best_field = ft.TextField(label="Meilleures fourmis", value="3", width=150)
    decay_field = ft.TextField(label="Décay", value="0.95", width=150)
    alpha_field = ft.TextField(label="Alpha", value="1", width=150)
    beta_field = ft.TextField(label="Beta", value="2", width=150)
    iteration_text = ft.Text("Itération: 0", size=16)
    pheromone_text = ft.Text("Phéromones moyennes: ", size=14)
    path_text = ft.Text("Meilleur chemin: ", size=14)

    # Boutons
    generer_btn = ft.ElevatedButton(
        "Générer Graphe", 
        icon=ft.icons.SHUFFLE, 
        on_click=lambda e: generer_nodes()
    )
    start_btn = ft.ElevatedButton(
        "Démarrer", 
        icon=ft.icons.PLAY_ARROW, 
        bgcolor="green", 
        color="white", 
        on_click=start_algorithm
    )
    stop_btn = ft.ElevatedButton(
        "Arrêter", 
        icon=ft.icons.STOP, 
        bgcolor="red", 
        color="white", 
        disabled=True, 
        on_click=stop_algorithm
    )
    restart_btn = ft.ElevatedButton(
        "Réinitialiser", 
        icon=ft.icons.REFRESH, 
        on_click=restart_graph
    )
    # Zone graphique
    graph_container = ft.Container(
        width=600,
        height=500,
        bgcolor="white",
        border=ft.Border.all(2, "black")
    )
    
    status_text = ft.Text("Prêt", size=16, color="green")
    
    def generer_nodes():
        """Génère des positions aléatoires pour les nœuds"""
        nonlocal nodes, distances, pheromones

        try:
            num_nodes = int(nodes_field.value)
        except ValueError:
            num_nodes = 20
        
        nodes = []
        for _ in range(num_nodes):
            x = random.uniform(50, 550)  # Marges de 50px
            y = random.uniform(50, 450)
            nodes.append((x, y))


        def calculer_distances():
            """Calcule la matrice des distances"""
            distances = []
            for i in range(len(nodes)):
                row = []
                for j in range(len(nodes)):
                    if i == j:
                        row.append(0)
                    else:
                        dx = nodes[i][0] - nodes[j][0]
                        dy = nodes[i][1] - nodes[j][1]
                        row.append(math.sqrt(dx*dx + dy*dy))
                distances.append(row)
            return distances
        
        distances = calculer_distances()
        pheromones = [[1.0 for _ in range(len(nodes))] for _ in range(len(nodes))]
        
    def create_line(x1, y1, x2, y2, color, thickness):
        dx = x2 - x1
        dy = y2 - y1
        length = math.sqrt(dx*dx + dy*dy)
        angle = math.atan2(dy, dx)

        return ft.Container(
            width=length,
            height=thickness,
            bgcolor=color,
            left=x1,
            top=y1 - thickness / 2,
            rotate=ft.Rotate(
                angle=angle,
                alignment=ft.alignment.Alignment(-1, 0)
            )
        )
    
    def draw_graph():
        """
        Dessine le graphe des villes avec :
        - les arêtes pondérées par les phéromones
        - le meilleur chemin courant en rouge
        - les nœuds (villes) numérotés
        """
        # Liste de formes graphiques à afficher dans le Stack
        shapes = []
        
        # ==========================
        # Dessin des arêtes (phéromones)
        # ==========================
        if pheromones and len(pheromones) > 0:
            # Valeur maximale des phéromones (pour normalisation)
            max_pheromone = max(max(row) for row in pheromones) if pheromones else 1

            # Parcours de toutes les paires de nœuds
            for i in range(len(nodes)):
                for j in range(i + 1, len(nodes)):
                    # Seuil minimal pour éviter l’encombrement visuel
                    if pheromones[i][j] > 0.1:
                        # Opacité proportionnelle à la quantité de phéromones
                        opacity = min(1, pheromones[i][j] / max_pheromone)

                        # Épaisseur proportionnelle aux phéromones
                        thickness = max(1, (pheromones[i][j] / max_pheromone) * 3)

                        # Création de la ligne entre les deux nœuds
                        line = create_line(
                            nodes[i][0], nodes[i][1],
                            nodes[j][0], nodes[j][1],
                            ft.Colors.with_opacity(opacity, ft.Colors.BLUE),
                            thickness
                        )
                        shapes.append(line)
        
        # ==========================
        # Dessin du meilleur chemin courant
        # ==========================
        if best_path:
            for i in range(len(best_path) - 1):
                start_idx = best_path[i]
                end_idx = best_path[i + 1]

                # Vérification de sécurité
                if start_idx < len(nodes) and end_idx < len(nodes):
                    line = create_line(
                        nodes[start_idx][0], nodes[start_idx][1],
                        nodes[end_idx][0], nodes[end_idx][1],
                        "red",   # Couleur du meilleur chemin
                        3        # Épaisseur renforcée
                    )
                    shapes.append(line)
        
        # ==========================
        # Dessin des nœuds (villes)
        # ==========================
        for i, (x, y) in enumerate(nodes):
            shapes.append(
                ft.Container(
                    width=20,
                    height=20,
                    bgcolor="green",
                    border_radius=10,   # Cercle
                    left=x - 10,
                    top=y - 10,
                    content=ft.Text(str(i), size=10, color="white"),
                    alignment=ft.alignment.Alignment(0, 0)
                )
            )
        
        # Mise à jour du conteneur graphique
        graph_container.content = ft.Stack(controls=shapes, width=600, height=500)
        page.update()   
        
        page.add(
            ft.Column([
                ft.Text("Paramètres de l'algorithme", size=20),
                ft.Row([nodes_field, ants_field, iterations_field]),
                generer_btn,
                ft.Divider(),
                status_text,
                graph_container
            ])
        )
    

    def update_callback(iter_num, current_best_path, current_pheromones):
        """
        Callback appelé par l’algorithme à chaque itération
        pour mettre à jour l’interface graphique.
        """
        nonlocal iteration, best_path, pheromones

        # Mise à jour des variables globales
        iteration = iter_num
        best_path = current_best_path[0] if current_best_path else []
        pheromones = current_pheromones

        async def update_ui():
            # Affichage du numéro d’itération
            iteration_text.value = f"Itération: {iteration}"

            # Affichage du meilleur chemin et de sa longueur
            if current_best_path:
                path_text.value = (
                    f"Meilleur chemin: {best_path} "
                    f"(longueur: {current_best_path[1]:.2f})"
                )

            # Calcul de la moyenne des phéromones
            avg = sum(sum(row) for row in pheromones) / (len(nodes) ** 2)
            pheromone_text.value = f"Phéromones moyennes: {avg:.4f}"

            # Redessiner le graphe
            draw_graph_graphe()

        # Lancement asynchrone pour ne pas bloquer l’UI
        page.run_task(update_ui)

    def start_algorithm(e):
        nonlocal running
        # Empêche un double lancement
        if running:
            return None

        running = True
        stop_event.clear()

        # Mise à jour de l’interface
        start_btn.disabled = True
        stop_btn.disabled = False
        status_text.value = "En cours d'exécution..."
        status_text.color = "orange"
        page.update()

        def run_ants():
            try:
                # Création de la colonie de fourmis
                colony = AntColony(
                    distances,
                    int(ants_field.value),
                    int(best_field.value),
                    int(iterations_field.value),
                    float(decay_field.value),
                    float(alpha_field.value),
                    float(beta_field.value),
                )
            except ValueError:
                # Valeurs par défaut en cas d’erreur utilisateur
                colony = AntColony(distances, 15, 3, 100, 0.95, 1, 2)

            # Lancement de l’algorithme
            colony.run(update_callback, stop_event)

            async def finalize():
                """
                Finalize the Ant Colony Optimization algorithm
                Called when the algorithm has finished its execution
                """
                nonlocal running
                running = False
                # Enable the "Start" button and disable the "Stop" button
                start_btn.disabled = False
                stop_btn.disabled = True
                # Update the status text
                status_text.value = "Terminé"
                status_text.color = "green"

                page.update()

            page.run_task(finalize)

            # Thread pour exécution non bloquante
            threading.Thread(target=run_ants, daemon=True).start()

    def stop_algorithm(e):
        """
        Arrête l’algorithme en cours d’exécution.
        Called when the "Stop" button is clicked.
        """
        nonlocal running
        # Set the stop event to signal the algorithm to stop
        stop_event.set()
        # Disable the "Stop" button and enable the "Start" button
        start_btn.disabled = False
        stop_btn.disabled = True
        # Update the status text
        status_text.value = "Arrêté"
        status_text.color = "red"
        # Update the page
        page.update()


    def restart_graph(e):
        """
        Réinitialise complètement le graphe et l’interface.
        """
        nonlocal iteration, best_path, running

        running = False
        stop_event.set()

        # Réinitialisation des variables
        iteration = 0
        best_path = []

        # Réinitialisation de l’UI
        iteration_text.value = "Itération: 0"
        path_text.value = "Meilleur chemin: "
        pheromone_text.value = "Phéromones moyennes: "
        status_text.value = "Prêt"
        status_text.color = "green"

        # Disable the "Stop" button and enable the "Start" button
        start_btn.disabled = False
        stop_btn.disabled = True

        # Génération de nouveaux nœuds
        generer_nodes()



if __name__ == "__main__":
    ft.run(main)