## Project 2 - MyMusic360
#### Team Members
* Balaji K Sadagopa
* Andrew Kling
* Suswith Gaddam

#### What is MyMusic360
<p>
MyMusic360 is a tool for you to store your custom music preferences. So in real-time, 
i.e. dymanically the song that is most likely to be liked by you can be played.
The likeness builds on your history of listening based on various static and dynamic triggers,
like, your location, location features currently like weather etc, 
your activity like if you are excercising (running), driving or relaxing etc,
your previous like favorite songs during these activities etc.
<p>
So our goal is to provide you with the song that will make you comfortable - the song you will "most like" at that moment.
We will try to select that song from multiple sources across the web like spotify, google your personal store etc.

#### Key Product features:
* recommend a friend based on similarity of songs (audio features), artists, category
user statistics - top songs, artists, category
* top artists/categories by region - Get most popular music based on location and then determine the best location for a user based on what kind of music they like
"rising" artists - artists who are getting more plays per day than previously
would require us pulling data day over day ourselves - perhaps need to limit look back to just one week
* Basic B % - how much does a users playlists match up with Top 100 songs
User music recommendation - create a playlist based on other playlists that allows user to set certain features such as a block list, keep music in same category, only artists that aren't in existing playlist,only songs that aren't in existing playlist, etc.
Take all songs from all playlists and recommend new playlists by k means clustering on audio features
