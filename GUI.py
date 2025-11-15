import sys
import time

import pygame

import GUI_utils
import GameUtils
from GameDisplay import GameDisplay



class GUI:
    def __init__(self):
        self.game = GameDisplay(GUI_utils.DEFAULT_GAME_HEIGHT)
        self.gui_utils = GUI_utils.GUIUtils()
        self.main_loop()

    def main_loop(self):
        while True:
            p =  self.game.pacman.get_cell_poz(self.game.pacman.poz)
            if self.game.board[p[1]][p[0]] == GameUtils.CELL_WALL:
                print("W")
            self.handle_events()
            b = self.game.change_direction_a_type(GameUtils.ACTOR_PACMAN, self.gui_utils.direction)
            print(b)
            self.game.move_a_type_default(GameUtils.ACTOR_PACMAN)

            self.game.draw()
            time.sleep(1 / GUI_utils.DEFAULT_FPS)

    def handle_events(self):
        #print("handle_events")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Continuous key press detection
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            #print("W pressed")
            self.gui_utils.direction = GameUtils.DIRECTION_UP
        elif keys[pygame.K_a]:
            #print("A pressed")
            self.gui_utils.direction = GameUtils.DIRECTION_LEFT
        elif keys[pygame.K_s]:
            #print("S pressed")
            self.gui_utils.direction = GameUtils.DIRECTION_DOWN
        elif keys[pygame.K_d]:
            #print("D pressed")
            self.gui_utils.direction = GameUtils.DIRECTION_RIGHT




GUI = GUI()
