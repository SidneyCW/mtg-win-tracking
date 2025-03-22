# mtg-win-tracking
## win tracking
this web app acts as a simple way to track wins in mtg games with our group of players
## user tracking
as well as win tracking this app tracks what decks players have as well as what matches they participated in
## elo tracking
elo is calculated and stored for both decks and players and actively updated by inputting matches
## match keys
the format for match keys is simple <br />
(number of game) - (followed by first initial of each player who participated in the match) <br />
i. e.
```
1KS
```
for 1st game in storage, then K (Keean) and S (Sidney)
## sql
this system uses a sql database storing the data in 5 tables [users, matches, match_players, player_decks, elo_history]
## running the web app
to initialize the databases after installing mysql run the following command
```
python db_util.py
```
while the app is local you can run it in your terminal by the following command
```
python app.py --host=0.0.0.0
```
