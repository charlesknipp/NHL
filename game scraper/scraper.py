import requests

# calculates the significance of a given score
def calculateSignificance(relative_to_final):
    if relative_to_final == -1:
        return 1
    elif relative_to_final == 0:
        return 2
    elif relative_to_final == 1:
        return 3
    elif relative_to_final == 2:
        return 4
    else:
        return 0

# converts the player name to a less cluttered: FIRST_INITIAL.LAS_TNAME
def refine(str):
    str1 = "".join([i for i in str if not i.isdigit()])
    str2 = str1.strip().replace("()","")
    return str2

# implement a filtration for unwanted text in place of blank observations
def scrapeGame(game_num,season):
    szn = str(season)+str(season+1)
    url = "http://www.nhl.com/scores/htmlreports/"+szn+"/GS02"+str(game_num).zfill(4)+".HTM"
    web_page = requests.get(url)
    raw_html = web_page.text

    html = raw_html.split("\n")

    for i in range(len(html)):
        if "Goal Scorer" in html[i]:
            idx = i-7
            break

    table = []
    row = []

    while True:
        item = html[idx]

        if "<td" in item:
            row.append(item[item.find(">")+1:item.find("</")].strip())
        elif "</tr>" in item:
            table.append(row)
            row = []

        # this condition breaks the while loop
        if "</table>" in item:
            break

        idx += 1

    goals = table[1:len(table)]
    teams = list(set([goal[4] for goal in goals]))
    rel_pts = [0]*len(goals)
    rel_sig = [0]*len(goals)

    team1,team2 = 0,0
    score1,score2 = 0,0

    for i in range(len(goals)):
        if goals[i][4] == teams[0]:
            team1 += 1
            rel_pts[i] = team1-team2
        else:
            team2 += 1
            rel_pts[i] = team2-team1

    for i in range(len(goals)):
        if goals[i][4] == teams[0]:
            score1 += 1
            pts_rel =  score1 - team2
            rel_sig[i] = calculateSignificance(pts_rel)
        else:
            score2 += 1
            pts_rel =  score2 - team1
            rel_sig[i] = calculateSignificance(pts_rel)

    goal_scorers = [refine(goal[5]) for goal in goals]
    primary_assisters = [refine(goal[6]) for goal in goals]
    secondary_assisters = [refine(goal[7]) for goal in goals]

    goal_output = [False]*len(goals)
    assist1_output = [False]*len(goals)
    assist2_output = [False]*len(goals)

    for i in range(len(goals)):
        goal_output[i] = [goal_scorers[i],"goal",game_num,rel_pts[i],rel_sig[i]]
        assist1_output[i] = [primary_assisters[i],"primary assist",game_num,rel_pts[i],rel_sig[i]]
        assist2_output[i] = [secondary_assisters[i],"secondary assist",game_num,rel_pts[i],rel_sig[i]]

    return goal_output,assist1_output,assist2_output

output = scrapeGame(151,2016)
for out in output:
    print(out)