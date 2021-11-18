import requests
PORT = 3030
URL = f'http://localhost:{PORT}/hive_api'


class Player():
    def __init__(self, id, name, non_placed_insects, number_of_moves, queen_bee_placed):
        self.id = id
        self.name = name
        self.non_placed_insects = non_placed_insects
        self.number_of_moves = number_of_moves
        self.queen_bee_placed = queen_bee_placed
        self.hexagons_hand = []
        self.hex_hand_selected = None
        self.hex_hand_hover = None


def get_game_stats():
    res = requests.post(f'{URL}/game/game_stats')
    stats = res.json()

    current_player_id = stats['current_player_id']
    hive = stats['hive']
    players_info = stats['players_info']

    p1_stats = players_info['p1']
    p2_stats = players_info['p2']

    p1 = Player(p1_stats['id'], p1_stats['name'], p1_stats['non_placed_insects'],
                p1_stats['number_of_moves'], p1_stats['queen_bee_placed'])

    p2 = Player(p2_stats['id'], p2_stats['name'], p2_stats['non_placed_insects'],
                p2_stats['number_of_moves'], p2_stats['queen_bee_placed'])

    return [current_player_id, p1, p2, hive]


def get_possible_placements():
    res = requests.post(f'{URL}/insect/get_possible_placements')
    possible_placements = res.json()['placements']
    return possible_placements


def place_insect(type, hexagon):
    res = requests.post(f'{URL}/insect/place_insect',
                        json={'type': type, 'hexagon': hexagon})

    data = res.json()

    try:
        msg = data['msg']
        return msg
    except:
        insect = data['insect']
        return insect