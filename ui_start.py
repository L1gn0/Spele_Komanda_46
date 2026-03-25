import tkinter as tk
from tkinter import messagebox

from config import THEME
from validators import validate_length


class StartScreen(tk.Frame):
    def __init__(self, master, on_start):
        super().__init__(master, padx=18, pady=18, bg=THEME["bg"])
        self.on_start = on_start

        self.opponent_var = tk.StringVar(value="human")
        self.algorithm_var = tk.StringVar(value="minimax")
        self.length_var = tk.IntVar(value=15)
        self.starting_player_var = tk.StringVar(value="human")  # human / computer

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self._build_ui()
        self._sync_controls()

    def _build_ui(self):
        title = tk.Label(
            self,
            text="Spēles iestatījumi",
            font=("Segoe UI", 20, "bold"),
            bg=THEME["bg"],
            fg=THEME["text"]
        )
        title.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 14))

        box1 = tk.LabelFrame(
            self,
            text="Pret ko spēlēsi?",
            padx=14,
            pady=14,
            bg=THEME["panel"],
            fg=THEME["text"]
        )
        box1.grid(row=1, column=0, sticky="nsew", padx=(0, 12), pady=(0, 12))

        tk.Radiobutton(
            box1,
            text="Cilvēks (2 spēlētāji)",
            variable=self.opponent_var,
            value="human",
            command=self._sync_controls,
            bg=THEME["panel"],
            fg=THEME["text"],
            selectcolor=THEME["bg"],
            activebackground=THEME["panel"],
            activeforeground=THEME["text"]
        ).pack(anchor="w", pady=4)

        tk.Radiobutton(
            box1,
            text="Dators",
            variable=self.opponent_var,
            value="computer",
            command=self._sync_controls,
            bg=THEME["panel"],
            fg=THEME["text"],
            selectcolor=THEME["bg"],
            activebackground=THEME["panel"],
            activeforeground=THEME["text"]
        ).pack(anchor="w", pady=4)

        box2 = tk.LabelFrame(
            self,
            text="Kurš sāk spēli?",
            padx=14,
            pady=14,
            bg=THEME["panel"],
            fg=THEME["text"]
        )
        box2.grid(row=1, column=1, sticky="nsew", padx=(0, 12), pady=(0, 12))

        self.rb_start_human = tk.Radiobutton(
            box2,
            text="Cilvēks",
            variable=self.starting_player_var,
            value="human",
            bg=THEME["panel"],
            fg=THEME["text"],
            selectcolor=THEME["bg"],
            activebackground=THEME["panel"],
            activeforeground=THEME["text"]
        )
        self.rb_start_computer = tk.Radiobutton(
            box2,
            text="Dators",
            variable=self.starting_player_var,
            value="computer",
            bg=THEME["panel"],
            fg=THEME["text"],
            selectcolor=THEME["bg"],
            activebackground=THEME["panel"],
            activeforeground=THEME["text"]
        )
        self.rb_start_human.pack(anchor="w", pady=4)
        self.rb_start_computer.pack(anchor="w", pady=4)

        box3 = tk.LabelFrame(
            self,
            text="Algoritms datoram",
            padx=14,
            pady=14,
            bg=THEME["panel"],
            fg=THEME["text"]
        )
        box3.grid(row=1, column=2, sticky="nsew", pady=(0, 12))

        self.rb_minimax = tk.Radiobutton(
            box3,
            text="Minimakss",
            variable=self.algorithm_var,
            value="minimax",
            bg=THEME["panel"],
            fg=THEME["text"],
            selectcolor=THEME["bg"],
            activebackground=THEME["panel"],
            activeforeground=THEME["text"]
        )
        self.rb_ab = tk.Radiobutton(
            box3,
            text="Alfa–beta",
            variable=self.algorithm_var,
            value="alphabeta",
            bg=THEME["panel"],
            fg=THEME["text"],
            selectcolor=THEME["bg"],
            activebackground=THEME["panel"],
            activeforeground=THEME["text"]
        )
        self.rb_minimax.pack(anchor="w", pady=4)
        self.rb_ab.pack(anchor="w", pady=4)

        box4 = tk.LabelFrame(
            self,
            text="Simbolu virknes garums (15–25)",
            padx=14,
            pady=14,
            bg=THEME["panel"],
            fg=THEME["text"]
        )
        box4.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(0, 12))

        tk.Label(
            box4,
            text="Garums:",
            bg=THEME["panel"],
            fg=THEME["text"]
        ).pack(side="left")

        self.spin = tk.Spinbox(
            box4,
            from_=15,
            to=25,
            width=6,
            textvariable=self.length_var,
            font=("Segoe UI", 12),
            bg=THEME["bg"],
            fg=THEME["text"],
            insertbackground=THEME["text"]
        )
        self.spin.pack(side="left", padx=10)

        note = tk.Label(
            self,
            text="Piezīme: pēc spēles noteikumiem pirmais simbols ir O. Ja sāk dators, tad dators spēlē ar O.",
            bg=THEME["bg"],
            fg=THEME["muted"],
            wraplength=900,
            justify="left"
        )
        note.grid(row=3, column=0, columnspan=3, sticky="w", pady=(0, 12))

        btns = tk.Frame(self, bg=THEME["bg"])
        btns.grid(row=4, column=0, columnspan=3, sticky="e")

        tk.Button(
            btns,
            text="Sākt spēli",
            command=self._start,
            padx=22,
            pady=10,
            bg=THEME["btn_bg"],
            fg=THEME["btn_fg"],
            activebackground=THEME["accent"],
            activeforeground=THEME["btn_fg"]
        ).pack(side="left", padx=10)

        tk.Button(
            btns,
            text="Iziet",
            command=self.master.destroy,
            padx=22,
            pady=10,
            bg=THEME["btn_bg"],
            fg=THEME["btn_fg"],
            activebackground=THEME["accent"],
            activeforeground=THEME["btn_fg"]
        ).pack(side="left")

    def _sync_controls(self):
        vs_comp = self.opponent_var.get() == "computer"
        algo_state = "normal" if vs_comp else "disabled"
        start_comp_state = "normal" if vs_comp else "disabled"

        self.rb_minimax.configure(state=algo_state)
        self.rb_ab.configure(state=algo_state)
        self.rb_start_computer.configure(state=start_comp_state)

        if not vs_comp and self.starting_player_var.get() == "computer":
            self.starting_player_var.set("human")

    def _start(self):
        ok, result = validate_length(self.length_var.get())
        if not ok:
            messagebox.showerror("Kļūda", result)
            return

        settings = {
            "opponent": self.opponent_var.get(),
            "algorithm": self.algorithm_var.get(),
            "length": result,
            "starting_player": self.starting_player_var.get()
        }
        self.on_start(settings)