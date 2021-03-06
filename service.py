import requests
PORT = 3030
URL = f'http://localhost:{PORT}/hive_api'


class Player():
    def __init__(self, id, name, non_placed_insects, number_of_moves, queen_bee_placed, game_over, type):
        self.id = id
        self.name = name
        self.non_placed_insects = non_placed_insects
        self.number_of_moves = number_of_moves
        self.queen_bee_placed = queen_bee_placed
        self.hexagons_hand = None
        self.hex_hand_selected = None
        self.hex_hand_hover = None
        self.game_over = game_over
        self.type = type


def play_ai():
    res = requests.post(f'{URL}/ai/play').json()
    status_code = res['status_code']
    msg = res['msg']
    if status_code == 200:
        return {'success': True, 'msg': msg, 'status_code': status_code}
    elif status_code == 400:
        return {'success': False, 'msg': msg, 'status_code': status_code}



def get_game_stats():
    res = requests.post(f'{URL}/game/game_stats')
    stats = res.json()

    current_player_id = stats['current_player_id']
    hive = stats['hive']
    players_info = stats['players_info']

    status_code = stats['status_code']

    p1_stats = players_info['p1']
    p2_stats = players_info['p2']

    p1 = Player(p1_stats['id'], p1_stats['name'], p1_stats['non_placed_insects'],
                p1_stats['number_of_moves'], p1_stats['queen_bee_placed'], p1_stats['game_over'], p1_stats['type_player'])

    p2 = Player(p2_stats['id'], p2_stats['name'], p2_stats['non_placed_insects'],
                p2_stats['number_of_moves'], p2_stats['queen_bee_placed'], p2_stats['game_over'], p2_stats['type_player'])

    return [current_player_id, p1, p2, hive]


def get_queen_surrounded():
    res = requests.post(f'{URL}/insect/queen_surrounded').json()
    status_code = res['status_code']
    msg = res['msg']
    if status_code == 200:
        return {'success': False, 'msg': res['msg'], 'status_code': status_code}
    elif status_code == 201:
        return {'success': True, 'msg': res['msg'], 'status_code': status_code}
    elif status_code == 202:
        return {'success': True, 'msg': res['msg'], 'status_code': status_code}
    elif status_code == 203:
        return {'success': True, 'msg': res['msg'], 'status_code': status_code}


def get_possible_placements(type):
    res = requests.post(
        f'{URL}/insect/get_possible_placements', json={'type': type}).json()
    status_code = res['status_code']
    if status_code == 400:
        return {'success': False, 'msg': res['msg'], 'status_code': status_code}
    elif status_code == 401:
        return {'success': False, 'msg': res['msg'], 'status_code': status_code}
    elif status_code == 200:
        return {'success': True, 'placements': res['placements'], 'status_code': status_code}


def get_possible_moves(type, id, hex):
    res = requests.post(
        f'{URL}/insect/get_possible_moves', json={'type': type, 'id': id, 'hexagon': hex}).json()
    status_code = res['status_code']
    if status_code == 400:
        return {'success': False, 'msg': res['msg']}
    elif status_code == 200:
        return {'success': True, 'moves': res['moves']}


def new_game(mode, level):
    requests.post(f'{URL}/game/new_game', json={'mode': mode, 'level': level})


def reset_game():
    requests.post(f'{URL}/game/reset_game')


def place_insect(type, hexagon):
    res = requests.post(f'{URL}/insect/place_insect',
                        json={'type': type, 'hexagon': hexagon}).json()
    status_code = res['status_code']
    if status_code == 400:
        return {'success': False, 'msg': res['msg']}
    elif status_code == 200:
        return {'success': True, 'insect': res['insect']}


def move_insect(insect, hexagon_ori, hexagon_end):
    type = insect[0]
    id = insect[1]
    lvl = insect[5]
    res = requests.post(f'{URL}/insect/move_insect',
                        json={'type': type, 'id': id, 'lvl': lvl, 'hexagon_ori': hexagon_ori, 'hexagon_end': hexagon_end}).json()
    status_code = res['status_code']
    if status_code == 400:
        return {'success': False, 'msg': res['msg']}
    elif status_code == 200:
        return {'success': True, 'insect': res['insectRes']}


def get_last_insect(hexagon):
    res = requests.post(f'{URL}/insect/get_last',
                        json={'hexagon': hexagon}).json()
    status_code = res['status_code']
    if status_code == 400:
        return {'success': False, 'msg': res['msg']}
    elif status_code == 200:
        return {'success': True, 'insect': res['insect']}
