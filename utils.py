from string import Template


def validate_index(index):
    if type(index) is not int:
        raise Exception(Template('invalid index $index: not an int').substitute(index=str(index)))
    if index < 0 or index > 23:
        raise Exception(Template('index out of bounds: $index').substitute(index=str(index)))


def validate_letter(letter):
    if type(letter) is not str:
        raise Exception(Template('invalid letter $letter: not a str').substitute(letter=letter))
    if len(letter) != 1:
        raise Exception(Template('letter must have length 1: $letter').substitute(letter=letter))


def index_to_letter(index):
    validate_index(index)
    return chr(index + ord('A'))


def letter_to_index(letter):
    validate_letter(letter)
    return ord(letter) - ord('A')


def get_edge_buddy_index(index, edge_index_groups):
    validate_index(index)
    for edge in edge_index_groups:
        if edge[0] == index:
            return edge[1]
        if edge[1] == index:
            return edge[0]


def get_corner_buddy_indices(index, corner_index_groups):
    validate_index(index)
    for corner in corner_index_groups:
        if corner[0] == index:
            return corner[1], corner[2]
        if corner[1] == index:
            return corner[0], corner[2]
        if corner[2] == index:
            return corner[0], corner[1]


def print_cycles(cycles):
    cycles_with_pipe = cycles[:]
    for index, cycle in enumerate(cycles_with_pipe):
        if index == 0:
            continue
        cycle[0] = '|' + str(cycle[0])

    flattened_cycles_with_pipe = [item for sublist in cycles_with_pipe for item in sublist]
    num_pairs = len(flattened_cycles_with_pipe) // 2
    has_remainder = len(flattened_cycles_with_pipe) % 2

    str_arr = []
    for i in range(num_pairs):
        str_arr.extend([str(el) for el in flattened_cycles_with_pipe[2*i: 2*i + 2]])
        str_arr.append(' ')
    if has_remainder:
        str_arr.append(str(flattened_cycles_with_pipe[-1]))
    print(''.join(str_arr))
