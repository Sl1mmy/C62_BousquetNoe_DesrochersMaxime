import sys
from sys import argv
import argparse

from entrainementDB import *
from rechercheDB import *
from clustering import *
from connexionDB import *

class Options:

    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser()
        self.group = self.parser.add_mutually_exclusive_group()


    def run(self):
        self.check_args()

        if self.args.action == 'training':
            self.training()

        elif self.args.action == 'research':
            self.research()

        elif self.args.action == 'clustering':
            self.clustering()

        elif self.args.action == 'regenerate_DB':
            self.regenerate_DB()


    def check_args(self):
        self.group.add_argument('-e', dest='action', action='store_const', const='training')
        self.group.add_argument('-r', dest='action', action='store_const', const='research')
        self.group.add_argument('-c', dest='action', action='store_const', const='clustering')
        self.group.add_argument('-b', dest='action', action='store_const', const='regenerate_DB')


        self.args, self.option_args = self.parser.parse_known_args()

        if len(sys.argv) == 1:
            print("\nERREUR - PAS ASSEZ DE PARAMETRES")
            exit()

    def training(self):
        self.parser.add_argument('-t',                   dest='size',        action='store', type=int, required=True)
        self.parser.add_argument('--enc', '--encodage',  dest='encoding',    action='store', required=True)
        self.parser.add_argument('--ch', '--chemin',     dest='path',        action='store', required=True)

        try:
            self.parser.parse_args(self.option_args, namespace=self.args)
        except:
            print("\nERREUR - PAS ASSEZ DE PARAMETRES (TAILLE, ENCODAGE, CHEMIN)")
            exit()

        try:
            window = self.args.__getattribute__('size')
            encoding = self.args.__getattribute__('encoding')
            path = self.args.__getattribute__('path')
        except:
            print("\nERREUR - ARGUMENTS NON VALIDES (TAILLE: int, ENCODAGE: string, CHEMIN: string)")
            exit()

        trainer = Trainer(window, encoding, path)
        answer = trainer.training()
        if answer == 1:
            exit()

    def research(self):
        self.parser.add_argument('-t', dest='size', action='store', type=int, required=True)

        try:
            self.parser.parse_args(self.option_args, namespace=self.args)
        except:
            print("\nERREUR - PAS ASSEZ DE PARAMETRES (TAILLE)")
            exit()

        try:
            window = self.args.__getattribute__('size')

            rep = input("""\nEntrez un mot, le nombre de synonymes que vous voulez et la methode de calcul, i.e. produit scalaire: 0, least-squares: 1, city-block: 2\n""")

            while rep != 'q':
                try:
                    word_to_search, nb_synonyms, method = rep.split()
                    search = Recherche(word_to_search.lower(), int(method), window)
                    result = search.search()
                    if result[0] == "Invalide":
                        print("\n ERREUR - TAILLE DE FENETRE INVALIDE")
                        rep = 'q'
                    else:
                        self.print_results(result, int(nb_synonyms))
                        rep = input("""\nEntrez un mot, le nombre de synonymes que vous voulez et la methode de calcul, i.e. produit scalaire: 0, least-squares: 1, city-block: 2\n""")
                except:
                    print("\nINVALIDE")
                    exit()
        except argparse.ArgumentError or argparse.ArgumentTypeError: 
            print("\nERREUR - TAILLE NON VALIDE (int)")
            exit()

    def clustering(self):
        self.parser.add_argument('-t',  dest='size',        action='store', type=int, required=True)
        self.parser.add_argument('-n',  dest='n_centroids', action='store', required=True)
        self.parser.add_argument('-k', dest='n_neighbors',    action='store', required=True)
        self.parser.add_argument('-m',  dest='max_words',   action='store', required=True)
        self.parser.add_argument('--normaliser', dest='normalize', action='store', required=False)

        try:
            self.parser.parse_args(self.option_args, namespace=self.args)
        except:
            print("\nERREUR - PAS ASSEZ DE PARAMETRES (TAILLE, NOMBRE CENTROIDES, NOMBRE DE VOTES, MOTS MAX, NORMALISER)")
            exit()

        try:
            window = self.args.__getattribute__('size')
            n_centroids = self.args.__getattribute__('n_centroids')
            n_neighbors = self.args.__getattribute__('n_neighbors')
            max_words = self.args.__getattribute__('max_words')
            normalize = self.args.__getattribute__('normalize')
        except:
            print("\nERREUR - ARGUMENTS NON VALIDES (TAILLE: int, NOMBRE CENTROIDES: int, NOMBRE DE VOTES: int, MOTS MAX: int)")
            exit()

        clustering = Clustering(window, n_centroids, n_neighbors, max_words, normalize)
        clustering.init()
        result = clustering.run()
        if result == 1:
            exit()


    def regenerate_DB(self):
        random_args = argv[2:]

        if len(random_args) == 0:
            db = ConnexionDB()
            db.drop_tables()
            print("\nBASE DE DONNÉES RESET")
        else:
            print("\nINVALIDE")

    def print_results(self, result_list, nb_synonym):
        print("\n")
        i = 0
        for result in result_list:
            i += 1
            print(f"{result[0]} --> {str(result[1])}")
            if i == nb_synonym:
                break

