import sys
import json

from init_new_player import init_player

def new_game(people, decks, winner):
    """Starts a new game, records match details, and updates player stats."""
    # Load match data safely
    try:
        with open("user_data/match_data", "r") as file:
            matches = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        matches = {}

    length_check_D = {x for x in decks if len(x) > 6}
    length_check_P = {x for x in people if len(x) > 6}
    winner_check = winner not in people

    if len(length_check_D) > 0 or len(length_check_P) > 0 or winner_check:
        return None
    
    # Prepare player-deck dictionary
    players = {person: decks[i] for i, person in enumerate(people)}

    # Generate a unique match key
    match_key = gen_key(people, matches)

    # Create match entry
    match = {
        match_key: {
            "winner": winner,
            "play_num": len(people),
            "players": players
        }
    }

    # Update match data
    matches.update(match)

    # Save updated match data
    with open("user_data/match_data", "w") as file:
        json.dump(matches, file, indent=4)

    # Update each player's stats
    for person in people:
        update_player_stats(person, players[person], match_key, win=(person == winner))

    return match_key

def update_player_stats(person, deck, key, win=False):
    """Updates a player's stats, adding matches and decks."""
    try:
        with open("user_data/users", "r") as file:
            users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        users = {}

    # Get or create player profile
    if person not in users:
        users[person] = init_player(person)

    player = users[person]

    # Update wins and losses
    player["wins"] += int(win)
    player["losses"] += int(not win)

    # Add deck if it's new
    if deck not in player["decks"]:
        player["decks"].append(deck)

    # Add match key if not already recorded
    if key not in player["matches"]:
        player["matches"].append(key)

    # Save updated user data
    with open("user_data/users", "w") as file:
        json.dump(users, file, indent=4)

def gen_key(people, matches):
    """Generates a unique match key based on existing match keys."""
    # Get existing match keys
    match_keys = list(matches.keys())

    # Determine last key and extract numeric prefix
    if match_keys:
        last_key = match_keys[-1]
        num_part = ''.join(filter(str.isdigit, last_key))  # Extract number
        next_num = int(num_part) + 1  # Increment
    else:
        next_num = 1  # Start numbering from 1 if no matches exist

    # Generate initials-based key suffix
    people_key = "".join(person[0] for person in people)

    # Create new match key
    new_key = f"{next_num}{people_key}"

    return new_key
