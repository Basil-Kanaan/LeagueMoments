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

                if latest_modified == datetime.now().minute or globals.debug_mode:
                    self._loading_screen_start(logs_path, globals.debug_mode)

            sleep(1)

    def _loading_screen_start(self, logs_path, debug=False):

        def tail(file):
            file.seek(0, 2)
            while True:
                line = file.readline()
                if line.strip():
                    yield line
                sleep(0.1)

        game_log_path = logs_path + os.sep + os.listdir(logs_path)[-1]

        if debug:
            print("Game not started")
            sleep(5)
            print("Starting Timer")
            self.app.times = [datetime.now()]
            globals.in_game = True

            sleep(10)
            print("Game ended")
            globals.in_game = False
            self.app.shelve_times()
        else:
            game_file: TextIO
            for filename in os.listdir(game_log_path):
                if "r3dlog.txt" in filename:
                    game_path = game_log_path + os.sep + filename
                    game_file = open(game_path)

            TeamOrder, TeamChaos = [], []
            TeamOrderIsAllies = False
            for line in tail(game_file):
                if "TeamOrder" in line:
                    line = line.split("Champion(")[1].split(")")[0]
                    TeamOrder.append(line)
                    if "**LOCAL**" in line:
                        TeamOrderIsAllies = True

                elif "TeamChaos" in line:
                    line = line.split("Champion(")[1].split(")")[0]
                    TeamChaos.append(line)

                elif "Connection Established" in line:
                    break

            if len(TeamOrder) == 8:
                return

            if TeamOrderIsAllies:
                self.app.allies, self.app.enemies = TeamOrder, TeamChaos
            else:
                self.app.allies, self.app.enemies = TeamChaos, TeamOrder

            for line in tail(game_file):
                if "GAMESTATE_PREGAME to GAMESTATE_SPAWN" in line:
                    self.app.times = [datetime.now()]
                    globals.in_game = True
                    break

            for line in tail(game_file):
                if "GAMESTATE_PRE_EXIT to GAMESTATE_EXIT" in line:
                    globals.in_game = False
                    self.app.shelve_times()
                    break

            game_file.close()
