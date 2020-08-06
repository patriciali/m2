from cube import Cube
import utils

##################################################
scramble = '''
F2 R2 D' L2 U2 L2 R2 U B2 F U' R' F2 U2 R U' B L2 U' R'
'''
hint_edge_cycle_starts_list = 'ABCJ'
hint_corner_cycle_starts_list = 'WC'
##################################################

scramble_arr = scramble.strip().split(' ')
hint_edge_cycle_starts = set([utils.letter_to_index(letter) for letter in hint_edge_cycle_starts_list])
hint_corner_cycle_starts = set([utils.letter_to_index(letter) for letter in hint_corner_cycle_starts_list])

cube = Cube()
cube.apply_scramble(scramble_arr)

edge_cycles = cube.get_edge_cycles(hint_edge_cycle_starts)
print('edges: ')
utils.print_cycles(edge_cycles)

corner_cycles = cube.get_corner_cycles(hint_corner_cycle_starts)
print('corners: ')
utils.print_cycles(corner_cycles)
