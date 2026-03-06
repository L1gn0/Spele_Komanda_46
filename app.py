from ui_start import StartScreen
from ui_game import GameGUI


class App:
    @staticmethod
    def show_start(root):
        for w in root.winfo_children():
            w.destroy()

        start = StartScreen(
            root,
            on_start=lambda settings: App.start_game(root, settings)
        )
        start.pack(fill="both", expand=True)

    @staticmethod
    def start_game(root, settings):
        for w in root.winfo_children():
            w.destroy()

        GameGUI(
            root,
            settings=settings,
            on_back=lambda: App.show_start(root)
        )