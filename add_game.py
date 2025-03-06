from db_util import get_db_connection
from init_new_player import init_player

def calculate_elo_change(player_elo, deck_elo, opponent_elo, win, K=84):
    player_elo = float(player_elo)
    deck_elo = float(deck_elo)
    opponent_elo = float(opponent_elo)

    # Make deck Elo have more weight (e.g., 70% deck, 30% player)
    combined_elo = (0.2 * player_elo) + (0.8 * deck_elo)
    expected_score = 1 / (1 + 10 ** ((opponent_elo - combined_elo) / 300))  # Increase impact
    actual_score = 1 if win else 0
    
    # Adjust K based on Elo difference
    elo_difference = opponent_elo - combined_elo
    if win:
        if elo_difference > 0:  # Defeating a stronger opponent
            K *= 1.5
        elif elo_difference < 0:  # Defeating a weaker opponent
            K *= 0.7
    else:
        if elo_difference > 0:  # Losing to a stronger opponent
            K *= 0.7
        elif elo_difference < 0:  # Losing to a weaker opponent
            K *= 1.5  # Punish losses to weaker opponents more
    
    new_elo = round(player_elo + K * (actual_score - expected_score))
    new_deck_elo = round(deck_elo + K * (actual_score - expected_score))
    
    return new_elo, new_deck_elo

def update_player_stats(person, deck, key, win=False):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Ensure player exists
    cursor.execute("SELECT * FROM users WHERE name = %s", (person,))
    player = cursor.fetchone()

    if not player:
        cursor.execute("INSERT INTO users (name, wins, losses, elo) VALUES (%s, 0, 0, 1000)", (person,))
        conn.commit()
        cursor.execute("SELECT * FROM users WHERE name = %s", (person,))
        player = cursor.fetchone()

    # Ensure deck exists in player_decks
    cursor.execute("SELECT * FROM player_decks WHERE player_name = %s AND deck = %s", (person, deck))
    player_deck = cursor.fetchone()

    if not player_deck:
        cursor.execute("INSERT INTO player_decks (player_name, deck, wins, games_played, elo) VALUES (%s, %s, 0, 0, 1000)", 
                       (person, deck))
        conn.commit()
        cursor.execute("SELECT * FROM player_decks WHERE player_name = %s AND deck = %s", (person, deck))
        player_deck = cursor.fetchone()

    # Get opponent's average Elo
    cursor.execute("SELECT AVG((elo + (SELECT elo FROM player_decks WHERE player_decks.player_name = users.name LIMIT 1)) / 2) as avg_elo FROM users WHERE name != %s", (person,))
    opponent_elo = cursor.fetchone()["avg_elo"] or 1000
    
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

