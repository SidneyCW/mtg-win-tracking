import mysql.connector
DB_CONFIG = {
    'host': 'localhost',
    'user': 'flaskuser',
    'password': 'DrXrus_5425',
    'database': 'mtg_tracker'
}

# initializes the connection to the database givin the credentials initialized above
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# initializes the database given that the database does not have any tables yet
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL,
            wins INT DEFAULT 0,
            losses INT DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id INT AUTO_INCREMENT PRIMARY KEY,
            match_key VARCHAR(50) UNIQUE NOT NULL,
            winner VARCHAR(50) NOT NULL,
            play_num INT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS match_players (
            match_id INT,
            player_name VARCHAR(50),
            deck VARCHAR(50),
            FOREIGN KEY (match_id) REFERENCES matches(id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()
