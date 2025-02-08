import sys
import json

def init_player(name):
    """Initializes a new player with default stats and saves to the users JSON file."""
    user = {
        "wins": 0,
        "losses": 0,
        "decks": [],
        "matches": []  # Added to track match history
    }

    try:
        with open("user_data/users", "r") as file:
            users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        users = {}  # If file is missing or empty, create a new dictionary

    # Check if player already exists
    if name in users:
        return users[name]  # Return existing player data

    # Add new player
    users[name] = user

    # Save updated users data
    with open("user_data/users", "w") as file:
        json.dump(users, file, indent=4)

    return user  # Return the newly created player data

