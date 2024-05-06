import numpy as np
import re
from connexionDB import *

class Recherche:

    def __init__(self, search_word, method, window):
        self.predictMethod = {0: self.__produit_scalaire, 1: self.__least_square, 2: self.__city_block}
        self.method_num = method
        self.method = self.predictMethod[method]
        self.word_to_search = search_word
        self.connexion = ConnexionDB()
        self.word_dict = self.connexion.get_words()
        self.cooc_matrix = self.connexion.get_cooc_matrix(len(self.word_dict), int(window))
        self.stop_words = []
        self.basic_result = []

    
    def search(self):
        if isinstance(self.cooc_matrix, str):
            self.basic_result.append("Invalide")
            return self.basic_result
        else:
            self.__checkup() #verifie si mot present dans le texte
            self.__get_stop_word() #prend une liste de stop-words

            for word, value in self.word_dict.items():
                if word != self.word_to_search and word not in self.stop_words:
                    score = self.method(self.word_array, self.cooc_matrix[value]) #attribut un score a chaque mot grace a la methode de calcul choisie
                    self.basic_result.append((word, score))

            if self.method_num == 0:
                return sorted(self.basic_result, reverse=True, key=lambda x: x[1]) #lambda : Trier selon le score
            else:
                return sorted(self.basic_result, key=lambda x: x[1])

    def __get_stop_word(self):
        self.stop_words = re.findall('\w+', open('TP3\stop_words.py', 'r', encoding="UTF-8").read())


    def __checkup(self):
        if self.word_to_search not in self.word_dict:
            print("WORD NOT PRESENT IN LIST")
            return 0
        else:
            index = self.word_dict[self.word_to_search]
            self.word_array = self.cooc_matrix[index]


    def __produit_scalaire(self, word_A, word_B):
        return np.sum(word_A * word_B)

    def __least_square(self, word_A, word_B):
        return np.sum(np.square(word_A - word_B))
        
    def __city_block(self, word_A, word_B):
        return np.sum(np.absolute(word_A - word_B))


