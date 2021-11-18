import pygame
from menu import *
from math import *
from tool import *
from service import *

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


LEFT, RIGHT = 1, 3


class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Hive')
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False, False, False
        self.LEFT_CLICK_KEY, self.RIGHT_CLICK_KEY = False, False
        self.MOUSE_POS = None
        self.DISPLAY_W, self.DISPLAY_H = 1300, 690
        self.MOUSE_MOTION = False

        self.hexagon_size = 40
        self.back_hexagons = []

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

        self.current_region = None

        self.hex_selected = None
        self.hex_hover = None

        # game stats
        stats = get_game_stats()
        self.p1 = stats[1]
        self.p2 = stats[2]
        self.hive = stats[3]
        current_player_id = stats[0]
        self.current_player = self.p1 if current_player_id == 'p1' else self.p2
        self.hexagon_hand_size = self.hexagon_size - 11

        self.possible_placements = None

        self.update_stats(self.p1)
        self.update_stats(self.p2)

        self.init_board()

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

    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.BACK_KEY:
                self.playing = False
            if self.LEFT_CLICK_KEY:
                self.handle_mouse_click()

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

            self.window.blit(self.display, (0, 0))
            pygame.display.update()
            self.reset_keys()

    def offset_coordinates(self, dir):
        size = self.hexagon_size
        w = sqrt(3)*size
        h = 2*size
        dw = w
        dh = 3/4*h

        if dir == 'U':
            self.CENTER.translate(self.CENTER.x, self.CENTER.y-dh)
        elif dir == 'D':
            self.CENTER.translate(self.CENTER.x, self.CENTER.y+dh)
        elif dir == 'L':
            self.CENTER.translate(self.CENTER.x-dw, self.CENTER.y)
        elif dir == 'R':
            self.CENTER.translate(self.CENTER.x+dw, self.CENTER.y)

        # recalculate hexagons coordinates
        for h in self.back_hexagons:
            p = Hex.pointy_hex_to_pixel(h.hex, size)
            h.update(center=Point(self.CENTER.x+p.x, self.CENTER.y+p.y))

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
        if self.current_region == 'center':
            self.handle_board_mouse_click()
        if self.current_region == 'up':
            self.hex_selected = None
            self.p1.hex_hand_selected = None
            self.p2.hex_hand_selected = None
        if self.current_region == 'left':
            self.handle_left_mouse_click()
            self.hex_selected = None
            self.p2.hex_hand_selected = None
        if self.current_region == 'right':
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
            elif event.type == pygame.MOUSEMOTION:
                self.MOUSE_POS = pygame.mouse.get_pos()
                self.MOUSE_MOTION = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False, False, False
        self.LEFT_CLICK_KEY, self.RIGHT_CLICK_KEY = False, False
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

    def init_board(self):
        size = self.hexagon_size
        w = sqrt(3)*size
        h = 2*size
        dw = w
        dh = 3/4*h
        center = Point(self.CENTER.x, self.CENTER.y)
        ad = Hex.axial_directions(q1=-20, q2=20, r1=-20, r2=20)

        for d in ad:
            p = Hex.pointy_hex_to_pixel(d, size)
            h = Hexagon(Point(center.x + p.x, center.y + p.y),
                        size, d, self.PALETTE[0])
            if d.q == 0 and d.r == 0:
                h.color = self.RED
                h.value = 0

            self.back_hexagons.append(h)

    def draw_board(self):
        hex_hover = None
        hex_selected = None
        hex_center = None
        for h in self.back_hexagons:
            x = h.center.x
            y = h.center.y

            rcr = self.rect_center_region

            if self.possible_placements:
                for pp in self.possible_placements:
                    if h.hex.q == pp[0] and h.hex.r == pp[1]:
                        _h = Hexagon(h.center, h.size-4, h.hex, h.color)
                        pygame.draw.lines(
                            self.display, self.PALETTE[4], True, _h.points, 4)

            for insect in self.hive:
                type = insect[0]
                pid = insect[2]
                hex = insect[3]

                if h.hex.q == hex[0] and h.hex.r == hex[1]:
                    pygame.draw.lines(
                        self.display, self.WHITE, True, h.points, 4)
                    if pid == 'p1':
                        pygame.draw.polygon(
                            self.display, self.PALETTE[0], h.points)
                        self.draw_text(type, 9, h.center.x, h.center.y,
                                       self.WHITE, self.font_name_default)
                    if pid == 'p2':
                        pygame.draw.polygon(
                            self.display, self.PALETTE[1], h.points)
                        self.draw_text(type, 9, h.center.x, h.center.y,
                                       self.WHITE, self.font_name_default)

            if h.hex.point.point == (0, 0):
                hex_center = h
            if self.hex_hover and self.hex_hover.point.point == h.hex.point.point:
                hex_hover = self.hex_hover
                self.draw_text(str(h.hex), 12, h.center.x,
                               h.center.y, self.WHITE, self.font_name_default)
            if self.hex_selected and self.hex_selected.point.point == h.hex.point.point:
                hex_selected = self.hex_selected

        if hex_hover:
            h = next((
                h for h in self.back_hexagons if h.hex.point.point == hex_hover.point.point), None)
            _h = Hexagon(h.center, h.size+1, h.hex, h.color)
            pygame.draw.lines(
                self.display, self.WHITE, True, _h.points, 4)
        if hex_selected:
            h = next((
                h for h in self.back_hexagons if h.hex.point.point == hex_selected.point.point), None)
            _h = Hexagon(h.center, h.size+1, h.hex, h.color)
            pygame.draw.lines(
                self.display, self.PALETTE[3], True, _h.points, 4)
        if hex_center:
            pygame.draw.circle(
                self.display, self.PALETTE[2], hex_center.center.point, 5, 0)
            pygame.draw.circle(
                self.display, self.WHITE, hex_center.center.point, 5, 1)

    def draw_menu_up(self):
        rect = self.rect_up_region
        self.draw_text(f"{self.current_player.name}'s turn", 15,
                       rect.centerx, rect.centery, self.WHITE, self.font_name_default)

        self.draw_menu_arrow()

    def draw_menu_left(self):
        rect = self.rect_left_region

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
            self.draw_text(h.value, 8, h.center.x, h.center.y,
                           self.WHITE, self.font_name_default)

        if self.p1.hex_hand_hover:
            for h in self.p1.hexagons_hand[::-1]:
                if h.value == self.p1.hex_hand_hover.value:
                    _h = Hexagon(h.center, h.size+2, h.hex, h.color)
                    pygame.draw.lines(
                        self.display, self.WHITE, True, _h.points, 4)
                    break
        if self.p1.hex_hand_selected:
            for h in self.p1.hexagons_hand[::-1]:
                if h.value == self.p1.hex_hand_selected.value:
                    _h = Hexagon(h.center, h.size+2, h.hex, h.color)
                    pygame.draw.lines(
                        self.display, self.PALETTE[3], True, _h.points, 4)
                    break

    def draw_menu_right(self):
        rect = self.rect_right_region

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
            self.draw_text(h.value, 8, h.center.x, h.center.y,
                           self.WHITE, self.font_name_default)

        if self.p2.hex_hand_hover:
            for h in self.p2.hexagons_hand[::-1]:
                if h.value == self.p2.hex_hand_hover.value:
                    _h = Hexagon(h.center, h.size+2, h.hex, h.color)
                    pygame.draw.lines(
                        self.display, self.WHITE, True, _h.points, 4)
                    break
        if self.p2.hex_hand_selected:
            for h in self.p2.hexagons_hand[::-1]:
                if h.value == self.p2.hex_hand_selected.value:
                    _h = Hexagon(h.center, h.size+2, h.hex, h.color)
                    pygame.draw.lines(
                        self.display, self.PALETTE[3], True, _h.points, 4)
                    break

    def draw_menu_arrow(self):
        r = self.rect_arrow_region
        # collidepoint = rect.collidepoint(self.MOUSE_POS)

        pygame.draw.rect(self.display, self.WHITE,
                         r, 1)
        size = r.h*40/100

        top_btn = pygame.Rect(0, 0, size, size)
        bottom_btn = pygame.Rect(0, 0, size, size)
        left_btn = pygame.Rect(0, 0, size, size)
        right_btn = pygame.Rect(0, 0, size, size)

        top_btn.center = (r.centerx, r.centery-size/2-2)
        bottom_btn.center = (r.centerx, r.centery+size/2+2)
        left_btn.center = (r.centerx-size-2, r.centery)
        right_btn.center = (r.centerx+size+2, r.centery)

        if self.LEFT_CLICK_KEY:
            if top_btn.collidepoint(self.MOUSE_POS):
                self.handle_arrow_btn('U')
            if bottom_btn.collidepoint(self.MOUSE_POS):
                self.handle_arrow_btn('D')
            if left_btn.collidepoint(self.MOUSE_POS):
                self.handle_arrow_btn('L')
            if right_btn.collidepoint(self.MOUSE_POS):
                self.handle_arrow_btn('R')

        pygame.draw.rect(self.display, self.PALETTE[2], top_btn, 0)
        pygame.draw.rect(self.display, self.PALETTE[2], bottom_btn, 0)
        pygame.draw.rect(self.display, self.PALETTE[2], left_btn, 0)
        pygame.draw.rect(self.display, self.PALETTE[2], right_btn, 0)
        self.draw_text('U', 15,  top_btn.centerx, top_btn.centery,
                       self.PALETTE[0], self.font_name_default)
        self.draw_text('D', 15,  bottom_btn.centerx,
                       bottom_btn.centery, self.PALETTE[0], self.font_name_default)
        self.draw_text('L', 15,  left_btn.centerx,
                       left_btn.centery, self.PALETTE[0], self.font_name_default)
        self.draw_text('R', 15,  right_btn.centerx,
                       right_btn.centery, self.PALETTE[0], self.font_name_default)

    def handle_arrow_btn(self, btn):
        if btn == 'L':
            self.LEFT_KEY = True
        if btn == 'R':
            self.RIGHT_KEY = True
        if btn == 'U':
            self.UP_KEY = True
        if btn == 'D':
            self.DOWN_KEY = True

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
        pass

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

        if self.possible_placements:
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
                    break

    def handle_left_mouse_click(self):
        self.possible_placements = None
        if self.p1.hex_hand_hover and self.current_player.id == 'p1':
            self.p1.hex_hand_selected = self.p1.hex_hand_hover
            self.possible_placements = get_possible_placements()

    def handle_right_mouse_click(self):
        self.possible_placements = None
        if self.p2.hex_hand_hover and self.current_player.id == 'p2':
            self.p2.hex_hand_selected = self.p2.hex_hand_hover
            self.possible_placements = get_possible_placements()
