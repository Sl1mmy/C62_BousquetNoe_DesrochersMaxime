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
    print("""\nEntrez un mot, le nombre de synonymes que vous voulez et la methode de calcul,
i.e. produit scalaire: 0, least-squares: 1, city-block: 2""")

    arguments = input("\ntapez Q pour quitter.\n\n")
    split_args = arguments.split()

    word_to_search, nb_synonyms, method = split_args

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
        coocurences(word_to_search, nb_synonyms, method)


def coocurences(mot, nb_synonymes, methode_calcul):
    research = Recherche()

    print("\RESULTAT") 
    #TODO: print_results( results, nb_synonyms)
    

    prompt() #restart prompt quand fini 

def print_results(results, nb_synonyms):
    #affichage des resultats
    print("\n")
    i = 0
    for result in results:
        i += 1
        #print(f"{}") 
        if i == nb_synonyms:
            break

def main():
    
    
    TAILLE_FENETRE = int(argv[1])
    ENCODAGE = str(argv[2])
    CHEMIN = str(argv[3])

    trainer = Entrainement(TAILLE_FENETRE, ENCODAGE, CHEMIN)

    if trainer.train() == "done":
        cls()
        prompt()
    else:
        print(f"{Fore.RED}WRONG FILE PATH / TYPE{Style.RESET_ALL}")


if __name__ == "__main__":
    quit(main())