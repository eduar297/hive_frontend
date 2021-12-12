import pygame
from menu import *
from math import *
from tool import *
from service import *
import json

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 233, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Palette
COLOR1 = (7, 30, 34)
COLOR2 = (29, 120, 116)
COLOR3 = (103, 146, 137)
COLOR4 = (197, 224, 99)
COLOR5 = (152, 206, 0)

LEVELS = {'lvl0': 0, 'lvl1': 1, 'lvl2': 2,
          'lvl3': 3}

LEFT, RIGHT = 1, 3

class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Hive')
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False, False, False
        self.ZOOM_IN_KEY, self.ZOOM_OUT_KEY = False, False
        self.LEFT_CLICK_KEY, self.RIGHT_CLICK_KEY = False, False
        self.MOUSE_POS = None
        self.DISPLAY_W, self.DISPLAY_H = 1300, 690
        self.MOUSE_MOTION = False

        self.LEVELS = LEVELS

        self.CENTER = Point(self.DISPLAY_W/2, self.DISPLAY_H/2)

        self.rect_up_region = pygame.Rect(
            0, 0, self.DISPLAY_W, self.DISPLAY_H*10/100)
        self.rect_left_region = pygame.Rect(
            0, self.DISPLAY_H*10/100, self.DISPLAY_W*10/100, self.DISPLAY_H*90/100)
        self.rect_right_region = pygame.Rect(
            self.DISPLAY_W*90/100, self.DISPLAY_H*10/100, self.DISPLAY_W*10/100, self.DISPLAY_H*90/100)
        self.rect_center_region = pygame.Rect(
            self.DISPLAY_W*10/100, self.DISPLAY_H*10/100, self.DISPLAY_W*80/100, self.DISPLAY_H*90/100)
        self.rect_arrow_region = pygame.Rect(
            self.DISPLAY_W*90/100, 0, self.DISPLAY_W*10/100, self.DISPLAY_H*10/100)
        self.rect_menu_up_btn_left = pygame.Rect(
            0, 0, self.DISPLAY_W*10/100, self.DISPLAY_H*10/100)

        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode(
            ((self.DISPLAY_W, self.DISPLAY_H)))

        self.font_name = '8-BIT WONDER.TTF'
        self.font_name_default = pygame.font.get_default_font()

        self.BLACK, self.WHITE, self.YELLOW, self.RED, self.GREEN, self.BLUE = BLACK, WHITE, YELLOW, RED, GREEN, BLUE
        self.PALETTE = [COLOR1, COLOR2, COLOR3, COLOR4, COLOR5]

        self.main_menu = MainMenu(self)
        self.options_menu = OptionsMenu(self)
        self.credits_menu = CreditsMenu(self)
        self.curr_menu = self.main_menu

        self.images = None

        # load default config
        self.load_config()
        self.mode = 'pvp'

        # game stats
        self.game_over = False
        self.info_msg = ''
        self.hexagon_size = 45
        self.hexagon_hand_size = 29
        self.current_region = None
        self.hex_selected = None
        self.hexagon_ori = None
        self.hex_hover = None
        stats = get_game_stats()
        self.p1 = stats[1]
        self.p2 = stats[2]
        self.hive = stats[3]
        current_player_id = stats[0]
        self.current_player = self.p1 if current_player_id == 'p1' else self.p2

        self.possible_placements = None
        self.possible_moves = None

        self.update_stats(self.p1)
        self.update_stats(self.p2)

        self.loadImgs()

    def update_stats(self, player):
        if player.id == 'p1':
            rect = self.rect_left_region
        elif player.id == 'p2':
            rect = self.rect_right_region

        insects = player.non_placed_insects

        hexagons = []

        queen_bee_count = 0
        beetle_count = 0
        grasshopper_count = 0
        spider_count = 0
        soldier_ant_count = 0
        ladybug_count = 0
        mosquito_count = 0
        pillbug_count = 0

        size = self.hexagon_hand_size
        w = sqrt(3)*size
        h = 2*size+10
        if player.id == 'p1':
            x = rect.midtop[0]-w/6
        elif player.id == 'p2':
            x = rect.midtop[0]+w/6
        y = rect.midtop[1] + 95

        if player.id == 'p1':
            for insect in insects:
                if insect[0] == 'queen_bee':
                    p = Point(x+w/5*queen_bee_count, y+h*0)
                    hex = Hex.pixel_to_pointy_hex(p, size)
                    hexagon = Hexagon(p, size, hex, self.PALETTE[0], insect[0])
                    queen_bee_count += 1
                    hexagons.append(hexagon)
                elif insect[0] == 'beetle':
                    p = Point(x+w/5*beetle_count, y+h*1)
                    hex = Hex.pixel_to_pointy_hex(p, size)
                    hexagon = Hexagon(p, size, hex, self.PALETTE[0], insect[0])
                    beetle_count += 1
                    hexagons.append(hexagon)
                elif insect[0] == 'grasshopper':
                    p = Point(x+w/5*grasshopper_count, y+h*2)
                    hex = Hex.pixel_to_pointy_hex(p, size)
                    hexagon = Hexagon(p, size, hex, self.PALETTE[0], insect[0])
                    grasshopper_count += 1
                    hexagons.append(hexagon)
                elif insect[0] == 'spider':
                    p = Point(x+w/5*spider_count, y+h*3)
                    hex = Hex.pixel_to_pointy_hex(p, size)
                    hexagon = Hexagon(p, size, hex, self.PALETTE[0], insect[0])
                    spider_count += 1
                    hexagons.append(hexagon)
                elif insect[0] == 'soldier_ant':
                    p = Point(x+w/5*soldier_ant_count, y+h*4)
                    hex = Hex.pixel_to_pointy_hex(p, size)
                    hexagon = Hexagon(p, size, hex, self.PALETTE[0], insect[0])
                    soldier_ant_count += 1
                    hexagons.append(hexagon)
                elif insect[0] == 'ladybug':
                    p = Point(x+w/5*ladybug_count, y+h*5)
                    hex = Hex.pixel_to_pointy_hex(p, size)
                    hexagon = Hexagon(p, size, hex, self.PALETTE[0], insect[0])
                    ladybug_count += 1
                    hexagons.append(hexagon)
                elif insect[0] == 'mosquito':
                    p = Point(x+w/5*mosquito_count, y+h*6)
                    hex = Hex.pixel_to_pointy_hex(p, size)
                    hexagon = Hexagon(p, size, hex, self.PALETTE[0], insect[0])
                    mosquito_count += 1
                    hexagons.append(hexagon)
                elif insect[0] == 'pillbug':
                    p = Point(x+w/5*pillbug_count, y+h*7)
                    hex = Hex.pixel_to_pointy_hex(p, size)
                    hexagon = Hexagon(p, size, hex, self.PALETTE[0], insect[0])
                    pillbug_count += 1
                    hexagons.append(hexagon)
        if player.id == 'p2':
            for insect in insects:
                if insect[0] == 'queen_bee':
                    p = Point(x-w/5*queen_bee_count, y+h*0)
                    hex = Hex.pixel_to_pointy_hex(p, size)
                    hexagon = Hexagon(p, size, hex, self.PALETTE[1], insect[0])
                    queen_bee_count += 1
                    hexagons.append(hexagon)
                elif insect[0] == 'beetle':
                    p = Point(x-w/5*beetle_count, y+h*1)
                    hex = Hex.pixel_to_pointy_hex(p, size)
                    hexagon = Hexagon(p, size, hex, self.PALETTE[1], insect[0])
                    beetle_count += 1
                    hexagons.append(hexagon)
                elif insect[0] == 'grasshopper':
                    p = Point(x-w/5*grasshopper_count, y+h*2)
                    hex = Hex.pixel_to_pointy_hex(p, size)
                    hexagon = Hexagon(p, size, hex, self.PALETTE[1], insect[0])
                    grasshopper_count += 1
                    hexagons.append(hexagon)
                elif insect[0] == 'spider':
                    p = Point(x-w/5*spider_count, y+h*3)
                    hex = Hex.pixel_to_pointy_hex(p, size)
                    hexagon = Hexagon(p, size, hex, self.PALETTE[1], insect[0])
                    spider_count += 1
                    hexagons.append(hexagon)
                elif insect[0] == 'soldier_ant':
                    p = Point(x-w/5*soldier_ant_count, y+h*4)
                    hex = Hex.pixel_to_pointy_hex(p, size)
                    hexagon = Hexagon(p, size, hex, self.PALETTE[1], insect[0])
                    soldier_ant_count += 1
                    hexagons.append(hexagon)
                elif insect[0] == 'ladybug':
                    p = Point(x-w/5*ladybug_count, y+h*5)
                    hex = Hex.pixel_to_pointy_hex(p, size)
                    hexagon = Hexagon(p, size, hex, self.PALETTE[1], insect[0])
                    ladybug_count += 1
                    hexagons.append(hexagon)
                elif insect[0] == 'mosquito':
                    p = Point(x-w/5*mosquito_count, y+h*6)
                    hex = Hex.pixel_to_pointy_hex(p, size)
                    hexagon = Hexagon(p, size, hex, self.PALETTE[1], insect[0])
                    mosquito_count += 1
                    hexagons.append(hexagon)
                elif insect[0] == 'pillbug':
                    p = Point(x-w/5*pillbug_count, y+h*7)
                    hex = Hex.pixel_to_pointy_hex(p, size)
                    hexagon = Hexagon(p, size, hex, self.PALETTE[1], insect[0])
                    pillbug_count += 1
                    hexagons.append(hexagon)

        if player.id == 'p1':
            self.p1.hexagons_hand = hexagons
        elif player.id == 'p2':
            self.p2.hexagons_hand = hexagons

    def load_config(self):
        try:
            file = open('config.json')
            with open('config.json') as file:
                config = json.load(file)
                self.level = config['level']
        except FileNotFoundError:
            config = {}
            config['level'] = 0
            config['level_coordenates'] = {
                "x": 520.0, "y": 395.0}
            config['level_state'] = 'lvl0'
            self.level = config['level']
            with open('config.json', 'w') as file:
                json.dump(config, file, indent=4)

    def save_config(self, level, level_coordenates, level_state):
        config = {}
        config['level'] = level
        config['level_coordenates'] = level_coordenates
        config['level_state'] = level_state
        with open('config.json', 'w') as file:
            json.dump(config, file, indent=4)

    def game_loop(self):
        new_game(self.mode, self.level)
        self.info_msg = ""
        self.hexagon_size = 40
        self.current_region = None
        self.hex_selected = None
        self.hex_hover = None
        self.game_over = False
        stats = get_game_stats()
        self.p1 = stats[1]
        self.p2 = stats[2]
        self.hive = stats[3]
        current_player_id = stats[0]
        self.current_player = self.p1 if current_player_id == 'p1' else self.p2
        self.hexagon_hand_size = self.hexagon_size - 11

        self.possible_placements = None
        self.possible_moves = None

        self.update_stats(self.p1)
        self.update_stats(self.p2)

        while self.playing:
            self.check_events()
            if self.BACK_KEY:
                self.playing = False
            if self.LEFT_CLICK_KEY:
                self.handle_mouse_click()

            if self.RIGHT_CLICK_KEY:
                self.possible_placements = None
                self.possible_moves = None
                self.hex_selected = None
                self.hexagon_ori = None
                self.p1.hex_hand_hover = None
                self.p1.hex_hand_selected = None
                self.p2.hex_hand_hover = None
                self.p2.hex_hand_selected = None

            if self.MOUSE_MOTION:
                self.handle_mouse_motion()

            self.display.fill(self.BLACK)
            self.display_game()

            if self.UP_KEY:
                self.offset_coordinates('U')
            if self.DOWN_KEY:
                self.offset_coordinates('D')
            if self.LEFT_KEY:
                self.offset_coordinates('L')
            if self.RIGHT_KEY:
                self.offset_coordinates('R')

            if self.ZOOM_IN_KEY:
                self.zoom('+')
            if self.ZOOM_OUT_KEY:
                self.zoom('-')

            self.window.blit(self.display, (0, 0))
            pygame.display.update()
            self.reset_keys()

        # self.info_msg = ""
        # self.hexagon_size = 40
        # self.current_region = None
        # self.hex_selected = None
        # self.hex_hover = None
        # stats = get_game_stats()
        # self.p1 = stats[1]
        # self.p2 = stats[2]
        # self.hive = stats[3]
        # current_player_id = stats[0]
        # self.current_player = self.p1 if current_player_id == 'p1' else self.p2
        # self.hexagon_hand_size = self.hexagon_size - 11

        # self.possible_placements = None
        # self.possible_moves = None

        # self.update_stats(self.p1)
        # self.update_stats(self.p2)

    def offset_coordinates(self, dir):
        size = self.hexagon_size
        w = sqrt(3)*size
        h = 2*size
        dw = w
        dh = 3/4*h

        if dir == 'D':
            self.CENTER.translate(self.CENTER.x, self.CENTER.y-dh)
        elif dir == 'U':
            self.CENTER.translate(self.CENTER.x, self.CENTER.y+dh)
        elif dir == 'L':
            self.CENTER.translate(self.CENTER.x-dw, self.CENTER.y)
        elif dir == 'R':
            self.CENTER.translate(self.CENTER.x+dw, self.CENTER.y)

    def handle_mouse_motion(self):
        region = None
        if self.is_in_rect(self.MOUSE_POS, self.rect_up_region):
            region = ('up', self.rect_up_region)
            self.handle_up_mouse_motion()
        elif self.is_in_rect(self.MOUSE_POS, self.rect_left_region):
            region = ('left', self.rect_left_region)
            self.handle_left_mouse_motion()
        elif self.is_in_rect(self.MOUSE_POS, self.rect_right_region):
            region = ('right', self.rect_right_region)
            self.handle_right_mouse_motion()
        elif self.is_in_rect(self.MOUSE_POS, self.rect_center_region):
            region = ('center', self.rect_center_region)
            self.handle_board_mouse_motion()
        self.current_region = region[0]

    def handle_mouse_click(self):
        if self.current_region == 'center' and not self.game_over:
            self.handle_board_mouse_click()
        if self.current_region == 'up':
            if not self.game_over:
                self.info_msg = ''
            self.possible_placements = None
            self.possible_moves = None
            self.hex_selected = None
            self.p1.hex_hand_selected = None
            self.p2.hex_hand_selected = None
        if self.current_region == 'left' and not self.game_over:
            self.handle_left_mouse_click()
            self.hex_selected = None
            self.p2.hex_hand_selected = None
        if self.current_region == 'right' and not self.game_over:
            self.handle_right_mouse_click()
            self.hex_selected = None
            self.p1.hex_hand_selected = None

    def is_in_rect(self, p, rect):
        x = p[0]
        y = p[1]
        tl = rect.topleft
        br = rect.bottomright
        return x >= tl[0] and y >= tl[1] and x <= br[0] and y <= br[1]

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                elif event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                elif event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                elif event.key == pygame.K_UP:
                    self.UP_KEY = True
                elif event.key == pygame.K_LEFT:
                    self.LEFT_KEY = True
                elif event.key == pygame.K_RIGHT:
                    self.RIGHT_KEY = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == LEFT:
                    self.LEFT_CLICK_KEY = True
                    self.MOUSE_POS = pygame.mouse.get_pos()
                if event.button == RIGHT:
                    self.RIGHT_CLICK_KEY = True
            elif event.type == pygame.MOUSEMOTION:
                self.MOUSE_POS = pygame.mouse.get_pos()
                self.MOUSE_MOTION = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False, False, False
        self.LEFT_CLICK_KEY, self.RIGHT_CLICK_KEY = False, False
        self.ZOOM_IN_KEY, self.ZOOM_OUT_KEY = False, False
        # self.MOUSE_POS = None
        # self.current_region = None
        self.MOUSE_MOTION = False

    def display_game(self):
        self.draw_board()

        # up
        pygame.draw.rect(self.display, self.BLACK,
                         self.rect_up_region, 0)
        pygame.draw.rect(self.display, self.WHITE,
                         self.rect_up_region, 1)
        # left
        pygame.draw.rect(self.display, self.BLACK,
                         self.rect_left_region, 0)
        pygame.draw.rect(self.display, self.WHITE,
                         self.rect_left_region, 1)
        # right
        pygame.draw.rect(self.display, self.BLACK,
                         self.rect_right_region, 0)
        pygame.draw.rect(self.display, self.WHITE,
                         self.rect_right_region, 1)
        # center
        pygame.draw.rect(self.display, self.WHITE,
                         self.rect_center_region, 1)

        self.draw_menu_up()
        self.draw_menu_left()
        self.draw_menu_right()

    def draw_text(self, text, size, x, y, color=WHITE, _font=None):
        if not _font:
            font = pygame.font.Font(self.font_name, size)
        else:
            font = pygame.font.Font(_font, size)

        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def draw_board(self):
        center = Point(self.CENTER.x, self.CENTER.y)
        size = self.hexagon_size
        Q = []
        D = {}
        hive = []

        # draw hive
        if self.hive:
            for insect in self.hive:
                type = insect[0]
                pid = insect[2]
                hex = Hex(insect[3][0], insect[3][1])

                p = Hex.pointy_hex_to_pixel(hex, size)

                if hex.point.point in Q:
                    D[hex.point.point] += 1
                    h1 = Hexagon(Point(
                        center.x + p.x + D[hex.point.point]*5, center.y + p.y + D[hex.point.point]*5), size-3, hex, self.WHITE)
                    h2 = Hexagon(Point(
                        center.x + p.x + D[hex.point.point]*5, center.y + p.y + D[hex.point.point]*5), size-5, hex, None)
                else:
                    Q.append(hex.point.point)
                    D[hex.point.point] = 0

                    h1 = Hexagon(Point(center.x + p.x, center.y +
                                 p.y), size-3, hex, self.WHITE)
                    h2 = Hexagon(
                        Point(center.x + p.x, center.y + p.y), size-5, hex, None)

                if pid == 'p1':
                    h2.color = self.PALETTE[0]
                if pid == 'p2':
                    h2.color = self.PALETTE[1]

                img_size = 110/100*size
                picture = pygame.transform.scale(
                    self.images[type], [img_size, img_size])
                hive.append([h1, h2, img_size, picture, D[hex.point.point]])

        for h in hive:
            h1 = h[0]
            h2 = h[1]
            img_size = h[2]
            picture = h[3]
            count = h[4]

            pygame.draw.lines(self.display, h1.color, True, h1.points, 3)
            pygame.draw.polygon(self.display, h2.color, h2.points)
            self.display.blit(
                picture, [h2.center.x-img_size/2, h2.center.y-img_size/2])

        # draw possible moves
        if self.possible_moves:
            for pm in self.possible_moves:
                p = Hex.pointy_hex_to_pixel(Hex(pm[0], pm[1]), size)
                h = Hexagon(Point(center.x + p.x, center.y + p.y),
                            size-3, pm, self.PALETTE[4])
                pygame.draw.lines(self.display, h.color, True, h.points, 4)

        # draw possible placements
        if self.possible_placements:
            for pp in self.possible_placements:
                p = Hex.pointy_hex_to_pixel(Hex(pp[0], pp[1]), size)
                h = Hexagon(Point(center.x + p.x, center.y + p.y),
                            size-3, pp, self.PALETTE[4])
                pygame.draw.lines(self.display, h.color, True, h.points, 4)

        # center
        # pygame.draw.circle(self.display, self.BLACK, center.point, 7, 0)
        # pygame.draw.circle(self.display, self.WHITE, center.point, 7, 2)

        # hexagon hover
        if self.hex_hover:
            if self.hex_hover.point.point in Q:
                _x, _y = D[self.hex_hover.point.point] * \
                    5, D[self.hex_hover.point.point]*5
            else:
                _x, _y = 0, 0
            p = Hex.pointy_hex_to_pixel(self.hex_hover, size)
            h = Hexagon(Point(center.x + p.x + _x, center.y + p.y+_y),
                        size-3, self.hex_hover, self.PALETTE[3])
            pygame.draw.lines(self.display, h.color, True, h.points, 3)
            self.draw_text(str(h.hex), 12, h.center.x, h.center.y,
                           self.WHITE, self.font_name_default)

        # hexagon selected
        if self.hex_selected:
            if self.hex_selected.point.point in Q:
                _x, _y = D[self.hex_selected.point.point] * \
                    5, D[self.hex_selected.point.point]*5
            else:
                _x, _y = 0, 0
            p = Hex.pointy_hex_to_pixel(self.hex_selected, size)
            h = Hexagon(Point(center.x + p.x + _x, center.y + _y + p.y),
                        size-3, self.hex_selected, self.PALETTE[3])
            pygame.draw.lines(self.display, h.color, True, h.points, 3)
            pygame.draw.circle(self.display, self.BLACK, h.center.point, 7, 0)
            pygame.draw.circle(
                self.display, self.PALETTE[3], h.center.point, 7, 2)

    def draw_menu_up(self):
        rect = self.rect_up_region
        self.draw_text(f"{self.current_player.name}'s turn", 15,
                       rect.centerx, rect.centery-10, self.WHITE, self.font_name_default)
        self.draw_text(f'{self.info_msg}', 12,
                       rect.centerx, rect.centery+10, self.RED, self.font_name_default)

        self.draw_menu_btn()
        self.draw_menu_up_left_btn()

    def draw_menu_left(self):
        rect = self.rect_left_region

        size = self.hexagon_hand_size
        img_size = 120/100*size

        self.draw_text(f'{self.p1.name}', 15,
                       rect.centerx, rect.topleft[1]+20, self.WHITE, self.font_name_default)
        self.draw_text(f'Number of Moves: {self.p1.number_of_moves}', 10,
                       rect.centerx, rect.topleft[1]+40, self.WHITE, self.font_name_default)
        if self.p1.hex_hand_selected:
            self.draw_text(f'{self.p1.hex_hand_selected.value}', 12,
                           rect.centerx, rect.topleft[1]+55, self.WHITE, self.font_name_default)

        for h in self.p1.hexagons_hand:
            pygame.draw.lines(self.display, self.WHITE, True, h.points, 4)
            pygame.draw.polygon(self.display, h.color, h.points)
            # self.draw_text(h.value, 8, h.center.x, h.center.y,
            #                self.WHITE, self.font_name_default)
            picture = pygame.transform.scale(
                self.images[h.value], [img_size, img_size])
            self.display.blit(
                picture, [h.center.x-img_size/2, h.center.y-img_size/2])

        if self.p1.hex_hand_hover:
            for h in self.p1.hexagons_hand[::-1]:
                if h.value == self.p1.hex_hand_hover.value:
                    _h = Hexagon(h.center, size, h.hex, h.color)
                    pygame.draw.lines(
                        self.display, self.PALETTE[3], True, _h.points, 3)
                    break
        if self.p1.hex_hand_selected:
            for h in self.p1.hexagons_hand[::-1]:
                if h.value == self.p1.hex_hand_selected.value:
                    _h = Hexagon(h.center, size, h.hex, h.color)
                    pygame.draw.lines(
                        self.display, self.PALETTE[3], True, _h.points, 3)
                    pygame.draw.circle(
                        self.display, self.BLACK, h.center.point, 5, 0)
                    pygame.draw.circle(
                        self.display, self.PALETTE[3], h.center.point, 5, 1)
                    break

    def draw_menu_right(self):
        rect = self.rect_right_region

        size = self.hexagon_hand_size
        img_size = 120/100*size

        self.draw_text(f'{self.p2.name}', 15,
                       rect.centerx, rect.topleft[1]+20, self.WHITE, self.font_name_default)
        self.draw_text(f'Number of Moves: {self.p2.number_of_moves}', 10,
                       rect.centerx, rect.topleft[1]+40, self.WHITE, self.font_name_default)
        if self.p2.hex_hand_selected:
            self.draw_text(f'{self.p2.hex_hand_selected.value}', 12,
                           rect.centerx, rect.topleft[1]+55, self.WHITE, self.font_name_default)

        for h in self.p2.hexagons_hand:
            pygame.draw.lines(self.display, self.WHITE, True, h.points, 4)
            pygame.draw.polygon(self.display, h.color, h.points)
            # self.draw_text(h.value, 8, h.center.x, h.center.y,
            #                self.WHITE, self.font_name_default)
            picture = pygame.transform.scale(
                self.images[h.value], [img_size, img_size])
            self.display.blit(
                picture, [h.center.x-img_size/2, h.center.y-img_size/2])

        if self.p2.hex_hand_hover:
            for h in self.p2.hexagons_hand[::-1]:
                if h.value == self.p2.hex_hand_hover.value:
                    _h = Hexagon(h.center, size, h.hex, h.color)
                    pygame.draw.lines(
                        self.display, self.PALETTE[3], True, _h.points, 3)
                    break
        if self.p2.hex_hand_selected:
            for h in self.p2.hexagons_hand[::-1]:
                if h.value == self.p2.hex_hand_selected.value:
                    _h = Hexagon(h.center, size, h.hex, h.color)
                    pygame.draw.lines(
                        self.display, self.PALETTE[3], True, _h.points, 2)
                    pygame.draw.circle(
                        self.display, self.BLACK, h.center.point, 5, 0)
                    pygame.draw.circle(
                        self.display, self.PALETTE[3], h.center.point, 5, 1)
                    break

    def draw_menu_up_left_btn(self):
        r = self.rect_menu_up_btn_left
        pygame.draw.rect(self.display, self.WHITE, r, 1)

        size = r.h*50/100
        back_btn = pygame.Rect(0, 0, size+5, size)
        reset_btn = pygame.Rect(0, 0, size+5, size)

        back_btn.center = (r.centerx-size/2-5, r.centery)
        reset_btn.center = (r.centerx+size/2+5, r.centery)

        pygame.draw.rect(self.display, self.PALETTE[2], back_btn, 0)
        pygame.draw.rect(self.display, self.PALETTE[2], reset_btn, 0)

        img_size1 = 110/100*size
        img_size2 = 100/100*size

        img_back = pygame.transform.scale(self.images['arrow'], [img_size1, img_size1])
        img_reset = pygame.transform.scale(self.images['reset'], [img_size2, img_size2])
        img_back = pygame.transform.rotate(img_back, 180)

        self.display.blit(img_back, [back_btn.centerx-img_size1/2, back_btn.centery-img_size1/2])
        self.display.blit(img_reset, [reset_btn.centerx-img_size2/2, reset_btn.centery-img_size2/2])


        if self.LEFT_CLICK_KEY:
            if back_btn.collidepoint(self.MOUSE_POS):
                self.playing = False
            elif reset_btn.collidepoint(self.MOUSE_POS):
                new_game(self.mode, self.level)
                self.info_msg = ""
                self.hexagon_size = 40
                self.current_region = None
                self.hex_selected = None
                self.hex_hover = None
                self.game_over = False
                stats = get_game_stats()
                self.p1 = stats[1]
                self.p2 = stats[2]
                self.hive = stats[3]
                current_player_id = stats[0]
                self.current_player = self.p1 if current_player_id == 'p1' else self.p2
                self.hexagon_hand_size = self.hexagon_size - 11

                self.possible_placements = None
                self.possible_moves = None

                self.update_stats(self.p1)
                self.update_stats(self.p2)

    def draw_menu_btn(self):
        r = self.rect_arrow_region

        pygame.draw.rect(self.display, self.WHITE, r, 1)
        size = r.h*40/100

        top_btn = pygame.Rect(0, 0, size, size)
        bottom_btn = pygame.Rect(0, 0, size, size)
        left_btn = pygame.Rect(0, 0, size, size)
        right_btn = pygame.Rect(0, 0, size, size)

        zoom_in_btn = pygame.Rect(0, 0, size, 10)
        zoom_out_btn = pygame.Rect(0, 0, size, 10)

        top_btn.center = (r.centerx, r.centery-size/2-2)
        bottom_btn.center = (r.centerx, r.centery+size/2+2)
        left_btn.center = (r.centerx-size-2, r.centery)
        right_btn.center = (r.centerx+size+2, r.centery)

        zoom_in_btn.center = (r.centerx+size+2, r.centery+24)
        zoom_out_btn.center = (r.centerx-size-2, r.centery+24)

        if self.LEFT_CLICK_KEY:
            if top_btn.collidepoint(self.MOUSE_POS):
                self.handle_btn('U')
            elif bottom_btn.collidepoint(self.MOUSE_POS):
                self.handle_btn('D')
            elif left_btn.collidepoint(self.MOUSE_POS):
                self.handle_btn('L')
            elif right_btn.collidepoint(self.MOUSE_POS):
                self.handle_btn('R')

            elif zoom_in_btn.collidepoint(self.MOUSE_POS):
                self.handle_btn('+')
            elif zoom_out_btn.collidepoint(self.MOUSE_POS):
                self.handle_btn('-')
                # -------------------------------------------------------------

        pygame.draw.rect(self.display, self.PALETTE[2], top_btn, 0)
        pygame.draw.rect(self.display, self.PALETTE[2], bottom_btn, 0)
        pygame.draw.rect(self.display, self.PALETTE[2], left_btn, 0)
        pygame.draw.rect(self.display, self.PALETTE[2], right_btn, 0)

        pygame.draw.rect(self.display, self.WHITE, zoom_in_btn, 0)
        pygame.draw.rect(self.display, self.WHITE, zoom_out_btn, 0)

        # self.draw_text('U', 15,  top_btn.centerx, top_btn.centery,
        #                self.PALETTE[0], self.font_name_default)
        # self.draw_text('D', 15,  bottom_btn.centerx,
        #                bottom_btn.centery, self.PALETTE[0], self.font_name_default)
        # self.draw_text('L', 15,  left_btn.centerx,
        #                left_btn.centery, self.PALETTE[0], self.font_name_default)
        # self.draw_text('R', 15,  right_btn.centerx,
        #                right_btn.centery, self.PALETTE[0], self.font_name_default)

        self.draw_text('+', 12,  zoom_in_btn.centerx,
                       zoom_in_btn.centery, self.BLACK, self.font_name_default)
        self.draw_text('-', 12,  zoom_out_btn.centerx,
                       zoom_out_btn.centery, self.BLACK, self.font_name_default)

        img_size = 110/100*size

        img_left = pygame.transform.scale(
            self.images['arrow'], [img_size, img_size])
        img_right = pygame.transform.scale(
            self.images['arrow'], [img_size, img_size])
        img_up = pygame.transform.scale(
            self.images['arrow'], [img_size, img_size])
        img_down = pygame.transform.scale(
            self.images['arrow'], [img_size, img_size])

        img_left = pygame.transform.rotate(img_left, 180)
        img_up = pygame.transform.rotate(img_left, 270)
        img_down = pygame.transform.rotate(img_left, 90)

        self.display.blit(
            img_left, [left_btn.centerx-img_size/2, left_btn.centery-img_size/2])
        self.display.blit(
            img_right, [right_btn.centerx-img_size/2, right_btn.centery-img_size/2])
        self.display.blit(
            img_up, [top_btn.centerx-img_size/2, top_btn.centery-img_size/2])
        self.display.blit(
            img_down, [bottom_btn.centerx-img_size/2, bottom_btn.centery-img_size/2])

    def handle_btn(self, btn):
        if btn == 'L':
            self.LEFT_KEY = True
        if btn == 'R':
            self.RIGHT_KEY = True
        if btn == 'U':
            self.UP_KEY = True
        if btn == 'D':
            self.DOWN_KEY = True
        if btn == '+':
            self.ZOOM_IN_KEY = True
        if btn == '-':
            self.ZOOM_OUT_KEY = True

    def handle_board_mouse_motion(self):
        self.p1.hex_hand_hover = None
        self.p2.hex_hand_hover = None

        mouse_x = self.MOUSE_POS[0]
        mouse_y = self.MOUSE_POS[1]

        center = self.CENTER

        hex_hover = Hex.pixel_to_pointy_hex(
            Point(mouse_x-center.x, mouse_y-center.y), self.hexagon_size)

        self.hex_hover = hex_hover

    def handle_up_mouse_motion(self):
        self.hex_hover = None
        self.p1.hex_hand_hover = None
        self.p2.hex_hand_hover = None

    def handle_left_mouse_motion(self):
        self.hex_hover = None
        self.p2.hex_hand_hover = None

        mouse_x = self.MOUSE_POS[0]
        mouse_y = self.MOUSE_POS[1]

        hex_hover = Hex.pixel_to_pointy_hex(
            Point(mouse_x, mouse_y), self.hexagon_hand_size)

        for h in self.p1.hexagons_hand:
            if hex_hover.q == h.hex.q and hex_hover.r == h.hex.r:
                self.p1.hex_hand_hover = h
                break

    def handle_right_mouse_motion(self):
        self.hex_hover = None
        self.p1.hex_hand_hover = None

        mouse_x = self.MOUSE_POS[0]
        mouse_y = self.MOUSE_POS[1]

        hex_hover = Hex.pixel_to_pointy_hex(
            Point(mouse_x, mouse_y), self.hexagon_hand_size)

        for h in self.p2.hexagons_hand:
            if hex_hover.q == h.hex.q and hex_hover.r == h.hex.r:
                self.p2.hex_hand_hover = h
                break

    def handle_board_mouse_click(self):
        self.hex_selected = Hex(self.hex_hover.q, self.hex_hover.r)

        if self.current_player.hex_hand_selected and self.hex_selected:
            insect = self.get_insects_in_hex(self.hex_selected)
            if insect and insect[2] == self.current_player.id:
                self.possible_placements = None
                self.current_player.hex_hand_selected = None
                self.hexagon_ori = None
                self.analize_possible_moves()

            elif self.possible_placements:
                self._place_insect()
                self.hexagon_ori = None

        elif self.hex_selected:
            if self.possible_moves:
                self._move_insect()
            else:
                self.analize_possible_moves()

    # If there is an insect in hex, it returns its properties.
    # (In case of having several, it returns a list with all, or empty in another case)
    def get_insects_in_hex(self, hex):
        last = get_last_insect([hex.q, hex.r])
        if last['success']:
            self.info_msg = ""
            return last['insect']
        else:
            self.info_msg = last['msg']

    # analize possible moves
    def analize_possible_moves(self):
        self.hexagon_ori = self.hex_selected
        self.current_player.hex_hand_selected = None
        if self.mode == 'pvai':
            self.info_msg = 'AI is thinking... ... ...'
        insect = self.get_insects_in_hex(self.hex_selected)
        if insect:
            type = insect[0]
            id = insect[1]
            pid = insect[2]
            hex = insect[3]
            placed = insect[4]
            if not self.current_player.id == pid:
                self.info_msg = "Wait for your turn!"
                self.hex_selected = None
            else:
                pm = get_possible_moves(type, id, hex)
                if pm['success']:
                    self.info_msg = ""
                    self.possible_moves = pm['moves']
                else:
                    self.info_msg = pm['msg']

    # move an insect if you can
    def _move_insect(self):
        self.possible_placements = None
        moved = False
        for pm in self.possible_moves:
            if self.hex_selected.q == pm[0] and self.hex_selected.r == pm[1]:
                insect = self.get_insects_in_hex(self.hexagon_ori)
                move_insect(
                    insect, insect[3], pm)

                moved = True

                self.possible_placements = None
                self.possible_moves = None
                self.hexagon_ori = None
                self.info_msg = ''

                # game stats
                stats = get_game_stats()
                current_player_id = stats[0]
                self.hive = stats[3]

                if current_player_id == 'p1':
                    self.p2 = stats[2]
                    self.update_stats(self.p2)
                    self.current_player = self.p1
                elif current_player_id == 'p2':
                    self.p1 = stats[1]
                    self.update_stats(self.p1)
                    self.current_player = self.p2

                # game over?
                qs = get_queen_surrounded()
                if qs['status_code'] != 200:
                    self.info_msg = qs['msg']
                    self.game_over = True
                    break

                if self.mode == 'pvai':
                    self.info_msg = 'AI is thinking... ... ...'
                    ai = play_ai()
                    self.info_msg = ai['msg']

                    stats = get_game_stats()
                    current_player_id = stats[0]
                    self.hive = stats[3]
                    self.p2 = stats[2]
                    self.update_stats(self.p2)
                    self.current_player = self.p1

                    # game over?
                    qs = get_queen_surrounded()
                    if qs['status_code'] != 200:
                        self.info_msg = qs['msg']
                        self.game_over = True
                        break

                break
        if not moved and not self.game_over:
            self.info_msg = 'Wrong place!!!'

    # place an insect if it is a valid position
    def _place_insect(self):
        self.possible_moves = None
        placed = False
        for pp in self.possible_placements:
            if self.hex_selected.q == pp[0] and self.hex_selected.r == pp[1]:
                place_insect(
                    self.current_player.hex_hand_selected.value, pp)
                # game stats
                stats = get_game_stats()
                current_player_id = stats[0]
                self.hive = stats[3]

                if current_player_id == 'p1':
                    self.p2 = stats[2]
                    self.update_stats(self.p2)
                    self.current_player = self.p1
                elif current_player_id == 'p2':
                    self.p1 = stats[1]
                    self.update_stats(self.p1)
                    self.current_player = self.p2
                self.possible_placements = None
                placed = True
                self.info_msg = ''
                # game over?
                qs = get_queen_surrounded()
                if qs['status_code'] != 200:
                    self.info_msg = qs['msg']
                    self.game_over = True
                    break

                if self.mode == 'pvai':
                    self.info_msg = 'AI is thinking... ... ...'
                    ai = play_ai()
                    self.info_msg = ai['msg']

                    stats = get_game_stats()
                    current_player_id = stats[0]
                    self.hive = stats[3]
                    self.p2 = stats[2]
                    self.update_stats(self.p2)
                    self.current_player = self.p1

                    # game over?
                    qs = get_queen_surrounded()
                    if qs['status_code'] != 200:
                        self.info_msg = qs['msg']
                        self.game_over = True
                        break

                break
        if not placed and not self.game_over:
            self.info_msg = 'Wrong place!!!'

    def handle_left_mouse_click(self):
        self.possible_moves = None
        self.possible_placements = None
        if self.current_player.id == 'p2':
            self.info_msg = "Wait for your turn!"
        else:
            self.info_msg = ''
        if self.p1.hex_hand_hover and self.current_player.id == 'p1':
            self.p1.hex_hand_selected = self.p1.hex_hand_hover
            pp = get_possible_placements(self.p1.hex_hand_selected.value)
            if pp['success']:
                self.possible_placements = pp['placements']
            else:
                if pp['status_code'] == 400:
                    self.info_msg = pp['msg']
                if pp['status_code'] == 401:
                    self.info_msg = pp['msg']
                    stats = get_game_stats()
                    current_player_id = stats[0]
                    if current_player_id == 'p1':
                        self.current_player = self.p1
                    elif current_player_id == 'p2':
                        self.current_player = self.p2

    def handle_right_mouse_click(self):
        self.possible_moves = None
        self.possible_placements = None
        if self.mode == 'pvai':
            if self.current_player.id == 'p1':
                self.info_msg = "It's not your turn!!!"
            else:
                self.info_msg = "Wait for the AI to play!!!"
        else:
            if self.current_player.id == 'p1':
                self.info_msg = "It's not your turn!!!"
            else:
                self.info_msg = ''
            if self.p2.hex_hand_hover and self.current_player.id == 'p2':
                self.p2.hex_hand_selected = self.p2.hex_hand_hover
                pp = get_possible_placements(self.p2.hex_hand_selected.value)
                if pp['success']:
                    self.possible_placements = pp['placements']
                else:
                    if pp['status_code'] == 400:
                        self.info_msg = pp['msg']
                    if pp['status_code'] == 401:
                        self.info_msg = pp['msg']
                        stats = get_game_stats()
                        current_player_id = stats[0]
                        if current_player_id == 'p1':
                            self.current_player = self.p1
                        elif current_player_id == 'p2':
                            self.current_player = self.p2

    def loadImgs(self):
        self.images = {
            'queen_bee': pygame.image.load('./img/queen_bee.png'),
            'beetle': pygame.image.load('./img/beetle.png'),
            'grasshopper': pygame.image.load('./img/grasshopper.png'),
            'spider': pygame.image.load('./img/spider.png'),
            'soldier_ant': pygame.image.load('./img/soldier_ant.png'),
            'ladybug': pygame.image.load('./img/ladybug.png'),
            'mosquito': pygame.image.load('./img/mosquito.png'),
            'pillbug': pygame.image.load('./img/pillbug.png'),
            'arrow': pygame.image.load('./img/arrow.png'),
            'reset': pygame.image.load('./img/reset.png')
        }

    def zoom(self, dir):
        if dir == '+' and self.hexagon_size <= 120:
            self.hexagon_size += 5
        elif dir == '-' and self.hexagon_size > 30:
            self.hexagon_size -= 5
