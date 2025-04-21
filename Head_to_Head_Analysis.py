import pandas as pd
import helper
import streamlit as st

deli = pd.read_csv('deliveries.csv')
match = pd.read_csv('matches.csv')
df = match[~match.winner.isna()]

# helper.main()
helper.overs_list(deli)
helper.season_list(match)
helper.team_list(match)

def team_list(match):

    teams = list(set(match['team1'].unique()).union(set(match['team2'].unique())))
    teams.sort()
    teams.insert(0, 'Overall')
    return teams

def head_to_head(team1, team2):
    df = match.copy()
    df = df[((df['team1'] == team1) & (df['team2'] == team2)) |
            ((df['team1'] == team2) & (df['team2'] == team1))]

    result_df = df['winner'].value_counts().reset_index()
    result_df.columns = ['Team', 'Wins']
    result_df = result_df[result_df['Team'].isin([team1, team2])]

    result_df.loc[len(result_df.index)] = ['No Result', len(df[df['result'] == 'no result'])]
    result_df = result_df.sort_values(by='Wins', ascending=False).reset_index(drop=True)
    return result_df

def bowl_vs_bat():
    df = deli[deli['is_wicket'] == 1]
    df = df[df['dismissal_kind'].isin([
        'bowled', 'caught', 'lbw', 'stumped', 'caught and bowled', 'hit wicket'
    ])]
    combo = df.groupby(['bowler', 'player_dismissed']).size().reset_index(name='Wickets')
    combo = combo.sort_values(by='Wickets', ascending=False).head(10)
    combo.columns = ['Bowler', 'Batsman', 'Wickets']
    return combo

def bat_vs_bowl():
    df = deli.copy()
    combo = df.groupby(['batter', 'bowler'])['batsman_runs'].sum().reset_index()
    combo = combo.sort_values(by='batsman_runs', ascending=False).head(10)
    combo.columns = ['Batsman', 'Bowler', 'Runs']
    return combo
