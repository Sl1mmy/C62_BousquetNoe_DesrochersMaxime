import numpy as np
from connexionDB import *

class Clustering:

    def __init__(self, window, n_centroids, max_words):
        self.window = int(window)
        self.n_centroids = int(n_centroids)
        self.max_words = int(max_words)

    

        