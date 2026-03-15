import random
import time


def is_terminal_state(state) -> bool:
    """Compatibility helper for game state terminal checks."""
    if hasattr(state, "is_terminal"):
        return state.is_terminal()
    return bool(getattr(state, "game_over", False))


def heuristic(state, ai_player: str) -> int:
    """
    Simple heuristic evaluation function:
    - At terminal states: large score difference multiplier
    - During search: current score difference + rough mobility bonus/penalty
    """
    opp = "X" if ai_player == "O" else "O"
    score_diff = state.score[ai_player] - state.score[opp]

    if is_terminal_state(state):
        return score_diff * 100               # terminal states get very high weight

    # Mobility heuristic: number of legal moves available
    moves = state.get_legal_moves()
    mobility_bonus = len(moves) * 1.5 if state.turn == ai_player else -len(moves) * 1.5

    return score_diff + mobility_bonus


# ====================== MINIMAX ======================
def minimax(state, depth: int, ai_player: str) -> int:
    """
    Classic minimax evaluation without alpha-beta pruning.
    Recursively evaluates the game tree to the given depth.
    """
    if depth == 0 or is_terminal_state(state):
        return heuristic(state, ai_player)

    legal_moves = state.get_legal_moves()
    if not legal_moves:
        return heuristic(state, ai_player)

    if state.turn == ai_player:
        # Maximizing player (AI)
        max_eval = float('-inf')
        for move in legal_moves:
            child = state.copy()
            child.apply_move(move)
            eval_score = minimax(child, depth - 1, ai_player)
            max_eval = max(max_eval, eval_score)
        return max_eval
    else:
        # Minimizing player (opponent)
        min_eval = float('inf')
        for move in legal_moves:
            child = state.copy()
            child.apply_move(move)
            eval_score = minimax(child, depth - 1, ai_player)
            min_eval = min(min_eval, eval_score)
        return min_eval


def minimax_move(game_state, depth=5):
    """
    Selects the best move using plain minimax search.
    Returns the move index or None if no moves are available.
    """
    ai_player = game_state.turn
    legal_moves = game_state.get_legal_moves()
    if not legal_moves:
        return None

    best_move = None
    best_value = float('-inf')

    for move in legal_moves:
        child = game_state.copy()
        child.apply_move(move)
        value = minimax(child, depth - 1, ai_player)
        if value > best_value:
            best_value = value
            best_move = move

    return best_move


# ====================== ALPHA-BETA PRUNING ======================
def alphabeta(state, depth: int, alpha: float, beta: float, ai_player: str, maximizing: bool) -> int:
    """
    Alpha-beta pruning version of minimax.
    Prunes branches that won't affect the final decision.
    """
    if depth == 0 or is_terminal_state(state):
        return heuristic(state, ai_player)

    legal_moves = state.get_legal_moves()
    if not legal_moves:
        return heuristic(state, ai_player)

    if maximizing:  # AI's turn (maximizing)
        max_eval = float('-inf')
        for move in legal_moves:
            child = state.copy()
            child.apply_move(move)
            eval_score = alphabeta(child, depth - 1, alpha, beta, ai_player, False)
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break  # Beta cutoff
        return max_eval
    else:  # Opponent's turn (minimizing)
        min_eval = float('inf')
        for move in legal_moves:
            child = state.copy()
            child.apply_move(move)
            eval_score = alphabeta(child, depth - 1, alpha, beta, ai_player, True)
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break  # Alpha cutoff
        return min_eval


def alphabeta_move(game_state, depth=6):
    """
    Selects the best move using alpha-beta pruning.
    Usually faster than plain minimax → can afford slightly deeper search.
    """
    ai_player = game_state.turn
    legal_moves = game_state.get_legal_moves()
    if not legal_moves:
        return None

    best_move = None
    best_value = float('-inf')
    alpha = float('-inf')
    beta = float('inf')

    for move in legal_moves:
        child = game_state.copy()
        child.apply_move(move)
        value = alphabeta(child, depth - 1, alpha, beta, ai_player, False)
        if value > best_value:
            best_value = value
            best_move = move
        alpha = max(alpha, value)
        if beta <= alpha:
            break  # Alpha cutoff at root level

    return best_move


# ====================== ENTRY POINT ======================
def choose_move(game_state, algorithm_name="minimax"):
    """
    Main function called from the UI.
    Selects and returns the best move according to the chosen algorithm.
    """
    legal = game_state.get_legal_moves()
    if not legal:
        return None

    start_time = time.time()

    if algorithm_name == "minimax":
        move = minimax_move(game_state, depth=5)
    elif algorithm_name == "alphabeta":
        move = alphabeta_move(game_state, depth=6)
    else:
        move = random.choice(legal)

    # Optional: for experiments you can log performance
    elapsed = time.time() - start_time
    print(f"{algorithm_name} | move took {elapsed:.3f}s")

    return move
