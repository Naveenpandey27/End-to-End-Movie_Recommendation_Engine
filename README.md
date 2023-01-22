# End-to-End-Movie Recommendation Engine

A content-based recommender system that recommends movies similar to the movie the user likes and analyses the sentiments of the reviews given by the user.

Check out the live demo:https://naveenpandey27-end-to-end-movie-recommendation-engin-app-yox39e.streamlit.app/

**output**

![outscree](https://user-images.githubusercontent.com/66298494/213917584-39ddc2d6-b34d-4a27-a9e9-bac3026189a2.png)


**How to get the API key?**

Create an account in https://www.themoviedb.org/. Once you successfully created an account, click on the API link from the left hand sidebar in your account settings and fill all the details to apply for an API key. If you are asked for the website URL, just give "NA" if you don't have one. You will see the API key in your API sidebar once your request has been approved.

**How to run the project?**

  **1 - Clone the repository to your local machine**

  git clone https://github.com/<username>/movie-recommendation-engine.git

  
  **2 - Install the necessary packages**

  pip install -r requirements.txt

  **3 - Run the application**
  
  streamlit run app.py




This is a movie recommendation engine built using Python and several machine learning libraries such as numpy, pandas, nltk, sklearn, and ast. The engine uses the TMDb movie dataset which is a dataset of over 5000 movies. The dataset includes information about movie titles, overviews, genres, keywords, cast, and crew.


**Preprocessing**

The first step in building this recommendation engine is preprocessing the data. The data is read in from two CSV files, one for movies and one for credits. The two datasets are then merged on the 'title' column. Only the relevant columns are kept, and any rows with missing values or duplicate rows are removed.


**Extracting Information**

The next step is to extract information from the 'genres' and 'keywords' columns. A function is defined to extract the 'name' value from each entry in the column. This function is then applied to the 'genres' and 'keywords' columns. A similar function is defined to extract the first 5 cast members and the name of the first director. These functions are applied to the 'cast' and 'crew' columns respectively.


**Text Processing**

The overview column is split into individual words and the 'genres', 'keywords', 'cast', and 'crew' columns are cleaned of spaces. A new 'tags' column is created by combining the values from the 'overview', 'genres', 'keywords', 'cast', and 'crew' columns.


**Cosine Similarity**

The final step is to calculate the cosine similarity between the movies based on their 'tags' column. The TfidfVectorizer function from sklearn is used to convert the text data in the 'tags' column into numerical data. The cosine_similarity function is then used to calculate the similarity between the movies.


**User Interface**

The final output is displayed as a Streamlit app where the user can select a movie from a drop-down list and then get a list of recommended movies. The recommended movies are displayed along with their poster images.


How to Use
Clone the repository to your local machine
Install the required libraries (numpy, pandas, nltk, sklearn, ast, pickle, streamlit, requests, PIL)
Run the app.py file
Select a movie from the drop-down list
Click on the 'Recommend' button
The recommended movies will be displayed along with their poster images.


**Prerequisites**

Python 3.6 or higher

Streamlit

Pandas

Requests

Pillow

NLTK

Sklearn
