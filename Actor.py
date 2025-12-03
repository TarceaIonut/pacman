import pygame

import GameUtils
import Maze
from HelperFunctions import image_black_transparent, direction_to_number, positon_add_direction_, scale_direction_



class Actor:
    def __init__(self, type_:int, row_col:tuple[int,int], cell_size:int):
        self.type = type_
        self.poz:tuple[int,int] = (int((row_col[1] + 0.5) * cell_size), int((row_col[0] + 0.5) * cell_size))
        self.cell_size = cell_size
        self.image_size = cell_size * 1.5
        self.direction = GameUtils.DIRECTION_UP
        self.animation_cycle:int = 0

        self.scared_state:bool = False
        self.eaten_state:bool = False

        if type_ == GameUtils.ACTOR_PACMAN:
            self.number_of_pixels_per_draw:int = self.cell_size // GameUtils.CYCLES_PER_CELL_PACMAN
        else:
            self.number_of_pixels_per_draw:int = self.cell_size // GameUtils.CYCLES_PER_CELL_GHOST

        self.image_scared_ghost = image_black_transparent("ghost_scared.png", self.image_size)
        self.image_eyes = pygame.transform.scale(pygame.image.load("eyes.png"),(self.image_size, self.image_size // 2)).convert_alpha()
        self.image_eyes.set_colorkey((70, 70, 70))

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
            image = image_black_transparent("red_left.png", self.image_size)
            self.image = [image,image,image,image]
        elif type_ == GameUtils.ACTOR_BLUE:
            self.nr_animations: int = 1
            image = image_black_transparent("blue.png", self.image_size)
            self.image = [image, image, image, image]
        elif type_ == GameUtils.ACTOR_ORANGE:
            self.nr_animations: int = 1
            image = image_black_transparent("orange.png", self.image_size)
            self.image = [image, image, image, image]
        elif type_ == GameUtils.ACTOR_PINK:
            self.nr_animations: int = 1
            image = image_black_transparent("pink.png", self.image_size)
            self.image = [image, image, image, image]
        else:
            raise NotImplementedError

    def reset_positions(self, row_col:tuple[int,int]):
        self.poz = (int((row_col[1] + 0.5) * self.cell_size), int((row_col[0] + 0.5) * self.cell_size))
        self.direction = GameUtils.DIRECTION_UP
        self.animation_cycle: int = 0
        self.scared_state: bool = False
        self.eaten_state: bool = False

    def draw(self, surface):
        image_nr:int = direction_to_number(self.direction) * self.nr_animations + (self.animation_cycle // 5) % self.nr_animations
        offset:float = (self.image_size / 2)
        #print(image_nr)
        if len(self.image) <= image_nr:
            print("not possible")
            raise NotImplementedError
        draw_poz = self.normalize_coordinates_for_display()

        if self.eaten_state:
            surface.blit(self.image_eyes, (draw_poz[0] - offset // 2, draw_poz[1] - offset // 2))
        elif self.scared_state:
            surface.blit(self.image_scared_ghost, (draw_poz[0] - offset, draw_poz[1] - offset))
        else:
            surface.blit(self.image[image_nr], (draw_poz[0] - offset, draw_poz[1] - offset))

        self.animation_cycle += 1

    def get_cell_poz(self, poz: tuple[int,int]) -> tuple[int,int]:
        return poz[0] // self.cell_size, poz[1] // self.cell_size
    def get_current_cell_poz(self):
        return self.get_cell_poz(self.poz)

    def normalize_coordinates_for_display(self) -> tuple[int,int]:
        if self.direction == GameUtils.DIRECTION_UP or self.direction == GameUtils.DIRECTION_DOWN:
            return int(((self.poz[0] // self.cell_size) + 0.5) * self.cell_size), self.poz[1]
        return self.poz[0], int(((self.poz[1] // self.cell_size) + 0.5) * self.cell_size)

    def get_new_poz(self, direction: tuple[int,int]):
        return positon_add_direction_(self.poz, scale_direction_(direction, self.number_of_pixels_per_draw))

    def change_direction_and_position_unchecked(self, direction: tuple[int,int]):
        p_x = self.poz[1] + direction[0] * self.number_of_pixels_per_draw
        p_y = self.poz[0] + direction[1] * self.number_of_pixels_per_draw
        self.poz = p_y, p_x
        self.direction = direction


def get_actor_poz(a: Actor) -> tuple[int,int]:
    return a.get_cell_poz(a.poz)