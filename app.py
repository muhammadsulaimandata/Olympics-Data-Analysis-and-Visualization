import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import preprocessor
import helper
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import gaussian_kde
import numpy as np


df = pd.read_csv('athlete_events_through_2026.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df)


st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://logodownload.org/wp-content/uploads/2020/03/olimpiada-olympic-games-logo.png')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete wise Analysis'))



if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,countries = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", countries)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal Tally in ' + str(selected_year) + ' Olympics')
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + ' Overall Performance')
    elif selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + ' Overall Performance in ' + str(selected_year))

    # Number of rows per page
    rows_per_page = 11

    # Calculate number of pages
    total_pages = (len(medal_tally) - 1) // rows_per_page + 1

    # Page selector
    page = st.number_input(
        "Page",
        min_value=1,
        max_value=total_pages,
        value=1,
        step=1
    )

    # Calculate start and end rows
    start = (page - 1) * rows_per_page
    end = start + rows_per_page

    # Display current page
    st.table(medal_tally.iloc[start:end])

    st.write(f"Page {page} of {total_pages}")


if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0]
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)


    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Athletes")
        st.title(athletes)
    with col3:
        st.header("Nations")
        st.title(nations)

    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x='Edition', y='region')
    st.title("Participating Nations Over Time")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x='Edition', y='Event')
    st.title("Events Over Time")
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x='Edition', y='Name')
    st.title("Athletes Over Time")
    st.plotly_chart(fig)

    st.title("Number of Events over Time (Every Sport)")
    fig, ax = plt.subplots(figsize = (20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    pivot_table = x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int')
    sns.heatmap(pivot_table, annot=True)
    st.pyplot(fig)


    st.title('Most Successful Athletes')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.sidebar.selectbox('Select a Sport', sport_list)
    x = helper.most_successful(df, selected_sport)


    rows_per_page = 11

    total_pages = (len(x) - 1) // rows_per_page + 1

    if 'page' not in st.session_state:
        st.session_state.page = 1

    start = (st.session_state.page - 1) * rows_per_page
    end = start + rows_per_page

    # Table first
    st.table(x.iloc[start:end])

    # Pagination below table
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if st.button("← Previous"):
            if st.session_state.page > 1:
                st.session_state.page -= 1

    with col2:
        st.write(
            f"Page {st.session_state.page} of {total_pages}"
        )

    with col3:
        if st.button("Next →"):
            if st.session_state.page < total_pages:
                st.session_state.page += 1


if user_menu == 'Country-wise Analysis':
    st.title('Country wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country', country_list)
    country_df = helper.yearwise_medal_tally(df, selected_country)

    fig = px.line(country_df, x='Year', y='Medal')
    st.title(selected_country + " Analysis Over Time")
    st.plotly_chart(fig)

    pt = helper.country_event_heatmap(df, selected_country)
    st.title(selected_country + " Excelles in these Sports")
    fig, ax = plt.subplots(figsize=(20, 20))
    sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    st.title('Top Athletes of ' + selected_country)
    top10_df = helper.most_successful_countrywise(df, selected_country)

    rows_per_page = 11

    total_pages = (len(top10_df) - 1) // rows_per_page + 1

    if 'page' not in st.session_state:
        st.session_state.page = 1

    start = (st.session_state.page - 1) * rows_per_page
    end = start + rows_per_page

    # Table first
    st.table(top10_df.iloc[start:end])

    # Pagination below table
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if st.button("← Previous"):
            if st.session_state.page > 1:
                st.session_state.page -= 1

    with col2:
        st.write(
            f"Page {st.session_state.page} of {total_pages}"
        )

    with col3:
        if st.button("Next →"):
            if st.session_state.page < total_pages:
                st.session_state.page += 1



if user_menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Age'].dropna()

    fig = go.Figure()

    # -----------------------------
    # Bronze Medalists
    # -----------------------------
    bronze_age = athlete_df.loc[
        athlete_df['Medal'] == 'Bronze', 'Age'
    ].dropna()

    kde = gaussian_kde(bronze_age)
    x = np.linspace(bronze_age.min(), bronze_age.max(), 500)

    fig.add_trace(
        go.Scatter(
            x=x,
            y=kde(x),
            mode='lines',
            name='Bronze Medalist'
        )
    )

    # -----------------------------
    # Silver Medalists
    # -----------------------------
    silver_age = athlete_df.loc[
        athlete_df['Medal'] == 'Silver', 'Age'
    ].dropna()

    kde = gaussian_kde(silver_age)
    x = np.linspace(silver_age.min(), silver_age.max(), 500)

    fig.add_trace(
        go.Scatter(
            x=x,
            y=kde(x),
            mode='lines',
            name='Silver Medalist'
        )
    )

    # -----------------------------
    # Gold Medalists
    # -----------------------------
    gold_age = athlete_df.loc[
        athlete_df['Medal'] == 'Gold', 'Age'
    ].dropna()

    kde = gaussian_kde(gold_age)
    x = np.linspace(gold_age.min(), gold_age.max(), 500)

    fig.add_trace(
        go.Scatter(
            x=x,
            y=kde(x),
            mode='lines',
            name='Gold Medalist'
        )
    )

    # -----------------------------
    # All Athletes
    # -----------------------------
    all_age = athlete_df['Age'].dropna()

    kde = gaussian_kde(all_age)
    x = np.linspace(all_age.min(), all_age.max(), 500)

    fig.add_trace(
        go.Scatter(
            x=x,
            y=kde(x),
            mode='lines',
            name='All Athlete'
        )
    )

    # -----------------------------
    # Layout
    # -----------------------------
    fig.update_layout(
        autosize = False,
        width = 1000,
        height = 600,
        xaxis_title='Age',
        yaxis_title='Density',
        template='plotly_white',
        legend_title_text=''
    )

    st.title('Distribution of Age')
    st.plotly_chart(fig, use_container_width=True)

    # Get all sports
    famous_sports = athlete_df['Sport'].dropna().unique()

    fig = go.Figure()

    for sport in famous_sports:

        # Filter sport
        temp_df = athlete_df[
            athlete_df['Sport'] == sport
            ]

        # Get Gold Medalist ages
        ages = temp_df[
            temp_df['Medal'] == 'Gold'
            ]['Age'].dropna()

        # Skip sports with insufficient data
        if len(ages) < 2:
            continue

        # Skip sports where all ages are identical
        if ages.nunique() < 2:
            continue

        # Create KDE
        kde = gaussian_kde(ages)

        # Create age range
        age_range = np.linspace(
            ages.min(),
            ages.max(),
            500
        )

        # Add KDE line
        fig.add_trace(
            go.Scatter(
                x=age_range,
                y=kde(age_range),
                mode='lines',
                name=sport
            )
        )

    # Chart layout
    fig.update_layout(
        title='Age Distribution of Gold Medalists by Sport',
        xaxis_title='Age',
        yaxis_title='Density',
        template='plotly',
        width=900,
        height=550,

        legend=dict(
            x=1.02,
            y=1,
            xanchor='left',
            yanchor='top'
        ),

        margin=dict(
            l=60,
            r=180,
            t=60,
            b=50
        )
    )

    fig.update_xaxes(
        range=[10, 95],
        dtick=10,
        showgrid=True
    )

    fig.update_yaxes(
        showgrid=True
    )

    # Display in Streamlit
    st.plotly_chart(
        fig,
        use_container_width=True
    )

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')

    selected_sport = st.selectbox('Select a Sport', sport_list)

    temp_df = helper.weight_v_height(df, selected_sport)

    fig, ax = plt.subplots()

    sns.scatterplot(
        x=temp_df['Weight'],
        y=temp_df['Height'],
        hue=temp_df['Medal'],
        style=temp_df['Sex'],
        s=60,
        ax=ax
    )

    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)