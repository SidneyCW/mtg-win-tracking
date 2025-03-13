import time
import mysql.connector
from flask import Flask, request, jsonify, render_template, url_for
import json
import os
from add_game import update_player_stats, gen_key
from db_util import get_db_connection
from init_new_player import init_player

app = Flask(__name__)

USER_DATA_PATH = "user_data/users"
MATCH_DATA_PATH = "user_data/match_data"

@app.context_processor
def override_url_for():
    def hashed_url_for(endpoint, **values):
        if endpoint == 'static':
            values['q'] = int(time.time())
        return url_for(endpoint, **values)
    return dict(url_for=hashed_url_for)

@app.route('/')
def home():
    return render_template('Main.html')

@app.route("/register_decks")
def register_decks():
    print("Serving register_deck.html")
    return render_template("register_deck.html")

@app.route("/vaults")
def vaults():
    print("Serving Vault.html")
    return render_template("Vault.html")


@app.route('/start_game', methods=['POST'])
def start_game():
    try:
        data = request.get_json()
        people = data['people']
        decks = data['decks']
        winner = data['winner']

        if len(people) != len(decks):
            return jsonify({"error": "Mismatch between players and decks"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        match_key = gen_key(people)

        cursor.execute("INSERT INTO matches (match_key, winner, play_num) VALUES (%s, %s, %s)",
                       (match_key, winner, len(people)))
        match_id = cursor.lastrowid

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
    player_name = request.args.get("player")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if player_name:
        cursor.execute("SELECT deck FROM player_decks WHERE player_name = %s", (player_name,))
    else:
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

        init_player(player_name)

        cursor.execute(
            "SELECT * FROM player_decks WHERE player_name = %s AND deck = %s",
            (player_name, deck_name),
        )
        existing_deck = cursor.fetchone()

        if existing_deck:
            return jsonify({"error": "Deck already exists for this player"}), 409

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
            return jsonify([])
        
        return jsonify(decks)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get_deck_elo", methods=["GET"])
def get_deck_elo():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT player_name, deck, elo FROM player_decks ORDER BY elo DESC
        """)
        
        deck_elo = cursor.fetchall()
        conn.close()

        if not deck_elo:
            return jsonify([]) 
        
        return jsonify(deck_elo)

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

@app.route("/get_player_elo", methods=["GET"])
def get_player_elo():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT name, elo FROM users ORDER BY elo DESC")
    p_elos = cursor.fetchall()
    conn.close()
    return jsonify(p_elos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


