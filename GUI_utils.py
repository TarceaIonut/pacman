import GameUtils

DEFAULT_GAME_HEIGHT:int =  1000
DEFAULT_FPS:int = 60

MODE_MANUAL:int = 0
MODE_AUTO:int = 1

ALGORITHM_GHOST_BFS:int = 0
ALGORITHM_GHOST_DFS:int = 1
ALGORITHM_GHOST_ASTAR:int = 2

ALGORITHM_PACMAN_REFLEX_AGENT:int = 0
ALGORITHM_PACMAN_MIN_MAX:int = 1
ALGORITHM_PACMAN_AB_PRUNING:int = 2

class GUIUtils:
    def __init__(self):
        self.direction = GameUtils.DIRECTION_LEFT
        self.mode = MODE_MANUAL
        self.alg_pacman = ALGORITHM_PACMAN_REFLEX_AGENT
        self.alg_ghost = ALGORITHM_GHOST_BFS