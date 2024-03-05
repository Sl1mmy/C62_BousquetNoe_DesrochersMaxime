from sys import argv
import os
import msvcrt as msv
from colorama import init, Fore, Style

from entrainement import *
from recherche import *

init(convert=True) #for Colorama



def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def prompt():
    split_args = None
    
    print("""\nEntrez un mot, le nombre de synonymes que vous voulez et la methode de calcul,
i.e. produit scalaire: 0, least-squares: 1, city-block: 2""")

    arguments = input("\ntapez Q pour quitter.\n\n")
    split_args = arguments.split()

    if(arguments == 'q'):
        cls()
        exit()
    elif(len(split_args) != 3):
        cls()
        print(f"{Fore.RED}MUST HAVE 3 ARGUMENTS{Style.RESET_ALL}")
        prompt()
    elif(split_args[0].isdigit() or not split_args[1].isdigit() or not split_args[2].isdigit()):
        cls()
        print(f"{Fore.RED}WRONG ARGUMENT TYPE: {Style.RESET_ALL}(str, int, int)")
        prompt()
    else:
        return split_args


def search(unique_words, matrix, search_word, nb_synonyms, method):
    research = Recherche(unique_words, matrix, search_word, int(method))
    print_results(research.search(), int(nb_synonyms))

def print_results(results, nb_synonyms):
    print("\n")
    i = 0
    for result in results:
        i += 1
        print(f"{result[0]} --> {str(result[1])}") 
        if i == nb_synonyms: #print jusqu'au nombre de mots max
            break

def main():
    TAILLE_FENETRE = int(argv[1])
    ENCODAGE = str(argv[2])
    CHEMIN = str(argv[3])

    trainer = Entrainement(TAILLE_FENETRE, ENCODAGE, CHEMIN)

    if trainer.train() == "done":
        cls()
        word_to_search, nb_synonyms, method = prompt()
        search(trainer.unique_words, trainer.cooccurence_matrix, word_to_search, nb_synonyms, method)
    else:
        print(f"{Fore.RED}WRONG FILE PATH / TYPE{Style.RESET_ALL}")


if __name__ == "__main__":
    quit(main())