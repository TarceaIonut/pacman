
CYCLES_PER_CELL_PACMAN:int = 10 #amound of draw() calls for pacman to go from a cell to an other (1 / speed)
CYCLES_PER_CELL_GHOST:int = 12 #amound of draw() calls for gosts to go from a cell to an other (1 / speed)

SMALL_POINT_TO_CELL:float = 6
BIG_POINT_TO_CELL:float = 1
CHERRY_TO_CELL:float = 0.66

CHERRY_ID:int = 10

POWERED_UP_TIME:int = 500
PACMAN_DEAD_TIME:int = 100
NEW_LEVEL_TIME:int = 100

PACMAN_LIVES:int = 3



#smaller <=> faster


#FOR EXTERNAL USE
DIRECTION_UP:tuple[int,int] = (0, -1)
DIRECTION_DOWN:tuple[int,int] = (0, 1)
DIRECTION_LEFT:tuple[int,int] = (-1, 0)
DIRECTION_RIGHT:tuple[int,int] = (1, 0)

CELL_FREE:int = 0
CELL_WALL:int = 1
CELL_SMALL_POINT:int = 2
CELL_BIG_POINT:int = 3

ACTOR_PACMAN:int = 0
ACTOR_RED:int = 1
ACTOR_BLUE:int = 2
ACTOR_ORANGE:int = 3
ACTOR_PINK:int = 4

POINTS_SMALL_POINT:int = 10
POINTS_BIG_POINT:int = 50
POINTS_GHOST_EAT:int = 200
POINTS_LOOSING:int = -500