import pandas as pd
import streamlit as st
import preprocessor
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df = pd.read_csv('ml/athlete_events.csv')
region_df = pd.read_csv('ml/noc_regions.csv')

st.sidebar.title("Olympics Analysis")

df = preprocessor.preprocess(df,region_df)

user_menu = st.sidebar.radio('Select an option',('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete-wise Analysis'))

# st.dataframe(df)


if user_menu == 'Medal Tally':

    st.sidebar.header("Medal Tally")

    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country",country)

    if selected_country=='Overall' and selected_year=='Overall':
        st.title('Overall Tally')

    else:
        st.title(str(selected_country)+' in '+str(selected_year))

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)

    st.table(medal_tally)


if user_menu == 'Overall Analysis':

    st.sidebar.header('Overall Analysis')




    # no. of editions
    # no. of cities
    # no. of events
    # no. of sports
    # no. of athletes
    # participating nations


    editions = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['NOC'].unique().shape[0]

    st.title("Top Statistics")

    col1,col2,col3 = st.columns(3)

    with col1:
        st.header("Editions")
        st.title(editions)

    with col2:
        st.header("Hosts")
        st.title(cities)

    with col3:
        st.header('Sports')
        st.title(sports)



    col1,col2,col3 = st.columns(3)

    with col1:
        st.header("Events")
        st.title(events)

    with col2:
        st.header("Nations")
        st.title(nations)

    with col3:
        st.header('Athletes')
        st.title(athletes)


    nations_over_time = helper.data_over_time(df,'NOC')
    st.title("Participating Nations Over The Years")
    fig = px.line(nations_over_time,x='Edition',y='NOC')
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df,'Event')
    st.title("Events Over The Years")
    fig = px.line(events_over_time,x='Edition',y='Event')
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df,'Name')
    st.title("Athletes Over The Years")
    fig = px.line(athletes_over_time,x='Edition',y='Name')
    st.plotly_chart(fig)

    st.title("No of events over time(Every sport)")
    fig,ax = plt.subplots(figsize=(20,20))

    x = df.drop_duplicates(['Year','Sport','Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype(int),annot=True)

    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0,'Overall')
    selected_sport = st.selectbox("Select a sport",sports_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)


if user_menu == "Country-wise Analysis":

    st.sidebar.title("Country-wise Analysis")

    country_list = df['NOC'].dropna().unique().tolist()
    country_list.sort()
    selected_coun = st.sidebar.selectbox("Select a country",country_list)

    country_df = helper.yearwise_medal_tally(df,selected_coun)
    st.title(selected_coun+" Medal tally Over The Years")
    fig = px.line(country_df,x='Year',y='Medal')
    st.plotly_chart(fig)

    st.title(selected_coun+" excellence over the year ")

    pt = helper.country_event_heatmap(df,selected_coun)
    fig,ax = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("Top 10 Athletes Of "+ selected_coun)
    top_ten_df = helper.most_successful_countrywise(df,selected_coun)
    st.table(top_ten_df)


if user_menu == 'Athlete-wise Analysis':

    athlete_df =  df.drop_duplicates(subset=['Name','NOC'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal']=='Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal']=='Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1,x2,x3,x4],['Overall Age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution Of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport']==sport]
        x.append(temp_df[temp_df['Medal']=='Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x,name,show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution Of Wrt Age (Gold Medalists)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    # ax = sns.scatterplot(temp_df['Weight'],temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=60)
    ax = sns.scatterplot(data=temp_df, x='Weight', y='Height', hue='Medal', style='Sex', s=60)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)


    

