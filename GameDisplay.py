import Maze
import pygame
import GameUtils
from Actor import Actor, get_actor_poz
from GameState import GameState
from HelperFunctions import create_board, positon_add_direction_, scale_direction_
import time

class GameDisplay:
    def __init__(self, height):
        self.board:list[list[int]] = create_board(Maze.DEFAULT_MAZE)
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

        self.game_state = GameState()

        pygame.init()
        pygame.display.set_caption("Pacman")

    def see_what_happens_in_a_move(self):

        if self.game_state.game_temp_pause:
            self.gameplay_paused()
        else:
            cell_poz_pacman = self.pacman.get_current_cell_poz()
            cell_poz_pink = self.pink.get_current_cell_poz()
            cell_poz_red = self.red.get_current_cell_poz()
            cell_poz_blue = self.blue.get_current_cell_poz()
            cell_poz_orange = self.orange.get_current_cell_poz()

            self.gameplay_points(cell_poz_pacman)
            if self.game_state.time_until_powered_up_stops == 0:
                self.game_state.powered_up_mode = False

            self.gameplay_phantom(cell_poz_pacman, cell_poz_pink, cell_poz_red, cell_poz_blue, cell_poz_orange)

    def gameplay_paused(self):
        if self.game_state.game_over:
            return
        if self.game_state.pacman_eaten:
            self.game_state.pacman_eaten_time -= 1
            if self.game_state.pacman_eaten_time == 0:
                self.reset_positions_game()
            self.game_state.pacman_eaten = False
        if self.game_state.wait_until_new_level:
            self.game_state.new_level_time -= 1
            if self.game_state.new_level_time == 0:
                self.reset_for_new_level()
            self.game_state.wait_until_new_level = False

    def reset_positions_game(self):
        self.pacman.reset_positions(Maze.DEFAULT_PACMAN)
        self.red.reset_positions(Maze.DEFAULT_RED)
        self.blue.reset_positions(Maze.DEFAULT_BLUE)
        self.orange.reset_positions(Maze.DEFAULT_ORANGE)
        self.pink.reset_positions(Maze.DEFAULT_PINK)

    def reset_for_new_level(self):
        self.board: list[list[int]] = create_board(Maze.DEFAULT_MAZE)
        self.pacman.reset_positions(Maze.DEFAULT_PACMAN)
        self.red.reset_positions(Maze.DEFAULT_RED)
        self.blue.reset_positions(Maze.DEFAULT_BLUE)
        self.orange.reset_positions(Maze.DEFAULT_ORANGE)
        self.pink.reset_positions(Maze.DEFAULT_PINK)
        self.game_state.reset_for_new_level()

    def gameplay_phantom(self, cell_poz_pacman, cell_poz_pink, cell_poz_red, cell_poz_blue, cell_poz_orange):

        if cell_poz_pacman == cell_poz_red and self.red.eaten_state == False:
            self.ghost_pacman_meat(self.red)
        if cell_poz_pacman == cell_poz_blue and self.blue.eaten_state == False:
            self.ghost_pacman_meat(self.blue)
        if cell_poz_pacman == cell_poz_orange and self.orange.eaten_state == False:
            self.ghost_pacman_meat(self.orange)
        if cell_poz_pacman == cell_poz_pink and self.pink.eaten_state == False:
            self.ghost_pacman_meat(self.pink)


    def ghost_pacman_meat(self, a: Actor):
        if not a.eaten_state:
            pass
        else:
            if self.game_state.powered_up_mode:
                a.eaten_state = True
            else:
                self.pacman_eat()

    def pacman_eat(self):
        self.game_state.lives -= 1
        if self.game_state.lives == 0:
            self.game_state.game_over = True

        self.game_state.pacman_eaten_time = GameUtils.PACMAN_DEAD_TIME
        self.game_state.game_temp_pause = True



    def gameplay_points(self, cell_poz_pacman:tuple[int,int]):
        current_cell = self.board[cell_poz_pacman[1]][cell_poz_pacman[0]]
        if current_cell == GameUtils.CELL_SMALL_POINT:
            self.game_state.game_score += GameUtils.POINTS_SMALL_POINT
            self.board[cell_poz_pacman[1]][cell_poz_pacman[0]] = GameUtils.CELL_FREE
        elif current_cell == GameUtils.CELL_BIG_POINT:
            self.game_state.game_score += GameUtils.POINTS_BIG_POINT
            self.game_state.powered_up_mode = True
            self.game_state.time_until_powered_up_stops += GameUtils.POWERED_UP_TIME
            self.board[cell_poz_pacman[1]][cell_poz_pacman[0]] = GameUtils.CELL_FREE



    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.pacman.draw(self.screen)
        #self.red.draw(self.screen)
        #self.blue.draw(self.screen)
        #self.pink.draw(self.screen)
        #self.orange.draw(self.screen)

        self.see_what_happens_in_a_move()

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
        if self.check_out_of_bounds_(poz):
            return False
        if self.board[poz[1]][poz[0]] == GameUtils.CELL_WALL:
            return False
        return True

    def check_out_of_bounds_(self, poz: tuple[int, int]) -> bool:
        if poz[0] < 0 or poz[0] >= len(self.board[0]) or poz[1] < 0 or poz[1] >= len(self.board):
            return True
        return False

    def check_new_position(self, poz: tuple[int, int], direction:tuple[int,int]) -> bool:

        curr_cell:tuple[int,int] = poz[0] // self.cell_size, poz[1] // self.cell_size
        if self.check_out_of_bounds_(curr_cell):
            return False
        if self.board[curr_cell[1]][curr_cell[0]] == GameUtils.CELL_WALL:
            return False
        if not self.check_positon_((curr_cell[0] + direction[0], curr_cell[1] + direction[1])):
            match direction:
                case GameUtils.DIRECTION_RIGHT:
                    return poz[0] - curr_cell[0] * self.cell_size <= self.cell_size // 2
                case GameUtils.DIRECTION_LEFT:
                    return poz[0] - curr_cell[0] * self.cell_size >= self.cell_size // 2
                case GameUtils.DIRECTION_UP:
                    return poz[1] - curr_cell[1] * self.cell_size >= self.cell_size // 2
                case GameUtils.DIRECTION_DOWN:
                    return poz[1] - curr_cell[1] * self.cell_size <= self.cell_size // 2
                case _:
                    raise NotImplementedError
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

    def move_a_type_default(self, a_type: int) -> bool:
        match a_type:
            case GameUtils.ACTOR_PACMAN:
                return self.move_actor_(self.pacman, self.pacman.direction)
            case GameUtils.ACTOR_RED:
                return self.move_actor_(self.red, self.red.direction)
            case GameUtils.ACTOR_BLUE:
                return self.move_actor_(self.blue, self.blue.direction)
            case GameUtils.ACTOR_PINK:
                return self.move_actor_(self.pink, self.pink.direction)
            case GameUtils.ACTOR_ORANGE:
                return self.move_actor_(self.orange, self.orange.direction)
            case _:
                raise NotImplementedError


    def change_direction_a_type(self, a_type: int, direction: tuple[int, int]) -> bool:
        match a_type:
            case GameUtils.ACTOR_PACMAN:
                return self.change_direction_actor(self.pacman, direction)
            case GameUtils.ACTOR_RED:
                return self.change_direction_actor(self.red, direction)
            case GameUtils.ACTOR_BLUE:
                return self.change_direction_actor(self.blue, direction)
            case GameUtils.ACTOR_PINK:
                return self.change_direction_actor(self.pink, direction)
            case GameUtils.ACTOR_ORANGE:
                return self.change_direction_actor(self.orange, direction)
            case _:
                raise NotImplementedError
    def change_direction_actor(self, a:Actor, direction: tuple[int, int]) -> bool:
        new_poz = a.get_new_poz(direction)
        if self.check_new_position(new_poz, direction):

            a.direction = direction
            return True
        return False

    def move_actor_(self, a:Actor, direction: tuple[int, int]) -> bool:
        new_poz = a.get_new_poz(direction)
        if direction == GameUtils.DIRECTION_UP:
            print("muie")
        if self.check_new_position(new_poz, direction):
            a.poz = new_poz
            a.direction = direction
            return True
        return False

    def game_paused(self):
        return self.game_state.game_temp_pause
    def game_over(self):
        return self.game_state.game_over



