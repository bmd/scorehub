## About

This simple flask app parses the ESPN BottomLine score feed and returns JSON right to your doorstep.

## Endpoints

#### Current
```/ping```
If the app is working, ```/ping``` returns a 200 response. Nothing more, nothing less.

```/ncaaf```
Returns a feed of NCAA DIV-I football scores.

#### Possible?
```/mlb``` , ```/nba```, ```/nfl```, ```/ncaab```

## Deploying

1. Clone this repository.
2. ```heroku create your-app```
3. ```git push heroku master```
4. ?
5. Profit. Or don't. Who would pay for this?