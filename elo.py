from db_util import get_db_connection

def players_win(pl_elo: list, dk_elo: list) -> list:
    for idx, player in enumerate(pl_elo):
        pl_elo[idx] = player + dk_elo[idx]
    w_elo = [int(100-(elo/sum(pl_elo))*100) for elo in pl_elo]
    return w_elo

def players_loss_w(w_elo: list) -> list:
    l_elo = [100-elo for elo in w_elo]
    return l_elo

def players_loss_b(pl_elo: list, dk_elo: list) -> list:
    l_elo = [int(100-elo) for elo in players_win(pl_elo, dk_elo)]
    return l_elo
