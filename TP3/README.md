
# TP2 : Synonyme BD
 
Fichier de configuration pour le TP2 du cours 62 - Donnés, Mégadonnés et Intelligence Artificielle 2.

## Options de lancement
Chaque options peuvent être fournies dans n'importe quel ordre, elles sont séparés pour 3 opérations distinctes:
 - `-e` spécifier l'opération d'entrainement
 - `-r` spécifier l'opération de recherche
 - `-b` spécifier l'opération de regénération de la BD.

**Entrainement**
 Voici les options utilisés pour l'entrainement, les valeurs `<valeur : datatype>` doivent suivre l'option, précédé d'un espace, ces options sont obligatoires :
 - `-t <taille : int>` : taille de fenêtre
 - `--encodage <encodage : String> / --enc <encodage : String>` : encodage du fichier
 - `--chemin <chemin : String> / --ch <chemin: String>` : chemin du fichier d'entrainement

> Exemple : `H:\GITHUB\C62_BousquetNoe_DesrochersMaxime\TP2>main.py -e -t 5 --encodage utf-8 --chemin textes\GerminalUTF8.txt`

**Recherche** :
Voici les options utilisés pour la recherche, les valeurs `<valeur : datatype>` doivent suivre l'option, précédé d'un espace, ces options sont obligatoires :
 - `-t <taille : int>` : taille de fenêtre

> Exemple : `H:\GITHUB\C62_BousquetNoe_DesrochersMaxime\TP2>main.py -r -t 5`

**Clustering** :
Voici les options utilisés pour le Clustering et KNN, les valeurs `<valeur : datatype>` doivent suivre l'option, précédé d'un espace, ces options sont obligatoires :
 - `-t <taille : int>` : taille de fenêtre
 - `-n <nombre : int>` : nombre de centroïdes
 - `-k <nombre : int>` : nombre de voisins
 - `-m <nombre : int>` : nombre maximal de mots à afficher par cluster
 - `--normaliser / --norm` : normalise les valeurs du KNN

> Exemple : `H:\GITHUB\C62_BousquetNoe_DesrochersMaxime\TP2>main.py -c -t 5 -n 5 -k 5 -m 10 --normaliser`

**Regénération** :
Il n'y a pas d'options supplémentaires pour la regénération de la BD.
> Exemple : `H:\GITHUB\C62_BousquetNoe_DesrochersMaxime\TP2>main.py -b`


## Options de recherche après lancement

Après avoir entré l'opération de recherche, il faut entrer un mot, le nombre de synonymes voulu et la méthode de calcul selon les trois possibles :
- `0` : produit scalaire
- `1` : least-square
- `2` : city-block

> Exemple : `bras 12 2`

Pour quitter le programme, appuyez sur `q`