import sqlite3
import numpy as np

DB_PATH = 'synonyms.db'
ACTIVATE_FK = 'PRAGMA foreign_keys = 1'

CREATE_WORD = '''
    CREATE TABLE IF NOT EXISTS synonyms_dict 
    (
        id      INT PRIMARY KEY NOT NULL,
        word    CHAR(24) NOT NULL
    )
'''
DROP_WORD = 'DROP TABLE IF EXISTS synonyms_dict'
INSERT_WORD = 'INSERT INTO synonyms_dict VALUES(?, ?)'

CREATE_MATRIX = '''
    CREATE TABLE IF NOT EXISTS matrix
    (
        word1 INT NOT NULL,
        word2 INT NOT NULL,
        frequence INT NOT NULL,
        window INT NOT NULL,

        PRIMARY KEY(word1, word2, window),
        FOREIGN KEY(word1) REFERENCES synonyms_dict(id),
        FOREIGN KEY(word2) REFERENCES synonyms_dict(id)
    )
'''
DROP_MATRIX = 'DROP TABLE IF EXISTS matrix'
INSERT_MATRIX = 'INSERT INTO matrix VALUES(?, ?, ?, ?)'

UPDATE_MATRIX = '''
    UPDATE matrix
        SET
            frequence = ?
        WHERE
            word1 = ? and
            word2 = ? and
            window = ?
'''

DELETE_EMPTY_VALS = 'DELETE FROM matrix WHERE frequence = 0'
GET_MATRIX = 'SELECT * FROM matrix WHERE window = ?'

CREATE_FILES = '''
    CREATE TABLE IF NOT EXISTS files
    (
        file_name TEXT NOT NULL,
        window INT NOT NULL,

        PRIMARY KEY(file_name, window)  
    )
'''
DROP_FILES = 'DROP TABLE IF EXISTS files'
INSERT_FILE_DB = 'INSERT INTO files VALUES(?, ?)'


class ConnexionDB():
    def __init__(self):
        try:
            self.connexion = sqlite3.connect(DB_PATH)
            self.cursor = self.connexion.cursor()
            self.cursor.execute(ACTIVATE_FK)
        except:
            print("ERREUR DE CONNEXION")

    def disconnect(self):
        self.cursor.close()
        self.connexion.close()

    def create_tables(self):
        self.cursor.execute(CREATE_WORD)
        self.cursor.execute(CREATE_MATRIX)
        self.cursor.execute(CREATE_FILES)

    def drop_tables(self):
        try:
            self.cursor.execute(DROP_WORD)
            self.cursor.execute(DROP_MATRIX)
            self.cursor.execute(DROP_FILES)
            self.cursor.execute('VACUUM')
        except:
            print("ERREUR DE SUPPRESSION")

    # tuples_word : [(id, word), (id, word), ...]
    def insert_new_word(self, tuples_word):
        self.cursor.executemany(INSERT_WORD, tuples_word)
        self.connexion.commit()


    # matrix : [(id1, id2, frequence), (id1, id2, frequence), ...]
    def insert_matrix(self, matrix):
        self.cursor.executemany(INSERT_MATRIX, matrix)
        self.connexion.commit()

    
    def update_matrix(self, matrix):
        self.cursor.executemany(UPDATE_MATRIX, matrix)
        self.connexion.commit()


    def get_words(self):
        unique_words = {}
        self.cursor.execute('SELECT * FROM synonyms_dict')
        rows = self.cursor.fetchall()

        for row in rows:
            unique_words[row[1]] = row[0]
        return unique_words 

    # dict : symbolise la matrice selon la taille de fenetre
    def get_cooc_dict(self, window):
        self.cursor.execute('SELECT * FROM matrix WHERE window = ?', (window, ))
        dict = {}
        rows = self.cursor.fetchall()
        for row in rows:
            dict[(row[0], row[1])] = row[2]
            dict[(row[1], row[0])] = row[2]
        return dict

    # matrix : la matrice elle meme
    def get_cooc_matrix(self, nb_unique_words, window):
        self.cursor.execute(GET_MATRIX, (window, ))
        matrix = np.zeros((nb_unique_words, nb_unique_words))
        rows = self.cursor.fetchall()
        if len(rows) == 0:
            matrix = "INVALID"
        else:
            for row in rows:
                matrix[row[0]][row[1]] = row[2]
                matrix[row[1]][row[0]] = row[2]
        return matrix

    def insert_new_file(self, file_name, window):
        insert = (file_name, window)
        self.cursor.execute(INSERT_FILE_DB, insert)
        self.connexion.commit()

    def get_file_db(self):
        try:
            self.cursor.execute('SELECT * FROM files')
            file_dict = {}
            results = self.cursor.fetchall()
            for result in results:
                file_dict[result[1]] = result[0]
            return file_dict
        except:
            return 0