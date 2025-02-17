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

