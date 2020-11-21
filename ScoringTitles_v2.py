# Author: Louis Leclerc
# Creation date: 28/10/2020
# Last update: 21/11/2020
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
    csv_reader = csv.reader(open(my_file, "r", encoding="latin-1"), delimiter="|")
    res = list(csv_reader)
    return res

#writes a csv and applies scoring function to the relevant keys
def add_to_csv(infile):
    with open("test_file_output.csv", "w", newline="", encoding="utf-8") as outfile:
        list_res = open_file(infile)
        final_table = csv.writer(outfile, delimiter="|", quotechar="'")

        #defining the first row
        first_row = [list_res[0][0], list_res[0][1]]
        res_num = 1
        for n in range(2, len(list_res[0]), 4):
            score_prob = f"Result {res_num} - Score"
            first_row.extend([score_prob])
            first_row.extend([list_res[0][n]])
            first_row.extend([list_res[0][n+1]])
            first_row.extend([list_res[0][n+2]])
            first_row.extend([list_res[0][n+3]])
            res_num+=1
        final_table.writerow(first_row)

        for row in list_res:        #buckle for each row
            original_title = row[1]
            new_row = []            #to add scores to the books' data

            if original_title=="Original Title": #passes on the first row
                pass

            else:
                print(f"Original Title n°{list_res.index(row)}: {original_title}")
                new_row.extend([row[0]])
                new_row.extend([row[1]])

                unsorted_data_dict = {} #a buckle will add the book data+score in a dict (key= score, values=book data)
                sorted_data_list = [] #dict values will be added to a list according to their score, in descending order

                for i in range(2, len(row), 4):
                    print(f"Row {list_res.index(row)} column {i} = {row[i]}") #shows book title under evaluation
                    data_with_score = [] #list to gather data and score of the title i
                    score = similarity(original_title, row[i])
                    print(f"Similarity score between {original_title} and {row[i]}: {score}%")

                    #list of the data on a book
                    data_with_score.extend([score])
                    data_with_score.extend([row[i]])
                    data_with_score.extend([row[i+1]])
                    data_with_score.extend([row[i+2]])
                    data_with_score.extend([row[i+3]])
                    print(f"New data for {i} => {data_with_score}")

                    #adding everything to a dict
                    if score in unsorted_data_dict.keys(): #watch for possible equal scores
                        score -= 0.01
                        unsorted_data_dict[score] = data_with_score
                    else:
                        unsorted_data_dict[score] = data_with_score
                print(f"unsorted_data_dict = {unsorted_data_dict}")
                for key in range(len(unsorted_data_dict)):
                    #selecting hightest key of the dict
                    all_keys = unsorted_data_dict.keys()
                    max_key = max(all_keys)
                    sorted_data_list.extend(unsorted_data_dict.pop(max_key)) #adding corresponding value to sorted_data_list
                    #erasing value of the dict
                print(f"sorted_data_list={sorted_data_list}")
                new_row.extend(sorted_data_list)
                final_table.writerow(new_row)
                print("\n")
    return final_table


#FINAL FUNCTION
add_to_csv(input_file)
