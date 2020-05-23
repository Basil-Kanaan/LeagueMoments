from tkinter import Tk, Button, Frame, Scrollbar, Listbox, Text, LabelFrame, Toplevel
from tkinter.filedialog import askdirectory
from game_checker import GameChecker
from hotkey_card import HotkeyCard
from configparser import ConfigParser
from datetime import datetime
import tkinter as tk
import keyboard
import globals
import os


class App:
    master: Tk

    sidebar: Frame
    buttons: dict
    dialogue: Text

    main: Frame
    gamecards: Listbox

    league_directory: str

    config: ConfigParser

    times: list

    def __init__(self):
        self.league_directory = "C:\Riot Games\League of Legends"
        self.master = Tk()
        master = self.master

        master.geometry("500x400")
        master.title("League Moments")

        self._init_sidebar(master)
        self._init_mainframe(master)

        keyboard.add_hotkey('CTRL+S', self.save_time, args=())

        self.config = ConfigParser()

    def _init_mainframe(self, parent):
        self.mainframe = Frame(parent)

        mainframe = self.mainframe
        mainframe.pack(fill="both", padx=20, pady=20, expand=True)

        scrollbar = Scrollbar(mainframe)
        self.gamecards = Listbox(mainframe, yscrollcommand=scrollbar.set)

        self.gamecards.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _init_sidebar(self, parent):
        self.sidebar = Frame(parent, relief=tk.RAISED, bd=2, bg="gray")

        sidebar = self.sidebar
        sidebar.pack(fill=tk.BOTH, side=tk.RIGHT)

        timestamp = Button(sidebar, text="Hotkeys...")
        directory = Button(sidebar, text="League Directory...")
        delete = Button(sidebar, text="Delete File", bg="#e3aaaa")

        timestamp.pack(side="top", fill="x", padx=10, pady=(5, 0))
        directory.pack(side="top", fill="x", padx=10, pady=(5, 0))
        delete.pack(side="top", fill="x", padx=10, pady=(5, 0))

        timestamp.config(command=self.hotkey_panel)
        directory.config(command=self.set_league_path)

        # Entry(sidebar, text="Test", state="disabled").pack(padx=10)

        label_frame = LabelFrame(sidebar, text="Dialogue:")
        label_frame.pack(side="bottom", padx=10, pady=5)

        self.dialogue = Text(label_frame, width=20, height=3, borderwidth="1", font=("device", 8))
        self.dialogue.pack()
        self.dialogue.insert(tk.END, "... text here ...")
        self.dialogue.configure(state="disabled")

    def hotkey_panel(self):
        master = self.master
        new_window = Toplevel(master)
        new_window.title("Hotkey Settings")
        new_window.grab_set()

        x, y, dx, dy = [int(i) for i in
                        master.winfo_geometry().replace("+", "x").split("x")]

        new_window.geometry(f"{x-40}x{y//2-40}+{dx+20}+{dy+20}")

        header_frame = Frame(new_window)
        header_frame.pack(side="top", fill="x", padx=10, pady=(10, 0))

        HotkeyCard(self, new_window, "Timestamp", "CTRL+S")

    def set_league_path(self):
        base_path = os.getcwd().split(os.sep)[0]
        path = askdirectory(mustexist=True, initialdir=base_path, title="Please select your League of Legends folder")
        path = os.sep.join(path.split("/"))
        self.league_directory = path

    def save_time(self):
        if globals.in_game:
            self.times.append(datetime.now())

    def shelve_times(self):
        start = self.times[0]

        times = []
        for time in self.times[1:]:
            time = (time - start).seconds
            minutes = time//60
            seconds = time % 60
            times.append(f"{minutes}:{seconds}")

        self.config.read('games.txt')
        self.config["GAME 1"] = times

        with open('games.txt', 'w') as gamefile:
            self.config.write(gamefile)

    def mainloop(self):
        self.master.mainloop()


class GameCard:
    def __init__(self):
        pass


if __name__ == "__main__":
    app = App()

    GameChecker(app).start()

    app.mainloop()
