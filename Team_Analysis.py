import pandas as pd
import helper

deli = pd.read_csv('deliveries.csv')
match = pd.read_csv('matches.csv')
df = match[~match.winner.isna()]

# helper.main()
helper.overs_list(deli)
helper.season_list(match)
helper.team_list(match)
#
# match.rename(columns={'id':'match_id'},inplace=True)

def TeamTally(year):

    global match

    new_df = pd.DataFrame()
    teams = match['team1'].unique()
    data = []

    # When 'Overall' is selected (for all seasons)
    if year == 'Overall':
        for team in teams:
            played = match[(match['team1'] == team) | (match['team2'] == team)].shape[0]
            wins = match[match['winner'] == team].shape[0]
            home_win = match[(match['winner'] == team) & (match['team1'] == team)].shape[0]
            away_win = match[(match['winner'] == team) & (match['team2'] == team)].shape[0]

            if played > 0:  # Only consider teams with matches played
                win_percentage = (wins / played) * 100 if played > 0 else 0
                data.append([team, played, wins, home_win, away_win, win_percentage])
        if len(data) > 0:
            new_df = pd.DataFrame(data, columns=["Team", "Matches Played", "Matches Won", "Home Wins", "Away Wins",
                                                 "Win Percentage"])
            new_df.sort_values("Matches Played", inplace=True, ascending=False)

        # st.dataframe(new_df)

        # plt.figure(figsize=(10, 6))
        # sns.barplot(data=new_df, x=new_df['Team'], y=new_df['Win Percentage'])
        # plt.xticks(rotation=90)
        # st.pyplot(plt)

    # When a specific year is selected
    else:
        for team in teams:
            played = match[((match['team1'] == team) | (match['team2'] == team)) & (match['season'] == year)].shape[0]
            wins = match[(match['winner'] == team) & (match['season'] == year)].shape[0]
            home_win = match[(match['winner'] == team) & (match['team1'] == team) & (match['season'] == year)].shape[0]
            away_win = match[(match['winner'] == team) & (match['team2'] == team) & (match['season'] == year)].shape[0]

            if played > 0:
                win_percentage = (wins / played) * 100 if played > 0 else 0
                data.append([team, played, wins, home_win, away_win, round(win_percentage)])

    # Assigning the data to a DataFrame with correct column names
    if len(data) > 0:
        new_df = pd.DataFrame(data, columns=["Team", "Matches Played", "Matches Won", "Home Wins", "Away Wins",
                                             "Win Percentage"])
        new_df.sort_values("Matches Played", inplace=True, ascending=False)

    return new_df


def playoffs():

    # Creating an empty DataFrame to store the final data
    df = match[match['match_type'] != 'League']
    fin = match[match['match_type'] == 'Final']
    new_df = pd.DataFrame()
    teams = df.team2.unique()
    data = []
    for team in teams:
        played = df[((df.team1 == team) | (df.team2 == team))].shape[0]
        wins = df[(df.winner == team)].shape[0]
        final_win = fin[(fin.winner == team)].shape[0]
        data.append([team, played, wins, final_win, (wins / played) * 100])
    new_df[["Team", "Matches Played", "Mathches Won", "Final Won", " Playoff Win Percentage"]] = data
    new_df.sort_values("Matches Played", inplace=True, ascending=False)
    return new_df



def toss_ana():

    tw = match[~(match['result'] == 'no result')]
    t_df = pd.DataFrame()
    teams = df.team1.unique()
    de1 = []
    for team in teams:
        tw_mw = tw[((tw['team1'] == team) | (tw['team2'] == team)) & (tw['toss_winner'] == team) & (
                    tw['winner'] == team)].shape[0]
        tl_mw = tw[((tw['team1'] == team) | (tw['team2'] == team)) & (tw['toss_winner'] != team) & (
                    tw['winner'] == team)].shape[0]
        tw_ml = tw[((tw['team1'] == team) | (tw['team2'] == team)) & (tw['toss_winner'] == team) & (
                    tw['winner'] != team)].shape[0]
        tl_ml = tw[((tw['team1'] == team) | (tw['team2'] == team)) & (tw['toss_winner'] != team) & (
                    tw['winner'] != team)].shape[0]

        wp1 = round(((tw_mw / (tw_mw + tw_ml)) * 100), 2) if (tw_mw + tw_ml) > 0 else 0
        wp2 = round(((tl_mw / (tl_mw + tl_ml)) * 100), 2) if (tl_mw + tl_ml) > 0 else 0
        lp1 = round(((tw_ml / (tw_mw + tw_ml)) * 100), 2) if (tw_mw + tw_ml) > 0 else 0
        lp2 = round(((tl_ml / (tl_mw + tl_ml)) * 100), 2) if (tl_mw + tl_ml) > 0 else 0

        if wp1 > 0:
            # de1.append([team, tw_mw, tl_mw, tw_ml, tl_ml])
            de1.append([team, wp1, wp2, lp1, lp2])
    t_df[["Team", "Toss Won Match Won (%)", "Toss Lost Match Won (%)", "Toss Won Match Lost (%)",
          "Toss Loss Match Loss (%)"]] = de1

    t_df.columns = pd.MultiIndex.from_tuples([
        ('Team', ''),
        ('Toss Won', 'Match Won (%)'),
        ('Toss Won', 'Match Lost (%)'),
        ('Toss Lost', 'Match Won (%)'),
        ('Toss Lost', 'Match Lost (%)')
    ])
    t_df.sort_values(('Toss Won', 'Match Won (%)'), inplace=True, ascending=False)
    return t_df

