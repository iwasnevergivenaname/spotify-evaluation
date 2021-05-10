# spotify evaluation 

hello :) welcome to an app that learned to align you, morally. built with Flask, SQLAlchemy, connected to a machine learning
application built with scikit-learn, and based on the ideology behind Dungeons and Dragons Moral Alignment

[play with the deployed version](https://spotify-evaluation.herokuapp.com/)

## getting started
before you run this code on your own machine, please log in and register an app with the
[Spotify for Developers API](https://developer.spotify.com/dashboard/).
you will need the client id and client secret that will be provided for each app you create on there. and then register 
http://127.0.0.1:5000/callback as the Redirect URI (found when you click the Edit Settings button).

in your terminal run 
```shell script
python3 -m venv venv
source venv/bin/activate
pip3 install requirements.txt
psql < spotify-evaluation.sql
export FLASK_ENV=development 
flask run
``` 
and open a web browser to [127.0.0.1:5000](http://127.0.0.1:5000/)

[fork and clone this backend repo to access the model making predictions](https://github.com/iwasnevergivenaname/spotify-backend)

## features of the application
this app can be broken into 3 mini apps: a static collection of pages (about or home page), an app to collect relevant 
artist data from spotify's api, and a machine learning model built to categorize songs based on track analysis. 

#### how it works
utilizing Spotify's API and OAuth, a user connect their spotify account to the app, the app makes calls to
Spotify requesting information about the users display information, top tracks, and artists. using the 
data of the tracks, a light hearted judgement is made and returned to the user. this app is meant to be
fun, while exploring a new medium with machine learning. 

#### judgement criteria 
everything is based off of the idea that music falling in specific ranges of data fall into one of these nine categories,
Lawful Good, Lawful Neutral, Lawful Evil, Neutral Good, True Neutral, Neutral Evil, Chaotic Good, Chaotic Neutral, Chaotic Evil.

the data in question would be the "audio features" returned for specific Tracks by Spotify. the information returned was
then pared down just to fields that were all measured by equal units. this left Popularity, Energy, Danceability, 
Acousticness, Speechiness, and Valence.

|      | pop | energy | dance | acoustic | speech | valence |
|------|-----|--------|-------|----------|--------|---------|
| mean | 26% | 48% | 54% | 50% | 11% | 52% |
| std | 22% | 27% | 18% | 38% | 18% | 26% |
| 50% | 25% | 47% | 55% | 52% | 5% | 54% |
| 75% | 42% | 71% | 70% | 90% | 8% | 74% |

low range will be considered anything below 30%, mid range is 30%-60%, and high range is 60%+ 
(speechiness will be treated slightly differently since it's an outlier)

as i was thinking about the moral alignments, i realized they boil down to action and motive. that's why you can have 
lawful (action) evil (motive) or chaotic (action) good (motive). now to apply that to the data i have available: out of 
all the categories danceability seems to be the best match for action and valence to motive. proceeding with that, i also
added in some conditions about popularity (ie relatively unloved songs or overplayed tracks) and energy 
(the relationship between low energy and more happy music specifically) to make sure my alignments are as accurate to my
 overly opinionated alignments as possible.

low = 0.0 - 0.39 <br>
mid = 0.4 - 0.69 <br>
high = 0.7 - 1.00

|      | Lawful | Neutral | Chaotic |
|------|-----|--------|-------
| Good | high dance | mid dance     | high dance | 
|      | high valence | low valence | low pop | 
|      | high pop |                |  low valence  | 
| Neutral | low dance | mid dance  | high dance | 
|      | low valence | mid valence | mid valence | 
|      | mid valence|              | low pop | 
| Evil | low dance | mid dance     | low energy |
|      | high pop |  low energy    |   high valence   |
|      | mid valence |  high valence | low pop |
|      | low energy |  | high dance |


#### techstack
- Flask
- Spotify's Developers API
- SQLAlchemy
- Scikit-learn
- Numpy
- Pandas


## references 
[Spotify Developer API](https://developer.spotify.com/documentation/web-api/) <br>
[Spotify Flask Auth Example by drshrey](https://github.com/drshrey/spotify-flask-auth-example) <br>
[Spotify Datasets from 1920-2020 by Yamac Eren Ay](https://www.kaggle.com/yamaerenay/spotify-dataset-19212020-160k-tracks) <br>
[Flask Blueprint Tutorial by hackersandslackers](https://github.com/hackersandslackers/flask-blueprint-tutorial) <br>

