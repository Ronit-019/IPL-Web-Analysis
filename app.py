import streamlit as st
import pandas as pd
import helper
import Team_Analysis,Player_Analysis,Batting_Performance,Bowling_Performance,Head_to_Head_Analysis

deli = pd.read_csv('deliveries.csv')
match = pd.read_csv('matches.csv')
df = match[~match.winner.isna()]

years = helper.season_list(match)
year = st.sidebar.selectbox("Select Season", years)

overs = helper.overs_list(deli)  # This should return a list of available seasons
over = st.sidebar.selectbox("Select Over", overs)


category = st.sidebar.selectbox("Select a Major Category",
                        ["About the Project","Team Analysis", "Player Analysis", "Over-Wise Analysis", "Batting Performance",
                         "Bowling Performance","Head-to-Head Analysis","Chase vs Defend Analysis"])

if category == "About the Project":
    st.image('IPL-Logo.jpg',width=300)
    st.write("""

---

# **IPL Data Analysis: 2008-2024**

Welcome to the **IPL Data Analysis: 2008-2024** project, an extensive and insightful look into the Indian Premier League's performance over 17 seasons. This analysis dives deep into teams, players, match trends, and statistics, revealing key insights that help understand how strategies, individual brilliance, and team dynamics have evolved over the years.

From batting and bowling performances to head-to-head matchups and over-wise analysis, explore IPL like never before!

---

### **Project Overview:**

#### **Team Analysis**:
This section focuses on team performance metrics, playoff appearances, and match statistics. Discover which teams have dominated over the years and how toss decisions have impacted results.
- **Key Topics:**
  - Team Tally
  - Playoff Appearances
  - Toss Analysis & Toss Decision Trends
  - Most Wins by City & Venue
  - Highest and Lowest Team Scores
  - Umpire Analysis
  [Explore Team Analysis ➔]

---

#### **Player Analysis**:
Dive into the individual performances of the top players in the IPL. This section covers the best batsmen, bowlers, wicketkeepers, and fielders over the years, offering insights into their achievements and contributions to the league.
- **Key Topics:**
  - Top 10 Batsmen & Bowlers
  - Top 10 Wicket Keepers
  - Man of the Match Leaders
  - Most Catches
  - Orange Cap (Top Scorer) & Purple Cap (Top Wicket-Taker)
  - Most Fifties, Hundreds, Highest Score
  - Best Bowling Figures
  [Explore Player Analysis ➔]

---

#### **Batting Performance**:
This section highlights the batting powerhouses of the IPL, covering the players who have scored the most sixes and fours, the strongest partnerships, and comparisons of strike rates and averages.
- **Key Topics:**
  - Most Sixes & Fours
  - Partnership Analysis
  - Strike Rate and Average
  [Explore Batting Performance ➔]

---

#### **Bowling Performance**:
Explore the top bowlers in the IPL through their economy rates, strike rates, and types of dismissals. This section provides a closer look at how bowlers have impacted the outcome of matches.
- **Key Topics:**
  - Bowler Economy Rate & Strike Rate
  - Dismissal Types (Batsmen & Bowlers)
  - Extras (Wides, No-Balls, etc.)
  [Explore Bowling Performance ➔]

---

#### **Head-to-Head Analysis**:
This section provides a comparison of teams and players when pitted against each other in head-to-head matchups. It highlights how teams and players have performed against specific opponents over the years.
- **Key Topics:**
  - Team Head-to-Head Comparisons
  - Batsman vs. Bowler Matchups
  - Bowler vs. Batsman Matchups
  [Explore Head-to-Head Analysis ➔]

---


### **Conclusion**:
This project delivers an in-depth examination of IPL's data from 2008 to 2024, offering cricket fans, analysts, and enthusiasts valuable insights into team strategies, player performances, and game outcomes. By analyzing key trends, this project provides a comprehensive look into the world of IPL and its evolution over the years.

Explore the data, uncover hidden patterns, and dive deep into the world of IPL with this detailed analysis.

---
   """)


