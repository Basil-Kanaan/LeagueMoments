from tkinter import Frame, Label, Button
from threading import Thread
import keyboard


class HotkeyCard(Frame):

    action: Label
    hotkey_label: Label
    hotkey_string: str

    def __init__(self, app, parent, action, hotkey, **kw):
        super().__init__(parent, **kw)

        self.app = app

        self.action = Label(self, text=action+":", width=10, anchor="e", bg="gray80")
        self.action.grid(row=0, column=0, sticky="nsew")

        self.hotkey_label = Label(self, text=hotkey, anchor="w", bg="white")
        self.hotkey_label.grid(row=0, column=1, sticky="nsew")
        self.hotkey_string = hotkey

        Button(self, text="Record", width=9, bg="lawngreen", command=self.set_hotkey)\
            .grid(row=0, column=2, sticky="nsew")

        Button(self, text="Delete", width=9, bg="#e3aaaa", command=self.delete_hotkey)\
            .grid(row=0, column=3, sticky="nsew")

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.pack(side="top", fill="x", padx=10, pady=(10, 0))

    def delete_hotkey(self):
        self.hotkey_label.config(text="")

    def set_hotkey(self):
        self.hotkey_label.config(text="Press Combination...")
        Thread(target=self.record_hotkey).start()

    def record_hotkey(self):
        rec = keyboard.read_hotkey(suppress=False).upper()
        keyboard.remove_hotkey(self.hotkey_string)
        keyboard.add_hotkey(rec, self.app.save_time)
        self.hotkey_label.config(text=rec)
        self.hotkey_string = rec
