# Author : Louis Leclerc
# Date : 18/11/2020
# Description: scoring algorithm to evaluate whether search results from Google Books API are relevant

import csv
import os
import unidecode
os.chdir("/home/luchin/Documents/Projets Data/Scraping BDD theatre")

input_file = "test_file.csv"

#algorithm evaluating similarity between a result and the original book title
def similarity(title_A, title_B):

    #Initiating scores counting the number of letters in common between each title
    score_base_AtoB = 0
    score_base_BtoA = 0

    #each title is uniformized to make the comparison easier
    title_A = title_A.lower() #all in lowercase
    title_B = title_B.lower()
    title_A_sorted = sorted(title_A) #sort letter to facilitate the comparison in buckle
    title_B_sorted = sorted(title_B)
    title_A_list = [i for i in title_A_sorted if i.isalnum] #creating list gathering all alphanum characters
    title_B_list = [j for j in title_B_sorted if j.isalnum]
    title_A_list_tobeemptied = [i for i in title_A_sorted if i.isalnum] #similar lists to be emptied through method .remove()
    title_B_list_tobeemptied = [j for j in title_B_sorted if j.isalnum]

    #1st score: number of letters of the title A in the title B
    for k in title_A_list:
        if k in title_B_list_tobeemptied:
            title_B_list_tobeemptied.remove(k)
            score_base_AtoB += 1
        else:
            pass

    #2nd score: number of letters of the title B in the title A
    for l in title_B_list:
        if l in title_A_list_tobeemptied:
            title_A_list_tobeemptied.remove(l)
            score_base_BtoA += 1

    #Each score as a %, and average of the two
    score_percentage_title_A = score_base_AtoB / len(title_A_sorted) * 100
    score_percentage_title_B = score_base_BtoA / len(title_B_sorted) * 100
    score_final_average = (score_percentage_title_A + score_percentage_title_B) / 2

    return round(score_final_average, 2)


#reads a csv and returns a list of all results (each as a list)
def open_file(my_file):
    csv_reader = csv.reader(open(my_file, "r", encoding="Windows-1252"), delimiter="|")
    res = list(csv_reader)
    return res

#writes a csv and applies scoring function to the relevant keys
def add_to_csv(infile):
    list_res = open_file(infile)
    first_row = list_res[0]
    for row in list_res:        #BOUCLE POUR CHAQUE ROW SAUF FIRST ROW
        original_title = row[1]
        if original_title=="Original Title":
            pass
        else:
            for i in range(2, len(row), 4):
                print(f"Original Title: {original_title}")
                res_title = row[i]
                print(f"Row {list_res.index(row)} column {i} = {res_title}")
                score = similarity(original_title, res_title)
                print(f"Similarity score between {original_title} and {res_title}: {score}%")
            print("\n")

        #SEE HOW TO WRITE THIS DATA INTO A CSV (OR INSERT INTO A LIST...)



    #with open("scoring_output_table.csv", "w", newline="", encoding="utf-8") as outfile:
    #DEFINIR READER
    #ECRIRE CSV REPRENANT CHAQUE COLONNE ET INTEGRANT SCORING A COTE DE CHAQUE RESULTAT DE TITRE



#FINAL FUNCTION GO!
add_to_csv(input_file)
