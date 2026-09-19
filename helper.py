import pandas as pd
import numpy as np


def medal_tally(df):

    medal_tally = df.drop_duplicates(
        subset=[
            'Team', 'NOC', 'Games', 'Year',
            'City', 'Sport', 'Event', 'Medal'
        ]
    )

    medal_tally = medal_tally.groupby('region').sum()[
        ['Gold', 'Silver', 'Bronze']
    ].sort_values('Gold', ascending=False)

    medal_tally['Total'] = (
        medal_tally['Gold']
        + medal_tally['Silver']
        + medal_tally['Bronze']
    )

    medal_tally['Rank'] = range(1, len(medal_tally) + 1)

    medal_tally = medal_tally.astype({
        'Gold': int,
        'Silver': int,
        'Bronze': int,
        'Total': int
    })

    medal_tally = medal_tally.reset_index()

    medal_tally = medal_tally[
        ['Rank', 'region', 'Gold', 'Silver', 'Bronze', 'Total']
    ]

    return medal_tally


def country_year_list(df):

    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    countries = np.unique(
        df['region'].dropna().values
    ).tolist()

    countries.sort()
    countries.insert(0, 'Overall')

    return years, countries


def fetch_medal_tally(df, years, countries):

    medal_df = df.drop_duplicates(
        subset=[
            'Team', 'NOC', 'Games', 'Year',
            'City', 'Sport', 'Event', 'Medal'
        ]
    )

    # --------------------------------------------------
    # 1. Overall Year + Overall Country
    # --------------------------------------------------

    if years == 'Overall' and countries == 'Overall':

        x = medal_df.groupby('region').sum()[
            ['Gold', 'Silver', 'Bronze']
        ].sort_values('Gold', ascending=False)

        x['Total'] = (
            x['Gold']
            + x['Silver']
            + x['Bronze']
        )

        x = x.reset_index()

        x['Rank'] = range(1, len(x) + 1)

        x = x[
            ['Rank', 'region', 'Gold', 'Silver', 'Bronze', 'Total']
        ]

    # --------------------------------------------------
    # 2. Overall Year + Specific Country
    # --------------------------------------------------

    elif years == 'Overall' and countries != 'Overall':

        temp_df = medal_df[
            medal_df['region'] == countries
        ]

        x = temp_df.groupby('Year').sum()[
            ['Gold', 'Silver', 'Bronze']
        ].sort_values('Year')

        x['Total'] = (
            x['Gold']
            + x['Silver']
            + x['Bronze']
        )

        x = x.reset_index()

        # Add selected country as a column
        x['region'] = countries

        x = x[
            ['Year', 'region', 'Gold', 'Silver', 'Bronze', 'Total']
        ]

    # --------------------------------------------------
    # 3. Specific Year + Overall Country
    # --------------------------------------------------

    elif years != 'Overall' and countries == 'Overall':

        temp_df = medal_df[
            medal_df['Year'] == int(years)
        ]

        x = temp_df.groupby('region').sum()[
            ['Gold', 'Silver', 'Bronze']
        ].sort_values('Gold', ascending=False)

        x['Total'] = (
            x['Gold']
            + x['Silver']
            + x['Bronze']
        )

        x = x.reset_index()

        x['Rank'] = range(1, len(x) + 1)

        x = x[
            ['Rank', 'region', 'Gold', 'Silver', 'Bronze', 'Total']
        ]

    # --------------------------------------------------
    # 4. Specific Year + Specific Country
    # --------------------------------------------------

    else:

        temp_df = medal_df[
            (medal_df['Year'] == int(years)) &
            (medal_df['region'] == countries)
        ]

        x = temp_df.groupby('region').sum()[
            ['Gold', 'Silver', 'Bronze']
        ]

        x['Total'] = (
            x['Gold']
            + x['Silver']
            + x['Bronze']
        )

        x = x.reset_index()

        x = x[
            ['region', 'Gold', 'Silver', 'Bronze', 'Total']
        ]

    # Make medal values integers
    x['Gold'] = x['Gold'].astype(int)
    x['Silver'] = x['Silver'].astype(int)
    x['Bronze'] = x['Bronze'].astype(int)
    x['Total'] = x['Total'].astype(int)

    return x


def data_over_time(df, column):
    nations_over_time = df.drop_duplicates(['Year', column])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'Year': 'Edition', 'count': column}, inplace=True)

    return nations_over_time


def most_successful(df, sport):
    temp_df = df.dropna(subset=["Medal"])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index().merge(df, left_on='Name', right_on='Name', how='left')[
        ['Name', 'count', 'Sport', 'region']].drop_duplicates('Name')
    x.rename(columns={'count': 'Medals', 'region': 'Region'}, inplace=True)
    return x


def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().merge(df, left_on='Name', right_on='Name', how='left')[
        ['Name', 'count', 'Sport']].drop_duplicates('Name')
    x.rename(columns={'Name': 'Player Name', 'count': 'Medals Count', 'Sport': 'Sport Name'}, inplace=True)
    return x

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final
