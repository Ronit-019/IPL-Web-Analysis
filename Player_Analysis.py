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

# years = helper.season_list(match)
# year = st.sidebar.selectbox("Select Season", years)
#
# overs = helper.overs_list(deli)  # This should return a list of available seasons
# over = st.sidebar.selectbox("Select Over", overs)

def top_10_batter(year):
    if year == "Overall":
        bt = match.merge(deli, on='match_id')
        bt = bt.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False).head(10).reset_index()
        bt = bt.rename(columns={'batter': 'Batsman', 'batsman_runs': 'Runs'})
        return bt
    else:
        bt = match.merge(deli, on='match_id')
        bt = bt[bt['season'] == year]
        bt = bt.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False).head(10).reset_index()
        bt = bt.rename(columns={'batter': 'Batsman', 'batsman_runs': 'Runs'})
        return bt


def top_10_bowler(year):
    if year == "Overall":
        df = match.merge(deli, on='match_id')
        df = df[df['is_wicket'] == 1]
        df = df.groupby('bowler')['player_dismissed'].count().sort_values(ascending=False).head(10).reset_index()
        df = df.rename(columns={'bowler': 'Bowler', 'player_dismissed': 'Wickets'})
        return df
    else:
        df = match.merge(deli, on='match_id')
        df = df[df['season'] == year]
        df = df[df['is_wicket'] == 1]
        df = df.groupby('bowler')['player_dismissed'].count().sort_values(ascending=False).head(10).reset_index()
        df = df.rename(columns={'bowler': 'Bowler', 'player_out': 'Wickets'})
        return df

def top_10_wk(year):
    if year == "Overall":
        df = match.merge(deli, on='match_id')
        df = df[df['dismissal_kind'].isin(['stumped', 'caught'])]
        wk_data = df.groupby('fielder')['player_dismissed'].count().sort_values(ascending=False).head(10).reset_index()
        wk_data = wk_data.rename(columns={'fielders_involved': 'Wicket Keeper', 'player_dismissed': 'Dismissals'})
        return wk_data
    else:
        df = match.merge(deli, on='match_id')
        df = df[df['season'] == year]
        df = df[df['dismissal_kind'].isin(['stumped', 'caught'])]
        wk_data = df.groupby('fielder')['player_dismissed'].count().sort_values(ascending=False).head(10).reset_index()
        wk_data = wk_data.rename(columns={'fielders_involved': 'Wicket Keeper', 'player_dismissed': 'Dismissals'})
        return wk_data

def man_of_match(year):

    if year == "Overall":
        df = match['player_of_match'].value_counts().head(10).reset_index()
        df.columns = ['Player', 'Awards']
        return df
    else:
        df = match[match['season'] == year]
        df = df['player_of_match'].value_counts().head(10).reset_index()
        df.columns = ['Player', 'Awards']
        return df

def most_catch(year):

    if year == "Overall":
        df = match.merge(deli, on='match_id')
        df = df[df['dismissal_kind'] == 'caught']
        df = df.groupby('fielder')['player_dismissed'].count().sort_values(ascending=False).head(10).reset_index()
        df.columns = ['Fielder', 'Catches']
        return df
    else:
        df = match.merge(deli, on='match_id')
        df = df[df['season'] == year]
        df = df[df['dismissal_kind'] == 'caught']
        df = df.groupby('fielder')['player_dismissed'].count().sort_values(ascending=False).head(10).reset_index()
        df.columns = ['Fielder', 'Catches']
        return df

def opcap():


    seasons = match['season'].unique()
    data = []

    for season in seasons:
        bat_df = match.merge(deli, on='match_id')
        bat_df = bat_df[bat_df['season'] == season]
        top_batsman = bat_df.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False).head(1)
        top_bowler = bat_df[bat_df['is_wicket'] == 1].groupby('bowler')['player_dismissed'].count().sort_values(ascending=False).head(1)

        data.append({
            'Season': season,
            'Orange Cap': top_batsman.index[0],
            'Runs': top_batsman.iloc[0],
            'Purple Cap': top_bowler.index[0],
            'Wickets': top_bowler.iloc[0]
        })

    return pd.DataFrame(data)

def most_fifties(year):

    if year == "Overall":
        df = match.merge(deli, on='match_id')
        df = df.groupby(['match_id', 'batter'])['batsman_runs'].sum().reset_index()
        df = df[df['batsman_runs'] >= 50]
        df = df[df['batsman_runs'] < 100]
        fifties = df['batter'].value_counts().head(10).reset_index()
        fifties.columns = ['Batsman', 'Fifties']
        return fifties
    else:
        df = match.merge(deli, on='match_id')
        df = df[df['season'] == year]
        df = df.groupby(['match_id', 'batter'])['batsman_runs'].sum().reset_index()
        df = df[df['batsman_runs'] >= 50]
        df = df[df['batsman_runs'] < 100]
        fifties = df['batter'].value_counts().head(10).reset_index()
        fifties.columns = ['Batsman', 'Fifties']
        return fifties


def most_hundreds(year):

    if year == "Overall":
        df = match.merge(deli, on='match_id')
        df = df.groupby(['match_id', 'batter'])['batsman_runs'].sum().reset_index()
        df = df[df['batsman_runs'] >= 100]
        hundreds = df['batter'].value_counts().head(10).reset_index()
        hundreds.columns = ['Batsman', 'Hundreds']
        return hundreds
    else:
        df = match.merge(deli, on='match_id')
        df = df[df['season'] == year]
        df = df.groupby(['match_id', 'batter'])['batsman_runs'].sum().reset_index()
        df = df[df['batsman_runs'] >= 100]
        hundreds = df['batter'].value_counts().head(10).reset_index()
        hundreds.columns = ['Batsman', 'Hundreds']
        return hundreds


def highest_score(year):
    if year == "Overall":
        df = match.merge(deli, on='match_id')
        df = df.groupby(['match_id', 'batter'])['batsman_runs'].sum().sort_values(ascending=False).head(10).reset_index()
        df = df.rename(columns={'batter': 'Batsman', 'batsman_runs': 'Score'})
        return df
    else:
        df = match.merge(deli, on='match_id')
        df = df[df['season'] == year]
        df = df.groupby(['match_id', 'batter'])['batsman_runs'].sum().sort_values(ascending=False).head(
            10).reset_index()
        df = df.rename(columns={'batter': 'Batsman', 'batsman_runs': 'Score'})
        return df

def bowl_fig(year):

    if year == "Overall":
        df = match.merge(deli, on='match_id')
        df = df[df['is_wicket'] == 1]
        bowler_fig = df.groupby(['match_id', 'bowler']).agg(
            wickets=('player_dismissed', 'count'),
            runs=('total_runs', 'sum')
        ).sort_values(by=['wickets', 'runs'], ascending=[False, True]).reset_index().head(10)

        bowler_fig = bowler_fig.rename(columns={'bowler': 'Bowler', 'wickets': 'Wickets', 'runs': 'Runs Conceded'})
        return bowler_fig
    else:
        df = match.merge(deli, on='match_id')
        df = df[df['season'] == year]
        df = df[df['is_wicket'] == 1]
        bowler_fig = df.groupby(['match_id', 'bowler']).agg(
            wickets=('player_dismissed', 'count'),
            runs=('total_runs', 'sum')
        ).sort_values(by=['wickets', 'runs'], ascending=[False, True]).reset_index().head(10)

        bowler_fig = bowler_fig.rename(columns={'bowler': 'Bowler', 'wickets': 'Wickets', 'runs': 'Runs Conceded'})
        return bowler_fig