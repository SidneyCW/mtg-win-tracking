import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'user': 'flaskuser',
    'password': 'DrXrus_5425',
    'database': 'mtg_tracker'
}

# Initializes the connection to the database given the credentials above
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

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

#runs command if script is run on its own
if __name__ == "__main__":
    init_db()
    print("Databases initialized successfully!")