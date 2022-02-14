# Author: 1uch1n (1uch1n@protonmail.com)
# Creation date: 06/10/2020
# Last update: 14/02/2022
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


#import modules
import requests #to scrap
import json     #to read API's response
import csv      #to read input CSV and write CSV as output
import unidecode #to turn latin accentuated characters into URL compatible letters
from time import time #to analyze time taken by request
from time import sleep #to pause scraping process

# location of files
import os
os.chdir(input('Set the location of the input files:\n->'))

# definition of upstream variables
my_file = input('What is the name of the input file?:\n->')
urlAPI = "https://www.googleapis.com/books/v1/volumes?q="
keyAPI = "&key=AIzaSyCbxRGAL4pcMVeL0GoaE9cKVP5LmoimpCU"


def open_file(file):
    '''convert each row of a single-column CSV into a string and returns them as a list'''
    res = []
    with open(file, encoding="utf-8") as f:
        rdr = csv.reader(f)
        for row in rdr:
            print(row)
            res.append(row[0])
    f.close()
    print(res)
    # return a list with one row per element
    return res


def correct_url(input_title):
    '''create a valid request URL from any title'''
    output_title = ""
    for i in input_title:
        if i.isalnum() == True:
            output_title += i
        else:
            output_title += "+"
    res = urlAPI + output_title + keyAPI
    return res


def scraper(url):
    '''select relevant data in "volume" for the first 10 results'''

    # print time of the request
    print(f"Now scrapping URL: {url}")
    start_time = time()
    response = requests.get(url) # API answer: <class 'requests.models.Response'>
    elapsed_time = time() - start_time
    print(f"Scrap intent done \n Request response: {response} \n Response delay : {round(elapsed_time, 2)} seconds")

    # turn page content into string
    page_content = response.text

    # create dictionnary from string content
    result_dct = json.loads(page_content)

    # number of results (object = int)
    n = result_dct["totalItems"]

    # if number of results > 10, we set a limit
    if n > 10:
        n = 10

    # elements containing info on all results (object = list)
    if "items" in result_dct:
        all_volume_info = result_dct["items"]

    # create empty dict in a list if no search result
    else:
        all_volume_info=[{"volumeInfo":""}]

    # dictionnary to gather n results of "items"
    res_dict = {}

    # fetch info on the i^th book (object = dict)
    for i in range(0, n):
        some_volume_info = all_volume_info[i]
        # select the revelant info on this particular book (object = dict)
        volume_info = some_volume_info["volumeInfo"]

        # empty list to gather info on the book i, reinitialized if new book
        res_list = []
        # empty value if no data, to ensure that output CSV will have symetric columns
        msg_return_error = "N/A"

        # define the relevant metadata within input dict
        # all values are returned as a string if there's a corresponding key
        # apart from "authors", which is returned as a list (even if there's only one author)
        # if there is no corresponding key, the value returned will be the error message above

        if "title" in volume_info:
            volume_title = volume_info["title"]

        else:
            volume_title = msg_return_error

        # gather all author names of a specific volume
        if "authors" in volume_info:
            # list of one or several authors
            all_volume_authors = volume_info["authors"]
            # count the number of authors
            count = len(all_volume_authors)
            # loop generating a string of one or several authors
            volume_authors = ""
            for j in range(0, count):
                volume_authors += all_volume_authors[j]
                #adds a coma between names if necessary
                if count>0 and j+1<count:
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


def general_function(input_file):
    ''' loop of all functions which returns a list from a CSV in input
     and write a CSV with all the result, a first row and the original book title'''
    with open("scoring_todo.csv", "w", newline="", encoding="utf-8") as csvfile:
        final_res = []
        final_table = csv.writer(csvfile, delimiter="|", quotechar="'")

        #create first row
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

        #create list of original titles and URLs to be scrapped
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
            if num_req%100==0:
                pause_time = time()
                print("\nPause scraping (long)")
                sleep(300)
                print(f"Pause duration: {time() - pause_time}\n*5")
            elif num_req%10==0:
                pause_time = time()
                print("\nPause scraping (short)")
                sleep(10)
                print(f"Pause duration: {time() - pause_time}\n")
        avg_time = total_time/num_req
        print(f"Average request time: {round(avg_time, 2)} seconds")
    return final_res


print(general_function(my_file))
