# Author: 1uch1n (1uch1n@protonmail.com)
# Creation date: 28/10/2020
# Last update: 14/02/2022
# Description: scoring algorithm to evaluate whether search results from Google Books API are relevant

import csv
import os
import unidecode
os.chdir("/home/luchin/Documents/AmIntel/Projets Data/Scraping BDD theatre")

input_file = "scoring_todo.csv"

def similarity(title_A, title_B):
    '''algorithm evaluating similarity between a result and the original book title by counting the number of letters
    in common between each title'''

    # initiate scores
    score_base_AtoB = 0
    score_base_BtoA = 0

    # uniformize each title to make the comparison easier
    # first, all in lowercase and print titles to check
    title_A = title_A.lower()
    print(f"Title A: {title_A}")
    title_B = title_B.lower()
    print(f"Title B: {title_B}")

    # sort letter to facilitate the comparison in buckle
    title_A_sorted = sorted(title_A)
    title_B_sorted = sorted(title_B)

    # creating list gathering all alphanum characters
    title_A_list = [i for i in title_A_sorted if i.isalnum]
    title_B_list = [j for j in title_B_sorted if j.isalnum]

    # similar lists to be emptied through method .remove()
    title_A_list_tobeemptied = [i for i in title_A_sorted if i.isalnum]
    title_B_list_tobeemptied = [j for j in title_B_sorted if j.isalnum]

    # 1st intermediary score: number of letters of the title A in the title B
    for k in title_A_list:
        if k in title_B_list_tobeemptied:
            title_B_list_tobeemptied.remove(k)
            score_base_AtoB += 1
        else:
            pass

    # 2nd intermediary score: number of letters of the title B in the title A
    for l in title_B_list:
        if l in title_A_list_tobeemptied:
            title_A_list_tobeemptied.remove(l)
            score_base_BtoA += 1

    # express each intermediary score as a percentage
    score_percentage_title_A = score_base_AtoB / len(title_A_sorted) * 100
    score_percentage_title_B = score_base_BtoA / len(title_B_sorted) * 100

    # return the average of the two scores and print the result to check
    score_final_average = (score_percentage_title_A + score_percentage_title_B) / 2
    print(f"Final similarity score: {score_final_average}%")
    return round(score_final_average, 2)


def open_file(my_file):
    ''' reads a csv and returns a list of all results (each as a list)'''
    csv_reader = csv.reader(open(my_file, "r", encoding="latin-1"), delimiter="|")
    res = list(csv_reader)
    print(f"Reading list of rows of .csv input file \n")
    return res

def add_to_csv(infile):
    '''writes a csv and applies scoring function to the relevant keys'''
    with open("scoring_done.csv", "w", newline="", encoding="latin-1") as outfile:
        list_res = open_file(infile)
        final_table = csv.writer(outfile, delimiter="|", quotechar="'")

        # define first row
        first_row = [list_res[0][0]]
        res_num = 1
        for n in range(1, len(list_res[0]), 4):
            score_prob = f"Result {res_num} - Score"
            first_row.extend([score_prob])
            first_row.extend([list_res[0][n]])
            first_row.extend([list_res[0][n+1]])
            first_row.extend([list_res[0][n+2]])
            first_row.extend([list_res[0][n+3]])
            res_num+=1
        final_table.writerow(first_row)
        print(f"First row written: {first_row}\n")

        # loop for each row
        for row in list_res:
            original_title = row[0]

            # set empty list to add scores to the books' data
            new_row = []

            # passe on the first row
            if original_title=="Original Title":
                pass

            else:
                print(f"\nRow under evaluation: {row}\n")
                print(f"\nSTARTING EVALUATING COMPARISON WITH ORIGINAL TITLE N°{list_res.index(row)}: \n{original_title}\n")
                print(f"Adding the original title to the new row: {row[0]}")
                new_row.extend([row[0]])

                # set empty dict to add the book data and its score (key= score, values=book data)
                unsorted_data_dict = {}

                # set an empty list to add dict values according to their score, in descending order
                sorted_data_list = []

                for i in range(1, len(row), 4):

                    # print book title under evaluation
                    print(f"\nBOOK TITLE UNDER EVALUATION:\n{row[i]}\n(Row {list_res.index(row)} column {i})\n")

                    # set empty list to gather data and score of the title i
                    data_with_score = []
                    score = similarity(original_title, row[i])
                    print(f"Similarity score between {original_title} and {row[i]}: {score}%")

                    # list all the data on the book
                    data_with_score.extend([score])
                    data_with_score.extend([row[i]])
                    data_with_score.extend([row[i+1]])
                    data_with_score.extend([row[i+2]])
                    data_with_score.extend([row[i+3]])
                    print(f"\nNew data added after row {list_res.index(row)} column {i} => {data_with_score}")

                    # add all the data to the dict
                    # and watch for possible equal scores
                    if score in unsorted_data_dict.keys():
                        score -= 0.01
                        unsorted_data_dict[score] = data_with_score
                    else:
                        unsorted_data_dict[score] = data_with_score
                print("\n"*3+f"unsorted_data_dict = {unsorted_data_dict}")

                for key in range(len(unsorted_data_dict)):
                    # select hightest key of the dict
                    all_keys = unsorted_data_dict.keys()
                    max_key = max(all_keys)
                    # add corresponding value to sorted_data_list
                    # and erase value of the dict
                    sorted_data_list.extend(unsorted_data_dict.pop(max_key))

                print(f"\nsorted_data_list={sorted_data_list}")
                new_row.extend(sorted_data_list)
                print(f"\nAdding new row: {new_row}")
                final_table.writerow(new_row)
                print("\n"*5)

    return final_table
