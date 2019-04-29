#Professor_code.py
# see: https://github.com/prof-rossetti/georgetown-opim-243-201901/blob/master/notes/python/packages/beautifulsoup.md

from bs4 import BeautifulSoup
import requests
import statistics
#import pandas as pd

#
##USER INTERFACE and INPUTS
#
print("------------------")
print("Welcome to OPIM analytics' college basketball points predictor tool")
print("Here you will enter two D1 basketball teams, and our program will spit out the projected score based off of Kenpom data")
print("------------------")
###Will need to put data validation to make sure user inputs valid teams!!!!
User_team1=input("Please enter team 1: ")
User_team2=input("Please enter team 2: ")
print("SCRAPING DATA")
#
##SCRAPING KENPOM DATA 
#
#print(f"The score for {User_team1} vs {User_team2} is:")

base_filepath = 'http://kenpom.com/index.php' #changed professor's filepath
#Use Requests package to get contents of page
raw_data = requests.get(base_filepath)
soup=BeautifulSoup(raw_data.text, "lxml") #Gets rid of Beautiful Soup error
ratings_table = soup.find("table", id="ratings-table")

print("RATINGS TABLE", type(ratings_table))

rows = ratings_table.find("tbody").findAll("tr") 

# weird, seeing some thead rows (like Strength of Schedule) in here as well...
print("ROWS", type(rows), len(rows))
#breakpoint()
teams=[]

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
        AdjO=cells[5].text #Teams adjusted offensive efficiency
        AdjD=cells[7].text #Teams adjusted Defense
        Tempo=cells[9].text #Teams Tempo
        team = {
          "Name": team_name,
          "AdjO": float(AdjO),
          "AdjD": float(AdjD),
          "Tempo": float(Tempo),
        }
        teams.append(team)
        #print(f"{rank}) {team_name} Adjusted Offense:  {AdjO}, Adjusted Defense: {AdjD}, Tempo: {Tempo} ")
    except IndexError as e:
        print("")
        #breakpoint()
 
##
#Matching User Input to Team in List
##
matching_team1 = [t for t in teams if t["Name"]==User_team1]
matching_team2 = [t for t in teams if t["Name"]==User_team2]
matching_team1_tempo = matching_team1[0]["Tempo"] #Team1 tempo
matching_team2_tempo = matching_team2[0]["Tempo"] #Team2 tempo

#Efficiency factor: How well Team1's offense will perform against Team2's defense
matching_team1_efficiency_adv = statistics.mean([matching_team1[0]["AdjO"],matching_team2[0]["AdjD"]])
matching_team1_std=(matching_team1_efficiency_adv/100) #Standardize per 100 possesions
matching_team2_efficiency_adv = statistics.mean([matching_team2[0]["AdjO"],matching_team1[0]["AdjD"]])
matching_team2_std=(matching_team2_efficiency_adv/100) #Standardize per 100 possesions

##
# TOTAL POINTS CALCULATION
## Average of teams standard efficiency advantage (points per 100 possesions) multiplied by tempo (how many possesions)
total_efficiency_factor = statistics.mean([matching_team1_std,matching_team2_std])*2
Average_tempo=statistics.mean([matching_team1_tempo,matching_team2_tempo])
Final_score=total_efficiency_factor*Average_tempo
print("--------------------")
print("ALGORITHM SUCCESSFUL")
print(f"The total predicted amount of points scored in a hypothetical game between {User_team1} and {User_team2} is: {Final_score}")
