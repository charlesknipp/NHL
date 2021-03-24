import pandas as pd

def getGameReport(url):
    pass

url = "http://www.nhl.com/scores/htmlreports/20202021/GS020151.HTM"
tables = pd.read_html(url)

# table[9] has the good shit
players = list(tables[9][5])
players.remove("Goal Scorer")

refine = lambda x: ''.join([i for i in x if not i.isdigit()])

# now we need to match the players from the sheet the NHL roster overall
players = [refine(player).strip().replace("()","") for player in players]