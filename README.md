# spotify evaluation 

welcome to this Flask personality evaluation app! judgements are made using a users available Spotify data 

##getting started
before you run this code on your own machine, please log in and register an app with the
[Spotify for Developers API](https://developer.spotify.com/dashboard/).
you will need the client id and client secret that will be provided for each app you create on there. and then register 
http://127.0.0.1:5000/callback as the Redirect URI (found when you click the Edit Settings button).

in your terminal run 
```shell script
source venv/bin/activate
pip3 install requirements.txt
flask run
``` 
and open a web browser to [127.0.0.1:5000](http://127.0.0.1:5000/)

## about the application
this app is just a personal take on Personality Quizzes using the ideology of Moral Alignment from Dungeons and Dragons

#### how it works
this app utilizes Spotify's API and OAuth. after a user connect their spotify account to the app, the app makes calls to
Spotify requesting information about the Users display information, top Tracks, Artists, and Playlist. using the combined
data of those Tracks and Artists, an light hearted judgement is made and returned to the user. this app is meant to be
fun, while exploring data visualization. 

#### judgement criteria 
everything is based off of the idea that music falling in specific ranges of data fall into one of these six categories,
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

my arbitrary alignment is as follows:

|      | Lawful | Neutral | Chaotic |
|------|-----|--------|-------
| Good | high dance | high dance  | high dance | 
|  | high valence | mid range everything else  | high energy| 
|  | |  | low pop | 
| Neutral | high acoustic | mid range everything | high energy | 
|  | low everything else | | mid valence | 
|  | |  | low pop | 
| Evil | low dance | low everything | high energy |
| | high acoustic |  | low dance |
| | high speech |  | low pop |



## some code to know

#### techstack
- Flask
- Spotify's Developers API



## visuals

![evolution of the homepage design](https://i.imgur.com/ZbgKAV7.png)
here is the evolution of the homepage webdesign 

using Spotify's green for initial inspiration, i was able to eventually find a match between Spotify and my own taste.


## routes

| Route Name | Description |
|------------|-------------|
| / | homepage |
| /connect | spotify redirect |
| /callback | registered redirect uri |
| /about | about page |


## future updates

## thank you

## references 
[Spotify Flask Auth Example by drshrey](spotify-flask-auth-example)

