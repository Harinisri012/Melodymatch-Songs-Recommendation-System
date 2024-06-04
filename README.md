# Melody Match
## Songs-Recommendation-System

It is a interactive recommendation system where user can ask for recommendation many times untill they want to exit the program.
First the system asks where the user want recommendation based on the songs they specify or recommendations based on the mood they specify or coorelating both.
when the user specify their choice they are prompted to give the input and the user gets an output of 5 song recommendations.
In this project we have used cosine similarity to select the similar to the songs that were specified by the user, and based on a few attributes from the dataset about the songs we have segregated the songs into different moods

## STEP 1 Data Preprocessing:
* Load the Data: Read the dataset into a DataFrame.
* Handle Missing Values: Check and handle missing values appropriately.
* Normalize/Standardize Features: Normalize or standardize numerical features for better performance.

## Step 2: Feature Engineering:
* Create Mood Labels: If not already present, create mood labels based on features like valence, energy, danceability, etc.
* Feature Selection: Select relevant features for recommendation, such as key, mode, danceability, valence, energy, acousticness, instrumentalness, and liveness_speechiness.

## Step 3: Content-Based Filtering:
* Content-based filtering recommends songs based on the features of the song you're currently listening to.
* Calculate Cosine Similarity: Use cosine similarity to find songs similar to the one currently being played.

## Step 4: Implementing the Recommendation System:
* Build a Recommendation Function: Create a function to recommend songs based on the current song or mood.

## Data set details:
This dataset has around 1.2 million songs with 
id, name, album, album_id, artists, artist_ids, track_number, disc_number, explicit, danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, year, release_date  
as attributes.

The link to download this Download this dataset -
https://www.kaggle.com/datasets/rodolfofigueroa/spotify-12m-songs/data
