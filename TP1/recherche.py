import numpy as np


class Recherche:

    def __init__(self, word) -> None:
        self.prediction_method = {0:self.__produit_scalaire, 1:self.__least_square, 2:self.__city_block}
        self.word_to_search = word

    def __produit_scalaire(self, motA, motB):
        return np.sum(motA, motB)

    def __least_square(self, motA, motB):
        return np.sum(np.square(motA - motB))
        

    def __city_block(self, motA, motB):
        return np.sum(np.absolute(motA, motB))