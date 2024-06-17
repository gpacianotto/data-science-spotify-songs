# from utils.spotify_api import get_song_data

# print(get_song_data("7CKyONPRmrLbed1QX8SiRp?si=a1152bf51fab41a3"))

import pandas as pd

genres = pd.read_csv("./genres.csv")

for genre in genres["track_genre"]:
    print(genre)
