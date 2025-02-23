from db_util import get_db_connection
from init_new_player import init_player

def update_player_stats(person, deck, key, win=False):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Initialize the player if they don't exist
    init_player(person)

    # Update player stats
    if win:
        cursor.execute("UPDATE users SET wins = wins + 1 WHERE name = %s", (person,))
    else:
        cursor.execute("UPDATE users SET losses = losses + 1 WHERE name = %s", (person,))

    # Check if the deck exists in `player_decks`
    cursor.execute("SELECT * FROM player_decks WHERE player_name = %s AND deck = %s", (person, deck))
    existing_deck = cursor.fetchone()

    if existing_deck:
        # Update deck stats
        cursor.execute("""
            UPDATE player_decks
            SET wins = wins + %s, games_played = games_played + 1
            WHERE player_name = %s AND deck = %s
        """, (1 if win else 0, person, deck))
    else:
        # Insert a new deck record
        cursor.execute("""
            INSERT INTO player_decks (player_name, deck, wins, games_played)
            VALUES (%s, %s, %s, 1)
        """, (person, deck, 1 if win else 0))
        
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