if category == "Team Analysis":
    sub_option = st.sidebar.radio("Select an option",
                          ["Team Tally", "Playoffs Appearances","Toss Analysis","Toss Decision Analysis",
                           "Most Wins by City","Most Wins by Venue","Highest Score as Team", "Lowest Score as Team","Umpire Analysis"])

    if sub_option == "Team Tally":
        st.header('Team Tally')
        df = Team_Analysis.TeamTally(year)  # Fetch Team Tally data based on selected year
        st.dataframe(df)
        st.table(df)

    elif sub_option == "Playoffs Appearances":
        st.header('Playoffs Appearances')
        df = Team_Analysis.playoffs()  # Fetch Playoffs data
        st.dataframe(df)

    elif sub_option == "Toss Analysis":
        st.header('Toss Analysis')
        df = Team_Analysis.toss_ana()
        st.dataframe(df)

    elif sub_option == "Toss Decision Analysis":
        st.header('Toss Decision Analysis')
        df = Team_Analysis.toss_deci_ana()
        st.dataframe(df)

    elif sub_option == "Most Wins by City":
        st.header('Most Wins By City')
        df = Team_Analysis.win_city()  # Fetch Most Wins by City data
        st.dataframe(df)

    elif sub_option == "Most Wins by Venue":
        st.header('Most Wins By Venue')
        df = Team_Analysis.win_venue()  # Fetch Most Wins by Venue dat
        st.dataframe(df)

    elif sub_option == "Highest Score as Team":
        st.header('Highest Score as Team')
        df = Team_Analysis.high_score()  # Fetch Highest Score data
        st.dataframe(df)
        st.table(df.head(30))

    elif sub_option == "Lowest Score as Team":
        st.header('Lowest Score as Team')
        df = Team_Analysis.low_score()  # Fetch Lowest Score data
        st.dataframe(df)

    elif sub_option == "Umpire Analysis":
        st.header('Umpire Analysis')
        df = Team_Analysis.umpire(year)  # Fetch Umpire Analysis data
        st.dataframe(df)


elif category == "Player Analysis":

    sub_option = st.sidebar.radio("Select an option",
                          ["Top 10 Batsman", "Top 10 Bowler", "Top 10 Wicket Keeper", "Man of Match","Most Catches",
                           "Orange & Purple Cap","Most Fifties", "Most Hundreds","Highest Score","Best Bowling Figures"])

    if sub_option == "Top 10 Batsman":
        st.header('Top 10 Batsman')
        df = Player_Analysis.top_10_batter(year)  # Fetch Top Batsmen data
        st.dataframe(df)

    elif sub_option == "Top 10 Bowler":
        st.header('Top 10 Bowler')
        df = Player_Analysis.top_10_bowler(year)  # Fetch Top Bowler data
        st.dataframe(df)

    elif sub_option == "Top 10 Wicket Keeper":
        st.header('Top 10 WicketKeeper')
        df = Player_Analysis.top_10_wk(year)  # Fetch Top Bowler data
        st.dataframe(df)

    elif sub_option == "Man of Match":
        st.header('Man of Match')
        df = Player_Analysis.man_of_match(year)  # Fetch Top Bowler data
        st.dataframe(df)

    elif sub_option == "Most Catches":
        st.header('Most Catches')
        df = Player_Analysis.most_catch(year)  # Fetch Top Bowler data
        st.dataframe(df)

    elif sub_option == "Orange & Purple Cap":
        st.header('Orange & Purple Cap')
        df = Player_Analysis.opcap()  # Fetch Top Bowler data
        st.dataframe(df)

    elif sub_option == "Most Fifties":
        st.header('Most Fifties')
        df = Player_Analysis.most_fifties(year)  # Fetch Top Bowler data
        st.dataframe(df)

    elif sub_option == "Most Hundreds":
        st.header('Most Hundreds')
        df = Player_Analysis.most_hundreds(year)  # Fetch Top Bowler data
        st.dataframe(df)

    elif sub_option == "Highest Score":
        st.header('Highest Score')
        df = Player_Analysis.highest_score(year)  # Fetch Highest Score data
        st.dataframe(df)

    elif sub_option == "Best Bowling Figures":
        st.header('Best Bowling Figures')
        df = Player_Analysis.bowl_fig(year)  # Fetch Highest Score data
        st.dataframe(df)

