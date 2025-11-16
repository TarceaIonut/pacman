import sys
import time

import pygame

import GUI_utils
import GameUtils
from Button import Button
from GameDisplay import GameDisplay

def make_button_simpler(screen, position:tuple[int,int], text:str) -> Button:
    return Button(screen, position, text, GUI_utils.COLOR_DEFAULT_BUTTON, GUI_utils.COLOR_DEFAULT_TEXT, GUI_utils.DEFAULT_SIZE)


class GUI:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pacman")
        self.game = GameDisplay(GUI_utils.DEFAULT_GAME_HEIGHT)
        self.gui_utils = GUI_utils.GUIUtils()

        self.button_play = make_button_simpler(self.game.screen, (1150, 800), "play")
        self.button_dfs = make_button_simpler(self.game.screen, (1000, 600), "Depth-First Search")
        self.button_bfs = make_button_simpler(self.game.screen, (1000, 500), "Breadth-First Search")
        self.button_astar = make_button_simpler(self.game.screen, (1000, 400), "A star")
        self.button_reflex = make_button_simpler(self.game.screen, (1300, 600), "Reflex Agent")
        self.button_minmax = make_button_simpler(self.game.screen, (1300, 500), "Minmax")
        self.button_ab_pruning = make_button_simpler(self.game.screen, (1300, 400), "Alpha-Beta pruning")
        self.button_manual = make_button_simpler(self.game.screen, (1300, 700), "Manual Mode")
        self.button_auto = make_button_simpler(self.game.screen, (1000, 700), "Auto Mode")

        self.complete_loop()

    def draw_text(self, poz:tuple[int,int], text:str):
        font = pygame.font.SysFont("Arial", GUI_utils.DEFAULT_SIZE // 3)
        text_surface = font.render(text, True, GUI_utils.COLOR_DEFAULT_TEXT)
        self.game.screen.blit(text_surface, poz)

    def clear_area(self, rect):
        pygame.draw.rect(self.game.screen, (0, 0, 0), rect)

    def draw_info(self):

        self.clear_area(pygame.Rect(1000, 50, 300, 300))

        self.draw_text((1000, 200), "Mode: " + self.gui_utils.mode_to_string())
        self.draw_text((1000, 250), "Pacman: " + self.gui_utils.alg_pacman_to_string())
        self.draw_text((1000, 300), "Ghost: " + self.gui_utils.alg_ghost_to_string())
        self.draw_text((1000, 100), "Lives: " + str(self.game.game_state.lives))
        self.draw_text((1000, 50),  "Points: " + str(self.game.game_state.game_score))


    def complete_loop(self):
        self.game.draw()
        while True:
            pygame.event.pump()
            self.draw_info()
            self.check_buttons()
            self.main_loop()
            self.draw_buttons()
            pygame.display.update()
            time.sleep(1 / GUI_utils.DEFAULT_FPS)


    def check_buttons(self):
        if self.button_play.click():
            self.gui_utils.play = True
        if self.button_dfs.click():
            self.gui_utils.alg_ghost = GUI_utils.ALGORITHM_GHOST_DFS
        if self.button_bfs.click():
            self.gui_utils.alg_ghost = GUI_utils.ALGORITHM_GHOST_BFS
        if self.button_astar.click():
            self.gui_utils.alg_ghost = GUI_utils.ALGORITHM_GHOST_ASTAR

        if self.button_reflex.click():
            self.gui_utils.alg_pacman = GUI_utils.ALGORITHM_PACMAN_REFLEX_AGENT
        if self.button_minmax.click():
            self.gui_utils.alg_pacman = GUI_utils.ALGORITHM_PACMAN_MIN_MAX
        if self.button_ab_pruning.click():
            self.gui_utils.alg_pacman = GUI_utils.ALGORITHM_PACMAN_AB_PRUNING

        if self.button_manual.click():
            self.gui_utils.mode = GUI_utils.MODE_MANUAL
        if self.button_auto.click():
            self.gui_utils.mode = GUI_utils.MODE_AUTO


    def draw_buttons(self) -> None:
        self.button_play.draw()
        self.button_dfs.draw()
        self.button_bfs.draw()
        self.button_astar.draw()
        self.button_reflex.draw()
        self.button_minmax.draw()
        self.button_ab_pruning.draw()
        self.button_manual.draw()
        self.button_auto.draw()

    def main_loop(self):
        if self.gui_utils.play:
            p = self.game.pacman.get_cell_poz(self.game.pacman.poz)
            if self.game.board[p[1]][p[0]] == GameUtils.CELL_WALL:
                print("W")
            self.handle_events()
            self.game.change_direction_a_type(GameUtils.ACTOR_PACMAN, self.gui_utils.direction)
            self.game.move_a_type_default(GameUtils.ACTOR_PACMAN)
            self.game.draw()




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
