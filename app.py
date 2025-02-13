from flask import Flask, request, jsonify, render_template
import json
import os
from add_game import new_game
from init_new_player import init_player

app = Flask(__name__)

# File paths
USER_DATA_PATH = "user_data/users"
MATCH_DATA_PATH = "user_data/match_data"

# Home page
@app.route('/')
def home():
    return render_template('Main.html')

# API to start a new game
@app.route('/new_game', methods=['POST'])
def start_game():
    data = request.json
    people = data.get('people', [])
    decks = data.get('decks', [])
    winner = data.get('winner', '')

    if not people or not decks or not winner:
        return jsonify({"error": "Missing required fields"}), 400

    match_key = new_game(people, decks, winner)
    return jsonify({"message": "Game added successfully", "match_key": match_key})

# API to fetch all players
@app.route('/players', methods=['GET'])
def get_players():
    try:
        with open(USER_DATA_PATH, 'r') as file:
            users = json.load(file)
        return jsonify(users)
    except (FileNotFoundError, json.JSONDecodeError):
        return jsonify({"error": "No players found"}), 404

# API to fetch all matches
@app.route('/matches', methods=['GET'])
def get_matches():
    try:
        with open(MATCH_DATA_PATH, 'r') as file:
            matches = json.load(file)
        return jsonify(matches)
    except (FileNotFoundError, json.JSONDecodeError):
        return jsonify({"error": "No matches found"}), 404

# Run the app on Raspberry Pi
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
