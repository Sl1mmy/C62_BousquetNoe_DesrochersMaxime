import re
import numpy as np



class Recherche:

    def __init__(self, unique_words: dict, cooccurence_matrix: np.ndarray, search_word: str, method: int) -> None:
        self.prediction_method = {0:self.__produit_scalaire, 1:self.__least_square, 2:self.__city_block}

        self.word_dict = unique_words
        self.matrix = cooccurence_matrix
        self.word_to_search = search_word
        self.method = self.prediction_method[method]
        self.method_num = method

        self.basic_result = []
        

    def search(self):
        self.__checkup() #verifie si mot present dans le texte
        self.__get_stop_words() #prend une liste de stop-words

        for word, value in self.word_dict.items():
            if word != self.word_to_search and word not in self.stop_words:
                score = self.method(self.word_array, self.matrix[value]) #attribut un score a chaque mot grace a la methode de calcul choisie
                self.basic_result.append((word, score))
        if self.method_num == 0:
            return sorted(self.basic_result, reverse=True, key=lambda x: x[1]) #lambda : Trier selon le score
        else:
            return sorted(self.basic_result, key=lambda x: x[1])



    def __checkup(self):
        if self.word_to_search not in self.word_dict:
            print("WORD NOT PRESENT IN LIST")
            return 0
        else:
            index = self.word_dict[self.word_to_search]
            self.word_array = self.matrix[index]

    def __get_stop_words(self):
        self.stop_words = re.findall('\w+', open('stop_words.py', 'r', encoding="UTF-8").read())

    def __produit_scalaire(self, word_A, word_B):
        return np.sum(word_A * word_B)

    def __least_square(self, word_A, word_B):
        return np.sum(np.square(word_A - word_B))
        

    def __city_block(self, word_A, word_B):
        return np.sum(np.absolute(word_A - word_B))