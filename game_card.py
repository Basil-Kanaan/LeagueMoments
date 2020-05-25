from tkinter import Frame, Label, Button, Listbox, Scrollbar


class GameCard(Frame):

    ally_team: Listbox
    enemy_team: Listbox

    timestamps: Listbox

    def __init__(self, parent, app, allies, enemies, timestamps, **kw):
        super().__init__(parent, relief="raised", bd=2, **kw)

        self.app = app

        self.ally_team = Listbox(self, height="5", width=5)
        self.ally_team.insert(0, *allies)
        self.ally_team.pack(side="left", fill="both", pady=2, padx=(2, 0), expand=True)

        Label(self, text="vs.", bd=5).pack(side="left", fill="y", pady=2)

        self.enemy_team = Listbox(self, height="5", width=5)
        self.enemy_team.insert(0, *enemies)
        self.enemy_team.pack(side="left", fill="both", pady=2, expand=True)

        scrollbar = Scrollbar(self)
        self.timestamps = Listbox(self, yscrollcommand=scrollbar.set, height=5, width=5)
        self.timestamps.insert(0, *timestamps)
        self.timestamps.pack(side="left")
        scrollbar.pack(side="left", fill="y", pady=2, padx=(0, 2))
        scrollbar.config(command=self.timestamps.yview)

        self.pack(side="top", fill="x", padx=2, pady=(2, 0))
