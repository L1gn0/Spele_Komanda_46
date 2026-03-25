import random
from dataclasses import dataclass

from game_logic import GameState
from algorithms import choose_move, GameStats


@dataclass
class ExperimentResult:
    algorithm_name: str
    computer_symbol: str
    winner: str
    computer_score: int
    human_score: int
    generated_nodes_total: int
    evaluated_nodes_total: int
    total_time: float
    computer_moves_count: int
    average_time: float
    initial_string: str


def simulate_one_game(
    algorithm_name: str,
    string_length: int = 15,
    computer_starts: bool = False,
    seed: int | None = None
) -> ExperimentResult:
    """
    Simulē vienu spēli bez GUI.
    Cilvēka gājieni tiek modelēti kā nejauši legāli gājieni.
    """
    if seed is not None:
        random.seed(seed)

    game = GameState()
    game.generate(string_length, starting_turn="O")

    # Pēc spēles noteikumiem sāk O.
    # Ja sāk dators, tad dators = O, cilvēks = X
    # Ja sāk cilvēks, tad cilvēks = O, dators = X
    if computer_starts:
        computer_symbol = "O"
        human_symbol = "X"
    else:
        computer_symbol = "X"
        human_symbol = "O"

    player_type = {
        computer_symbol: "computer",
        human_symbol: "human"
    }

    initial_string = game.s

    game_stats = GameStats(
        algorithm_name=algorithm_name,
        computer_symbol=computer_symbol
    )

    if not game.has_any_legal_move() and len(game.s) > 1:
        game.game_over = True

    while not game.game_over:
        current_player_type = player_type[game.turn]

        if current_player_type == "computer":
            move_index, stats = choose_move(
                game_state=game,
                algorithm_name=algorithm_name,
                computer_symbol=computer_symbol
            )

            if move_index is None:
                game.game_over = True
                break

            game_stats.add_search(stats)
            game.apply_move(move_index)

        else:
            legal_moves = game.get_legal_moves()
            if not legal_moves:
                game.game_over = True
                break

            move_index = random.choice(legal_moves)
            game.apply_move(move_index)

    o_score = game.score["O"]
    x_score = game.score["X"]

    computer_score = game.score[computer_symbol]
    human_score = game.score[human_symbol]

    if computer_score > human_score:
        winner = "computer"
    elif human_score > computer_score:
        winner = "human"
    else:
        winner = "draw"

    return ExperimentResult(
        algorithm_name=algorithm_name,
        computer_symbol=computer_symbol,
        winner=winner,
        computer_score=computer_score,
        human_score=human_score,
        generated_nodes_total=game_stats.generated_nodes_total,
        evaluated_nodes_total=game_stats.evaluated_nodes_total,
        total_time=game_stats.total_time,
        computer_moves_count=game_stats.computer_moves_count,
        average_time=game_stats.average_time,
        initial_string=initial_string
    )


def run_experiments(
    algorithm_name: str,
    num_games: int = 10,
    string_length: int = 15,
    alternate_starting_player: bool = True,
    base_seed: int = 1000
):
    """
    Palaiž vairākas spēles un atgriež sarakstu ar rezultātiem.
    """
    results = []

    for i in range(num_games):
        if alternate_starting_player:
            computer_starts = (i % 2 == 0)
        else:
            computer_starts = False

        result = simulate_one_game(
            algorithm_name=algorithm_name,
            string_length=string_length,
            computer_starts=computer_starts,
            seed=base_seed + i
        )
        results.append(result)

    return results


