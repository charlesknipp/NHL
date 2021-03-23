from pprint import pprint

class Point():
    pts     = 0
    goals   = 0
    assists = 0

    primary_assists   = 0
    secondary_assists = 0

    def __init__(self):
        Point.pts += 1

    def getPoints(self):
        return self.pts

    def getGoals(self):
        return self.goals

class Goal(Point):
    Point.goals += 1
    pass

class PrimaryAssist(Point):
    Point.assists += 1
    Point.primary_assists += 1
    pass

class SecondaryAssist(Point):
    Point.assists += 1
    Point.secondary_assists += 1
    pass

goal = Goal()
pprint(Point.__dict__)