import streamlit as st
import pandas as pd


st.sidebar.header("-- Welcome to CrickInfo --")
# st.sidebar.write("This is a simple web app that shows the IPL data")
st.sidebar.subheader("Select the The Type")

option = st.sidebar.radio(
    "Choose the Format:",
    ("IPL Analysis :trophy:   ", "2024 Season Analysis :bookmark_tabs:" , "2025 Auction Analysis :chart_with_upwards_trend:" , "Specific Team Analysis :chart_with_upwards_trend:")
)
# st.write(f"{option} data will be displayed")

data = pd.read_csv('matches.csv')
data.replace({'team1':{'Kings XI Punjab':'Punjab Kings' , 'Royal Challengers Bangalore' : 'Royal Challengers Bengaluru' , 'Delhi Daredevils': 'Delhi Capitals' , 'Rising Pune Supergiant':'Rising Pune Supergiants'},
             'team2':{'Kings XI Punjab':'Punjab Kings' , 'Royal Challengers Bangalore' : 'Royal Challengers Bengaluru' , 'Delhi Daredevils': 'Delhi Capitals' , 'Rising Pune Supergiant':'Rising Pune Supergiants'},
            'winner':{'Kings XI Punjab':'Punjab Kings' , 'Royal Challengers Bangalore' : 'Royal Challengers Bengaluru ' ,'Delhi Daredevils': 'Delhi Capitals' , 'Rising Pune Supergiant':'Rising Pune Supergiants'},
            'toss_winner':{'Kings XI Punjab':'Punjab Kings' , 'Royal Challengers Bangalore' : 'Royal Challengers Bengaluru ' ,'Delhi Daredevils': 'Delhi Capitals' , 'Rising Pune Supergiant':'Rising Pune Supergiants'}

              },inplace=True)
df = data.copy()
data.drop(['id' , 'method' , 'umpire1' , 'umpire2' , 'target_overs' , 'super_over'] , axis = 1 , inplace = True )

data.city.fillna('Dubai' , inplace = True)
finalist_data = data[data['match_type'] == 'Final']
finalist_data.sort_values('season' , ascending = False , inplace = True)
finalist_data = finalist_data.drop(['result' , 'result_margin' , 'venue' , 'target_runs' , 'toss_winner' , 'toss_decision'] ,axis = 1).reset_index(drop= True)

team_name = data['team1'].unique().tolist()
team_name.insert(0 , 'Overall')
years = data['season'].unique().tolist()
years.sort(reverse = True)
years.insert(0 , 'Overall')


