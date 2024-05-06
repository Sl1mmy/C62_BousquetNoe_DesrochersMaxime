import numpy as np
import random
from time import time
from connexionDB import *



class Clustering:

    def __init__(self, window, n_centroids, n_neighbors, max_words, normalize):
        self.window = int(window)
        self.n_centroids = int(n_centroids)
        self.max_words = int(max_words)

        # KNN arguments ----------------------
        self.features = ["nom", "adjectif", "determinant", "verbe", "pronom", "adverbe", "preposition", "conjonction", "interjection"]
        #self.classes = # TODO figure out
        #self.etiquettes = # TODO figure out

        self.n_neighbors = int(n_neighbors)
        self.is_normalized = normalize

        # ------------------------------------

        self.connexion = ConnexionDB()
        self.word_dict = self.connexion.get_words()
        self.cooc_matrix = self.connexion.get_cooc_matrix(len(self.word_dict), int(window))
        self.centroids = []
        self.clusters_data = []
        self.n_iterations = 0
        self.n_changes = 0
        self.stable = False

    def init(self):
        self.global_time = time()
        self.iteration_time = time()

        self.clusters = []
        self.clusters_data = []
        indexCentroids = random.sample(range(0, len(self.word_dict)), self.n_centroids)

        for i in range(0, self.n_centroids):
            self.centroids.append(self.cooc_matrix[indexCentroids[i]])
            self.clusters.append({})
            self.clusters_data.append([])

        self.allocate_cluster(self.centroids, self.clusters)

        self.n_changes = len(self.word_dict)

        self.print_iteration()

    def print_iteration(self):      
        print("\n============================================================================")
        print(f'Iteration {self.n_iterations}')
        print(f'{self.n_changes} changements de cluster en {round((time() - self.iteration_time), 2)} secondes.\n')
        for i in range(0, self.n_centroids):
            print(f'Il y a {len(self.clusters[i])} points (mots) regroupés autour du centroïde no {i}')

    def run(self):
        while(not self.stable):
            self.iteration_time = time()
            self.iterate()
            self.print_iteration()

        print("done")
        self.print_results()
        # candidat: (list: [])
        # type_vote: 0 (démocrate), 1 (harmonique), 2 (distance)
        # votes = self.vote(candidat, self.n_votes, type_vote, self.is_normalized)
        # print results

    def iterate(self):
        self.n_changes = 0
        new_centroids = []
        self.clusters_data = []
        self.new_clusters = []

        for cluster in self.clusters:
            cluster = np.array(list(cluster.values()))
            self.clusters_data.append([]) # afficher scores
            self.new_clusters.append({}) # calcul des centroides
            new_centroids.append(np.average(cluster, axis=0))

        self.allocate_cluster(new_centroids, self.new_clusters)

        self.n_iterations += 1

        self.calculate_change(new_centroids)

    def allocate_cluster(self, centroids, cluser_dict):
        for word, value in self.word_dict.items():
            temp_result = []
            for i in range(0, self.n_centroids):
                temp_result.append(self.__least_square(centroids[i], self.cooc_matrix[value]))
            
            best_score = np.amin(temp_result)

            result = np.where(temp_result == best_score)
            cluster_index = result[0][0]
            self.clusters_data[cluster_index].append((word, best_score))
            cluser_dict[cluster_index][value] = self.cooc_matrix[value]

    def calculate_change(self, new_centroids):
        self.n_changes = 0

        for i in range(self.n_centroids):
            if self.clusters[i].keys() != self.new_clusters[i].keys():
                self.n_changes += self.dict_compare(self.clusters[i], self.new_clusters[i])

            self.clusters[i] = self.new_clusters[i]
            if len(self.clusters[i]) > 0:
                self.centroids[i] = new_centroids[i]

        if self.n_changes == 0:
            self.stable = True

    def print_results(self):
        print("\n****************************************************************************")
        print(f'\n\nClustering en {self.n_iterations} itérations. Temps écoulés : {round((time() - self.global_time), 2)} secondes\n')
        for i in range(len(self.clusters_data)):
            print("\nGroupe", i, "\n")
            self.clusters_data[i] = sorted(self.clusters_data[i], key= lambda x: x[1])
            for j in range(self.max_words):
                if j < len(self.clusters_data[i]):
                    print(f"{self.clusters_data[i][j][0]} --> {str(round(self.clusters_data[i][j][1]), 2)}")

    def dict_compare(self, d1, d2):
        d1_keys = set(d1.keys())
        d2_keys = set(d2.keys())
        removed = d2_keys - d1_keys
        return len(removed)

    def __least_square(self, word_A, word_B):
        return np.sum(np.square(word_A - word_B))

    # - KNN -------------------------------------------------------------

    # candidat: features d'un mot inconnu
    def vote(self, candidat: list, n_voisins: int, type_vote: int, normalize: int) -> list[tuple[str, float]]:
        self.features.append(candidat)
        features = np.array(self.features)
        self.features.pop()
        if normalize:
            features = self.normalize(features)
        
        # À l'étape nécessaire, le clustering fournit DÉJÀ
        # les distances d'un mot à son cluster
        distances = np.sum( (features[-1] - features[:-1])**2, axis = 1 )
        voisins = np.argsort(distances)[:n_voisins]
        fonction_vote = [self.__democrate, self.__harmonique, self.__distance][type_vote]
        votes = {classe:0 for classe in self.classes}
        for position_voisin in range(len(voisins)):
            rangee_voisin = voisins[position_voisin]
            distance_voisin = distances[rangee_voisin]
            etiquette_voisin = self.etiquettes[rangee_voisin]
            votes[etiquette_voisin] += fonction_vote(distance_voisin, position_voisin)
        return sorted(votes.items(), key=lambda t:t[1], reverse=True)
        
    # chaque vecteur de feature (coordonnée) est transformé
    # en vecteur unitaire, donc divisé par sa norme
    def normalize(self, m: np.ndarray) -> np.ndarray:
        return (m.transpose()/np.linalg.norm(m, axis=1)).transpose()
    
    def __democrate(self, distance2: float, position: int) -> float: return 1.0
    def __harmonique(self, distance2: float, position: int) -> float: return 1.0/(position + 1)
    def __distance(self, distance2: float, position: int) -> float: return 1.0/(distance2 + 1) 

