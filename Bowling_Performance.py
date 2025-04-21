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

def top_ec_sr():
    df = deli[deli['is_wicket'] == 1]

    balls = deli[deli['extras_type'] != 'wides'].groupby('bowler')['ball'].count()
    overs = balls // 6 + (balls % 6) / 6
    runs = deli.groupby('bowler')['total_runs'].sum()
    wickets = df.groupby('bowler')['is_wicket'].count()

    valid_bowlers = balls[balls >= 120].index  # Bowlers with at least 20 overs
    runs = runs.loc[valid_bowlers]
    overs = overs.loc[valid_bowlers]
    wickets = wickets.loc[valid_bowlers]

    er_sr = pd.DataFrame({
        'Runs': runs,
        'Overs': overs,
        'Wickets': wickets
    })

    er_sr['Economy'] = er_sr['Runs'] / er_sr['Overs']
    er_sr['Strike Rate'] = balls.loc[valid_bowlers] / er_sr['Wickets']
    er_sr = er_sr.reset_index().rename(columns={'bowler': 'Bowler'})
    er_sr = er_sr[['Bowler', 'Runs', 'Overs', 'Wickets', 'Economy', 'Strike Rate']]
    er_sr = er_sr.sort_values(by='Economy').head(10)
    return er_sr


def dis_bowler():
    df = deli[deli['is_wicket'] == 1]
    df = df[df['dismissal_kind'].notnull()]

    dis = df.groupby(['bowler', 'dismissal_kind']).size().unstack(fill_value=0)
    dis['Total Wickets'] = dis.sum(axis=1)

    dis = dis.sort_values(by='Total Wickets', ascending=False).head(10)
    dis = dis.reset_index().rename(columns={'bowler': 'Bowler'})

    return dis


def dis_batter():
    df = deli[deli['is_wicket'] == 1]
    df = df[df['dismissal_kind'].notnull()]

    dis = df.groupby(['player_dismissed', 'dismissal_kind']).size().unstack(fill_value=0)
    dis['Total Dismissals'] = dis.sum(axis=1)

    dis = dis.sort_values(by='Total Dismissals', ascending=False).head(10)
    dis = dis.reset_index().rename(columns={'player_dismissed': 'Batter'})

    return dis


def most_extras(year):
    df = match.merge(deli, on='match_id')

    if year != "Overall":
        df = df[df['season'] == year]

    df = df[df['extras_type'].notnull()]

    # Count extras per type per bowling team
    extras = df.groupby(['bowling_team', 'extras_type']).size().unstack(fill_value=0)

    # Add total extras column
    extras['Total Extras'] = extras.sum(axis=1)

    # Sort by total extras
    extras = extras.sort_values(by='Total Extras', ascending=False).head(10)

    # Reset index and rename
    extras = extras.reset_index().rename(columns={'bowling_team': 'Team'})

    return extras

