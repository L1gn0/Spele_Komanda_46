import random


class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.s = ""
        self.turn = "O"
        self.score = {"O": 0, "X": 0}
        self.game_over = True

    def generate(self, n: int):
        self.s = "".join(random.choice(["X", "O"]) for _ in range(n))
        self.turn = "O"
        self.score = {"O": 0, "X": 0}
        self.game_over = False

    def legal_move_at(self, i: int):
        if self.game_over or i < 0 or i >= len(self.s) - 1:
            return None

        pair = self.s[i:i + 2]
        t = self.turn

        if t == "O":
            if pair == "XX":
                return ("O", 2)
            if pair in ("XO", "OX"):
                return ("O", 1)
        else:
            if pair == "OO":
                return ("X", 2)
            if pair in ("XO", "OX"):
                return ("X", 1)

        return None

    def has_any_legal_move(self) -> bool:
        if self.game_over:
            return False
        return any(self.legal_move_at(i) is not None for i in range(len(self.s) - 1))

    def get_legal_moves(self):
        if self.game_over:
            return []
        return [i for i in range(len(self.s) - 1) if self.legal_move_at(i) is not None]

    def apply_move(self, i: int):
        info = self.legal_move_at(i)
        if info is None:
            raise ValueError("Illegal move")

        replacement, pts = info
        pair = self.s[i:i + 2]

        self.s = self.s[:i] + replacement + self.s[i + 2:]
        self.score[self.turn] += pts

        if len(self.s) <= 1:
            self.game_over = True
            return pair, replacement, pts

        self.turn = "X" if self.turn == "O" else "O"

        if not self.has_any_legal_move():
            self.game_over = True

        return pair, replacement, pts

    def winner_text(self) -> str:
        o, x = self.score["O"], self.score["X"]
        if o > x:
            return "Uzvar O (apļi)!"
        if x > o:
            return "Uzvar X (krustiņi)!"
        return "Neizšķirts!"

    def copy(self):
        """Returns a deep copy of the current game state for search purposes."""
        new_state = GameState()
        new_state.s = self.s
        new_state.turn = self.turn
        new_state.score = self.score.copy()
        new_state.game_over = self.game_over
        return new_state