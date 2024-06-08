import gradio as gr
from functools import partial
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# dataset: https://www.kaggle.com/datasets/rodolfofigueroa/spotify-12m-songs/data
df = pd.read_csv("path/to/csv.csv")

def categorize_mood(row):
    if row['valence'] > 0.5 and row['energy'] > 0.5:
        return 'happy'
    elif row['valence'] < 0.5 and row['energy'] < 0.5:
        return 'sad'
    elif row['energy'] > 0.7:
        return 'energetic'
    elif row['acousticness'] > 0.5 and row['energy'] < 0.5:
        return 'calm'
    else:
        return 'neutral'

df['mood'] = df.apply(categorize_mood, axis=1)
df['name'] = df['name'].str.lower()


def recommend_songs_by_song_name(song_name, df, n_recommendations=5):
    # Check if the song exists in the dataset
    if song_name not in df['name'].values:
        raise ValueError("The specified song name does not exist in the dataset.")
    
    song = df[df['name'] == song_name].iloc[0]
    features = ['danceability', 'energy', 'key', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
    song_features = song[features].values.reshape(1, -1)

    # Calculate cosine similarity between the song and all other songs
    similarity_scores = cosine_similarity(song_features, df[features])

    # Get indices of top similar songs
    similar_song_indices = similarity_scores.argsort()[0][::-1][1:n_recommendations+1]
    return df.iloc[similar_song_indices][['name', 'artists', 'album', 'mood']]

def recommend_songs_by_mood(mood, df, n_recommendations=5):
    recommendations = df[df['mood'] == mood].sample(n=n_recommendations)
    return recommendations[['name', 'album']]\
    

def hybrid_recommendation(df, song_name, mood, n_recommendations=5):
    # Get song-based recommendations
    song_recommendations = recommend_songs_by_song_name(song_name=song_name, n_recommendations=n_recommendations * 2)
    # Filter recommendations by mood
    mood_recommendations = song_recommendations[song_recommendations['mood'] == mood].head(n_recommendations)    
    return mood_recommendations

recommend_songs_by_song_name = partial(recommend_songs_by_song_name, df = df)    
recommend_songs_by_mood = partial(recommend_songs_by_mood, df = df)
hybrid_recommendation = partial(hybrid_recommendation, df = df)



##########################
# Gradio interface
##########################

def byMood(mood, amount):
    try:
        recommendations = recommend_songs_by_mood(mood, n_recommendations=amount)
        return recommendations
    except Exception as e: return pd.DataFrame([{"Error": e}])

def byName(name, amount):
    try:
        recommendations = recommend_songs_by_song_name(name, n_recommendations=amount)
        recommendations["artists"] = recommendations["artists"].apply(lambda x: x.removeprefix("[").removesuffix("]"))
        return recommendations
    except Exception as e: return pd.DataFrame([{"Error": e}])

def hybrid(name, mood, amount):
    try: 
        recommendations = hybrid_recommendation(song_name = name, mood = mood, n_recommendations = amount)
        recommendations["artists"] = recommendations["artists"].apply(lambda x: x.removeprefix("[").removesuffix("]"))
        return recommendations
    except Exception as e: return pd.DataFrame([{"Error": e}])

with gr.Blocks() as demo:
    name_interface = gr.Interface(fn=byName,
                inputs=[gr.Textbox(label = "Song Name"),gr.Slider(minimum=1, maximum=100, step=1)],
                outputs="dataframe"
                )
                
    mood_interface = gr.Interface(fn=byMood,
                inputs=[gr.Dropdown(["happy", "sad", "energetic", "calm", "neutral"], label = "Mood"), gr.Slider(minimum=1, maximum=100, step=1)],
                outputs="dataframe"
                )
    
    hybrid_interface = gr.Interface(fn=hybrid,
                inputs=[gr.Textbox(label = "Song Name"), gr.Textbox(label = "Mood"), gr.Slider(minimum=1, maximum=100, step=1)],
                outputs="dataframe"
                )

demo.launch()