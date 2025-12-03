import pygame

import GameUtils
import Maze


def scale_direction_(direction: tuple[int, int], scalar: int) -> tuple[int, int]:
    return direction[0] * scalar, direction[1] * scalar
def positon_add_direction_(poz: tuple[int, int], direction: tuple[int, int]) -> tuple[int, int]:
    return poz[0] + direction[0], poz[1] + direction[1]



def direction_to_number(direction:tuple[int,int]) -> int:
    if GameUtils.DIRECTION_UP == direction:
        return 0
    if GameUtils.DIRECTION_LEFT == direction:
        return 1
    if GameUtils.DIRECTION_DOWN == direction:
        return 2
    if GameUtils.DIRECTION_RIGHT == direction:
        return 3
    print(direction)
    raise NotImplementedError

def image_black_transparent(path: str, size: float) -> pygame.Surface:
    image_full = pygame.transform.scale(pygame.image.load(path),(size, size)).convert_alpha()
    image_full.set_colorkey((0, 0, 0))
    return image_full


def create_board(board: list[list[int]]) -> list[list[int]]:
    rows = len(board)
    cols = len(board[0])
    new_board:list[list[int]] = []
    for row in board:
        new_board.append([x for x in row])
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == Maze.DEFAULT_POINT:
                new_board[row][col] = GameUtils.CELL_SMALL_POINT
            elif board[row][col] == Maze.DEFAULT_WALL:
                new_board[row][col] = GameUtils.CELL_WALL
            elif board[row][col] == Maze.DEFAULT_NO_POINT:
                new_board[row][col] = GameUtils.CELL_FREE
            else:
                print("error, unknown value ", board[row][col], " at row, col = " , row, ", ", cols)
                raise NotImplementedError
    for (x,y) in Maze.DEFAULT_BIG_POINT:
        new_board[x][y] = GameUtils.CELL_BIG_POINT

    return new_board
