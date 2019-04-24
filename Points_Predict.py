#Professor_code.py
# see: https://github.com/prof-rossetti/georgetown-opim-243-201901/blob/master/notes/python/packages/beautifulsoup.md

from bs4 import BeautifulSoup
import requests
#import pandas as pd

#
##USER INTERFACE and INPUTS
#
print("------------------")
print("Welcome to OPIM analytics' college basketball points predictor tool")
print("Here you will enter two D1 basketball teams, and our program will spit out the projected score based off of Kenpom data")
print("------------------")
User_team1=input("Please enter team 1:")
User_team2=input("Please enter team 2:")
print("GETTING HTML CONTENTS...")
#
##SCRAPING KENPOM DATA 
#
#print(f"The score for {User_team1} vs {User_team2} is:")

# TODO: use the requests package to get the contents of the page, instead of reading from file
# ... if you need to get behind the paywall to access the page, you can use the selenium package to automate the login process
print("RATINGS TABLE", type(ratings_table))

rows = ratings_table.find("tbody").findAll("tr") 
# weird, seeing some thead rows (like Strength of Schedule) in here as well...
print("ROWS", type(rows), len(rows))
#breakpoint()

for row in rows:
    print("--------------------")
    # print(type(row)) #> <class 'bs4.element.Tag'>
    #cells = row.findAll("td")
    # after the 40th team (end of first table), seeing:
    #> IndexError: list index out of range

    try:
        cells = row.findAll("td")
        rank = cells[0].text
        #team_name = cells[1].text #> includes the rank as well, so if you just want the team name...
        team_name = cells[1].find("a").text
        print(f"{rank}) {User_team1} ")
    except IndexError as e:
        print(e)
        #breakpoint()
        # looks like offending rows include:

        # <tr class="thead1">
        #   <th class="hard_left"></th>
        #   <th class="next_left"></th>
        #   <th colspan="3"></th>
        #   <th class="divide" colspan="4">
        #   </th><th class="divide" colspan="2">
        #   </th><th class="divide" colspan="2"></th>
        #   <th class="divide" colspan="6">Strength of Schedule</th>
        #   <th class="divide" colspan="2">NCSOS</th>
        # </tr>
        # hoefully we can just skip them
        #next()
