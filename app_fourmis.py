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
    
    # Champs de saisie
    nodes_field = ft.TextField(label="Nombre de nœuds", value="20", width=150)
    ants_field = ft.TextField(label="Nombre de fourmis", value="15", width=150)
    iterations_field = ft.TextField(label="Itérations", value="100", width=150)
    
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
        nonlocal nodes
        try:
            num_nodes = int(nodes_field.value)
        except ValueError:
            num_nodes = 100
        
        nodes = []
        for _ in range(num_nodes):
            x = random.uniform(50, 550)  # Marges de 50px
            y = random.uniform(50, 450)
            nodes.append((x, y))
        
        print(f"{len(nodes)} nœuds générés")
        dessiner_graphe()
    
    def dessiner_graphe():
        """Dessine les nœuds sur le graphe"""
        shapes = []
        
        # Dessiner chaque nœud comme un cercle vert
        for i, (x, y) in enumerate(nodes):
            cercle = ft.Container(
                width=20,
                height=20,
                bgcolor="green",
                border_radius=10,
                left=x - 10,  # Centrer le cercle
                top=y - 10,
                content=ft.Text(str(i), size=10, color="white"),
                alignment=ft.alignment.Alignment(0, 0)
            )
            shapes.append(cercle)
        
        # Mettre à jour le conteneur avec un Stack (empilement)
        graph_container.content = ft.Stack(
            controls=shapes,
            width=600,
            height=500
        )
        page.update()
    
    # Bouton pour générer le graphe
    btn_generer = ft.ElevatedButton(
        "Générer le Graphe",
        on_click=lambda e: generer_nodes()
    )
    
    page.add(
        ft.Column([
            ft.Text("Paramètres de l'algorithme", size=20),
            ft.Row([nodes_field, ants_field, iterations_field]),
            btn_generer,
            ft.Divider(),
            status_text,
            graph_container
        ])
    )
    
    # Générer un graphe initial
    generer_nodes()

if __name__ == "__main__":
    ft.run(main)