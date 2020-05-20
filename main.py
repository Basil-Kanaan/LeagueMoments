from tkinter import Tk, Button, Label, Frame, Scrollbar, Listbox, Entry, Text, LabelFrame, Toplevel
from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory
from datetime import datetime
from threading import Thread
from time import sleep
import tkinter as tk
import configparser
import os
from typing import TextIO

app_closed = False
in_game = False


class App:
    master: Tk

    sidebar: Frame
    buttons: dict
    dialogue: Text

    main: Frame
    gamecards: Listbox

    league_directory: str

    def __init__(self):
        self.league_directory = "C:\Riot Games\League of Legends"
        self.master = Tk()
        master = self.master

        master.geometry("500x400")
        master.title("League Moments")

        self._init_sidebar(master)
        self._init_mainframe(master)

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

        HotkeyCard(new_window, "Timestamp")

    def set_league_path(self):
        base_path = os.getcwd().split(os.sep)[0]
        path = askdirectory(mustexist=True, initialdir=base_path, title="Please select your League of Legends folder")
        path = os.sep.join(path.split("/"))
        self.league_directory = path

    def mainloop(self):
        self.master.mainloop()


class GameChecker(Thread):

    app: App
    start_time: datetime

    def __init__(self, _app):
        super().__init__()
        self.app = _app

    def run(self):
        sep = os.sep

        while not app_closed:

            league_path = self.app.league_directory
            logs_path = league_path + sep + "Logs" + sep + "GameLogs"

            if os.path.exists(logs_path):
                timestamp = os.path.getmtime(logs_path)
                latest_modified = datetime.fromtimestamp(timestamp).minute

                if latest_modified == datetime.now().minute:
                    self._loading_screen_start(logs_path)

            sleep(1)

    def _loading_screen_start(self, logs_path):
        game_log_path = logs_path + os.sep + os.listdir(logs_path)[-1]

        game_file: TextIO
        for filename in os.listdir(game_log_path):
            if "r3dlog.txt" in filename:
                game_path = game_log_path + os.sep + filename
                game_file = open(game_path)

        for line in self._tail(game_file):
            print(line.strip())

            pre_to_spawn = "GAMESTATE_PREGAME to GAMESTATE_SPAWN"
            spawn_to_loop = "GAMESTATE_SPAWN to GAMESTATE_GAMELOOP"
            loop_to_end = "GAMESTATE_PRE_EXIT to GAMESTATE_EXIT"

            if pre_to_spawn in line:
                # TODO: WORK ON THIS
                self.start_time = datetime.now()
                print("\nGAME STARTED\n")
                in_game = True

            if loop_to_end in line:
                in_game = False
                break

        game_file.close()

    def _tail(self, file):
        file.seek(0, 2)
        while True:
            line = file.readline()
            if line.strip():
                yield line
            sleep(0.1)


class GameCard:
    def __init__(self):
        pass


class HotkeyCard(Frame):

    action: Label
    hotkey: Entry

    def __init__(self, parent, action, **kw):
        super().__init__(parent, **kw)

        self.action = Label(self, text=action+":", width=10, anchor="e", bg="gray80")
        self.action.grid(row=0, column=0, sticky="nsew")

        self.hotkey = Entry(self, state="disabled")
        self.hotkey.grid(row=0, column=1, sticky="nsew")

        Button(self, text="Record", width=9, bg="lawngreen", command=self.set_hotkey)\
            .grid(row=0, column=2, sticky="nsew")

        Button(self, text="Delete", width=9, bg="#e3aaaa", command=self.delete_hotkey)\
            .grid(row=0, column=3, sticky="nsew")

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.pack(side="top", fill="x", padx=10, pady=(10, 0))

    def delete_hotkey(self):
        self.hotkey.configure(state="normal")
        self.hotkey.delete(0, 'end')
        self.hotkey.configure(state="disabled")

    def set_hotkey(self):
        self.hotkey.configure(state="normal")
        self.hotkey.insert(0, 'Press Combination...')
        self.hotkey.configure(state="disabled")

        self.bind("<KeyPress>", self._key_press)

    def _key_press(self, event):
        print("Key: ", event.char)


if __name__ == "__main__":
    app = App()

    config = configparser.ConfigParser()
    GameChecker(app).start()

    app.mainloop()
    app_closed = True


