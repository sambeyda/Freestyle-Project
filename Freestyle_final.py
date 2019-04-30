
from bs4 import BeautifulSoup
import requests
import statistics

#
##USER INTERFACE and INPUTS
#
print("------------------")
print("Welcome to OPIM analytics' college basketball points predictor tool")
print("Here you will enter two D1 basketball teams, and our program will spit out the projected score based off of Kenpom data")
print("------------------")

###TODO:Will need to put data validation to make sure user inputs valid teams!!!!

User_team1=input("Please enter team 1: ")
User_team2=input("Please enter team 2: ")

print("SCRAPING DATA")
#
##SCRAPING KENPOM DATA 
#

base_filepath = 'http://kenpom.com/index.php' #changed professor's filepath

#Use Requests package to get contents of page

raw_data = requests.get(base_filepath)
soup=BeautifulSoup(raw_data.text, "lxml") #Gets rid of Beautiful Soup error
ratings_table = soup.find("table", id="ratings-table")

#print("RATINGS TABLE", type(ratings_table))

rows = ratings_table.find("tbody").findAll("tr") 


teams=[] #Empty list for future appendage

for row in rows: #Loop
    try:
        cells = row.findAll("td")
        rank = cells[0].text
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
        print("") #TODO: Get rid of this
        #breakpoint()
 
##
#Matching User Input to Team in List
##
print("------------------")
try: #DATA VALIDATION to exit script if user's inputted teams aren't found
  matching_team1 = [t for t in teams if t["Name"]==User_team1]
  matching_team2 = [t for t in teams if t["Name"]==User_team2]
  matching_team1_tempo = matching_team1[0]["Tempo"] #Team1 tempo
  matching_team2_tempo = matching_team2[0]["Tempo"] #Team2 tempo
except IndexError:
  print("Your inputted teams cannot be found, please run the script again!")
  exit()


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
print("ALGORITHM SUCCESSFUL")
print("------------------")
print(f"The total predicted amount of points scored in a hypothetical game between {User_team1} and {User_team2} is: {int(Final_score)}")
print("------------------")
print("PLEASE INVEST WISELY: OPIM ANALYTICS DOES NOT TAKE RESPONSIBILITY!!!!")
