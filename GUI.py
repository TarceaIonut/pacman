import time
import GUI_utils
import GameUtils
from GameDisplay import GameDisplay



class GUI:
    def __init__(self):
        self.game = GameDisplay(GUI_utils.DEFAULT_GAME_HEIGHT)
        self.main_loop()

    def main_loop(self):
        while True:
            self.game.move_a_type(GameUtils.ACTOR_PACMAN, GameUtils.DIRECTION_LEFT)
            self.game.draw()
            time.sleep(0.02)

    def get_direction(self):
        

GUI = GUI()
