from string import Template
import utils
import random

NUM_EDGE_STICKERS = 24
NUM_CORNER_STICKERS = 24

EDGE_LETTER_GROUPS = [
    'AQ',
    'BM',
    'CI',
    'DE',
    'JP',
    'NT',
    'RH',
    'FL',
    'KU',
    'VO',
    'WS',
    'GX',
]
CORNER_LETTER_GROUPS = [
    'AER',
    'BQN',
    'CMJ',
    'DIF',
    'KPV',
    'OTW',
    'GLU',
    'HSX',
]
EDGE_INDEX_GROUPS = [(utils.letter_to_index(edge[0]), utils.letter_to_index(edge[1])) for edge in EDGE_LETTER_GROUPS]
CORNER_INDEX_GROUPS = [(
    utils.letter_to_index(corner[0]),
    utils.letter_to_index(corner[1]),
    utils.letter_to_index(corner[2])) for corner in CORNER_LETTER_GROUPS]

EDGE_FACE_PERMUTATIONS = {
    'U': ['ABCD', 'EQMI'],
    'L': ['EFGH', 'DLXR'],
    'F': ['IJKL', 'CPUF'],
    'R': ['MNOP', 'BTVJ'],
    'B': ['QRST', 'AHWN'],
    'D': ['UVWX', 'KOSG'],
}
CORNER_FACE_PERMUTATIONS = {
    'U': ['ABCD', 'EQMI', 'RNJF'],
    'L': ['EFGH', 'DLXR', 'AIUS'],
    'F': ['IJKL', 'CPUF', 'DMVG'],
    'R': ['MNOP', 'BTVJ', 'CQWK'],
    'B': ['QRST', 'AHWN', 'BEXO'],
    'D': ['UVWX', 'KOSG', 'LPTH'],
}

EDGE_BUFFER_STICKER_INDEX = utils.letter_to_index('U')
EDGE_BUFFER_BUDDY_INDEX = utils.get_edge_buddy_index(EDGE_BUFFER_STICKER_INDEX, EDGE_INDEX_GROUPS)
CORNER_BUFFER_STICKER_INDEX = utils.letter_to_index('E')
CORNER_BUFFER_BUDDY_INDICES = utils.get_corner_buddy_indices(CORNER_BUFFER_STICKER_INDEX, CORNER_INDEX_GROUPS)


