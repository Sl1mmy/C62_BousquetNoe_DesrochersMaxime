import re
import sys
import numpy as np

class Entrainement:

    def __init__(self, window_scale, encoding, path) -> None:
        self.window = int(window_scale)
        self.encoding = encoding
        self.path = path
        self.unique_words = None
        self.coocurence_matrix = None

    def train(self):
        try:
            word_list = re.findall('\w+', open(self.path, 'r', encoding=self.encoding).read()) #ne prend pas les points (TODO peutetre a changer)
            word_list = [w.lower() for w in word_list]
        except:
            return "failed"
        
        self.unique_words = self.__new_unique_list(word_list) #donne la liste de mots uniques par rapport a la liste extrait du texte

        self.cooccurence_matrix = np.zeros((len(self.unique_words), len(self.unique_words))) #cree une matrice de la taille du nombre de mots uniques

        self.__fill_matrix(self.unique_words, word_list) #remplit la matrice de cooccurence avec les donnees

        return "done"

    
    def __new_unique_list(self, list):
        unique_words = {}

        for word in list:
            if word not in unique_words:
                unique_words[word] = len(unique_words)

        return unique_words
    
    def __fill_matrix(self, unique_words, word_list):
        half_window = self.window // 2

        for i in range(len(word_list)):
            central_word_index = unique_words[word_list[i]]
            for j in range(1, half_window + 1):
                if i + j < len(word_list):
                    neighbor_word_index = unique_words[word_list[i + j]]
                    if central_word_index != neighbor_word_index:
                        self.cooccurence_matrix[central_word_index][neighbor_word_index] += 1
                        self.cooccurence_matrix[neighbor_word_index][central_word_index] += 1

        # print(self.unique_words)
        # print(self.cooccurence_matrix)
        print("done")
    




