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
###Will need to put data validation to make sure user inputs valid teams!!!!
User_team1=input("Please enter team 1:")
User_team2=input("Please enter team 2:")
print("GETTING HTML CONTENTS...")
#
##SCRAPING KENPOM DATA 
#
#print(f"The score for {User_team1} vs {User_team2} is:")

base_filepath = 'http://kenpom.com/index.php' #changed professor's filepath
#Use Requests package to get contents of page
raw_data = requests.get(base_filepath)
soup=BeautifulSoup(raw_data.text)
ratings_table = soup.find("table", id="ratings-table")

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
        print(f"{rank}) {team_name} ")
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
