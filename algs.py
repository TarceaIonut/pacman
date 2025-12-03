import heapq
from collections import deque

import GUI_utils
import GameUtils
import GameDisplay
import Maze


def move(actor_in: int, pacman_alg_id: int, ghost_alg_id: int, gameDisplay: GameDisplay) -> tuple[list[tuple[int, int]], tuple[int, int]]:
    if actor_in == GameUtils.ACTOR_PACMAN:
        return move_pacman(pacman_alg_id, gameDisplay)
    else:
        return move_ghost(actor_in, ghost_alg_id, gameDisplay)

def move_pacman(ghost_alg_id: int, gameDisplay:GameDisplay) -> tuple[list[tuple[int, int]], tuple[int, int]]:
    print("move_pac to d = ", (0,0), [])
    return [],(0,0)

def move_ghost(ghost_in: int, ghost_alg_id: int, gameDisplay: GameDisplay) -> tuple[list[tuple[int, int]], tuple[int, int]]:
    p,d = get_ghost_path_and_next_move(gameDisplay, ghost_in, ghost_alg_id)
    print("move_ghost to d = , id = ", d, p, ghost_in)
    return p, d


CORNER_ACTOR_RED = (0, 26)
CORNER_ACTOR_PINK = (0, 1)
CORNER_ACTOR_BLUE = (30, 26)
CORNER_ACTOR_ORANGE = (30, 1)


def clamp_position(game: GameDisplay, pos: tuple[int, int]) -> tuple[int, int]:
    # pos is within board bounds and not wall
    board = game.get_board_copy()
    y, x = pos

    y = max(0, min(y, len(board) - 1))
    x = max(0, min(x, len(board[0]) - 1))

    if board[y][x] == GameUtils.CELL_WALL:
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                new_y, new_x = y + dy, x + dx
                if (0 <= new_y < len(board) and
                        0 <= new_x < len(board[0]) and
                        board[new_y][new_x] != GameUtils.CELL_WALL):
                    return new_y, new_x
    return y, x

def get_target_for_ghost(game: GameDisplay, id_actor: int) -> tuple[int, int]:
    pacman_pos = reverse_tuple(game.pacman.get_current_cell_poz())

    if id_actor == GameUtils.ACTOR_RED:  #Blinky
        return pacman_pos

    elif id_actor == GameUtils.ACTOR_PINK:  #Pinky
        pacman_direction = game.pacman.direction
        dy, dx = pacman_direction

        target_y = pacman_pos[0] + (4 * dy)
        target_x = pacman_pos[1] + (4 * dx)

        return clamp_position(game, (target_y, target_x))

    elif id_actor == GameUtils.ACTOR_BLUE:  # Inky
        blinky_pos = reverse_tuple(game.red.get_current_cell_poz())

        pacman_direction = game.pacman.direction
        dy, dx = pacman_direction

            # Point 2 squares ahead of Pac-Man
        intermediate_y = pacman_pos[0] + (2 * dy)
        intermediate_x = pacman_pos[1] + (2 * dx)

            # Vector from Blinky to intermediate point, doubled
        vector_y = intermediate_y - blinky_pos[0]
        vector_x = intermediate_x - blinky_pos[1]

        target_y = blinky_pos[0] + (2 * vector_y)
        target_x = blinky_pos[1] + (2 * vector_x)

        return clamp_position(game, (target_y, target_x))

    elif id_actor == GameUtils.ACTOR_ORANGE:  # Clyde
        clyde_pos = reverse_tuple(game.orange.get_current_cell_poz())

            #Euclidean dist
        distance_y = clyde_pos[0] - pacman_pos[0]
        distance_x = clyde_pos[1] - pacman_pos[1]
        distance = (distance_y ** 2 + distance_x ** 2) ** 0.5

        if distance > 8:
            return pacman_pos
        else:
            return CORNER_ACTOR_ORANGE

    return pacman_pos

def BFS(game: GameDisplay, id_actor: int) -> list[tuple[int, int]]:

    board = game.get_board_copy()
    start = game.get_poz_actor_type(id_actor)
    target = get_target_for_ghost(game, id_actor) #poz final

    queue = deque([start])
    visited = {start: True}
    parent = {start: None}

    while queue:
        y, x = queue.popleft()

        if (y, x) == target:
            path = []
            curr = (y, x)
            while curr is not None:
                path.append(curr)
                curr = parent[curr]
            path.reverse()
            return path

        for dy, dx in game.get_possible_directions_for_actor_type(id_actor): # aici ar fi folosita change dir sa ia locatii noi
            poz_nou_y, poz_nou_x = y + dy, x + dx

            if 0 <= poz_nou_y < len(board) and 0 <= poz_nou_x < len(board[0]):
                if board[poz_nou_y][poz_nou_x] == GameUtils.CELL_WALL:
                    continue

                neigh = (poz_nou_y, poz_nou_x)
                if neigh not in visited:
                    visited[neigh] = True
                    parent[neigh] = (y, x)
                    queue.append(neigh)
    return []

def reverse_tuple(t:tuple[int, int]) -> tuple[int, int]:
    return t[1], t[0]

def DFS(game: GameDisplay, id_actor: int) -> list[tuple[int, int]]:

    board = game.get_board_copy()
    start =  reverse_tuple(game.get_poz_actor_type(id_actor))
    target = get_target_for_ghost(game, id_actor)


    stack = [start]
    visited = {start: True}
    parent = {start: None}

    while stack:
        x, y = stack.pop()

        if (x, y) == target:
            path = []
            curr = (x, y)
            while curr is not None:
                path.append(curr)
                curr = parent[curr]
            path.reverse()
            return path

        is_dead = False

        match id_actor:
            case GameUtils.ACTOR_ORANGE:
                is_dead = game.orange.eaten_state
            case GameUtils.ACTOR_RED:
                is_dead = game.red.eaten_state
            case GameUtils.ACTOR_BLUE:
                is_dead = game.blue.eaten_state
            case GameUtils.ACTOR_PINK:
                is_dead = game.pink.eaten_state
            case _:
                raise NotImplementedError

        for dx, dy in get_possible_poz_for_ghost(board, (x, y), is_dead):
            if (dx, dy) not in visited:
                visited[(dx, dy)] = True
                parent[(dx, dy)] = (x, y)
                stack.append((dx, dy))


    return []

