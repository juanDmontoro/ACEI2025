import pandas as pd
import numpy as np
# import pyreadr 

df_tracks = pd.read_csv('https://juandmontoro.github.io/ACEI2025/data/final_data_similitud.csv',index_col=0)
df_tracks = df_tracks[(df_tracks['role']=="lead")|(df_tracks['role']=="solo")]
df_genre = pd.read_csv('https://juandmontoro.github.io/ACEI2025/data/genre_artists.csv',index_col=0)
diversity = pd.read_csv('https://juandmontoro.github.io/ACEI2025/data/artists_similarity.csv', 
                        index_col=0)
df_centrality = pd.read_csv('https://juandmontoro.github.io/ACEI2025/data/artist_centrality.csv')
#merge

df = pd.merge(df_tracks.drop(columns="artist_genres"),
              df_genre[['id','genre','genreMB','nTags']],
              left_on='artist_id',right_on='id',how="left")

df = pd.merge(df.drop(columns='id'), diversity.drop(columns='name'),left_on='artist_id',right_on='id')

# llenamos nas en centrality
df_centrality['closeness']=df_centrality['closeness'].fillna(1)
df_centrality['between']=df_centrality['between'].fillna(0)
df_centrality['eigenval']=df_centrality['eigenval'].fillna(0)


df = pd.merge(df.drop(columns='id'), df_centrality.drop(columns='artist_name'),on='artist_id')


y = df['streams']
# ALTERNATIVAS PARA LA respuesta: track_popularity, weeks, top_ten (muy pocas obs.), peek_position (se puede hacer top ten), times_at_peek (pocas obs.), peek_streams


variables_eliminar = ['track_name',
                     'streams','nTags',
                    'markets',
                    'day',
                    'track_popularity',
                    'artist_popularity',
                    'followers','collab_popularity','sum_popularity','collab_followers','sum_followers','weeks',
                    'top_ten','peek_position','times_at_peek','peek_streams','track_id','artist_id','artist_name','type','genre','release_date']
X =df.drop(columns=variables_eliminar)

month_map = {
    1: 'January', 2: 'February', 3: 'March', 4: 'April',
    5: 'May', 6: 'June', 7: 'July', 8: 'August',
    9: 'September', 10: 'October', 11: 'November', 12: 'December'
}

key_map = {
    0: 'C', 1: 'C#', 2: 'D', 3: 'D#',
    4: 'E', 5: 'F', 6: 'F#', 7: 'G',
    8: 'G#', 9: 'A', 10: 'A#', 11: 'B'
}

mode_map = {0: 'minor', 1: 'major'}

X['key']=X['key'].replace(key_map)
X['mode'] = X['mode'].replace(mode_map)
X['month'] = X['month'].replace(month_map)