if option == "IPL Analysis :trophy:   ":
    st.markdown("""
    <div style="background-color:#1E90FF; padding:5px; border-radius:10px">
    <h3 style="color:white; text-align:center;">Overall IPL Analysis</h3>
    </div>
    """, unsafe_allow_html=True)
    # st.markdown("""
    # <div style="background-color:#1E90FF; padding:5px; border-radius:10px">
    # <h3 style="color:white; text-align:center;">Matches Played</h3>
    # </div>
    # """, unsafe_allow_html=True)
    st.write("")
    st.write("")
    col1 , col2 ,col3 = st.columns(3)
    with col1:
        st.subheader("Total Matches" )
        st.subheader(data.shape[0])
    with col2:
        st.subheader("Total Seasons ")
        st.subheader(data['season'].nunique())
    with col3:
        st.subheader("Total Teams")
        st.subheader(data['team1'].nunique())
    col4 , col5 , col6 = st.columns(3)
    with col4:
        st.subheader("Total Venues")
        st.subheader(data['venue'].nunique())
    with col6:
        st.subheader("Super-Overs")
        st.subheader(df.super_over.value_counts()[1])
    with col5:
        st.subheader("Total Cities")
        st.subheader(df['city'].nunique())
    # //////////////////////////////////////////////////////////////////
    # final data records
    st.markdown("""
    <h3 style="color:Red; text-align:Left; font-size: 40px; margin-top: 20px">Successful Teams</h3>
    """, unsafe_allow_html=True)
    winners = finalist_data.winner.value_counts().reset_index()
    winners.rename(columns = {'winner' : 'Winning Teams' , 'count' : 'Title Won'} , inplace = True)
    st.table(winners)
    # //////////////////////////////////////////////////////////////////
    # Visiualization
    winners.columns = ['Winning Team' , 'Title Won']
    pix = px.bar(winners , x = 'Winning Team' , y = 'Title Won')
    custom_colors = ['Yellow', 'Blue', 'Darkblue', 'Purple' ,'Orange' , 'Lightblue' , 'Pink']

    fig = px.pie(winners , values = 'Title Won' , names = 'Winning Team')
    fig = go.Figure(data=[go.Pie(
        labels=winners['Winning Team'], 
        values=winners['Title Won'], 
        textinfo='label+value',
        marker = dict(colors = custom_colors)
    )])
    
    pix = go.Figure(data= [go.Bar(
        x = winners['Winning Team'],
        y = winners['Title Won'],
        marker_color = custom_colors
    )])
    
    col1 , col2 = st.columns(2)
    with col2:
        st.plotly_chart(fig , use_container_width=True)
    with col1:
        st.plotly_chart(pix , use_container_width=True)


    # //////////////////////////////////////////////////////////////////
    st.markdown("""
    <h3 style="color:Red; text-align:Left; font-size: 40px; margin-top: 20px">Final Records</h3>
    """, unsafe_allow_html=True)
    st.table(finalist_data)

    st.markdown(""" 
    <h3 style="color:Red; text-align:Left; font-size: 40px; margin-top: 20px">IPL Venues</h3>
    """ , unsafe_allow_html = True)

    col1 , col2 , col3 = st.columns(3)
    with col1:
        # st.subheader("ToVenues")

        year = st.selectbox("Select the Year" , years)
        if year != 'Overall':
            year_data = data[data['season'] == year].sort_values('season' , ascending = False)
        else:
            year_data = data
        year_data = year_data.drop(['result' , 'result_margin' , 'match_type' , 'target_runs' , 'toss_winner' , 'toss_decision'] ,axis = 1 ).reset_index(drop= True).sort_values('season' , ascending = False)
    with col2:
        team = st.selectbox("Select the Team" , team_name)
        if team == 'Overall':
            year_data = year_data
        else:
            year_data = year_data[(year_data['team1'] == team) | (year_data['team2'] == team)]
         
    with col3:
        venue = st.selectbox("Select the Venue" , year_data['venue'].unique())
        
   
    if year == 'Overall':
        select_Data = year_data[(year_data['venue'] == venue)].head(5)
    else:
        select_Data = year_data[(year_data['venue'] == venue) & (year_data['season'] == year)].head(5)
    st.table(select_Data)
    
    if year != 'Overall':
        venue_counts = data[data['season'] == year]
    else:
        venue_counts = data
    venue_counts = venue_counts['venue'].value_counts().reset_index()
    venue_counts.columns = ["Venue", "Matches"]
    # Create Plotly Bar Chart
    fig = px.bar(venue_counts, x="Venue", y="Matches", color="Matches",
                 title=f"Number of Matches Played at Each Venue ({year})")

    # Update layout (optional)
    fig.update_layout(xaxis_tickangle=45, xaxis_title="Venue", yaxis_title="Number of Matches")
    fig.update_layout(
        width=1200,  
        height=700,  
        xaxis_tickangle=-45,  
        xaxis_title="Venue", 
        yaxis_title="Number of Matches "
    )
    st.plotly_chart(fig , use_container_width=True)

    # match played
    st.markdown(""" 
    <h3 style="color:Red; text-align:Left; font-size: 40px; margin-top: 20px">No. of matches per Year</h3>
    """ , unsafe_allow_html = True)
    matches_data = data
    matches_per_season = matches_data['season'].value_counts().sort_index()
    matches_per_season = matches_per_season.reset_index()
    matches_per_season.columns = ['season' , 'count']
    fig = px.line(matches_per_season, x="season", y="count", title="Matches Played per Year(with results)", markers=True)

    st.plotly_chart(fig , use_container_width=True)

    # supper over
    st.markdown(""" 
    <h3 style="color:Red; text-align:Left; font-size: 40px; margin-top: 20px">Super Overs Played</h3>
    """ , unsafe_allow_html = True)
    super_over_data = df[df.super_over == 'Y']
    super_over_data.drop([ 'id','method' , 'umpire1' , 'umpire2' , 'match_type' , 'toss_winner' , 'target_overs' ,'result_margin' , 'target_runs' , 'result', 'toss_decision'] , axis = 1 , inplace = True)
    super_over_data.sort_values('season' , ascending = False , inplace = True)
    super_over_data.city.fillna('Dubai' , inplace = True)

    st.table(super_over_data.head(10))