def get_possible_poz_for_ghost(board: list[list[int]], actor_poz: tuple[int, int], is_dead:bool) -> list[tuple[int, int]]:
    poz_up = actor_poz[0] + GameUtils.DIRECTION_UP[0], actor_poz[1] + GameUtils.DIRECTION_UP[1]
    poz_down = actor_poz[0] + GameUtils.DIRECTION_DOWN[0], actor_poz[1] + GameUtils.DIRECTION_DOWN[1]
    poz_left = actor_poz[0] + GameUtils.DIRECTION_LEFT[0], actor_poz[1] + GameUtils.DIRECTION_LEFT[1]
    poz_right = actor_poz[0] + GameUtils.DIRECTION_RIGHT[0], actor_poz[1] + GameUtils.DIRECTION_RIGHT[1]

    list_dir = []

    if check_poz_ghost(board, poz_up, is_dead ,actor_poz):
        list_dir.append(poz_up)
    if check_poz_ghost(board, poz_left, is_dead ,actor_poz):
        list_dir.append(poz_left)
    if check_poz_ghost(board, poz_down, is_dead ,actor_poz):
        list_dir.append(poz_down)
    if check_poz_ghost(board, poz_right, is_dead ,actor_poz):
        list_dir.append(poz_right)

    return list_dir

def check_poz_ghost(board: list[list[int]], actor_poz: tuple[int, int], is_dead:bool, actor_prev_poz: tuple[int,int]) -> bool:
    if is_dead:
        return is_in_bounds(board, actor_poz) and (not is_wall(board, actor_poz) or inside_rec(actor_poz))
    else:
        return is_in_bounds(board, actor_poz) and (not is_wall(board, actor_poz) or (inside_rec(actor_poz) and inside_rec(actor_prev_poz)))

def inside_rec(actor_poz: tuple[int, int]) -> bool:
    a1 = (Maze.DEFAULT_GHOST_RECHARGE_REC[0][0] <= actor_poz[0] <= Maze.DEFAULT_GHOST_RECHARGE_REC[0][1])
    a2 = (Maze.DEFAULT_GHOST_RECHARGE_REC[1][0] <= actor_poz[1] <= Maze.DEFAULT_GHOST_RECHARGE_REC[1][1])
    return a1 and a2

def is_wall(board: list[list[int]], actor_poz: tuple[int, int]) -> bool:
    return board[actor_poz[0]][actor_poz[1]] == GameUtils.CELL_WALL

def is_in_bounds(board: list[list[int]], actor_poz: tuple[int, int]) -> bool:
    return 0 <= actor_poz[0] < len(board) and 0 <= actor_poz[1] < len(board[0])

def heuristic(pos: tuple[int, int], target: tuple[int, int]) -> float:
        #Manhattan
    return abs(pos[0] - target[0]) + abs(pos[1] - target[1])

def A_star(game: GameDisplay, id_actor: int) -> list[tuple[int, int]]:

    board = game.get_board_copy()
    start = game.get_poz_actor_type(id_actor)
    target = get_target_for_ghost(game, id_actor)

        # Priority queue: (f_score, counter, position)
    counter = 0
    heap = [(0, counter, start)]
    counter += 1

    visited = set()
    parent = {start: None}
    g_score = {start: 0}
    f_score = {start: heuristic(start, target)}  # g + h

    while heap:
        current_f, _, current = heapq.heappop(heap)

        y, x = current

        if current in visited:
            continue

        visited.add(current)

        if current == target:
            path = []
            curr = current
            while curr is not None:
                path.append(curr)
                curr = parent[curr]
            path.reverse()
            return path

        for dy, dx in game.get_possible_directions_for_actor_type(id_actor):
            poz_nou_y, poz_nou_x = y + dy, x + dx

            if 0 <= poz_nou_y < len(board) and 0 <= poz_nou_x < len(board[0]):
                if board[poz_nou_y][poz_nou_x] == GameUtils.CELL_WALL:
                    continue

                neigh = (poz_nou_y, poz_nou_x)

                if neigh in visited:
                    continue

                tentative_g = g_score[current] + 1

                if neigh not in g_score or tentative_g < g_score[neigh]:
                    parent[neigh] = current
                    g_score[neigh] = tentative_g
                    f_score[neigh] = tentative_g + heuristic(neigh, target)
                    heapq.heappush(heap, (f_score[neigh], counter, neigh))
                    counter += 1

    return []

def get_ghost_path_and_next_move(game: GameDisplay, ghost_id: int, algorithm: int) -> tuple[list[tuple[int, int]], tuple[int, int]]:
    if algorithm == GUI_utils.ALGORITHM_GHOST_DFS:
        path = DFS(game, ghost_id)
    elif algorithm == GUI_utils.ALGORITHM_GHOST_ASTAR:
        path = A_star(game, ghost_id)
    elif algorithm == GUI_utils.ALGORITHM_GHOST_BFS:
        path = BFS(game, ghost_id)
    else:
        raise NotImplementedError

    if len(path) < 2:
        return path, (0, 0)

    current_pos = path[0]
    next_pos = path[1]

    direction = (next_pos[0] - current_pos[0], next_pos[1] - current_pos[1])

    return path, direction