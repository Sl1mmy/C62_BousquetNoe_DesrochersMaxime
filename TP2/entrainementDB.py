import re
from connexionDB import *

class Trainer:

    def __init__(self, window_size, encoding, path):
        self.window = int(window_size)
        self.encoding = encoding
        self.path = path
        self.unique_words = None
        self.connexion = ConnexionDB()
        self.connexion.create_tables()

    def training(self):
        try:
            file = self.connexion.get_file_db()
            if file == 0 or self.path not in file.values() or self.window not in file:
                word_list = re.findall(
                    '\w+', open(self.path, 'r', encoding=self.encoding).read())
                word_list = [x.lower() for x in word_list]
                self.connexion.insert_new_file(self.path, self.window)
            else:
                print('\n FICHIER DEJA DANS BD')
                return 0
        except:
            print('\n FICHIER NON RECONNU')
            return 1
        
        self.unique_words = self.__create_unique_list(word_list)
        self.__coocurences(self.unique_words, word_list)
        return 0

    def __create_unique_list(self, word_list):
        unique_words = self.connexion.get_words()
        tuples_list = []

        for word in word_list:
            if word not in unique_words:
                tuples_list.append((len(unique_words), word))
                unique_words[word] = len(unique_words)
        self.connexion.insert_new_word(tuples_list)
        return unique_words


    def __coocurences(self, unique_words, word_list):
        half_window = self.window // 2
        dict_cooc = {}

        for i in range(len(word_list)):
            central_word = unique_words[word_list[i]]
            for j in range(1, half_window + 1):
                if not i + j >= len(word_list) and central_word != unique_words[word_list[i + j]]:
                    
                    index = unique_words[word_list[i + j]]
                    if (central_word, index) not in dict_cooc:
                        dict_cooc[(central_word, index)] = 1
                    else:
                        dict_cooc[(central_word, index)] += 1

                    if (index, central_word) not in dict_cooc:
                        dict_cooc[(index, central_word)] = 1
                    else:
                        dict_cooc[(index, central_word)] += 1

        tuples_list_to_update = []
        tuples_list_to_add = []
        words_to_add_dict = {}

        words_added_dict = self.connexion.get_cooc_dict(self.window)

        for key in dict_cooc:
            # mot existant a modifier
            if (key[0], key[1]) in words_added_dict:
                value = dict_cooc[key[0], key[1]] + words_added_dict[key[0], key[1]]
                tuples_list_to_update.append((value, key[0], key[1], self.window))
            # nouveau mot a ajouter
            elif (key[1], key[0]) not in words_to_add_dict:
                tuples_list_to_add.append((key[0], key[1], dict_cooc[(key[0], key[1])], self.window))
                words_to_add_dict[(key[0], key[1])] = dict_cooc[(key[0], key[1])]

        
        self.connexion.insert_matrix(tuples_list_to_add)
        if len(words_added_dict) > 1:
            self.connexion.update_matrix(tuples_list_to_update)