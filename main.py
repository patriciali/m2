from cube import Cube
import utils

##################################################
scramble = '''
U2 B' U2 L2 R2 F2 D2 R2 F2 U2 R F' L' D B R U B R' U'
'''
hint_edge_cycle_starts_list = 'LAT'
hint_corner_cycle_starts_list = ''
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
