import mysql.connector
from elo_utils import calculate_elo_change
from dotenv import dotenv_values
from pathlib import Path

dotenv_path = Path(".env")
dotenv = dotenv_values(dotenv_path)
# Initializes the connection to the database given the credentials above
def get_db_connection():
    return mysql.connector.connect(**dotenv["DB_CONFIG"])

# Initializes the database if tables do not exist
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL COLLATE utf8_general_ci,
            wins INT DEFAULT 0,
            losses INT DEFAULT 0,
	    elo INT DEFAULT 500
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id INT AUTO_INCREMENT PRIMARY KEY,
            match_key VARCHAR(50) UNIQUE NOT NULL COLLATE utf8_general_ci,
            winner VARCHAR(50) NOT NULL COLLATE utf8_general_ci,
            play_num INT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS match_players (
            match_id INT,
            player_name VARCHAR(50) COLLATE utf8_general_ci,
            deck VARCHAR(50) COLLATE utf8_general_ci,
            FOREIGN KEY (match_id) REFERENCES matches(id) ON DELETE CASCADE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS player_decks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            player_name VARCHAR(50) COLLATE utf8_general_ci,
            deck VARCHAR(50) COLLATE utf8_general_ci,
            wins INT DEFAULT 0,
            games_played INT DEFAULT 0,
	    elo INT DEFAULT 500,
            UNIQUE(player_name, deck),
            FOREIGN KEY (player_name) REFERENCES users(name) ON DELETE CASCADE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS elo_history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            player_name VARCHAR(50) COLLATE utf8mb4_general_ci,
            deck VARCHAR(50) COLLATE utf8mb4_general_ci,
            old_elo INT,
            new_elo INT,
            match_id INT,
            FOREIGN KEY (player_name) REFERENCES users(name) ON DELETE CASCADE,
            FOREIGN KEY (deck) REFERENCES player_decks(deck) ON DELETE CASCADE,
            FOREIGN KEY (match_id) REFERENCES matches(id) ON DELETE CASCADE
        )
    ''')


    conn.commit()
    conn.close()

def update_player_stats(person, deck, key, win=False):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Ensure player exists
    cursor.execute("SELECT * FROM users WHERE name = %s", (person,))
    player = cursor.fetchone()

    # If player doesn't exist initialize player values
    if not player:
        cursor.execute("INSERT INTO users (name, wins, losses, elo) VALUES (%s, 0, 0, 500)", (person,))
        conn.commit()
        cursor.execute("SELECT * FROM users WHERE name = %s", (person,))
        player = cursor.fetchone()

    # Ensure deck exists in player_decks
    cursor.execute("SELECT * FROM player_decks WHERE player_name = %s AND deck = %s", (person, deck))
    player_deck = cursor.fetchone()

    #If deck doesn't exist initialize deck values
    if not player_deck:
        cursor.execute("INSERT INTO player_decks (player_name, deck, wins, games_played, elo) VALUES (%s, %s, 0, 0, 500)", 
                       (person, deck))
        conn.commit()
        cursor.execute("SELECT * FROM player_decks WHERE player_name = %s AND deck = %s", (person, deck))
        player_deck = cursor.fetchone()

    # Get opponent's average Elo
    cursor.execute("SELECT AVG((elo + (SELECT elo FROM player_decks WHERE player_decks.player_name = users.name LIMIT 1)) / 2) as avg_elo FROM users WHERE name != %s", (person,))
    opponent_elo = cursor.fetchone()["avg_elo"] or 500
    
    # Calculate new Elo ratings
    new_player_elo, new_deck_elo = calculate_elo_change(player["elo"], player_deck["elo"], opponent_elo, win)
    
    # Update player stats
    if win:
        cursor.execute("UPDATE users SET wins = wins + 1, elo = %s WHERE name = %s", (new_player_elo, person))
        cursor.execute("UPDATE player_decks SET wins = wins + 1, elo = %s, games_played = games_played + 1 WHERE player_name = %s AND deck = %s",
                       (new_deck_elo, person, deck))
    else:
        cursor.execute("UPDATE users SET losses = losses + 1, elo = %s WHERE name = %s", (new_player_elo, person))
        cursor.execute("UPDATE player_decks SET elo = %s, games_played = games_played + 1 WHERE player_name = %s AND deck = %s",
                       (new_deck_elo, person, deck))

    conn.commit()
    conn.close()

def gen_key(people):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Count total matches to generate a unique number prefix
    cursor.execute("SELECT COUNT(*) FROM matches")
    match_count = cursor.fetchone()[0] + 1  # Start from 1

    # Generate a unique key using the match count and first letter of each player's name
    people_key = ''.join(person[0].upper() for person in people)
    new_key = f"{match_count}{people_key}"

    conn.close()
    return new_key