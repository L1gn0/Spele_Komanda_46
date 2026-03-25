import random
import time
from dataclasses import dataclass


@dataclass
class SearchStats:
    generated_nodes: int = 0
    evaluated_nodes: int = 0
    elapsed_time: float = 0.0
    algorithm_name: str = ""

    def to_dict(self):
        return {
            "generated_nodes": self.generated_nodes,
            "evaluated_nodes": self.evaluated_nodes,
            "elapsed_time": self.elapsed_time,
            "algorithm_name": self.algorithm_name,
        }


@dataclass
class GameStats:
    algorithm_name: str = ""
    computer_symbol: str = ""
    generated_nodes_total: int = 0
    evaluated_nodes_total: int = 0
    total_time: float = 0.0
    computer_moves_count: int = 0

    def add_search(self, search_stats: SearchStats):
        self.generated_nodes_total += search_stats.generated_nodes
        self.evaluated_nodes_total += search_stats.evaluated_nodes
        self.total_time += search_stats.elapsed_time
        self.computer_moves_count += 1

    @property
    def average_time(self) -> float:
        if self.computer_moves_count == 0:
            return 0.0
        return self.total_time / self.computer_moves_count

    def to_dict(self):
        return {
            "algorithm_name": self.algorithm_name,
            "computer_symbol": self.computer_symbol,
            "generated_nodes_total": self.generated_nodes_total,
            "evaluated_nodes_total": self.evaluated_nodes_total,
            "total_time": self.total_time,
            "computer_moves_count": self.computer_moves_count,
            "average_time": self.average_time,
        }


def heuristic(game_state, computer_symbol):
    human_symbol = "O" if computer_symbol == "X" else "X"

    if game_state.game_over:
        comp_score = game_state.score[computer_symbol]
        human_score = game_state.score[human_symbol]

        if comp_score > human_score:
            return 10000
        if comp_score < human_score:
            return -10000
        return 0

    comp_score = game_state.score[computer_symbol]
    human_score = game_state.score[human_symbol]

    score_diff = comp_score - human_score
    legal_moves_now = len(game_state.get_legal_moves())
    mobility = legal_moves_now if game_state.turn == computer_symbol else -legal_moves_now

    return score_diff * 10 + mobility


def minimax(game_state, depth, maximizing, computer_symbol, stats):
    if depth == 0 or game_state.game_over:
        stats.evaluated_nodes += 1
        return heuristic(game_state, computer_symbol), None

    legal_moves = game_state.get_legal_moves()
    if not legal_moves:
        stats.evaluated_nodes += 1
        return heuristic(game_state, computer_symbol), None

    best_move = None

    if maximizing:
        max_eval = float("-inf")
        for move in legal_moves:
            child = game_state.copy()
            child.apply_move(move)
            stats.generated_nodes += 1

            eval_score, _ = minimax(
                child,
                depth - 1,
                False,
                computer_symbol,
                stats
            )

            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move

        return max_eval, best_move

    min_eval = float("inf")
    for move in legal_moves:
        child = game_state.copy()
        child.apply_move(move)
        stats.generated_nodes += 1

        eval_score, _ = minimax(
            child,
            depth - 1,
            True,
            computer_symbol,
            stats
        )

        if eval_score < min_eval:
            min_eval = eval_score
            best_move = move

    return min_eval, best_move


def minimax_move(game_state, computer_symbol):
    stats = SearchStats(algorithm_name="minimax")
    maximizing = (game_state.turn == computer_symbol)

    _, move = minimax(
        game_state,
        depth=6,
        maximizing=maximizing,
        computer_symbol=computer_symbol,
        stats=stats
    )

    if move is None:
        legal_moves = game_state.get_legal_moves()
        move = random.choice(legal_moves) if legal_moves else None

    return move, stats


def alphabeta(game_state, depth, alpha, beta, maximizing, computer_symbol, stats):
    if depth == 0 or game_state.game_over:
        stats.evaluated_nodes += 1
        return heuristic(game_state, computer_symbol), None

    legal_moves = game_state.get_legal_moves()
    if not legal_moves:
        stats.evaluated_nodes += 1
        return heuristic(game_state, computer_symbol), None

    best_move = None

    if maximizing:
        max_eval = float("-inf")
        for move in legal_moves:
            child = game_state.copy()
            child.apply_move(move)
            stats.generated_nodes += 1

            eval_score, _ = alphabeta(
                child,
                depth - 1,
                alpha,
                beta,
                False,
                computer_symbol,
                stats
            )

            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move

            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break

        return max_eval, best_move

    min_eval = float("inf")
    for move in legal_moves:
        child = game_state.copy()
        child.apply_move(move)
        stats.generated_nodes += 1

        eval_score, _ = alphabeta(
            child,
            depth - 1,
            alpha,
            beta,
            True,
            computer_symbol,
            stats
        )

        if eval_score < min_eval:
            min_eval = eval_score
            best_move = move

        beta = min(beta, eval_score)
        if beta <= alpha:
            break

    return min_eval, best_move


def alphabeta_move(game_state, computer_symbol):
    stats = SearchStats(algorithm_name="alphabeta")
    maximizing = (game_state.turn == computer_symbol)

    _, move = alphabeta(
        game_state,
        depth=6,
        alpha=float("-inf"),
        beta=float("inf"),
        maximizing=maximizing,
        computer_symbol=computer_symbol,
        stats=stats
    )

    if move is None:
        legal_moves = game_state.get_legal_moves()
        move = random.choice(legal_moves) if legal_moves else None

    return move, stats


def choose_move(game_state, algorithm_name="minimax", computer_symbol="X"):
    legal_moves = game_state.get_legal_moves()
    if not legal_moves:
        return None, SearchStats(algorithm_name=algorithm_name)

    start = time.perf_counter()

    if algorithm_name == "minimax":
        move, stats = minimax_move(game_state, computer_symbol)
    elif algorithm_name == "alphabeta":
        move, stats = alphabeta_move(game_state, computer_symbol)
    else:
        move = random.choice(legal_moves)
        stats = SearchStats(algorithm_name="random")
        stats.generated_nodes = len(legal_moves)
        stats.evaluated_nodes = 1

    stats.elapsed_time = time.perf_counter() - start

    print(
        f"{stats.algorithm_name} | computer={computer_symbol} | "
        f"generated={stats.generated_nodes} | "
        f"evaluated={stats.evaluated_nodes} | "
        f"time={stats.elapsed_time:.6f}s"
    )

    return move, stats