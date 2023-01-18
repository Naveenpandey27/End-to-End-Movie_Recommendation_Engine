# Import necessary libraries
import numpy as np
import pandas as pd
import ast
import nltk
import pickle
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Initialize PorterStemmer
ps = PorterStemmer()

# Read in the movie and credit data
movies_data = pd.read_csv('tmdb_5000_movies.csv')
credits_data = pd.read_csv('tmdb_5000_credits.csv')

# Merge the data on the 'title' column
movies = pd.merge(movies_data, credits_data, on = 'title')

# Checking top 5 rows after merging dataframes
movies.head()

# Keep only the relevant columns
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

# Checking if data contains null value
movies.isnull().sum()

# Remove any rows with missing values
movies.dropna(inplace = True)

# Remove any duplicate rows
movies.duplicated().sum()

# Define a function to extract the 'name' value from the 'genres' and 'keywords' columns
def ExtractGenres(obj):
    
    extract_name = []
    for i in ast.literal_eval(obj):
        extract_name.append(i['name'])
        
    return extract_name    

# Apply the Extract function to the 'genres' and 'keywords' columns
movies['genres'] = movies['genres'].apply(ExtractGenres)
movies['keywords'] = movies['keywords'].apply(ExtractGenres)
movies.head()

# Define a function to extract the first 5 cast members
def ExtractCast(obj):
    
    extract_cast = []
    count = 0
    for i in ast.literal_eval(obj):
        if count != 5:
            extract_cast.append(i['name'])
            count += 1
        else:
            break
        
    return extract_cast 

# Apply the ExtractCast function to the 'cast' column
movies['cast'] = movies['cast'].apply(ExtractCast)

# Define a function to extract the name of the first director
def extract_director_name(obj):
    
    director_name = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            director_name.append(i['name'])
            break
        
    return director_name

# Apply the extract_director_name function to the 'crew' column
movies['crew'] = movies['crew'].apply(extract_director_name)

# Split the 'overview' column into individual words
movies['overview'] = movies['overview'].apply(lambda x: x.split())

# Remove spaces from the values in the 'genres', 'keywords', 'cast', and 'crew' columns
movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['crew'] = movies['crew'].apply(lambda x: [i.replace(" ", "") for i in x])

# Check the top 5 rows
movies.head()

# Create a new 'tags' column that combines the values from the 'overview', 'genres', 'keywords', 'cast', and 'crew' columns
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

# Create a new DataFrame with only the 'movie_id', 'title', and 'tags' columns
new_data = movies[['movie_id', 'title', 'tags']]

# Convert the 'tags' column to lowercase and join the list of words into a single string
new_data['tags'] = new_data['tags'].apply(lambda x: " ".join(x))
new_data['tags'] = new_data['tags'].apply(lambda x: x.lower())

# Define a function to stem the words in the 'tags' column
def stemming(text):
    
    stemmed_words = []
    for i in text.split():
        stemmed_words.append(ps.stem(i))
        
    return " ".join(stemmed_words)

# Apply the stemming function to the 'tags' column
new_data['tags'] = new_data['tags'].apply(stemming)

# Create a TfidfVectorizer object with a maximum number of features of 5000 and remove english stop word
vectorizer = TfidfVectorizer(max_features = 5000, stop_words = 'english')

# Fit and transform the 'tags' column and convert it to an array
vectors = vectorizer.fit_transform(new_data['tags']).toarray()

# Compute the cosine similarity of the vectors
similarity = cosine_similarity(vectors)

# Define a function to recommend movies based on a given input movie
def recommend_movies(movie):
    movie_index = new_data[new_data['title'] == movie].index[0]
    distances = similarity[movie_index]
    # Sort the distances in descending order and get the top 10 most similar movies
    movies_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x: x[1])[1:11]
    
    # Print the titles of the recommended movies
    for i in movies_list:
        print(new_data.iloc[i[0]].title)

# Test the function with the input movie 'Avatar'
recommend_movies('Avatar')

# Serialize the new_data DataFrame and similarity array to binary files
pickle.dump(new_data.to_dict(), open('movie_dict.pkl', 'wb'))
pickle.dump(similarity,open('similarity.pkl','wb'))