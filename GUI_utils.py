import GameUtils

DEFAULT_GAME_HEIGHT:int =  1000
DEFAULT_FPS:int = 200

MODE_MANUAL:int = 0
MODE_AUTO:int = 1

ALGORITHM_GHOST_BFS:int = 0
ALGORITHM_GHOST_DFS:int = 1
ALGORITHM_GHOST_ASTAR:int = 2

ALGORITHM_PACMAN_REFLEX_AGENT:int = 0
ALGORITHM_PACMAN_MIN_MAX:int = 1
ALGORITHM_PACMAN_AB_PRUNING:int = 2

COLOR_DEFAULT_BUTTON:tuple[int,int,int] = (128,214,238)
COLOR_DEFAULT_TEXT:tuple[int,int,int] = (0,68,119)
COLOR_DEFAULT_TEXT2:tuple[int,int,int] = (0,68,119)

DEFAULT_SIZE:int = 80

class GUIUtils:
    def __init__(self):
        self.direction_pacman = GameUtils.DIRECTION_UP

        self.direction_red = GameUtils.DIRECTION_UP
        self.direction_blue = GameUtils.DIRECTION_UP
        self.direction_orange = GameUtils.DIRECTION_UP
        self.direction_pink = GameUtils.DIRECTION_UP

        self.mode = MODE_MANUAL
        self.alg_pacman = ALGORITHM_PACMAN_REFLEX_AGENT
        self.alg_ghost = ALGORITHM_GHOST_BFS
        self.play = False

    def mode_to_string(self) -> str:
        if self.mode == MODE_MANUAL:
            return "Manual"
        if self.mode == MODE_AUTO:
            return "Auto"
        raise NotImplementedError

    def alg_pacman_to_string(self) -> str:
        if self.alg_pacman == ALGORITHM_PACMAN_AB_PRUNING:
            return "AB Pruning"
        if self.alg_pacman == ALGORITHM_PACMAN_MIN_MAX:
            return "Minmax"
        if self.alg_pacman == ALGORITHM_PACMAN_REFLEX_AGENT:
            return "Reflex Agent"
        raise NotImplementedError

    def alg_ghost_to_string(self) -> str:
        if self.alg_ghost == ALGORITHM_GHOST_BFS:
            return "BFS"
        if self.alg_ghost == ALGORITHM_GHOST_DFS:
            return "DFS"
        if self.alg_ghost == ALGORITHM_GHOST_ASTAR:
            return "ASTAR"
        raise NotImplementedError