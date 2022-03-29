Enhance a bibliography with Google Books search engine

Two-steps: data mining and scoring

1st step: automated data collection
	
Objective: Collecting bibliographic data from automated researches made on https://books.google.com/

Source: Google Books API. Example of the Google Books data of a search on the term “Hamlet”: https://www.googleapis.com/books/v1/volumes?q=Hamlet

Short description of the script:

Input = List of book titles

Ouput = Selection of relevant data (title, author, publisher, publication date, description) for each of the first ten results of Google Books for each title


2nd step: relevancy evaluation through scoring

Problem: Searches from Google Books can return very diverse results, sometimes quite different from the search request.

Objective: Selecting the closest result to the original search request among the first 10 results of Google.

Short description of the script: A very simple scoring algorythm evaluates to which extent each result from Google Books is similar to the original search request

Input = original books title + 10 search results from Google Books

Output = Percentage of similarity between the original title and the search results. All results are sorted according to their score, in order to immediately identify which results have the highest similarity score.
