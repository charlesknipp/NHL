from pprint import pprint

class Game(object):

    actions = ["goal","primary assist","secondary assist"]

    # not sure how the data will be structured in bulk, but it must include
    # a sequence of points which could be split into tuples each tuple will 
    # have a frequency and significance per action

    def __init__(self):
        self.actions = []
        self.players = []
        self.read()

    # the idea here is that obs is in action like a goal, primary assist, and
    # secondary assist with information on player and score relative to the op-
    # posing team 

    def read(self,obs:dict):
        self.actions.append(obs)
        self.players.append(obs["players"])
    
    def getPlayers(self):
        return self.players

    def actionType(self,type):
        for action in self.actions:
            return action["type"]


class Player(object):

    # per post game data, each score type is associated with a player, so for a
    # given player, there exists a collection of statistics collected on a per
    # game level

    def __init__(self,name):
        self.name = name
        self.games = []
        self.goals = []
        self.pri_assists = []
        self.sec_assists = []
        self.schedule()

    def schedule(self,games):
        for game in games:
            if self.name in game.players:
                self.games.append(game)