import GameUtils

class GameState:
    def __init__(self):
        self.game_score: int = 0
        self.powered_up_mode: bool = False
        self.time_until_powered_up_stops: int = 0

        self.lives = GameUtils.PACMAN_LIVES
        self.game_over = False
        self.pacman_eaten = False
        self.pacman_eaten_time: int = 0

        self.game_temp_pause:bool = False
        self.wait_until_new_level = False

        self.new_level_time: int = 0

    def reset_for_new_level(self):
        self.powered_up_mode = False