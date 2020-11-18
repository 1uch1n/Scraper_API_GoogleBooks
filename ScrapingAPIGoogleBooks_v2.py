# Author: Louis Leclerc
# Creation date: 06/10/2020
# Last updated: 18/11/2020
# Description:
    # scraping API Google Books
    # collect bibliographic data from automated researches
    # input = CSV of book titles (only one column without first row)
    # output = CSV of Google Books data on these books

# Notes on Google Books API
    # In the API vocabulary, "volume" = bibliographic information (title, author, publisher, publication date, description...)
    # public data available through API Key
    # token identification for advanced researh (unnecessary here)
    # Request URL model = https://www.googleapis.com/books/v1/volumes?q=search+terms&key=yourAPIKey
    # more info on https://developers.google.com/books/docs/overview


#importing modules
import requests #to scrap
import json     #to read API's response
import csv      #to read input CSV and write CSV as output
import unidecode #to turn latin accentuated characters into URL compatible letters
from time import time #to  analyze time taken by request

# location of files
import os
os.chdir("/home/luchin/Documents/Projets Data/Scraping BDD theatre")

#definition of upstream variables
my_file = "input_table.csv"
urlAPI = "https://www.googleapis.com/books/v1/volumes?q="
keyAPI = "&key=AIzaSyCbxRGAL4pcMVeL0GoaE9cKVP5LmoimpCU"
country_query = "&country=CL" #set to research in Chile


#function converting each row of a single-column CSV into a string and returns them in a list
def open_file(file):
    with open(file, encoding="latin-1") as f:
        res = f.read().splitlines()
    f.close()
    return res #return a list with one row per element


#function creating a valid request URL from any title
def correct_url(input_title):
    output_title = ""
    for i in input_title:
        if i.isalnum() == True:
            output_title += i
        else:
            output_title += "+"
    compatible_title = unidecode.unidecode(output_title)
    res = urlAPI + compatible_title + keyAPI + country_query
    return res


#function selecting relevant data in "volume" for the first 10 results
#also prints time of the request
def scraper(url):
    print(f"Now scrapping URL: {url}")
    start_time = time()
    response = requests.get(url) #API answer: <class 'requests.models.Response'>
    elapsed_time = time() - start_time
    print(f"Scrap intent done \n Request response: {response} \n Response delay : {round(elapsed_time, 2)} seconds")
    page_content = response.text #turns page content into string
    result_dct = json.loads(page_content) #create dictionnary from string content
    n = result_dct["totalItems"] #number of results (object = int)
    if n > 10:     # if number of results > 10, we set a limit
        n = 10
    if "items" in result_dct:
        all_volume_info = result_dct["items"] #elements containing info on all résults (object = list)
    else:
        all_volume_info=[{"volumeInfo":""}] #creates empty dict in a list if no search result
    res_dict = {} #dictionnary to gather n results of "items"

    for i in range(0, n):
        some_volume_info = all_volume_info[i] #fetching info on the ith book (object = dict)
        volume_info = some_volume_info["volumeInfo"] #selecting the revelant info on this particular book (object = dict)

        res_list = [] #empty list to gather info on the book i, reinitialized if new book
        msg_return_error = "N/A" #empty value if no data, to ensure that output CSV will have symetric columns

        # defining the relevant metadata within input dict
        # all values are returned as a string if there's a corresponding key
        # apart from "authors", which is returned as a list (even if there's only one author)
        # if there is no corresponding key, the value returned will be the error message above

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
        print(f"Key {i} : {res_list}")
        res_dict.update({i: res_list})
    return res_dict


#buckle of all functions which returns a list from a CSV in input
#also writes a CSV with all the result, a first row and the original book title
def general_function(input_file):
    with open("output_table.csv", "w", newline="", encoding="utf-8") as csvfile:
        final_res = []
        final_table = csv.writer(csvfile, delimiter="|", quotechar="'")

        #creating first row
        first_row = ["Original Title"]
        for n in range(1, 11):
            ntitle = [f"Result {n} - Title"]
            nauthor = [f"Result {n} - Authors"]
            npublisher = [f"Result {n} - Publishers"]
            ndate = [f"Result {n} - Publication Date"]
            first_row.extend(ntitle)
            first_row.extend(nauthor)
            first_row.extend(npublisher)
            first_row.extend(ndate)
        final_table.writerow(first_row)

        #creating list of original titles and URLs to be scrapped
        list_original_titles = []
        list_valid_URL = []
        for i in open_file(input_file):
            list_original_titles.extend([i])
            list_valid_URL.extend([correct_url(i)])

        #data is scrapped from a list of URLs and imported into a CSV
        #also prints request delay
        num_req = 1
        total_time = 0
        for j in list_valid_URL:
            start_time = time() # pour évaluer temps de chaque requête
            print(f"About to scrap data on: '{list_original_titles[list_valid_URL.index(j)]}'")
            relevant_data = scraper(j)
            elapsed_time = time() - start_time
            num_req += 1
            total_time += elapsed_time
            list_data = []
            list_data.extend([list_original_titles[list_valid_URL.index(j)]])
            for n in relevant_data:
                list_data.extend(relevant_data[n])
            final_table.writerow(list_data)
            final_res.extend(list_data)
            print(f"Request {num_req} done\n New row added to the final table: {list_data} \n")
        avg_time = total_time/num_req
        print(f"Average request time: {round(avg_time, 2)} seconds")
    return final_res


print(general_function(my_file))
