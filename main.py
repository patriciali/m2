from cube import Cube
import utils

##################################################
scramble = '''
F2 U F R L' B' L2 F L B' D2 F2 U' F2 D R2 D2 L2 D' L2
'''
hint_edge_cycle_starts_list = 'OAD'
hint_corner_cycle_starts_list = 'DJ'
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
