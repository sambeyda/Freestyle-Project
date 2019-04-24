# see: https://github.com/prof-rossetti/georgetown-opim-243-201901/blob/master/notes/python/packages/beautifulsoup.md

from bs4 import BeautifulSoup

print("GETTING HTML CONTENTS...")

# TODO: use the requests package to get the contents of the page, instead of reading from file
# ... if you need to get behind the paywall to access the page, you can use the selenium package to automate the login process

html_filepath = "kenpom-page.html"

soup = BeautifulSoup(open(html_filepath), features="lxml") # added the features param after seeing a warning message about it

ratings_table = soup.find("table", id="ratings-table")
print("RATINGS TABLE", type(ratings_table))

rows = ratings_table.find("tbody").findAll("tr") # weird, seeing some thead rows (like Strength of Schedule) in here as well...
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
        print(f"{rank}) {team_name}")
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
