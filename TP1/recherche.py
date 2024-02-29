import numpy as np


class Recherche:

    def __init__(self, word) -> None:
        self.prediction_method = {0:self.__produit_scalaire, 1:self.__least_square, 2:self.__city_block}
        self.word_to_search = word

    def search(self):
        pass


    def __produit_scalaire(self, wordA, wordB):
        return np.sum(wordA, wordB)

    def __least_square(self, wordA, wordB):
        return np.sum(np.square(wordA - wordB))
        

    def __city_block(self, wordA, wordB):
        return np.sum(np.absolute(wordA, wordB))