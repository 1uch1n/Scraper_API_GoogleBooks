# Auteur : Louis Leclerc
# Date : 06/10/2020 - 27/10/2020
# Description :
    # scraping API Google Books
    # recueille données bibliographiques à partir d'une recherche automatisée
    # input = liste de titres d'ouvrage en csv
    # output = csv des info Google Books sur ces ouvrages

# Notes sur l'API Google Books
    # Dans le vocabulaire de l'API, "volume" = informations bibliographies (titre, auteur, éditeur, date, description...)
    # Clé API pour les données publiques
    # authentification par token pour fonctionnalités plus poussées (pas nécessaire ici)
    # URL de requête-type = https://www.googleapis.com/books/v1/volumes?q=search+terms&key=yourAPIKey
    # plus d'info sur https://developers.google.com/books/docs/overview


# Importation des modules
import requests # pour scraper
import json     # pour lire le rendu de l'API
import csv      # pour écrire un csv en sortie du programme
from time import time # pour évaluer temps des requêtes GET

# localisation du fichier des valeurs à chercher
import os
os.chdir("/home/luchin/Documents/Projets Data/Scraping BDD theatre")

# définition de variables en amont
my_file = "input_table.csv"
urlAPI = "https://www.googleapis.com/books/v1/volumes?q="
keyAPI = "&key=AIzaSyCbxRGAL4pcMVeL0GoaE9cKVP5LmoimpCU"


# BLOC 1 : fonction qui convertit les rows d'un CSV en string et les retourne dans une liste
def open_file(file):
    with open(file, encoding="Windows-1252") as f:
        res = f.read().splitlines()
    f.close()
    return res # retourne une liste avec un row csv par élément (il faut un csv d'une seule colonne "titre" en input)


# BLOC 2 : fonction qui crée une URL de requête valide à partir d'un nom
def correct_url(input_title):
    output_title = ""
    for i in input_title:
        if i.isalnum() == True:
            output_title += i
        else:
            output_title += "+"
    return urlAPI + output_title + keyAPI


# BLOC 3 : fonction qui sélectionne les données pertinentes dans "volume" pour les 10 premiers résultats
def scraper(url):
    response = requests.get(url) #réponse de l'API <class 'requests.models.Response'>
    page_content = response.text #on transforme contenu de la page en string
    result_dct = json.loads(page_content) #on crée un dictionnaire à partir du contenu en string
    n = result_dct["totalItems"] #nombre de résultats (objet = int)
    if n > 10:     # si nombre de résultat > 10, on limite
        n = 10
    all_volume_info = result_dct["items"] #elements contenant les infos sur tous les résultats (objet = liste)
    res_dict = {} #dictionnaire vide pour accueillir les n résultats de "items"

    for i in range(0, n):
        some_volume_info = all_volume_info[i] #on va chercher info sur ième résultat (objet = dictio)
        volume_info = some_volume_info["volumeInfo"] #on prend infos qui nous intéresse (objet = dictio)

        res_list = [] #liste vide pour accueillir les infos de chaque résultat. Se réinitialise pour nouveaux résultats.
        msg_return_error = "N/A" #valeur vide si absence de données, pour s'assurer de la symétrie des colonnes en csv.

        # on définit chaque métadonné qui nous intéresse dans le dict en input
        # chaque valeur revient sous forme de string s'il y a la clé correspondantes
        # si absence de clé, la valeur sera par défaut le message d'erreur

        if "title" in volume_info:
            volume_title = volume_info["title"]
        else:
            volume_title = msg_return_error
        if "authors" in volume_info: # boucle qui produit un string d'un ou plusieurs auteurs
            all_volume_authors = volume_info["authors"] #retourne une liste d'un ou plusieurs auteurs
            count = len(all_volume_authors)
            volume_authors = ""
            for j in range(0, count):
                volume_authors += all_volume_authors[j]
                if count>0 and j+1<count: #ajoute une virgule entre les noms si jamais
                    volume_authors += ", "
        else:
            volume_authors = msg_return_error
        if "publisher" in volume_info:
            volume_publisher = volume_info["publisher"]
        else:
            volume_publisher = msg_return_error
        if "publishedDate" in volume_info:
            volume_date = volume_info["publishedDate"]
        else:
            volume_date = msg_return_error
        res_list.extend([volume_title, volume_authors, volume_publisher, volume_date])
        res_dict.update({i: res_list})
    return res_dict # retourne les éléments du DICT en input en liste d'éléments en output


# BLOC 5 : boucle de toutes les fonctions à partir d'un fichier en input
# Retourne une liste en output, et crée un CSV avec les données au passage

def general_function(input_file):
    with open("output_table.csv", "w", newline="", encoding="Windows-1252") as csvfile:
        final_res = []
        final_table = csv.writer(csvfile, delimiter="|")

        # étape 1 = créer liste d'URL à scraper
        list_valid_URL = []
        for i in open_file(input_file):
            list_valid_URL.extend([correct_url(i)])

        # étape 2 = scraper données de la liste d'URL et l'importer dans un CSV en ajoutant le temps de requête GET
        num_req = 1
        for j in list_valid_URL:
            start_time = time() # pour évaluer temps de chaque requête
            relevant_data = scraper(j)
            elapsed_time = time()-start_time
            print(f"Requête n°{num_req} : {round(elapsed_time, 2)} secondes")
            num_req += 1
            for j in relevant_data:
                final_table.writerow(relevant_data[j])
                final_res.extend(relevant_data[j])
    return final_res




print(general_function(my_file))