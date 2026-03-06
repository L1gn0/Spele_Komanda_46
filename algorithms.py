import random


def choose_move(game_state, algorithm_name="minimax"):
    legal_moves = game_state.get_legal_moves()
    if not legal_moves:
        return None

    if algorithm_name == "minimax":
        return minimax_move(game_state)

    if algorithm_name == "alphabeta":
        return alphabeta_move(game_state)

    return random.choice(legal_moves)


def minimax_move(game_state):
    # Pagaidām vietturis
    return random.choice(game_state.get_legal_moves())


def alphabeta_move(game_state):
    # Pagaidām vietturis
    return random.choice(game_state.get_legal_moves())