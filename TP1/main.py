from sys import argv
import os
import msvcrt as msv
from colorama import init, Fore, Style

from entrainement import *
from recherche import *

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def prompt():
    print("""\nEntrez un mot, le nombre de synonymes que vous voulez et la methode de calcul,
i.e. produit scalaire: 0, least-squares: 1, city-block: 2""")

    arguments = input("\ntapez Q pour quitter.\n\n")
    split_args = arguments.split(" ")
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
        coocurences(mot=split_args[0], nb_synonymes=split_args[1], methode_calcul=split_args[2])


def coocurences(mot, nb_synonymes, methode_calcul):
    print("\nCoocurences ICI")
    #calculer 

    #restart prompt quand fini
    prompt()

def afficher_resultats():
    #affichage des resultats
    return 0
    city_block = 0

    return city_block

def create_trainer():
    pass


if __name__ == "__main__":
    TAILLE_FENETRE = int(argv[1])
    ENCODAGE = str(argv[2])
    CHEMIN = str(argv[3])

    create_trainer(TAILLE_FENETRE, ENCODAGE, CHEMIN)

    init(convert=True) #for Colorama

    cls()
    prompt()