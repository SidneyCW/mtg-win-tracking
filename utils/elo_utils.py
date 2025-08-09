from utils.db_utils import get_db_connection
from utils.init_new_player import init_player

def calculate_elo_change(player_elo, deck_elo, opponent_elo, win, K=50):
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
            K *= 2.1
        elif elo_difference < 0:  # Defeating a weaker opponent
            K *= 1.3
    else:
        if elo_difference > 0:  # Losing to a stronger opponent
            K *= 0.1
        elif elo_difference < 0:  # Losing to a weaker opponent
            K *= 0.2  # Punish losses to weaker opponents more
    
    new_elo = round(player_elo + K * (actual_score - expected_score))
    new_deck_elo = round(deck_elo + K * (actual_score - expected_score))
    
    return new_elo, new_deck_elo
