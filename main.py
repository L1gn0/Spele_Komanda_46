import tkinter as tk
import tkinter.font as tkfont

from config import THEME, WINDOW_TITLE, WINDOW_SIZE, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT
from app import App


def main():
    root = tk.Tk()
    root.title(WINDOW_TITLE)
    root.geometry(WINDOW_SIZE)
    root.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

    tkfont.nametofont("TkDefaultFont").configure(size=12)
    root.configure(bg=THEME["bg"])

    App.show_start(root)
    root.mainloop()


if __name__ == "__main__":
    main()