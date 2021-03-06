import pygame
from tool import Hexagon, Point
import json


class Menu():
    def __init__(self, game, offset):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W/2, self.game.DISPLAY_H/2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = offset

    def draw_cursor(self):
        self.game.draw_text('*', 15, self.cursor_rect.x,
                            self.cursor_rect.y, self.game.RED)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

    def decorate_screen(self, x, y):
        size = 40
        h1 = Hexagon(Point(x, y), size)
        w = h1.w
        h = h1.h
        h2 = Hexagon(Point(x+w, y), size)
        h3 = Hexagon(Point(x+2*w, y), size)
        h4 = Hexagon(Point(x+w/2, y+3/4*h), size)
        h5 = Hexagon(Point(x+3/2*w, y+3/4*h), size)
        h6 = Hexagon(Point(x+w, y+3/2*h), size)
        h7 = Hexagon(Point(x-w/2, y+3/4*h), size)
        h8 = Hexagon(Point(x-w, y+3/2*h), size)
        h9 = Hexagon(Point(x, y+3/2*h), size)
        h10 = Hexagon(Point(x+w*2, y+3/2*h), size)
        h11 = Hexagon(Point(x-w, y), size)
        h12 = Hexagon(Point(x+1/2*w, y+3/4*h*3), size)
        h13 = Hexagon(Point(x+3/2*w, y+3/4*h*3), size)
        h14 = Hexagon(Point(x+5/2*w, y+3/4*h*3), size)
        h15 = Hexagon(Point(x+w, y+3/4*h*4), size)
        h16 = Hexagon(Point(x-2*w, y), size)
        h17 = Hexagon(Point(x-3/2*w, y-3/4*h), size)

        hexagons = [h1, h2, h3, h4, h5, h6, h7,
                    h8, h9, h10, h11, h12, h13, h14, h15, h16, h17]

        for h in hexagons:
            pygame.draw.lines(self.game.display,
                              self.game.YELLOW, True, h.points, 4)


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game, -190)
        self.state = 'PVP'
        self.pvpx, self.pvpy = self.mid_w, self.mid_h+50
        self.pvaix, self.pvaiy = self.mid_w, self.mid_h+90
        self.optionsx, self.optionsy = self.mid_w, self.mid_h+130
        self.creditsx, self.creditsy = self.mid_w, self.mid_h+170
        self.quitx, self.quity = self.mid_w, self.mid_h+210
        self.cursor_rect.midtop = (self.pvpx+self.offset, self.pvpy)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)

            self.decorate_screen(80, 27)
            self.decorate_screen(self.mid_w+400, self.mid_h+150)

            self.game.draw_text('Hive', 80, self.mid_w, 120, self.game.YELLOW)
            self.game.draw_text('Main Menu', 35, self.mid_w, self.mid_h-20)
            self.game.draw_text('Player vs Player', 25, self.pvpx, self.pvpy)
            self.game.draw_text('Player vs AI', 25, self.pvaix, self.pvaiy)
            self.game.draw_text('Difficulty', 25, self.optionsx, self.optionsy)
            self.game.draw_text('Credits', 25, self.creditsx, self.creditsy)
            self.game.draw_text('Quit', 25, self.quitx, self.quity)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'PVP':
                self.cursor_rect.midtop = (
                    self.pvaix+self.offset, self.pvaiy)
                self.state = 'PVAI'
            elif self.state == 'PVAI':
                self.cursor_rect.midtop = (
                    self.optionsx+self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (
                    self.creditsx+self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (
                    self.quitx+self.offset, self.quity)
                self.state = 'Quit'
            elif self.state == 'Quit':
                self.cursor_rect.midtop = (
                    self.pvpx+self.offset, self.pvpy)
                self.state = 'PVP'
        elif self.game.UP_KEY:
            if self.state == 'PVP':
                self.cursor_rect.midtop = (
                    self.quitx+self.offset, self.quity)
                self.state = 'Quit'

            elif self.state == 'PVAI':
                self.cursor_rect.midtop = (
                    self.pvpx+self.offset, self.pvpy)
                self.state = 'PVP'

            elif self.state == 'Options':
                self.cursor_rect.midtop = (
                    self.pvaix+self.offset, self.pvaiy)
                self.state = 'PVAI'

            elif self.state == 'Credits':
                self.cursor_rect.midtop = (
                    self.optionsx+self.offset, self.optionsy)
                self.state = 'Options'

            elif self.state == 'Quit':
                self.cursor_rect.midtop = (
                    self.creditsx+self.offset, self.creditsy)
                self.state = 'Credits'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'PVP':
                self.game.playing = True
                self.game.mode = 'pvp'
            elif self.state == 'PVAI':
                self.game.playing = True
                self.game.mode = 'pvai'
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options_menu
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits_menu
            elif self.state == 'Quit':
                self.game.running, self.game.playing = False, False
                self.game.curr_menu.run_display = False
            self.run_display = False


class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game, -130)
        self.lvl0x, self.lvl0y = self.mid_w, self.mid_h+50
        self.lvl1x, self.lvl1y = self.mid_w, self.mid_h+90
        # self.lvl2x, self.lvl2y = self.mid_w, self.mid_h+130
        # self.lvl3x, self.lvl3y = self.mid_w, self.mid_h+170
        self.infox, self.infoy = self.mid_w, self.mid_h+160
        try:
            open('config.json')
            with open('config.json') as file:
                config = json.load(file)
                self.state = config['level_state']
                self.cursor_rect.midtop = (
                    config['level_coordenates']['x'], config['level_coordenates']['y'])
        except:
            self.state = 'lvl0'
            self.cursor_rect.midtop = (self.lvl0x + self.offset, self.lvl0y)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)

            self.decorate_screen(80, 27)
            self.decorate_screen(self.mid_w+400, self.mid_h+150)

            self.game.draw_text('Hive', 80, self.mid_w, 120, self.game.YELLOW)
            self.game.draw_text('Difficulty level', 35,
                                self.mid_w, self.mid_h-20)
            self.game.draw_text('Easy', 25, self.lvl0x, self.lvl0y, self.game.PALETTE[1])
            self.game.draw_text('Medium', 25, self.lvl1x, self.lvl1y, self.game.PALETTE[0])
            # self.game.draw_text('Hard', 25, self.lvl2x, self.lvl2y)
            # self.game.draw_text('Expert', 25, self.lvl3x,self.lvl3y, self.game.PALETTE[0])
            self.game.draw_text('Press enter key to save or backspace to return',
                                15, self.infox, self.infoy, color=self.game.RED)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'lvl0':
                self.cursor_rect.midtop = (
                    self.lvl1x+self.offset, self.lvl1y)
                self.state = 'lvl1'
            elif self.state == 'lvl1':
                self.cursor_rect.midtop = (
                    self.lvl0x+self.offset, self.lvl0y)
                self.state = 'lvl0'
            # elif self.state == 'lvl2':
            #     self.cursor_rect.midtop = (
            #         self.lvl3x+self.offset, self.lvl3y)
            #     self.state = 'lvl3'
            # elif self.state == 'lvl3':
            #     self.cursor_rect.midtop = (
            #         self.lvl0x+self.offset, self.lvl0y)
            #     self.state = 'lvl0'
        elif self.game.UP_KEY:
            # if self.state == 'lvl3':
            #     self.cursor_rect.midtop = (
            #         self.lvl2x+self.offset, self.lvl2y)
            #     self.state = 'lvl2'
            # elif self.state == 'lvl2':
            #     self.cursor_rect.midtop = (
            #         self.lvl1x+self.offset, self.lvl1y)
            #     self.state = 'lvl1'
            if self.state == 'lvl1':
                self.cursor_rect.midtop = (
                    self.lvl0x+self.offset, self.lvl0y)
                self.state = 'lvl0'
            elif self.state == 'lvl0':
                self.cursor_rect.midtop = (
                    self.lvl1x+self.offset, self.lvl1y)
                self.state = 'lvl1'

    def check_input(self):
        self.move_cursor()
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.START_KEY:
            self.game.level = self.game.LEVELS[self.state]
            self.game.curr_menu = self.game.main_menu
            self.game.save_config(self.game.level, {'x': self.cursor_rect.midtop[0], 'y': self.cursor_rect.midtop[1]}, self.state)
            self.run_display = False


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game, -130)
        self.creditsx, self.creditsy = self.mid_w, self.mid_h+50
        self.infox, self.infoy = self.mid_w, self.mid_h+120

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)

            self.decorate_screen(80, 27)
            self.decorate_screen(self.mid_w+400, self.mid_h+150)

            self.game.draw_text('Hive', 80, self.mid_w, 120, self.game.YELLOW)
            self.game.draw_text('Credits', 35, self.mid_w, self.mid_h-20)
            self.game.draw_text('Made by Eduar2 Andy Yadiel',
                                25, self.creditsx, self.creditsy)
            self.game.draw_text('Press enter or backspace key to go back',
                                15, self.infox, self.infoy, color=self.game.RED)
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY or self.game.START_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
