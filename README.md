## About

This simple flask app parses the ESPN BottomLine score feed and returns JSON right to your doorstep. There are certainly more sophisticated and robust sports data APIs available, but this has the advantage of being simple, free, and easy to modify for whatever you're working on. You can see a working version of the app at [http://scorehub.herokuapp.com](http://scorehub.herokuapp.com).

## Endpoints
#### Current
```
/ping
```

If the app is working, ```/ping``` returns a 200 response. Nothing more, nothing less.

```
/ncaaf
```

Returns a json response object of this week's NCAA DIV-I football scores. No historical data is available.

#### Planned
```/mlb```: MLB score data

```/nba```: NBA score data 

```/nfl```: NFL score data 

```/ncaab```: NCAA Basketball score data

## Deploying
This code is MIT licensed, so you can do pretty much whatever you want with it. Clone this repository to your local machine. Then, from the application directory, run ```heroku create your-app-name``` and ```git push heroku master```.

The final step is to enable a caching solution so that results are cached. I've used memcachier (```heroku addons:add memcachier```) for my own deploy, but I've included the flask-heroku-cacheify extension, so you should be able to use just about any other heroku caching add-on with no additional configuration.

## Version History

##### Current Version 0.1.0
- NCAAF and PING endpoints are functional
- Results are returned as json objects
- App can easily be deployed to Heroku without configuration
- Results are cached for 5 minutes. Caching does not account for time-delay of results.
