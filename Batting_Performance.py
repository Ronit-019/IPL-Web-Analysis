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


def sixes():
    df = deli[deli['batsman_runs'] == 6]
    sixes = df['batter'].value_counts().head(10).reset_index()
    sixes.columns = ['Batsman', 'Sixes']
    return sixes

def fours():
    df = deli[deli['batsman_runs'] == 4]
    fours = df['batter'].value_counts().head(10).reset_index()
    fours.columns = ['Batsman', 'Fours']
    return fours

def partnership():
    df = deli.copy()
    df['partnership'] = df['batsman_runs'] + df['extra_runs']

    partnership_df = df.groupby(['match_id', 'inning', 'batting_team', 'batter', 'non_striker'])['partnership'].sum().reset_index()
    partnership_df = partnership_df.sort_values(by='partnership', ascending=False).head(10)
    partnership_df = partnership_df.rename(columns={
        'batting_team': 'Team',
        'batter': 'Batsman 1',
        'non_striker': 'Batsman 2',
        'partnership': 'Runs'
    })
    return partnership_df


def top_sr_avg(year):
    df = match.merge(deli, on='match_id')

    if year != "Overall":
        df = df[df['season'] == year]

    runs_df = df.groupby('batter')['batsman_runs'].sum()
    balls_df = df[df['extras_type'] != 'wides'].groupby('batter')['ball'].count()

    valid_batters = runs_df[runs_df >= 100].index  # Only those with 100+ runs
    runs_df = runs_df.loc[valid_batters]
    balls_df = balls_df.loc[valid_batters]

    avg_df = df[df['batter'].isin(valid_batters)]
    outs = avg_df[avg_df['is_wicket'] == 1]
    outs = outs[outs['player_dismissed'] == outs['batter']]
    dismissals = outs.groupby('batter')['is_wicket'].count()

    sr_avg = pd.DataFrame({
        'Runs': runs_df,
        'Balls': balls_df,
        'Innings': df[df['batter'].isin(valid_batters)].groupby('batter')['match_id'].nunique()
    })

    sr_avg['Dismissals'] = dismissals
    sr_avg['Strike Rate'] = (sr_avg['Runs'] / sr_avg['Balls']) * 100
    sr_avg['Average'] = sr_avg['Runs'] / sr_avg['Dismissals']
    sr_avg = sr_avg.reset_index().rename(columns={'batter': 'Batsman'})
    sr_avg = sr_avg[['Batsman', 'Runs', 'Balls', 'Strike Rate', 'Average']].sort_values(by='Runs',
                                                                                        ascending=False).head(10)
    return sr_avg