def toss_deci_ana():

    td = match[~(match['result'] == 'no result')]
    t_wf = pd.DataFrame()
    teams = match.team1.unique()
    dt1 = []
    dt2 = []
    for team in teams:

        total_toss_won = match[((match['team1'] == team) | (match['team2'] == team)) & (match['toss_winner'] == team)].shape[0]

        total_toss_lost = match[((match['team1'] == team) | (match['team2'] == team)) & (match['toss_winner'] != team)].shape[0]

        bat_deci = match[((match['team1'] == team) | (match['team2'] == team)) & (match['toss_decision'] == 'bat') & (match['toss_winner'] == team)].shape[0]

        field_deci = match[((match['team1'] == team) | (match['team2'] == team)) & (match['toss_decision'] == 'field') & (match['toss_winner'] == team)].shape[0]

        field_won_deci = match[((match['team1'] == team) | (match['team2'] == team)) & (match['toss_decision'] == 'field') & (match['toss_winner'] == team) & (match['winner'] == team)].shape[0]

        bat_won_deci = match[((match['team1'] == team) | (match['team2'] == team)) & (match['toss_decision'] == 'bat') & (match['toss_winner'] == team) & (match['winner'] == team)].shape[0]

        # Check if 'field_deci' is not zero before performing the division
        if field_deci > 0:
            Win_Rate_After_Choosing_Field = (field_won_deci / field_deci) * 100
        else:
            Win_Rate_After_Choosing_Field = 0  # Handle zero case (could be NaN or another value if preferred)

        # Check if 'bat_deci' is not zero before performing the division
        if bat_deci > 0:
            Win_Rate_After_Choosing_Bat = (bat_won_deci / bat_deci) * 100
        else:
            Win_Rate_After_Choosing_Bat = 0  # Handle zero case

        dt1.append([team, total_toss_won, total_toss_lost, Win_Rate_After_Choosing_Field, Win_Rate_After_Choosing_Bat])

    t_wf[["Team", "Total Toss Won", "Total Toss Lost", " Win(%) After Choosing Fielding","Win(%) After Choosing Batting"]] = dt1

    return t_wf


def win_city():
    m1 = match.groupby(['city', 'winner']).size().reset_index(name='No of Wins')
    m1 = m1.sort_values(by='No of Wins', ascending=False).head(9)
    m1 = m1.rename(columns={'city': 'City', 'winner': 'Winner Team'})
    return m1

def win_venue():
    m2 = match.groupby(['venue', 'winner']).size().reset_index(name='No of Wins')
    m2 = m2.sort_values(by='No of Wins', ascending=False).head(9)
    m2 = m2.rename(columns={'venue': 'Venue', 'winner': 'Winner Team'})
    return m2

def high_score():

    mg = match.merge(deli, on='match_id')
    mg = mg[(mg['method'] != 'D/L')]
    mg = mg[(mg['result'] != 'no result')]
    hg = mg.groupby(['match_id', 'batting_team'])['total_runs'].sum().sort_values(ascending=False)
    hg = hg.reset_index()
    hg = hg.drop(columns='match_id')
    hg = hg.rename(columns={'batting_team': 'Team', 'total_runs': 'Score'})
    # hg = hg.set_index('Team')
    return hg

def low_score():

    mg = match.merge(deli, on='match_id')
    mg = mg[(mg['method'] != 'D/L')]
    mg = mg[(mg['result'] != 'no result')]
    lw = mg.groupby(['match_id', 'batting_team'])['total_runs'].sum().sort_values(ascending=False).tail(10)
    lw = lw.reset_index()
    lw = lw.drop(columns='match_id')
    lw = lw.rename(columns={'batting_team': 'Team', 'total_runs': 'Score'})
    lw = lw.set_index('Team')
    lw = lw.sort_values(by='Score')
    return lw

def umpire(year):

    teams = match['team1'].unique()
    u1 = match['umpire1'].unique()
    u2 = match['umpire2'].unique()
    u1 = set(u1)
    u2 = set(u2)
    ump = list(u1.union(u2))

    if year == 'Overall':
        new_df = pd.DataFrame()
        data = []
        for team in teams:
            mt_won = match[(match['team1'] == team) | (match['winner'] == team) & (match['winner'] == team)]
            mt_lost = match[(match['team1'] == team) | (match['winner'] == team) & (match['winner'] != team)]
            for u in ump:
                won_count = mt_won[(mt_won['umpire1'] == u) | (mt_won['umpire2'] == u)].shape[0]
                lost_count = mt_lost[(mt_lost['umpire1'] == u) | (mt_lost['umpire2'] == u)].shape[0]
                if won_count > 0 or lost_count > 0:
                    data.append([team, u, won_count, lost_count])
        new_df = pd.DataFrame(data, columns=["Team", "Umpire", "Won", "Lost"])
        new_df.sort_values(["Won", "Lost"], inplace=True, ascending=False)
        return new_df
    else:
        ms = match[match['season'] == year]
        new_df = pd.DataFrame()
        data = []
        for team in teams:
            mt_won = ms[((ms['team1'] == team) | (ms['team2'] == team)) & (ms['winner'] == team)]
            mt_lost = ms[((ms['team1'] == team) | (ms['team2'] == team)) & (ms['winner'] != team)]
            for u in ump:
                won_count = mt_won[(mt_won['umpire1'] == u) | (mt_won['umpire2'] == u)].shape[0]
                lost_count = mt_lost[(mt_lost['umpire1'] == u) | (mt_lost['umpire2'] == u)].shape[0]
                if won_count > 0 or lost_count > 0:
                    data.append([team, u, won_count, lost_count])
        new_df = pd.DataFrame(data, columns=["Team", "Umpire", "Won", "Lost"])
        new_df.sort_values(["Won", "Lost"], inplace=True, ascending=False)
        return new_df