def summarize_results(results: list[ExperimentResult]):
    total_games = len(results)
    computer_wins = sum(1 for r in results if r.winner == "computer")
    human_wins = sum(1 for r in results if r.winner == "human")
    draws = sum(1 for r in results if r.winner == "draw")

    total_generated = sum(r.generated_nodes_total for r in results)
    total_evaluated = sum(r.evaluated_nodes_total for r in results)
    total_time = sum(r.total_time for r in results)
    total_computer_moves = sum(r.computer_moves_count for r in results)

    avg_generated_per_game = total_generated / total_games if total_games else 0.0
    avg_evaluated_per_game = total_evaluated / total_games if total_games else 0.0
    avg_time_per_game = total_time / total_games if total_games else 0.0
    avg_time_per_move = total_time / total_computer_moves if total_computer_moves else 0.0

    return {
        "games": total_games,
        "computer_wins": computer_wins,
        "human_wins": human_wins,
        "draws": draws,
        "total_generated": total_generated,
        "total_evaluated": total_evaluated,
        "total_time": total_time,
        "total_computer_moves": total_computer_moves,
        "avg_generated_per_game": avg_generated_per_game,
        "avg_evaluated_per_game": avg_evaluated_per_game,
        "avg_time_per_game": avg_time_per_game,
        "avg_time_per_move": avg_time_per_move,
    }


def print_results_table(results: list[ExperimentResult]):
    print("\n" + "=" * 110)
    print(
        f"{'Nr.':<4} {'Alg.':<10} {'Comp':<5} {'Winner':<10} "
        f"{'CompScore':<10} {'HumanScore':<11} "
        f"{'GenNodes':<10} {'EvalNodes':<10} {'Moves':<7} {'AvgTime':<10}"
    )
    print("-" * 110)

    for i, r in enumerate(results, start=1):
        print(
            f"{i:<4} {r.algorithm_name:<10} {r.computer_symbol:<5} {r.winner:<10} "
            f"{r.computer_score:<10} {r.human_score:<11} "
            f"{r.generated_nodes_total:<10} {r.evaluated_nodes_total:<10} "
            f"{r.computer_moves_count:<7} {r.average_time:<10.5f}"
        )

    print("=" * 110)


def print_summary(summary: dict, algorithm_name: str):
    print(f"\nKOPSAVILKUMS algoritmam: {algorithm_name}")
    print("-" * 45)
    print(f"Spēļu skaits: {summary['games']}")
    print(f"Datora uzvaras: {summary['computer_wins']}")
    print(f"Cilvēka uzvaras: {summary['human_wins']}")
    print(f"Neizšķirti: {summary['draws']}")
    print(f"Ģenerētās virsotnes kopā: {summary['total_generated']}")
    print(f"Novērtētās virsotnes kopā: {summary['total_evaluated']}")
    print(f"Kopējais laiks: {summary['total_time']:.5f}s")
    print(f"Datora gājieni kopā: {summary['total_computer_moves']}")
    print(f"Vidēji ģenerētas virsotnes spēlē: {summary['avg_generated_per_game']:.2f}")
    print(f"Vidēji novērtētas virsotnes spēlē: {summary['avg_evaluated_per_game']:.2f}")
    print(f"Vidējais laiks spēlē: {summary['avg_time_per_game']:.5f}s")
    print(f"Vidējais laiks uz datora gājienu: {summary['avg_time_per_move']:.5f}s")


def main():
    NUM_GAMES = 10
    STRING_LENGTH = 15

    print("Palaiž Minimaksa eksperimentus...")
    minimax_results = run_experiments(
        algorithm_name="minimax",
        num_games=NUM_GAMES,
        string_length=STRING_LENGTH,
        alternate_starting_player=True,
        base_seed=1000
    )
    print_results_table(minimax_results)
    minimax_summary = summarize_results(minimax_results)
    print_summary(minimax_summary, "minimax")

    print("\n\nPalaiž Alfa-beta eksperimentus...")
    alphabeta_results = run_experiments(
        algorithm_name="alphabeta",
        num_games=NUM_GAMES,
        string_length=STRING_LENGTH,
        alternate_starting_player=True,
        base_seed=2000
    )
    print_results_table(alphabeta_results)
    alphabeta_summary = summarize_results(alphabeta_results)
    print_summary(alphabeta_summary, "alphabeta")


if __name__ == "__main__":
    main()