class Cube:
    def __init__(self):
        self.edges = [i for i in range(NUM_EDGE_STICKERS)]
        self.corners = [i for i in range(NUM_CORNER_STICKERS)]

    def print_edges(self):
        print([utils.index_to_letter(sticker) for sticker in self.edges])

    def print_corners(self):
        print([utils.index_to_letter(sticker) for sticker in self.corners])

    def print(self):
        print('edges: ')
        self.print_edges()
        print('corners: ')
        self.print_corners()

    # *_cycle_letters is a string representing cycle notation (using letters)
    def __apply_cycle_edges(self, edge_cycle_letters):
        edge_cycle_indices = [utils.letter_to_index(letter) for letter in edge_cycle_letters]
        edge_cycle_indices.append(edge_cycle_indices[0])
        current_sticker = self.edges[edge_cycle_indices[0]]
        for i in range(len(edge_cycle_letters)):
            next_sticker = self.edges[edge_cycle_indices[i + 1]]
            self.edges[edge_cycle_indices[i + 1]] = current_sticker
            current_sticker = next_sticker

    def __apply_cycle_corners(self, corner_cycle_letters):
        corner_cycle_indices = [utils.letter_to_index(letter) for letter in corner_cycle_letters]
        corner_cycle_indices.append(corner_cycle_indices[0])
        current_sticker = self.corners[corner_cycle_indices[0]]
        for i in range(len(corner_cycle_letters)):
            next_sticker = self.corners[corner_cycle_indices[i + 1]]
            self.corners[corner_cycle_indices[i + 1]] = current_sticker
            current_sticker = next_sticker

    def __apply_move(self, move):
        edge_permutations = EDGE_FACE_PERMUTATIONS[move]
        corner_permutations = CORNER_FACE_PERMUTATIONS[move]
        for edge_permutation in edge_permutations:
            self.__apply_cycle_edges(edge_permutation)
        for corner_permutation in corner_permutations:
            self.__apply_cycle_corners(corner_permutation)

    def apply_scramble(self, scramble_moves_list):
        for move in scramble_moves_list:
            if len(move) == 1:
                self.__apply_move(move)
            elif len(move) == 2:
                if move[1] == '2':
                    self.__apply_move(move[0])
                    self.__apply_move(move[0])
                elif move[1] == "'":
                    self.__apply_move(move[0])
                    self.__apply_move(move[0])
                    self.__apply_move(move[0])
                else:
                    raise Exception(Template('invalid move "$move"').substitute(move=str(move)))
            else:
                raise Exception(Template('invalid move "$move"').substitute(move=str(move)))

    def get_edge_cycles(self, hint_cycle_starts):
        unvisited_stickers = set()
        for i in range(NUM_EDGE_STICKERS):
            unvisited_stickers.add(i)

        edge_cycles = []
        is_buffer_cycle = True

        while len(unvisited_stickers) != 0:
            current_cycle = []

            current_sticker = EDGE_BUFFER_STICKER_INDEX if is_buffer_cycle else \
                random.sample(hint_cycle_starts, 1)[0] if len(hint_cycle_starts) else \
                random.sample(unvisited_stickers, 1)[0]
            if not is_buffer_cycle or current_sticker != EDGE_BUFFER_STICKER_INDEX:
                current_cycle.append(current_sticker)
            while current_sticker in unvisited_stickers:
                current_sticker_buddy = utils.get_edge_buddy_index(current_sticker, EDGE_INDEX_GROUPS)
                unvisited_stickers.remove(current_sticker)
                unvisited_stickers.remove(current_sticker_buddy)

                if current_sticker in hint_cycle_starts:
                    hint_cycle_starts.remove(current_sticker)
                if current_sticker_buddy in hint_cycle_starts:
                    hint_cycle_starts.remone(current_sticker_buddy)

                current_sticker = self.edges[current_sticker]
                is_current_sticker_on_buffer_piece = current_sticker == EDGE_BUFFER_STICKER_INDEX or \
                    current_sticker == EDGE_BUFFER_BUDDY_INDEX
                if not is_buffer_cycle or not is_current_sticker_on_buffer_piece:
                    current_cycle.append(current_sticker)

            is_solved_cycle = len(current_cycle) == 2 and current_cycle[0] == current_cycle[1]
            if len(current_cycle) and not is_solved_cycle:
                edge_cycles.append(current_cycle)
            if is_buffer_cycle:
                is_buffer_cycle = False

        letter_edge_cycles = [[utils.index_to_letter(el) for el in cycle] for cycle in edge_cycles]
        return letter_edge_cycles

    def get_corner_cycles(self, hint_cycle_starts):
        unvisited_stickers = set()
        for i in range(NUM_CORNER_STICKERS):
            unvisited_stickers.add(i)

        corner_cycles = []
        is_buffer_cycle = True

        while len(unvisited_stickers) != 0:
            current_cycle = []

            current_sticker = CORNER_BUFFER_STICKER_INDEX if is_buffer_cycle else \
                random.sample(hint_cycle_starts, 1)[0] if len(hint_cycle_starts) else \
                random.sample(unvisited_stickers, 1)[0]
            if not is_buffer_cycle or current_sticker != CORNER_BUFFER_STICKER_INDEX:
                current_cycle.append(current_sticker)
            while current_sticker in unvisited_stickers:
                current_sticker_buddy_indices = utils.get_corner_buddy_indices(current_sticker, CORNER_INDEX_GROUPS)
                unvisited_stickers.remove(current_sticker)
                for buddy_index in current_sticker_buddy_indices:
                    unvisited_stickers.remove(buddy_index)

                if current_sticker in hint_cycle_starts:
                    hint_cycle_starts.remove(current_sticker)
                for buddy_index in current_sticker_buddy_indices:
                    if buddy_index in hint_cycle_starts:
                        hint_cycle_starts.remone(buddy_index)

                current_sticker = self.corners[current_sticker]
                is_current_sticker_on_buffer_piece = current_sticker == CORNER_BUFFER_STICKER_INDEX or \
                    current_sticker in CORNER_BUFFER_BUDDY_INDICES
                if not is_buffer_cycle or not is_current_sticker_on_buffer_piece:
                    current_cycle.append(current_sticker)

            is_solved_cycle = len(current_cycle) == 2 and current_cycle[0] == current_cycle[1]
            if len(current_cycle) and not is_solved_cycle:
                corner_cycles.append(current_cycle)
            if is_buffer_cycle:
                is_buffer_cycle = False

        letter_corner_cycles = [[utils.index_to_letter(el) for el in cycle] for cycle in corner_cycles]
        return letter_corner_cycles
