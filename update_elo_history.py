import mysql.connector
import math
from add_game import update_player_stats, calculate_elo_change
from init_new_player import init_deck, init_player

DB_CONFIG = {
    'host': 'localhost',
    'user': 'flaskuser',
    'password': 'DrXrus_5425',
    'database': 'mtg_tracker'
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def update_all_elos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Reset all Elos to default
    cursor.execute("UPDATE users SET elo = 1000, wins = 0, losses = 0")
    cursor.execute("UPDATE decks SET elo = 1000")
    conn.commit()

    # Get all matches in order of play
    cursor.execute("SELECT * FROM matches ORDER BY id ASC")
    matches = cursor.fetchall()

    for match in matches:
        match_id = match['id']
        winner = match['winner']

        # Get all players and decks
        cursor.execute("SELECT * FROM match_players WHERE match_id = %s", (match_id,))
        players = cursor.fetchall()
        people = [p['player_name'] for p in players]
        decks = [p['deck'] for p in players]

        # Fetch current Elos
        cursor.execute("SELECT name, elo FROM users")
        user_elos = {row['name']: row['elo'] for row in cursor.fetchall()}

        cursor.execute("SELECT player_name, deck_name, elo FROM player_decks")
        deck_elos = {(row['player_name'], row['deck_name']): row['elo'] for row in cursor.fetchall()}

        for i, person in enumerate(people):
            deck = decks[i]
            init_player(person)
            init_deck(person, deck)

            player_elo = user_elos.get(person, 1000)
            deck_elo = deck_elos.get((person, deck), 1000)

            # Get opponent Elos
            opponents_elo = []
            for j, opp in enumerate(people):
                if i != j:
                    opp_elo = user_elos.get(opp, 1000)
                    opp_deck_elo = deck_elos.get((opp, decks[j]), 1000)
                    opp_combined = 0.3 * opp_elo + 0.7 * opp_deck_elo
                    opponents_elo.append(opp_combined)

            win_flag = (person == winner)
            new_player_elo, new_deck_elo = calculate_elo_change(player_elo, deck_elo, opponents_elo, win_flag)

            # Update stats
            if win_flag:
                cursor.execute("UPDATE users SET wins = wins + 1, elo = %s WHERE name = %s", (new_player_elo, person))
            else:
                cursor.execute("UPDATE users SET losses = losses + 1, elo = %s WHERE name = %s", (new_player_elo, person))

            cursor.execute("UPDATE player_decks SET elo = %s WHERE player_name = %s AND deck_name = %s",
                           (new_deck_elo, person, deck))

            cursor.execute("UPDATE match_players SET elo = %s, deck_elo = %s WHERE match_id = %s AND player_name = %s",
                           (new_player_elo, new_deck_elo, match_id, person))

    conn.commit()
    conn.close()
    print("Elo ratings updated successfully!")

if __name__ == "__main__":
    update_all_elos()