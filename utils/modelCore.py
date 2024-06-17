from keras import models
from utils.spotify_api import get_song_data, get_song_features
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder

def loadModel():
    return models.load_model("./neural-network/song_classifier.keras")

def getDataFrame(id):
    song_data = get_song_data(id)
    song_features = get_song_features(id)

    return song_to_dataframe(song_features=song_features, song_data=song_data)


def song_to_dataframe(song_features, song_data):
    # Select relevant fields from the audio features data
    song_features_info = {
        'id': song_features.get('id'),
        'name': song_data.get('name'),
        'artists': [artist['name'] for artist in song_data.get('artists', [])],
        'album': song_data['album']['name'] if 'album' in song_data else None,
        'release_date': song_data['album']['release_date'] if 'album' in song_data else None,
        'popularity': song_data.get('popularity'),
        'danceability': song_features.get('danceability'),
        'energy': song_features.get('energy'),
        'key': song_features.get('key'),
        'loudness': song_features.get('loudness'),
        'mode': song_features.get('mode'),
        'speechiness': song_features.get('speechiness'),
        'acousticness': song_features.get('acousticness'),
        'instrumentalness': song_features.get('instrumentalness'),
        'liveness': song_features.get('liveness'),
        'valence': song_features.get('valence'),
        'tempo': song_features.get('tempo'),
        'duration_ms': song_features.get('duration_ms'),
        'time_signature': song_features.get('time_signature')
    }
    return pd.DataFrame([song_features_info])

def getTrainX():
    return pd.read_csv("./neural-network/X_train.csv")

def getTrainY():
    return pd.read_csv("./neural-network/training_labels.csv")

def classify(id):
    model = loadModel()
    new_songs = getDataFrame(id)
    
    print("dataframe: ",new_songs)
    features = [
        'popularity', 
        'duration_ms', 
        'danceability', 
        'energy', 
        'key', 
        'loudness', 
        'mode', 
        'speechiness', 
        'acousticness', 
        'instrumentalness', 
        'liveness', 
        'valence', 
        'tempo', 
        'time_signature'
    ]

    X_new = new_songs[features].values

    X = getTrainX()

    y = getTrainY()

    scaler = StandardScaler()

    scaler.fit(X)

    X_new = scaler.transform(X_new)

    y_new_pred = model.predict(X_new)

    label_encoder = LabelEncoder()
    label_encoder.fit(y)

    prob_df = pd.DataFrame(y_new_pred, columns=label_encoder.classes_)

    print(prob_df)

    new_songs_with_probs = pd.concat([new_songs, prob_df], axis=1)

    new_songs_with_probs['predicted_genre'] = label_encoder.inverse_transform(np.argmax(y_new_pred, axis=1))

    return new_songs_with_probs

# Testing classification
# classify("7CKyONPRmrLbed1QX8SiRp?si=a1152bf51fab41a3")
