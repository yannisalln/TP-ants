import random
import time
import threading

class AntColony:
    def __init__(self, distances, n_ants, n_best, n_iterations, decay, alpha=1, beta=2):
        """
        Initialise la colonie de fourmis.
        
        Paramètres :
        - distances : matrice des distances entre les villes
        - n_ants : nombre de fourmis par itération
        - n_best : nombre de meilleurs chemins qui déposent des phéromones
        - n_iterations : nombre d'itérations de l'algorithme
        - decay : taux d'évaporation des phéromones (entre 0 et 1)
        - alpha : importance des phéromones (α)
        - beta : importance de l'heuristique (β)
        """
        self.distances = distances
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
        
        # Initialiser la matrice de phéromones
        n = len(distances)
        self.pheromones = [[1.0 for _ in range(n)] for _ in range(n)]
        
        # Variables pour le meilleur chemin trouvé
        self.meilleur_chemin = None
        self.meilleure_distance = float('inf')
        
        # Toutes les indices de villes
        self.all_indices = range(n)

    def calculer_distance_chemin(self, chemin):
        """
        Calcule la distance totale d'un chemin.
        
        Paramètre :
        - chemin : liste d'indices représentant l'ordre des villes
        
        Retourne :
        - La distance totale du chemin
        """
        total = 0
        for i in range(len(chemin) - 1):
            total += self.distances[chemin[i]][chemin[i+1]]
        return total

    def generer_chemin_fourmi(self):
        """
        Génère un chemin complet pour une fourmi.
        
        Retourne :
        - Un tuple (chemin, distance) pour la fourmi
        """
        # Commencer par une ville aléatoire
        chemin = [random.randint(0, len(self.distances) - 1)]
        
        # Ajouter les autres villes
        while len(chemin) < len(self.distances):
            prochaines_probas = self.calculer_probabilites_mouvement(chemin)
            prochaine_ville = self.choisir_prochaine_ville(prochaines_probas)
            chemin.append(prochaine_ville)
        
        return (chemin, self.calculer_distance_chemin(chemin))

    def calculer_probabilites_mouvement(self, chemin):
        """
        Calcule les probabilités de mouvement vers chaque ville.
        
        Paramètre :
        - chemin : le chemin actuel de la fourmi
        
        Retourne :
        - Liste des probabilités normalisées
        """
        ville_actuelle = chemin[-1]
        probabilites = []
        
        for ville in self.all_indices:
            if ville in chemin:
                probabilites.append(0)  # Ville déjà visitée
            else:
                # Calculer la probabilité selon la formule
                pheromone = self.pheromones[ville_actuelle][ville] ** self.alpha
                heuristique = (1.0 / self.distances[ville_actuelle][ville]) ** self.beta
                probabilites.append(pheromone * heuristique)
        
        # Normaliser les probabilités
        total = sum(probabilites)
        if total > 0:
            return [p / total for p in probabilites]
        else:
            return [0] * len(probabilites)

    def choisir_prochaine_ville(self, probabilites):
        """
        Choisit la prochaine ville selon les probabilités.
        
        Paramètre :
        - probabilites : liste des probabilités normalisées
        
        Retourne :
        - L'indice de la prochaine ville
        """
        r = random.random()
        cumul = 0
        
        for i, p in enumerate(probabilites):
            cumul += p
            if cumul >= r:
                return i
        
        return len(probabilites) - 1

    def deposer_pheromones(self, tous_les_chemins):
        """
        Dépose des phéromones sur les meilleurs chemins.
        
        Paramètre :
        - tous_les_chemins : liste de tous les chemins générés
        """
        # Trier les chemins par distance (du meilleur au pire)
        chemins_tries = sorted(tous_les_chemins, key=lambda x: x[1])
        
        # Déposer des phéromones sur les n_best meilleurs chemins
        for chemin, distance in chemins_tries[:self.n_best]:
            for i in range(len(chemin) - 1):
                ville1, ville2 = chemin[i], chemin[i+1]
                # La quantité de phéromones est inversement proportionnelle à la distance
                self.pheromones[ville1][ville2] += 1.0 / distance

    def evaporer_pheromones(self):
        """
        Fait évaporer les phéromones selon le taux de décroissance.
        """
        n = len(self.pheromones)
        for i in range(n):
            for j in range(n):
                self.pheromones[i][j] *= self.decay

    def executer_iteration(self):
        """
        Exécute une itération complète de l'algorithme.
        
        Retourne :
        - Un tuple (meilleur_chemin, meilleure_distance) pour cette itération
        """
        # Générer les chemins pour toutes les fourmis
        tous_les_chemins = []
        for _ in range(self.n_ants):
            tous_les_chemins.append(self.generer_chemin_fourmi())
        
        # Trouver le meilleur chemin de cette itération
        meilleur_chemin_iteration = min(tous_les_chemins, key=lambda x: x[1])
        
        # Mettre à jour le meilleur chemin global
        if meilleur_chemin_iteration[1] < self.meilleure_distance:
            self.meilleur_chemin = meilleur_chemin_iteration[0]
            self.meilleure_distance = meilleur_chemin_iteration[1]
        
        # Déposer et évaporer les phéromones
        self.deposer_pheromones(tous_les_chemins)
        self.evaporer_pheromones()
        
        return meilleur_chemin_iteration

    def run(self, callback_maj, evenement_arret):
        """
        Exécute l'algorithme complet.
        
        Paramètres :
        - callback_maj : fonction de callback appelée après chaque itération
        - evenement_arret : threading.Event pour arrêter l'algorithme
        """
        for iteration in range(self.n_iterations):
            # Vérifier si l'arrêt a été demandé
            if evenement_arret.is_set():
                break
            
            # Exécuter une itération
            chemin_courant, distance_courante = self.executer_iteration()
            
            # Appeler le callback de mise à jour
            callback_maj(iteration, chemin_courant, self.pheromones)
            
            # Petite pause pour permettre la mise à jour de l'interface
            time.sleep(0.1)

# Exemple d'utilisation
if __name__ == "__main__":
    # Matrice de distances d'exemple (4 villes)
    distances = [
        [0, 2, 9, 10],
        [1, 0, 6, 4],
        [15, 7, 0, 8],
        [6, 3, 12, 0]
    ]
    
    # Créer la colonie de fourmis
    colonie = AntColony(
        distances=distances,
        n_ants=3,
        n_best=5,
        n_iterations=100,
        decay=0.95,
        alpha=1,
        beta=2
    )
    
    # Créer un événement d'arrêt
    evenement_arret = threading.Event()
    
    # Définir une fonction de callback
    def callback_maj(iteration, chemin, pheromones):
        if iteration % 10 == 0:
            print(f"Iteration {iteration}: Meilleur chemin = {chemin}, Distance = {colonie.meilleure_distance}")
            print("Pheromones matrix:")
            for row in pheromones:
                print(row)  
    
    # Exécuter l'algorithme
    colonie.run(callback_maj, evenement_arret)