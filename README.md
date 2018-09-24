## Project 2 - MyMusic360
#### Team Members
* Balaji K Sadagopa
* Andrew Kling
* Suswith Gaddam

***What is MyMusic360***
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
<p>
You signon to the app using face detection, Microsoft FACE API AI-ML is used to capture you current mood as you logon. This information is used to recommend songs.

***Key Product features:***
* Credential check based on picture taken. 
* If not a setup - configured user, then allowed in as a guest user.
* Face attributed - mood is read using microsost FACE Api.
* For existing-setup user, their collection from Spotify is accessed and song matching close to existing mood is played.
* For guest user, song matching the users mood from the current top 100 list is played.

