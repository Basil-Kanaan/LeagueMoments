from datetime import datetime
from threading import Thread
from typing import TextIO
from time import sleep
import globals
import os


class GameChecker(Thread):

    def __init__(self, _app):
        super().__init__()
        self.app = _app

    def run(self):
        sep = os.sep

        while not globals.app_closed:

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
            if "GAMESTATE_PREGAME to GAMESTATE_SPAWN" in line:
                self.app.times = [datetime.now()]
                globals.in_game = True

        for line in self._tail(game_file):
            if "GAMESTATE_PRE_EXIT to GAMESTATE_EXIT" in line:
                globals.in_game = False
                self.app.s
                break

        game_file.close()

    def _tail(self, file):
        file.seek(0, 2)
        while True:
            line = file.readline()
            if line.strip():
                yield line
            sleep(0.1)
