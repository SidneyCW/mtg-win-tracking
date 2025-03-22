import mysql.connector
from db_util import get_db_connection

def init_player(name):
    """Initializes a new player in the MySQL database if they don't already exist."""
    
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if player already exists
    cursor.execute("SELECT * FROM users WHERE name = %s", (name,))
    player = cursor.fetchone()

    if player:
        conn.close()
        return player  # Return existing player data

    # Insert new player with default stats
    cursor.execute("INSERT INTO users (name, wins, losses, elo) VALUES (%s, 0, 0, 1000)", (name,))
    conn.commit()
    conn.close()

    return {"name": name, "wins": 0, "losses": 0}  # Return new player data

def init_deck(player_name, deck_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM player_decks WHERE player_name = %s AND deck = %s", (player_name, deck_name))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO player_decks (player_name, deck, elo) VALUES (%s, %s, %s)", (player_name, deck_name, 1000))
        conn.commit()
    conn.close()

