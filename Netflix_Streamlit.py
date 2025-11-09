# Import Libraries
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from textblob import TextBlob

# Title of the App
st.title('Netflix Data Analysis and Visualization')

# Load the dataset
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

# Specify the correct path to your 'netflix_titles.csv' file
file_path = 'netflix_titles.csv'
df = load_data(file_path)


# Sidebar for navigation
st.sidebar.title("Navigation")
options = st.sidebar.selectbox("Select a Section", ['Content Rating Distribution', 'Top Directors', 'Top Actors', 'Yearly Production Trends', 'Top Countries', 'Sentiment Analysis', 'Top Genres'])

# Content Rating Distribution
if options == 'Content Rating Distribution':
    st.header("Distribution of Content Ratings")
    x = df.groupby(['rating']).size().reset_index(name='counts')
    pieChart = px.pie(x, values='counts', names='rating', title='Distribution of Content Ratings on Netflix', template='plotly_dark')
    st.plotly_chart(pieChart)

# Top Directors
if options == 'Top Directors':
    st.header("Top 5 Directors on Netflix")
    df['director'] = df['director'].fillna('Director Not specified')
    directors_list = df['director'].str.split(',', expand=True).stack().to_frame(name='Director')
    directors = directors_list.groupby(['Director']).size().reset_index(name='Total Count')
    directors = directors[directors.Director != 'Director Not specified']
    directors = directors.sort_values(by=['Total Count'], ascending=False)
    top5Directors = directors.head(5)
    barChart = px.bar(top5Directors, x='Total Count', y='Director', color='Director', title='Top 5 Directors on Netflix', template='plotly_dark')
    st.plotly_chart(barChart)

# Top Actors
if options == 'Top Actors':
    st.header("Top 5 Actors on Netflix")
    Cast_list = df['cast'].str.split(',', expand=True).stack().to_frame(name='Actors')
    Casts = Cast_list.groupby(['Actors']).size().reset_index(name='Total Count')
    Casts = Casts.sort_values(by=['Total Count'], ascending=False)
    top5Actors = Casts.head(5)
    barChart = px.bar(top5Actors, x='Total Count', y='Actors', color='Actors', title='Top 5 Actors on Netflix', template='plotly_dark')
    st.plotly_chart(barChart)

# Yearly Production Trends
if options == 'Yearly Production Trends':
    st.header("Content Production Trends by Year")
    df1 = df[['type', 'release_year']].rename(columns={"release_year": "Release Year", "type": "Type"})
    df2 = df1.groupby(['Release Year', 'Type']).size().reset_index(name="Total_Count")
    df2 = df2[df2['Release Year'] >= 2000]
    graph = px.line(df2, x="Release Year", y='Total_Count', color='Type', title='Trend of Content Produced on Netflix Every Year', template='plotly_dark')
    st.plotly_chart(graph)

# Top Countries Producing Netflix Content
if options == 'Top Countries':
    st.header("Top 5 Countries Producing Netflix Content")
    Country_list = df['country'].str.split(',', expand=True).stack().to_frame(name='Country')
    Countries = Country_list.groupby(['Country']).size().reset_index(name='Total Count')
    Countries = Countries.sort_values(by=['Total Count'], ascending=False)
    top5Country = Countries.head(5)
    barChart = px.bar(top5Country, x='Total Count', y='Country', color='Country', title='Top 5 Countries Producing Netflix Content', template='plotly_dark')
    st.plotly_chart(barChart)

# Sentiment Analysis
if options == 'Sentiment Analysis':
    st.header("Sentiment Analysis of Netflix Content Descriptions")
    df3 = df[['release_year', 'description']].rename(columns={'release_year': 'Release Year', 'description': 'Description'})
    sentiments = []
    
    for index, row in df3.iterrows():
        d = row['Description']
        testimonial = TextBlob(d)
        P = testimonial.sentiment.polarity
        if P == 0:
            sentiments.append("Neutral")
        elif P > 0:
            sentiments.append("Positive")
        else:
            sentiments.append("Negative")
    
    df3['Sentiment'] = sentiments
    df3 = df3.groupby(['Release Year', 'Sentiment']).size().reset_index(name='Total Count')
    df3 = df3[df3['Release Year'] > 2005]
    barGraph = px.bar(df3, x="Release Year", y='Total Count', color='Sentiment', title='Sentiment Analysis of Content on Netflix', template='plotly_dark')
    st.plotly_chart(barGraph)

# Top Genres
if options == 'Top Genres':
    st.header("Top 5 Genres on Netflix")
    Genre_list = df['listed_in'].str.split(',', expand=True).stack().to_frame(name='Genre')
    Genres = Genre_list.groupby(['Genre']).size().reset_index(name='Total Count')
    Genres = Genres.sort_values(by=['Total Count'], ascending=False)
    top5Genre = Genres.head(5)
    barChart = px.bar(top5Genre, x='Total Count', y='Genre', color='Genre', title='Top 5 Genres on Netflix', template='plotly_dark')
    st.plotly_chart(barChart)

# Footer section
st.sidebar.markdown("Developed with ❤️ using Streamlit")
