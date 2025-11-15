import Maze
import pygame

CELL_FREE:int = 0
CELL_WALL:int = 1
CELL_SMALL_POINT:int = 2
CELL_BIG_POINT:int = 3
ACTOR_PACMAN:int = 0
ACTOR_RED:int = 1
ACTOR_BLUE:int = 2
ACTOR_ORANGE:int = 3
ACTOR_PINK:int = 4

DIRECTION_UP:tuple[int,int] = (-1, 0)
DIRECTION_DOWN:tuple[int,int] = (1, 0)
DIRECTION_LEFT:tuple[int,int] = (0, -1)
DIRECTION_RIGHT:tuple[int,int] = (0, 1)

def direction_to_number(direction:tuple[int,int]) -> int:
    if DIRECTION_UP == direction:
        return 0
    if DIRECTION_LEFT == direction:
        return 1
    if DIRECTION_DOWN == direction:
        return 2
    if DIRECTION_RIGHT == direction:
        return 3
    raise NotImplementedError

def image_black_trasparent(path: str, size: float) -> pygame.Surface:
    image_full = pygame.transform.scale(pygame.image.load(path),(size, size)).convert_alpha()
    image_full.set_colorkey((0, 0, 0))
    return image_full

class Actor:
    def __init__(self, type:int, row_col:tuple[int,int], cell_size:int):
        self.type = type
        self.x = row_col[1] * cell_size
        self.y = row_col[0] * cell_size
        self.cell_size = cell_size
        self.image_size = cell_size * 1.5
        self.direction = DIRECTION_UP
        self.animation_cycle:int = 0

        if type == ACTOR_PACMAN:
            image_full = image_black_trasparent("pacman_full.png", self.image_size)
            self.image = [
                image_full,
                image_black_trasparent("pacman_half_up.png", self.image_size),
                image_black_trasparent("pacman_empty_up.png", self.image_size),
                image_full,
                image_black_trasparent("pacman_half_left.png", self.image_size),
                image_black_trasparent("pacman_empty_left.png", self.image_size),
                image_full,
                image_black_trasparent("pacman_half_down.png", self.image_size),
                image_black_trasparent("pacman_empty_down.png", self.image_size),
                image_full,
                image_black_trasparent("pacman_half_right.png", self.image_size),
                image_black_trasparent("pacman_empty_right.png", self.image_size),
            ]
            self.nr_animations: int = 3
        elif type == ACTOR_RED:
            self.nr_animations: int = 2
            self.image = []
        elif type == ACTOR_BLUE:
            self.nr_animations: int = 2
            self.image = []
        elif type == ACTOR_ORANGE:
            self.nr_animations: int = 2
            self.image = []
        elif type == ACTOR_PINK:
            self.nr_animations: int = 2
            self.image = []
        else:
            raise NotImplementedError

    def draw(self, surface):
        image_nr:int = direction_to_number(self.direction) + (self.animation_cycle // 33) % self.nr_animations
        offset:float = (self.image_size - self.cell_size)
        #print(image_nr)
        if len(self.image) <= image_nr:
            print("not possible")
            return
        surface.blit(self.image[image_nr], (self.x + offset, self.y))
        self.animation_cycle += 1


    def _match_pacman_to_file(self) -> str:
        animation = self.animation_cycle % 3
        global DIRECTION_UP, DIRECTION_DOWN, DIRECTION_LEFT, DIRECTION_RIGHT
        match self.direction, animation:
            case (DIRECTION_UP, 0):
                return "pacman_full_up"
            case (DIRECTION_UP, 1):
                return "pacman_half_up"
            case (DIRECTION_UP, 2):
                return "pacman_empty_up"

            case (DIRECTION_DOWN, 0):
                return "pacman_full_down"
            case (DIRECTION_DOWN, 1):
                return "pacman_half_down"
            case (DIRECTION_DOWN, 2):
                return "pacman_empty_down"

            case (DIRECTION_LEFT, 0):
                return "pacman_full_left"
            case (DIRECTION_LEFT, 1):
                return "pacman_half_left"
            case (DIRECTION_LEFT, 2):
                return "pacman_empty_left"

            case (DIRECTION_RIGHT, 0):
                return "pacman_full_right"
            case (DIRECTION_RIGHT, 1):
                return "pacman_half_right"
            case (DIRECTION_RIGHT, 2):
                return "pacman_empty_right"
        raise NotImplementedError
    def _match_red_to_file(self) -> str:
        return "pacman_full.png"
    def _match_blue_to_file(self) -> str:
        return "pacman_full.png"
    def _match_orange_to_file(self) -> str:
        return "pacman_full.png"
    def _match_pink_to_file(self) -> str:
        return "pacman_full.png"

    def match_type_to_file(self) -> str:
        global ACTOR_PACMAN, ACTOR_RED, ACTOR_BLUE, ACTOR_ORANGE, ACTOR_PINK
        if self.type == ACTOR_PACMAN:
            return self._match_pacman_to_file()
        elif self.type == ACTOR_RED:
            return self._match_red_to_file()
        elif self.type == ACTOR_BLUE:
            self._match_blue_to_file()
        elif self.type == ACTOR_ORANGE:
            self._match_orange_to_file()
        elif self.type == ACTOR_PINK:
            self._match_pink_to_file()
        else:
            raise NotImplementedError



def create_board(board: list[list[int]]) -> list[list[int]]:
    rows = len(board)
    cols = len(board[0])
    new_board:list[list[int]] = board.copy()
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == Maze.DEFAULT_FREE:
                new_board[row][col] = CELL_FREE
            elif board[row][col] == Maze.DEFAULT_WALL:
                new_board[row][col] = CELL_SMALL_POINT
            elif board[row][col] == Maze.DEFAULT_NO_POINT:
                new_board[row][col] = CELL_FREE
            else:
                print("error, unknown value ", board[row][col], " at row, col = " , row, ", ", cols)
                raise NotImplementedError
    for (x,y) in Maze.DEFAULT_BIG_POINT:
        new_board[x][y] = CELL_BIG_POINT

    return new_board


class GameDisplay:
    def __init__(self, width, height, maze:list[list[int]]):
        self.width = width
        self.height = height
        self.board:list[list[int]] = create_board(maze)
        self.cell_size = min(width // len(self.board[0]), height // len(self.board))
        self.screen = pygame.display.set_mode((width, height))

        self.pacman = Actor(ACTOR_PACMAN, Maze.DEFAULT_PACMAN ,self.cell_size)
        self.red = Actor(ACTOR_RED, Maze.DEFAULT_RED ,self.cell_size)
        self.blue = Actor(ACTOR_BLUE, Maze.DEFAULT_BLUE ,self.cell_size)
        self.pink = Actor(ACTOR_PINK, Maze.DEFAULT_PINK ,self.cell_size)
        self.orange = Actor(ACTOR_ORANGE, Maze.DEFAULT_ORANGE ,self.cell_size)

        self.background = pygame.transform.scale(pygame.image.load("Empty_board_default.png"), (width, height))


        pygame.init()
        pygame.display.set_caption("Pacman")

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.pacman.draw(self.screen)
        #self.red.draw(self.screen)
        #self.blue.draw(self.screen)
        #self.pink.draw(self.screen)
        #self.orange.draw(self.screen)
        pygame.display.update()

    def draw_board(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                cell = self.board[row][col]
                if cell == CELL_FREE:
                    color = (0, 0, 255)
                elif cell == CELL_WALL:
                    color = (0, 0, 0)
                elif cell == CELL_SMALL_POINT:
                    color = (255, 255, 255)
                elif cell == CELL_BIG_POINT:
                    color = (128, 128, 128)
                else:
                    color = (255, 0, 0)
                pygame.draw.rect(
                    self.screen,
                    color,
                    (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                )

        pygame.display.flip()

game = GameDisplay(1000, 1000, Maze.DEFAULT_MAZE)
while True:
    game.draw()

