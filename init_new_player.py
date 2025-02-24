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
    cursor.execute("INSERT INTO users (name, wins, losses) VALUES (%s, 0, 0)", (name,))
    conn.commit()
    conn.close()

    return {"name": name, "wins": 0, "losses": 0}  # Return new player data


