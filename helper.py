import pandas as pd

deli = pd.read_csv('deliveries.csv')
match = pd.read_csv('matches.csv')
df = match[~match.winner.isna()]


# helper.py

def overs_list(deli):

    overs = deli['over'].unique().tolist()
    return overs

def season_list(match):

    seasons = match['season'].unique().tolist()
    seasons.sort()
    seasons.insert(0, 'Overall')
    return seasons


def team_list(match):

    teams = list(set(match['team1'].unique()).union(set(match['team2'].unique())))
    teams.sort()
    teams.insert(0, 'Overall')
    return teams
