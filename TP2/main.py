import sys
from sys import argv
import argparse

from entrainementDB import *
from rechercheDB import *
from connexionDB import *

def main():
    window = encoding = path = None
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()

    group.add_argument('-e', dest='action', action='store_const', const='training')
    group.add_argument('-r', dest='action', action='store_const', const='research')
    group.add_argument('-b', dest='action', action='store_const', const='regenerate_DB')

    args, option_args = parser.parse_known_args()

    if len(sys.argv) == 1:
        print("\nERREUR - PAS ASSEZ DE PARAMETRES")
        exit()

    if args.action == 'training':
        parser.add_argument('-t',                   dest='size',        action='store', type=int, required=True)
        parser.add_argument('--enc', '--encodage',  dest='encoding',    action='store', required=True)
        parser.add_argument('--ch', '--chemin',     dest='path',        action='store', required=True)

        try:
            parser.parse_args(option_args, namespace=args)
        except:
            print("\nERREUR - PAS ASSEZ DE PARAMETRES (TAILLE, ENCODAGE, CHEMIN)")
            exit()

        try:
            window = args.__getattribute__('size')
            encoding = args.__getattribute__('encoding')
            path = args.__getattribute__('path')
        except:
            print("\nERREUR - ARGUMENTS NON VALIDES (TAILLE: int, ENCODAGE: string, CHEMIN: string)")
            exit()

        trainer = Trainer(window, encoding, path)
        answer = trainer.training()
        if answer == 1:
            exit()
        

    elif args.action == 'research':
        parser.add_argument('-t', dest='size', action='store', type=int, required=True)

        try:
            parser.parse_args(option_args, namespace=args)
        except:
            print("\nERREUR - PAS ASSEZ DE PARAMETRES (TAILLE)")
            exit()

        try:
            window = args.__getattribute__('size')

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
                        print_results(result, int(nb_synonyms))
                        rep = input("""\nEntrez un mot, le nombre de synonymes que vous voulez et la methode de calcul, i.e. produit scalaire: 0, least-squares: 1, city-block: 2\n""")
                except:
                    print("\nINVALIDE")
                    exit()
                        

        except: 
            print("\nERREUR - TAILLE NON VALIDE (int)")
            exit()

        
    elif args.action == 'regenerate_DB':
        random_args = argv[2:]

        if len(random_args) == 0:
            db = ConnexionDB()
            db.drop_tables()
            print("\nBASE DE DONNÉES RESET")
        else:
            print("\nINVALIDE")
        
def print_results(result_list, nb_synonym):
    print("\n")
    i = 0
    for result in result_list:
        i += 1
        print(f"{result[0]} --> {str(result[1])}")
        if i == nb_synonym:
            break





if __name__ == '__main__':
    quit(main())