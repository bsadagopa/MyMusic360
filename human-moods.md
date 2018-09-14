7 Main human moods:
-------------------
1. Anger
2. Fear
3. Disgust 
4. Happiness 
5. Sadness
6. Surprise
7. Contempt
8. Neutral

 Music Genre 
 -----------
 Note: Can add international sections like indian, chinese ...
 Link: https://www.musicgenreslist.com/
 -----------------
 Alternative Music
 Blues
 Classical Music
 Country Music
 Dance Music
 Easy Listening
 Electronic Music
 European Music (Folk / Pop)
 Hip Hop / Rap
 Indie Pop
 Inspirational (incl. Gospel)
 Asian Pop (J-Pop, K-pop)
 Jazz
 Latin Music
 New Age
 Opera
 Pop (Popular music)
 R&B / Soul
 Reggae
 Rock
 Singer / Songwriter (inc. Folk)
 World Music / Beats


 Mapping of Music to Mood
 ------------------------
 Note: 
 1. This can be a user preference.
 2. Sub-categorization based on (spotify) music categorization like 
 	positive, workout etc, 
 	spotify audio features link (can use valence..):
 	https://developer.spotify.com/documentation/web-api/reference/tracks/get-several-audio-features/
 ------------------------
 Calculation Algorithm: TBD
 Set a range for each attribute, like ,
 pseudocode:
 if(use_mood == "anger") {
 	from (user_prefered_genre) {
 		select top 10 positive upbeat songs
 	}
 }

 Example:

1. Anger = { "danceability": 0.457,
       "energy": 0.815,
       "key": 1,
       "loudness": -7.199,
       "mode": 1,
       "speechiness": 0.034,
       "acousticness": 0.102,
       "instrumentalness": 0.0319,
       "liveness": 0.103,
       "valence": 0.382,
       "tempo": 96.083
   }
2. Fear
3. Disgust 
4. Happiness 
5. Sadness
6. Surprise
7. Contempt
