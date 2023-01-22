# Import necessary libraries
import streamlit as st
import pickle
import base64
import pandas as pd
import requests
from PIL import Image
from io import BytesIO

# Function to fetch the poster of a movie using the movie's ID
def fetch_poster(movie_id):
    # Construct the URL to make the API call
    url = 'https://api.themoviedb.org/3/movie/{}?api_key=0afbf159a46fe7b96d78d362432aa48a&language=en-US'.format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path
   
# Function to recommend movies based on the movie selected by the user
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x: x[1])[1:8]
    
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
        
    return recommended_movie_names, recommended_movie_posters

# Load the movie data pickle and similarity data pickle file
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
st.markdown("<h1 style='text-align: center; color: red;'>Movie Recommendation Engine</h1>", unsafe_allow_html=True)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Create a dropdown for the user to select a movie
# selected_movie_name = st.selectbox("", movies['title'].values)

# Function to add background image from local path
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
    }}
    .movie-title {{
        color: white;
        font-weight: bold;
    }}
    .movie-info {{
        color: white;
        font-weight: bold;
        margin-left:80px;
        font-size: 25px;
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

# Reading jpg image to set background
add_bg_from_local('recommend.jpg')

# Creating Recommend button'
selected_movie_name = st.selectbox("", movies['title'].values)
if st.button('Recommend'):
    recommended_movie_names, recommended_movie_posters= recommend(selected_movie_name)  
    # Creates 6 columns and divides the recommended movies into two groups of 3.
    # This will display the group of 3 movie movie in the first 3 columns
    col1, col2, col3, = st.columns((3))
    # It will iterate through the first group of recommended movies and display their names and posters in the first 3 columns.
    for i in range(0,3):
        with col1:
            # It formats the display of the movie names
            # This "unsafe_allow_html=True" argument is used to enable the use of HTML tags in the markdown function.
            st.markdown(f'<div class="movie-title"><b>{recommended_movie_names[i]}</b></div>', unsafe_allow_html=True)
            st.image(recommended_movie_posters[i])
            col1 = col2
            col2 = col3
            
    # This will display the group of 3 movie movie in the second 3 columns
    col4, col5, col6 = st.columns((3))
    # It will iterate through the second group of recommended movies and display their names and posters in the next 3 columns.
    for j in range(3,6):
        with col4:
            st.markdown(f'<div class="movie-title"><b>{recommended_movie_names[j]}</b></div>', unsafe_allow_html=True)
            st.image(recommended_movie_posters[j])
            col4 = col5
            col5 = col6