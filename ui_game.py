import tkinter as tk
from tkinter import messagebox

from config import THEME
from game_logic import GameState
from algorithms import choose_move
from tree import make_state, build_game_tree, tree_to_text


class GameGUI(tk.Frame):
    def __init__(self, master, settings, on_back):
        super().__init__(master, bg=THEME["bg"])
        self.settings = settings
        self.on_back = on_back

        self.game = GameState()
        self.selected = []
        self.player_type = {"O": "human", "X": "human"}

        self._build_ui()
        self._apply_settings_and_start()

    def _build_ui(self):
        self.pack(fill="both", expand=True)

        top = tk.Frame(self, padx=14, pady=14, bg=THEME["panel"])
        top.pack(fill="x")

        tk.Button(
            top,
            text="Atpakaļ uz sākumu",
            command=self._back,
            padx=16,
            pady=8,
            bg=THEME["btn_bg"],
            fg=THEME["btn_fg"],
            activebackground=THEME["accent"],
            activeforeground=THEME["btn_fg"]
        ).pack(side="left")

        self.turn_lbl = tk.Label(
            top,
            text="Gājiens: -",
            font=("Segoe UI", 13, "bold"),
            bg=THEME["panel"],
            fg=THEME["text"]
        )
        self.turn_lbl.pack(side="left", padx=16)

        self.score_lbl = tk.Label(
            top,
            text="Punkti O: 0 | X: 0",
            font=("Segoe UI", 13),
            bg=THEME["panel"],
            fg=THEME["text"]
        )
        self.score_lbl.pack(side="left", padx=16)

        self.meta_lbl = tk.Label(
            top,
            text="",
            font=("Segoe UI", 11),
            bg=THEME["panel"],
            fg=THEME["muted"]
        )
        self.meta_lbl.pack(side="left", padx=16)

        self.info_lbl = tk.Label(
            self,
            text="Izvēlies 2 blakus esošus simbolus.",
            bg=THEME["panel"],
            fg=THEME["text"],
            padx=14,
            pady=8,
            font=("Segoe UI", 11)
        )
        self.info_lbl.pack(fill="x")

        self.board_frame = tk.Frame(self, padx=14, pady=14, bg=THEME["bg"])
        self.board_frame.pack(fill="both", expand=True)

    def _apply_settings_and_start(self):
        n = self.settings["length"]
        opponent = self.settings["opponent"]
        alg = self.settings["algorithm"]

        self.game.generate(n)

        if opponent == "computer":
            self.player_type = {"O": "human", "X": "computer"}
            alg_name = "Minimakss" if alg == "minimax" else "Alfa–beta"
            self.meta_lbl.config(text=f"Pret datoru | Algoritms: {alg_name} | Pagaidām random")
        else:
            self.player_type = {"O": "human", "X": "human"}
            self.meta_lbl.config(text="2 cilvēki uz viena datora")

        if not self.game.has_any_legal_move() and len(self.game.s) > 1:
            self.game.game_over = True

        self._refresh()
        self.after(150, self._maybe_computer_move)

    def _back(self):
        self.destroy()
        self.on_back()

    def _make_tree(self):
        state = make_state(self.game.s, turn=self.game.turn)
        tree = build_game_tree(state, depth=3, ai_player=self.game.turn)
        print(tree_to_text(tree))

    def _maybe_computer_move(self):
        if self.game.game_over:
            return
        if self.player_type.get(self.game.turn) != "computer":
            return

        move_index = choose_move(self.game, self.settings["algorithm"])
        if move_index is None:
            self.game.game_over = True
            self._refresh()
            self._show_end()
            return

        pair, repl, pts = self.game.apply_move(move_index)
        self._make_tree()
        self.info_lbl.config(text=f"Dators: {pair} → {repl} (+{pts}p)")
        self._refresh()

        if self.game.game_over:
            self._show_end()
        else:
            self.after(150, self._maybe_computer_move)

    def _on_symbol_click(self, idx: int):
        if self.game.game_over:
            return
        if self.player_type.get(self.game.turn) != "human":
            return

        if idx in self.selected:
            self.selected.remove(idx)
        else:
            if len(self.selected) >= 2:
                self.selected.clear()
            self.selected.append(idx)

        if len(self.selected) == 2:
            a, b = sorted(self.selected)

            if b != a + 1:
                self.info_lbl.config(text="Jāizvēlas tieši 2 blakus esoši simboli.")
                self.selected.clear()
                self._refresh()
                return

            if self.game.legal_move_at(a) is None:
                self.info_lbl.config(text=f"Nelegāls gājiens {self.game.s[a:b+1]} priekš {self.game.turn}.")
                self.selected.clear()
                self._refresh()
                return

            pair, repl, pts = self.game.apply_move(a)
            self._make_tree()
            self.selected.clear()
            self.info_lbl.config(text=f"Gājiens: {pair} → {repl} (+{pts}p)")
            self._refresh()

            if self.game.game_over:
                self._show_end()
            else:
                self.after(150, self._maybe_computer_move)
        else:
            self._refresh()

    def _show_end(self):
        messagebox.showinfo(
            "Spēle beigusies",
            f"Punkti O: {self.game.score['O']} | X: {self.game.score['X']}\n{self.game.winner_text()}"
        )

    def _refresh(self):
        if not self.game.game_over:
            turn_color = THEME["o_bg"] if self.game.turn == "O" else THEME["x_bg"]
            who = self.player_type.get(self.game.turn, "human")
            who_txt = "cilvēks" if who == "human" else "dators"
            self.turn_lbl.config(text=f"Gājiens: {self.game.turn} ({who_txt})", fg=turn_color)
        else:
            self.turn_lbl.config(text="Gājiens: -", fg=THEME["text"])

        self.score_lbl.config(text=f"Punkti O: {self.game.score['O']} | X: {self.game.score['X']}")

        for w in self.board_frame.winfo_children():
            w.destroy()

        if not self.game.s:
            tk.Label(
                self.board_frame,
                text="Nav spēles. Atgriezies uz sākumu un sāc no jauna.",
                bg=THEME["bg"],
                fg=THEME["muted"]
            ).pack()
            return

        row1 = tk.Frame(self.board_frame, bg=THEME["bg"])
        row1.pack(pady=(0, 10))

        row2 = tk.Frame(self.board_frame, bg=THEME["bg"])
        row2.pack()

        for i, ch in enumerate(self.game.s):
            is_sel = i in self.selected
            base_bg = THEME["o_bg"] if ch == "O" else THEME["x_bg"]
            normal_bg = THEME["sel"] if is_sel else base_bg

            btn = tk.Button(
                row1,
                text=ch,
                width=4,
                height=2,
                font=("Consolas", 22, "bold"),
                bg=normal_bg,
                fg=THEME["btn_fg"],
                activebackground=THEME["accent"],
                activeforeground=THEME["btn_fg"],
                relief="sunken" if is_sel else "raised",
                bd=2,
                command=lambda idx=i: self._on_symbol_click(idx)
            )
            btn.grid(row=0, column=i, padx=4, pady=4)

            def on_enter(e, b=btn, sel=is_sel):
                if not sel:
                    b.configure(bg=THEME["accent"])

            def on_leave(e, b=btn, bg_back=normal_bg):
                b.configure(bg=bg_back)

            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

            tk.Label(
                row2,
                text=str(i),
                font=("Consolas", 11),
                bg=THEME["bg"],
                fg=THEME["muted"]
            ).grid(row=0, column=i, padx=4)