elif category == "Batting Performance":
    sub_option = st.sidebar.radio("Select an option",
                          ["Most Sixes", "Most Fours", "Partnership Analysis",
                           "Strike Rate And Average"])

    if sub_option == "Strike Rate And Average":
        st.header('Strike Rate And Average')
        df = Batting_Performance.top_sr_avg(year)  # Fetch Top Strike Rate data
        st.dataframe(df)

    elif sub_option == "Most Sixes":
        st.header('Most Sixes')
        df = Batting_Performance.sixes()  # Fetch Highest Score data
        st.dataframe(df)

    elif sub_option == "Most Fours":
        st.header('Most Fours')
        df = Batting_Performance.fours()  # Fetch Highest Score data
        st.dataframe(df)

    elif sub_option == "Partnership Analysis":
        st.header('Partnership Analysis')
        df = Batting_Performance.partnership()  # Fetch Highest Score data
        st.dataframe(df)

elif category == "Bowling Performance":
    sub_option = st.sidebar.radio("Select an option",
                          ["Bowler Economy Rate And Strike Rate", "Dismissal Types Of Bowler",
                           "Dismissal Types Of Batter", "Extras by Type"])

    if sub_option == "Bowler Economy Rate And Strike Rate":
        st.header('Bowler Economy Rate And Strike Rate')
        df = Bowling_Performance.top_ec_sr()  # Fetch Top Strike Rate data
        st.dataframe(df)

    elif sub_option == "Dismissal Types Of Bowler":
       st.header('Dismissal Types Of Bowler')
       df = Bowling_Performance.dis_bowler()  # Fetch Highest Score data
       st.dataframe(df)

    elif sub_option == "Dismissal Types Of Batter":
       st.header('Dismissal Types Of Batter')
       df = Bowling_Performance.dis_batter()  # Fetch Highest Score data
       st.dataframe(df)

    elif sub_option == "Extras by Type":
        st.header('Extras by Type')
        df = Bowling_Performance.most_extras(year)  # Fetch Highest Score data
        st.dataframe(df)

elif category == "Head-to-Head Analysis":
    sub_option = st.sidebar.radio("Select an option",
                          ["Head-to-Head Comparisons","Batsman V/S Bowler","Bowler V/S Batsman"])

    if sub_option == "Head-to-Head Comparisons":
        st.header('Head-to-Head Comparisons')
        teams = Head_to_Head_Analysis.team_list(match)  # 'Overall' should be included in the list of years
        team1 = st.sidebar.selectbox("Select Team1", teams)

        teams = Head_to_Head_Analysis.team_list(match)  # 'Overall' should be included in the list of years
        team2 = st.sidebar.selectbox("Select Team2", teams)

        df = Head_to_Head_Analysis.head_to_head(team1,team2)  # Fetch Head to Head data
        st.dataframe(df)

    elif sub_option == "Bowler V/S Batsman":
        st.header('Bowler V/S Batsman')
        df = Head_to_Head_Analysis.bowl_vs_bat()  # Fetch Umpire Analysis data
        st.dataframe(df)

    elif sub_option == "Batsman V/S Bowler":
        st.header('Batsman V/S Bowler')
        df = Head_to_Head_Analysis.bat_vs_bowl()  # Fetch Umpire Analysis data
        st.dataframe(df)
