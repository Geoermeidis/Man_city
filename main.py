from bs4 import BeautifulSoup as Bs
import requests
import re
import pandas as pd


url = "https://www.mancity.com/results"
page = requests.get(url)
soup = Bs(page.content, 'html.parser')

scores_ = soup.find_all('div', class_="fixture-body__score-goals")
times_ = soup.find_all('time', class_="fixture-header__competition-time")
comp_ = soup.find_all('p', class_="fixture-header__competition-name")
ground_ = soup.find_all('li', class_="grid grid-bleed fixture fixtures-list-item")
result_ = soup.find_all('svg', class_="game-result__icon")

city_goals, op_goals, dates, comps, opponents, ground, results = [], [], [], [], [], [], []

for elem in scores_:

    temp = elem["aria-label"]
    if "Manchester City" in temp:
        city_goals.append(int(re.findall("\d+", elem["aria-label"])[0]))
    else:
        target = temp.index(" score")
        opponents.append(temp[0:target])
        op_goals.append(int(re.findall("\d+", elem["aria-label"])[0]))

for elem in ground_:
    temp = elem["aria-label"]
    limit = temp.index("versus")
    target = temp.index("Manchester City")
    if target < limit:
        ground.append("H")
    else:
        ground.append("A")

for i in range(len(times_)):
    date = times_[i].get_text()
    date = re.sub("\n", "", date)
    comp = comp_[i].get_text()
    comp = re.sub("\n", "", comp)

    dates.append(date)
    comps.append(comp)

for elem in result_:
    temp = elem["aria-label"]
    print(temp)
    if temp[0] == "W" or temp[0] == "w":
        results.append("W")
    elif temp[0] == "L" or temp[0] == "l":
        results.append("L")
    else:
        results.append("D")

# print(f"Manchester City has scored {sum(city_goals)} goals and has conceded {sum(op_goals)} goals")

df = pd.DataFrame({"Date": [elem for elem in dates], "Competition": [elem for elem in comps],
                   "City Goals": [elem for elem in city_goals], "Opponent goals": [elem for elem in op_goals],
                   "Opponent": [elem for elem in opponents], "Ground": [elem for elem in ground],
                   "Result": [elem for elem in results]})

print(df.to_string())

# see of home or away , ground
# opposite team name
# show if it is a win, draw or lose
