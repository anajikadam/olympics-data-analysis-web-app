import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

import preprocessor,helper

from preprocessor import IMG_URL, df, region_df
from helper import bootstrapCard1, bootstrapCard2, bootstrapCard3

df = preprocessor.preprocess(df,region_df)

#------------------------------------ sidebar ---------------------------------------------------------------#
st.sidebar.title("Olympics Analysis")
st.sidebar.image(IMG_URL)
user_menu = st.sidebar.radio('Select an Option',
                                ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')
                            )

#------------------------------------ Medal Tally ---------------------------------------------------------------#
if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    st.write("""
                ## This is a historical dataset on the modern Olympic Games, including all the Games from Athens 1896 to Rio 2016
                In this implementation, the **Streamlit** library is used for building Web App for data visualization for Olympic Games data.

             """)
    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally, title = helper.fetch_medal_tally(df, selected_year, selected_country)

    st.title(title)
    st.table(medal_tally.head(10))    # Print Table 10 record
    if st.checkbox('Show Graph'):
        st.subheader('Bar chart for Top 10 Country')
        medal_tally11, _ = helper.fetch_medal_tally(df, 'Overall', 'Overall')
        st.plotly_chart(helper.barchart1(medal_tally11))

    if st.checkbox('Show All Record'):
        st.subheader('All Record for '+title)
        st.write(medal_tally)


#------------------------------------ Overall Analysis ---------------------------------------------------------------#
if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1  # because 1 extra year is in data
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        components.html( bootstrapCard1("Editions", editions) )
    with col2:
        components.html( bootstrapCard2("Hosts cities", cities) )
    with col3:
        components.html( bootstrapCard3("Sports", sports) )

    col1, col2, col3 = st.columns(3)
    with col1:
        components.html( bootstrapCard1("Events", events) )
    with col2:
        components.html( bootstrapCard2("Nations", nations) )
    with col3:
        components.html( bootstrapCard3("Athletes", athletes) )

    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x="Edition", y="region")  # plot line chart for Edition vs region
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Edition", y="Event")   # plot line chart for Edition vs Event
    st.title("Events over the years")
    st.plotly_chart(fig)

    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Edition", y="Name")  # plot line chart for Edition vs athlete Name
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    st.title("No. of Events over Years(Every Sport)")
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)

    st.title("Most successful Athletes (Top 20)")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport',sport_list)
    x = helper.most_successful(df, selected_sport)
    st.table(x)

#------------------------------------ Country-wise Analysis ---------------------------------------------------------------#
if user_menu == 'Country-wise Analysis':

    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    country_list.remove('India',)
    country_list[0] = 'India'
    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)
    country_df, title = helper.fetch_medal_tally(df, "Overall", selected_country)
    st.subheader(title)
    st.write(country_df)

    st.title(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("Top 10 athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)

#------------------------------------ Athlete wise Analysis ---------------------------------------------------------------#
if user_menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4],
                     ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                     show_hist=False, show_rug=False)
    fig.update_layout(autosize=True)
    st.title("Distribution of Age")
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
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=True)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(temp_df['Weight'],temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=60)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=True)
    st.plotly_chart(fig)



