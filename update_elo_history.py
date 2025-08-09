import mysql.connector
import math
from utils.db_utils import update_player_stats
from dotenv import dotenv_values
from pathlib import Path

dotenv_path = Path(".env")
dotenv = dotenv_values(dotenv_path)

def get_db_connection():
    return mysql.connector.connect(**dotenv['DB_CONFIG'])

def update_all_elos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get all matches
    cursor.execute("SELECT * FROM matches")
    matches = cursor.fetchall()
    
    for match in matches:
        match_id = match['id']
        winner = match['winner']
        
        # Get all players in the match
        cursor.execute("SELECT * FROM match_players WHERE match_id = %s", (match_id,))
        players = cursor.fetchall()
        
        for player in players:
            person = player['player_name']
            deck = player['deck']
            win = (person == winner)
            update_player_stats(person, deck, match_id, win)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_all_elos()
    print("Elo ratings updated successfully!")
