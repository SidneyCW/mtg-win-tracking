import sys
import json
import mysql.connector
from flask import Flask, request, jsonify, render_template, url_for
from db_util import get_db_connection
def update_player_stats(person, deck, key, win=False):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if player exists
    cursor.execute("SELECT * FROM users WHERE name = %s", (person,))
    player = cursor.fetchone()

    if player:
        # Update existing player
        cursor.execute("UPDATE users SET wins = wins + %s, losses = losses + %s WHERE name = %s",
                       (1 if win else 0, 0 if win else 1, person))
    else:
        # Create new player
        cursor.execute("INSERT INTO users (name, wins, losses) VALUES (%s, %s, %s)",
                       (person, 1 if win else 0, 0 if win else 1))

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

