import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from data import joe_thornton as jt
from data import conor_garland as cg

# this filters out games without recorded actions
def filterGames(obs,sig=False):
    if sig == False:
        return [r for r in obs if sum([i for i,j in r]) != 0]
    else:
        return [r for r in obs if sum([j for i,j in r]) != 0]

def getSignificantResults(matrix):
    # designed specifically to operate under the -6 to +6 reltive score structure
    reduced_matrix = filterGames(matrix,True)
    sig_obs = [[0]*13 for i in range(0,4)]

    # iterate over the reduced matrix
    for game in reduced_matrix:
        game_transpose = list(zip(*game))

        for sig in range(1,5):
            for i in range(0,13):
                if sig == game_transpose[1][i]:
                    sig_obs[sig-1][i] += game_transpose[0][i]

    return [sum(sig) for sig in zip(*sig_obs)]

def getResults(matrix):
    return [sum(game) for game in zip(*[[i for i,j in obs] for obs in matrix])]

def table(cum_list):
    return "".join(["%3d"]*len(cum_list)) % tuple(cum_list)

roster = {
    "conor garland": cg,
    "joe thornton": jt
}

for (name,player) in roster.items():
    cum_sig_goals = getSignificantResults(player.goal_matrix)
    cum_goals = getResults(player.goal_matrix)

    cum_sig_pri_assists = getSignificantResults(player.primary_assist_matrix)
    cum_pri_assists = getResults(player.primary_assist_matrix)

    cum_sig_sec_assists = getSignificantResults(player.secondary_assist_matrix)
    cum_sec_assists = getResults(player.secondary_assist_matrix)

    total_goals   = sum(cum_goals)
    total_assists = sum(cum_sec_assists) + sum(cum_pri_assists)
    total_points  = total_goals + total_assists
    confirmation  = [total_goals,total_assists,total_points]

    total_sig_goals   = sum(cum_sig_goals)
    total_sig_assists = sum(cum_sig_sec_assists) + sum(cum_sig_pri_assists)
    total_sig_points  = total_sig_goals + total_sig_assists
    sig_confirmation  = [total_sig_goals,total_sig_assists,total_sig_points]

    print("\n%-25s%35s" % (name,"points relative to opponent"))
    print("%25s %s" % (" ",table(range(-6,7))))

    print("\n%-25s %s" % ("total goals:",table(cum_goals)))
    print("%-25s %s" % ("total primary assists:",table(cum_pri_assists)))
    print("%-25s %s" % ("total secondary assists:",table(cum_sec_assists)))

    print("\n%-25s %s" % ("sig. goals:",table(cum_sig_goals)))
    print("%-25s %s" % ("sig. primary assists:",table(cum_sig_pri_assists)))
    print("%-25s %s\n" % ("sig. secondary assists:",table(cum_sig_sec_assists)))

    ratios = [sig_confirmation[i]/confirmation[i] for i in range(0,3)]
    print("ratios: ["+', '.join(['%.2f']*3) % tuple(ratios) +"]\n")
