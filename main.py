import tkinter as tk
import tkinter.font as tkfont

from config import THEME, WINDOW_TITLE
from app import App


def main():
    root = tk.Tk()
    root.title(WINDOW_TITLE)

    try:
        root.state("zoomed")
    except Exception:
        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()
        root.geometry(f"{screen_w}x{screen_h}+0+0")

    tkfont.nametofont("TkDefaultFont").configure(size=12)
    root.configure(bg=THEME["bg"])

    App.show_start(root)
    root.mainloop()


if __name__ == "__main__":
    main()