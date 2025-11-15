

import Maze
import pygame
import GameUtils


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
    raise NotImplementedError

def image_black_transparent(path: str, size: float) -> pygame.Surface:
    image_full = pygame.transform.scale(pygame.image.load(path),(size, size)).convert_alpha()
    image_full.set_colorkey((0, 0, 0))
    return image_full

class Actor:
    def __init__(self, type_:int, row_col:tuple[int,int], cell_size:int):
        self.type = type_
        self.poz:tuple[int,int] = (int((row_col[1] + 0.5) * cell_size), int((row_col[0] + 0.5) * cell_size))
        self.cell_size = cell_size
        self.image_size = cell_size * 1.5
        self.direction = GameUtils.DIRECTION_UP
        self.animation_cycle:int = 0
        if type_ == GameUtils.ACTOR_PACMAN:
            self.number_of_pixels_per_draw:int = self.cell_size // GameUtils.CYCLES_PER_CELL_PACMAN
        else:
            self.number_of_pixels_per_draw:int = self.cell_size // GameUtils.CYCLES_PER_CELL_GHOST

        if type_ == GameUtils.ACTOR_PACMAN:
            image_full = image_black_transparent("pacman_full.png", self.image_size)
            self.image = [
                image_full,
                image_black_transparent("pacman_half_up.png", self.image_size),
                image_black_transparent("pacman_empty_up.png", self.image_size),
                image_full,
                image_black_transparent("pacman_half_left.png", self.image_size),
                image_black_transparent("pacman_empty_left.png", self.image_size),
                image_full,
                image_black_transparent("pacman_half_down.png", self.image_size),
                image_black_transparent("pacman_empty_down.png", self.image_size),
                image_full,
                image_black_transparent("pacman_half_right.png", self.image_size),
                image_black_transparent("pacman_empty_right.png", self.image_size),
            ]
            self.nr_animations: int = 3
        elif type_ == GameUtils.ACTOR_RED:
            self.nr_animations: int = 1
            self.image = []
        elif type_ == GameUtils.ACTOR_BLUE:
            self.nr_animations: int = 1
            self.image = []
        elif type_ == GameUtils.ACTOR_ORANGE:
            self.nr_animations: int = 1
            self.image = []
        elif type_ == GameUtils.ACTOR_PINK:
            self.nr_animations: int = 1
            self.image = []
        else:
            raise NotImplementedError

    def draw(self, surface):
        image_nr:int = direction_to_number(self.direction) + (self.animation_cycle // 50) % self.nr_animations
        offset:float = (self.image_size / 2)
        #print(image_nr)
        if len(self.image) <= image_nr:
            print("not possible")
            return
        draw_poz = self.normalize_coordinates_for_display()
        surface.blit(self.image[image_nr], (draw_poz[0] - offset, draw_poz[1] - offset))

        self.animation_cycle += 1

    def get_cell_poz(self, poz: tuple[int,int]) -> tuple[int,int]:
        return poz[0] // self.cell_size, poz[1] // self.cell_size
    def get_current_cell_poz(self):
        return self.get_cell_poz(self.poz)

    def normalize_coordinates_for_display(self) -> tuple[int,int]:
        if self.direction == GameUtils.DIRECTION_UP or self.direction == GameUtils.DIRECTION_DOWN:
            return int(((self.poz[0] // self.cell_size) + 0.5) * self.cell_size), self.poz[1]
        return int(((self.poz[1] // self.cell_size) + 0.5) * self.cell_size), self.poz[0]

    def get_new_poz(self, direction: tuple[int,int]):
        return positon_add_direction_(self.poz, scale_direction_(direction, self.number_of_pixels_per_draw))


def create_board(board: list[list[int]]) -> list[list[int]]:
    rows = len(board)
    cols = len(board[0])
    new_board:list[list[int]] = board.copy()
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


def get_actor_poz(a: Actor) -> tuple[int,int]:
    return a.get_cell_poz(a.poz)


class GameDisplay:
    def __init__(self, height, maze:list[list[int]]):
        self.board:list[list[int]] = create_board(maze)
        self.cell_size = height // len(self.board)
        self.width = self.cell_size * len(self.board[0])
        self.height = self.cell_size * len(self.board)

        self.screen = pygame.display.set_mode((self.width, self.height))

        self.pacman = Actor(GameUtils.ACTOR_PACMAN, Maze.DEFAULT_PACMAN ,self.cell_size)
        self.red = Actor(GameUtils.ACTOR_RED, Maze.DEFAULT_RED ,self.cell_size)
        self.blue = Actor(GameUtils.ACTOR_BLUE, Maze.DEFAULT_BLUE ,self.cell_size)
        self.pink = Actor(GameUtils.ACTOR_PINK, Maze.DEFAULT_PINK ,self.cell_size)
        self.orange = Actor(GameUtils.ACTOR_ORANGE, Maze.DEFAULT_ORANGE ,self.cell_size)

        self.background = pygame.transform.scale(pygame.image.load("Empty_board_default.png"), (self.width, self.height))

        self.small_point_size:int = self.cell_size / GameUtils.SMALL_POINT_TO_CELL
        self.big_point_size:int = self.cell_size / GameUtils.BIG_POINT_TO_CELL
        self.cherry_size:int = self.cell_size / GameUtils.CHERRY_TO_CELL

        self.small_point_image = pygame.transform.scale(pygame.image.load("small_point.png"), (self.small_point_size, self.small_point_size))
        self.big_point_image = pygame.transform.scale(pygame.image.load("big_point.png"), (self.big_point_size, self.big_point_size))
        self.cherry_image = pygame.transform.scale(pygame.image.load("cherry.png"), (self.cherry_size, self.cherry_size))

        self.game_score:int = 0
        self.powered_up_mode:bool = False
        self.time_until_powered_up_stops:int = 0

        pygame.init()
        pygame.display.set_caption("Pacman")

    def see_what_happens_in_a_move(self):
        cell_poz = self.pacman.get_current_cell_poz()
        self.gameplay_points(cell_poz)
        if self.time_until_powered_up_stops == 0:
            self.powered_up_mode = False
        


    def gameplay_points(self, cell_poz:tuple[int,int]):
        current_cell = self.board[cell_poz[1]][cell_poz[0]]
        if current_cell == GameUtils.CELL_SMALL_POINT:
            self.game_score += GameUtils.POINTS_SMALL_POINT
        elif current_cell == GameUtils.CELL_BIG_POINT:
            self.game_score += GameUtils.POINTS_BIG_POINT
            self.powered_up_mode = True
            self.time_until_powered_up_stops += GameUtils.POWERED_UP_TIME



    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.pacman.draw(self.screen)
        #self.red.draw(self.screen)
        #self.blue.draw(self.screen)
        #self.pink.draw(self.screen)
        #self.orange.draw(self.screen)

        self.draw_board()
        pygame.display.update()

    def draw_board(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                draw_poz:tuple[int,int] = positon_add_direction_(scale_direction_((col, row), self.cell_size),
                                                                 (self.cell_size // 2, self.cell_size // 2))
                cell = self.board[row][col]
                if cell == GameUtils.CELL_SMALL_POINT or cell == GameUtils.CELL_BIG_POINT:
                    self.draw_object(draw_poz, cell)

        pygame.display.flip()

    def draw_object(self, screen_poz:tuple[int,int], object_id:int) -> None:
        match object_id:
            case GameUtils.CELL_FREE | GameUtils.CELL_WALL:
                return None
            case GameUtils.CELL_SMALL_POINT:
                offset = self.small_point_size // 2
                self.screen.blit(self.small_point_image, (screen_poz[0] - offset, screen_poz[1] - offset))
            case GameUtils.CELL_BIG_POINT:
                offset = self.big_point_size // 2
                self.screen.blit(self.big_point_image, (screen_poz[0] - offset, screen_poz[1] - offset))
            case GameUtils.CHERRY_ID:
                offset = self.cherry_size // 2
                self.screen.blit(self.cherry_image, (screen_poz[0] - offset, screen_poz[1] - offset))
            case _:
                raise NotImplementedError
        return None


    def get_poz_actor_type(self, a_type: int) -> tuple[int,int]:
        match a_type:
            case GameUtils.ACTOR_PACMAN:
                return get_actor_poz(self.pacman)
            case GameUtils.ACTOR_RED:
                return get_actor_poz(self.red)
            case GameUtils.ACTOR_BLUE:
                return get_actor_poz(self.blue)
            case GameUtils.ACTOR_PINK:
                return get_actor_poz(self.pink)
            case GameUtils.ACTOR_ORANGE:
                return get_actor_poz(self.orange)
            case _:
                raise NotImplementedError

    def get_board_copy(self) -> list[list[int]]:
        my_copy:list[list[int]] = []
        for row in self.board:
            my_copy.append(row.copy())
        return my_copy

    def check_positon_(self, poz: tuple[int, int]) -> bool:
        if self.board[poz[1]][poz[0]] == GameUtils.CELL_WALL:
            return False
        return True


    def get_possible_directions_for_actor_type(self, a_type:int) -> list[tuple[int,int]]:
        match a_type:
            case GameUtils.ACTOR_PACMAN:
                return self.get_possible_directions_of_an_actor_(self.pacman)
            case GameUtils.ACTOR_RED:
                return self.get_possible_directions_of_an_actor_(self.red)
            case GameUtils.ACTOR_BLUE:
                return self.get_possible_directions_of_an_actor_(self.blue)
            case GameUtils.ACTOR_PINK:
                return self.get_possible_directions_of_an_actor_(self.pink)
            case GameUtils.ACTOR_ORANGE:
                return self.get_possible_directions_of_an_actor_(self.orange)
            case _:
                raise NotImplementedError

    def get_possible_directions_of_an_actor_(self, a: Actor) -> list[tuple[int, int]]:
        direction_up_cell:tuple[int,int] = a.get_cell_poz(a.get_new_poz(GameUtils.DIRECTION_UP))
        direction_left_cell: tuple[int, int] = a.get_cell_poz(a.get_new_poz(GameUtils.DIRECTION_LEFT))
        direction_down_cell: tuple[int, int] = a.get_cell_poz(a.get_new_poz(GameUtils.DIRECTION_DOWN))
        direction_right_cell: tuple[int, int] = a.get_cell_poz(a.get_new_poz(GameUtils.DIRECTION_RIGHT))

        list_good_directions:list[tuple[int, int]] = []

        if self.check_positon_(direction_up_cell):
            list_good_directions.append(direction_up_cell)
        if self.check_positon_(direction_left_cell):
            list_good_directions.append(direction_left_cell)
        if self.check_positon_(direction_down_cell):
            list_good_directions.append(direction_down_cell)
        if self.check_positon_(direction_right_cell):
            list_good_directions.append(direction_right_cell)

        return list_good_directions

    def move_a_type(self, a_type: int, direction: tuple[int, int]) -> bool:
        match a_type:
            case GameUtils.ACTOR_PACMAN:
                return self.move_actor_(self.pacman, direction)
            case GameUtils.ACTOR_RED:
                return self.move_actor_(self.red, direction)
            case GameUtils.ACTOR_BLUE:
                return self.move_actor_(self.blue, direction)
            case GameUtils.ACTOR_PINK:
                return self.move_actor_(self.pink, direction)
            case GameUtils.ACTOR_ORANGE:
                return self.move_actor_(self.orange, direction)
            case _:
                raise NotImplementedError

    def move_actor_(self, a:Actor, direction: tuple[int, int]) -> bool:
        new_poz = a.get_new_poz(direction)
        if self.check_positon_(a.get_cell_poz(new_poz)):
            a.poz = new_poz
            a.direction = direction
            return True
        return False

game = GameDisplay(1000, Maze.DEFAULT_MAZE)
while True:
    game.draw()