if option == "Specific Team Analysis :chart_with_upwards_trend:":
    st.markdown("""
    <div style="background-color:red; padding:5px; border-radius:10px">
    <h3 style="color:white; text-align:center;">Specific Team Analysis</h3>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(""" 
    <div style = "margin-top:30px"> </div>
    """ , unsafe_allow_html = True)

    col1 , col2 , col3 = st.columns([1,2,1])
    with col1:
        st.markdown(""" 
    <h3 style="color:#007FFF; text-align:Left; font-size: 30px; margin-top: 20px">Select Your Team</h3>
    """ , unsafe_allow_html = True)

    with col2 :
        team1 = team_name.copy()
        team1.remove('Overall')
        team = st.selectbox("Select the Team" , team1)
        team_data = data[(data['team1'] == team) | (data['team2'] == team)]
    
    with col3:
        year = st.selectbox("Select the Year" , years)
        if year != 'Overall':
            team_data = team_data[team_data['season'] == year]
        else:
            team_data = team_data
    team_data = team_data.drop(['result' , 'result_margin' , 'match_type' , 'target_runs' , 'toss_winner' , 'toss_decision'] ,axis = 1 ).reset_index(drop= True).sort_values('season' , ascending = False)

    st.markdown(""" 
    <div style = "margin-top:30px"> </div>
    """ , unsafe_allow_html = True)
    
    st.subheader(f"Season tally for {team} in {year}")
    if year != 'Overall':
        st.table(team_data)
    else:
        st.table(team_data.head(10))
if option == "2025 Auction Analysis":
    auc = pd.read_csv('ipl_2025_auction_players.csv')
    # auc = auc[auc.Base != "-"]
    auc = auc[auc.Type != "WK"]
    auc = auc[auc.Sold != "Unsold" ]
    auc = auc[auc.Sold != "TBA" ]
    

    st.markdown("""
    <div style="background-color:red; padding:5px; border-radius:10px">
    <h3 style="color:white; text-align:center;">2025 Auction Analysis</h3>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(""" 
    <div style = "margin-top:30px"> </div>
    """ , unsafe_allow_html = True)

    st.subheader("Teams Reteined Players")

    col1 , col2  = st.columns([1,2])
    with col1:
        st.markdown(""" 
    <h3 style="color:#007FFF; text-align:Left; font-size: 30px; margin-top: 20px">Select Your Team</h3>
    """ , unsafe_allow_html = True)

    with col2 :
        retention = auc[auc.Base == "-"]
        retention.drop('Base' , axis = 1 , inplace = True)
        auc_team = retention['Team'].unique().tolist()
        auc_team.insert(0 , 'Overall')
        # team1.remove('Overall')
        team = st.selectbox("Select the Team" , auc_team)
        if team != 'Overall':
            auc_data = retention[retention['Team'] == team]
        else:
            auc_data = retention
    st.table(auc_data)
    
    st.markdown("""
    
    <h3 style="color:Red;">Expensive Players List</h3>
    """, unsafe_allow_html=True)
    auc = auc[auc.Base != "-"]

    auc['Sold'] = pd.to_numeric(auc['Sold'], errors='coerce')

# Sort the DataFrame by 'Sold' values in descending order
    auc_sorted = auc.sort_values('Sold', ascending=False)

    # Reset the index of the sorted DataFrame
    auc_sorted = auc_sorted.reset_index(drop=True)

    auc_sorted.columns = ['Players' , 'Team' , 'Type' , 'Base' , 'Sold']
    # Visualization using Plotly Express
    fig = px.bar(auc_sorted.head(20), x='Players', y='Sold', title='Top Expensive Players in IPL ', 
                 labels={'Player': 'Player Name', 'Sold': 'Amount Sold'},
                 hover_data=['Base', 'Type']) # Include relevant columns in hover data
    st.table(auc_sorted.head(10))
    st.plotly_chart(fig , use_container_width=True)

    # team performance

    st.markdown("""
    
    <h3 style="color:Red;">Team Auction Performace</h3>
    """, unsafe_allow_html=True)
    def team_auction(team):
        team_auc = auc.groupby('Team').get_group(team)
        team_auc = team_auc.sort_values('Sold', ascending=False).reset_index(drop = True)
        # print(team_auc)
        # print(team_auc.Players.count())
        # print(team_auc.Sold.sum())

        # Visualization using Plotly Express for the given team
        fig = px.bar(team_auc, x='Players', y='Sold', title=f'Players and Spending for {team}',
                     labels={'Players': 'Player Name', 'Sold': 'Amount Spent'},
                     hover_data=['Base', 'Type'])
        st.table(team_auc)
        st.plotly_chart(fig , use_container_width=True)
        
        col1 , col2 = st.columns(2)
        # with col1:
        #     st.subheader(f"Total Players : {team_auc.Players.count()}")
        # with col2:
        #     st.subheader(f"Total Amount Spent : {team_auc.Sold.sum()}")
        with col1:
            pie_team = team_auc.Type.value_counts().reset_index()
            nfig = px.pie(pie_team, values='count', names='Type', title=f'Types of Players in {team}')
        
            st.plotly_chart(nfig , use_container_width=True)
        with col2:
            pie_team = team_auc.Sold.value_counts().reset_index()
            nfig = px.pie(pie_team, values='count', names='Sold', title=f'Price slots of the {team}')
        
            st.plotly_chart(nfig , use_container_width=True)

    if team != 'Overall':   
        team_auction(team)
    else:
        st.write("Please Select the Team for detailed Analysis")
    st.markdown(f"""
    
    <h3 style="color:Red;">Top Price Hike Players {team}</h3>
    """, unsafe_allow_html=True)
    if team != 'Overall':
        hike = auc.groupby('Team').get_group(team)
        hike['Sold'] = pd.to_numeric(hike['Sold'], errors='coerce')
        hike['Base'] = pd.to_numeric(hike['Base'], errors='coerce')

  
        hike['Difference'] = hike['Sold'] - hike['Base']
        hike['Percentage_Hike'] = ((hike['Difference'] / hike['Base']) * 100).round(2)

        # Sort the DataFrame by the percentage hike in descending order
        st.table(hike.sort_values('Percentage_Hike' , ascending = False).head(10))
    else:
        hike = auc.copy()
        hike['Sold'] = pd.to_numeric(hike['Sold'], errors='coerce')
        hike['Base'] = pd.to_numeric(hike['Base'], errors='coerce')

  
        hike['Difference'] = hike['Sold'] - hike['Base']
        hike['Percentage_Hike'] = ((hike['Difference'] / hike['Base']) * 100).round(2)

        # Sort the DataFrame by the percentage hike in descending order
        st.table(hike.sort_values('Percentage_Hike' , ascending = False).head(10))


if option == "2024 Season Analysis :bookmark_tabs:":
    st.markdown("""
    <h3 style="color:Red; text-align:center; font-size: 40px;">2024 Season Analysis</h3>
    </div>
    """, unsafe_allow_html=True)

    last_data = data[data['season'] == 2024].sort_values('target_runs' , ascending = False)
    last_data = last_data.drop(['season', 'result_margin' , 'match_type' , 'toss_winner' ,'toss_decision'] ,axis = 1).reset_index(drop= True)
    
    high_score = last_data[last_data['target_runs'] >= 200]

    col1 , col2 , col3 = st.columns(3)
    with col1:
        st.subheader("Total Matches" )
        st.subheader(last_data.shape[0])
    with col2:
        st.subheader("Total Venues")
        st.subheader(last_data['venue'].nunique())
    with col3:
        st.subheader("200+ scores")
        st.subheader(high_score.shape[0])
        
    col1, col2 ,col3 = st.columns(3)
    with col1:
        st.subheader("Starting Date :")
        st.subheader("Fri 22 Mar, 2024")
    with col2:
        st.subheader("Ending Date :")
        st.subheader("Sun 26 May, 2024")
    
    st.markdown("""
    <h4 style = "color: Blue; font-size: 32px; margin-top:20px;">Top season scores</h4>
    """ , unsafe_allow_html = True)
    
    st.table(last_data.head(10))
    top_fig = px.bar(last_data.head(10) , x = 'winner' , y = 'target_runs' , title = "Top 10 scores in 2024 Season")
    st.plotly_chart(top_fig , use_container_width=True)


    st.markdown("""
    <h4 style = "color: Blue; font-size: 32px; margin-top:20px;">Venue having 200+ scores</h4>
    """ , unsafe_allow_html = True)

    st.table(high_score.venue.value_counts().reset_index())
    venue_data = high_score.venue.value_counts().reset_index()
    nig = px.pie(venue_data , values = 'count' , names = 'venue' , title = "counts of Venue in which 200+ scores")
    st.plotly_chart(nig , use_container_width=True)

    st.markdown("""
    <h4 style = "color: Blue; font-size: 32px; margin-top:0px;">Highest Run-chase</h4>
    """ , unsafe_allow_html = True)
    st.table(last_data[last_data['result'] == 'wickets'].head(10))
    highest_chases = last_data[last_data['result'] == 'wickets'].sort_values('target_runs', ascending=False).head(10)
    fig_chase = px.bar(highest_chases, x='team1', y='target_runs', color='team1', title=f"Highest Run Chases ")
    st.plotly_chart(fig_chase, use_container_width=True)


    



    



    
           
            
    


        

        
    

    

