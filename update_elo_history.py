import mysql.connector
import math
from add_game import update_player_stats

DB_CONFIG = {
    'host': 'localhost',
    'user': 'flaskuser',
    'password': 'DrXrus_5425',
    'database': 'mtg_tracker'
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def calculate_elo_change(player_elo, deck_elo, opponent_elo, win, K=48):
    player_elo = float(player_elo)
    deck_elo = float(deck_elo)
    opponent_elo = float(opponent_elo)

    combined_elo = (player_elo + deck_elo) / 2  # Average of player and deck Elo
    expected_score = 1 / (1 + 10 ** ((opponent_elo - combined_elo) / 400))
    actual_score = 1 if win else 0
    
    # Adjust K based on Elo difference
    elo_difference = opponent_elo - combined_elo
    if win:
        if elo_difference > 0:  # Defeating a stronger opponent
            K *= 1.2
        elif elo_difference < 0:  # Defeating a weaker opponent
            K *= 0.8
    else:
        if elo_difference > 0:  # Losing to a stronger opponent
            K *= 0.6
        elif elo_difference < 0:  # Losing to a weaker opponent
            K *= 1.4
    
    new_elo = round(player_elo + K * (actual_score - expected_score))
    new_deck_elo = round(deck_elo + K * (actual_score - expected_score))
    
    return new_elo, new_deck_elo

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
