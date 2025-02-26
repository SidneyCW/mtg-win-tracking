import time
import mysql.connector
from flask import Flask, request, jsonify, render_template, url_for
import json
import os
from add_game import update_player_stats, gen_key
from db_util import get_db_connection
from init_new_player import init_player

app = Flask(__name__)

# File paths
USER_DATA_PATH = "user_data/users"
MATCH_DATA_PATH = "user_data/match_data"

@app.context_processor
def override_url_for():
    def hashed_url_for(endpoint, **values):
        if endpoint == 'static':
            values['q'] = int(time.time())  # Adds a timestamp to force reload
        return url_for(endpoint, **values)
    return dict(url_for=hashed_url_for)

# Home page
@app.route('/')
def home():
    return render_template('Main.html')

# Register Deck Page
@app.route("/register_decks")
def register_decks():
    print("Serving register_deck.html")  # Debugging step
    return render_template("register_deck.html")

# Vault Page
@app.route("/vaults")
def vaults():
    print("Serving Vault.html")  # Debugging step
    return render_template("Vault.html")







# API to start a new game

@app.route('/start_game', methods=['POST'])
def start_game():
    try:
        data = request.get_json()
        people = data['people']  # List of player names
        decks = data['decks']  # List of corresponding decks
        winner = data['winner']  # Name of the winner

        if len(people) != len(decks):
            return jsonify({"error": "Mismatch between players and decks"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Generate a unique match key
        match_key = gen_key(people)

        # Insert match into the database
        cursor.execute("INSERT INTO matches (match_key, winner, play_num) VALUES (%s, %s, %s)",
                       (match_key, winner, len(people)))
        match_id = cursor.lastrowid

        # Insert each player and their deck into match_players
        for i, person in enumerate(people):
            cursor.execute("INSERT INTO match_players (match_id, player_name, deck) VALUES (%s, %s, %s)",
                           (match_id, person, decks[i]))
            update_player_stats(person, decks[i], match_key, win=(person == winner))

        conn.commit()
        conn.close()
        
        return jsonify({"message": "Game started successfully", "match_key": match_key}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/matches", methods=["GET"])
def get_matches():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM matches")
    matches = cursor.fetchall()
    conn.close()

    return jsonify(matches)

@app.route("/players", methods=["GET"])
def get_players():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    players = cursor.fetchall()
    conn.close()

    return jsonify(players)

@app.route("/get_decks", methods=["GET"])
def get_decks():
    player_name = request.args.get("player")  # Get player from URL query

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if player_name:
        # ✅ Fetch decks only for this player
        cursor.execute("SELECT deck FROM player_decks WHERE player_name = %s", (player_name,))
    else:
        # Return all decks (default behavior)
        cursor.execute("SELECT DISTINCT deck FROM player_decks")

    decks = [row["deck"] for row in cursor.fetchall()]
    conn.close()

    return jsonify({"decks": decks})

@app.route("/register_deck", methods=["POST"])
def register_deck():
    try:
        data = request.get_json()
        player_name = data.get("player")
        deck_name = data.get("deck")

        if not player_name or not deck_name:
            return jsonify({"error": "Player name and deck name are required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Ensure the player exists
        init_player(player_name)

        # Check if the deck already exists for the player
        cursor.execute(
            "SELECT * FROM player_decks WHERE player_name = %s AND deck = %s",
            (player_name, deck_name),
        )
        existing_deck = cursor.fetchone()

        if existing_deck:
            return jsonify({"error": "Deck already exists for this player"}), 409

        # Insert new deck for the player
        cursor.execute(
            "INSERT INTO player_decks (player_name, deck, wins, games_played) VALUES (%s, %s, 0, 0)",
            (player_name, deck_name),
        )
        conn.commit()
        conn.close()

        return jsonify({"message": "Deck registered successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get_player_decks", methods=["GET"])
def get_player_decks():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT player_name, deck, wins FROM player_decks ORDER BY wins DESC
        """)
        
        decks = cursor.fetchall()
        conn.close()

        if not decks:
            return jsonify([])  # Return empty list if no data
        
        return jsonify(decks)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get_wins", methods=["GET"])
def get_wins():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT name, wins FROM users ORDER BY wins DESC")
    players = cursor.fetchall()
    conn.close()
    return jsonify(players)












# Run the app on Raspberry Pi
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


