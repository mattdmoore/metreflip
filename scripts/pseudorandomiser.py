from sys import argv
from rhythm_parameters import *
from copy import deepcopy


def select_rhythms(participant_id):
    bitmask = get_bitmask(participant_id, 4)
    inverse = get_bitmask((participant_id ^ 0xF), 4)

    pool = [(259, 76),  # targets
            (135, 82),
            (196, 57),
            (133, 148),

            (195, 70),  # foils
            (94, 66),
            (31, 36),
            (29, 27)]

    blocks = {key: apply_bitmask(pool, mask) for key, mask in enumerate((bitmask, inverse))}

    for b in blocks.values():
        for i, (key, val) in enumerate(b.items()):
            if not val['foil']:
                val['metre'] = 3 + ((participant_id + i) % 2)
                val['invert'] = bool((participant_id + i // 2) % 2)
            else:
                val['invert'] = False
            print(i, key, val)

    blocks[2] = deepcopy({**blocks[0], **blocks[1]})
    for i, (key, val) in enumerate(blocks[2].items()):
        if ((i // 4) % 2 and (participant_id + i) % 2) or not val['foil']:
            val['invert'] = not val['invert']
        print(i, key, val)
    return blocks


def get_bitmask(x, n):
    return bin(x % n ** 2)[2:].zfill(n) * 2


def apply_bitmask(pool, bitmask):
    return {pool[i][int(val)]: RHYTHM_PARAMETERS[pool[i][int(val)]] for i, val in enumerate(bitmask)}


def main(participant_id):
    return select_rhythms(participant_id)


if __name__ == '__main__':
    if any(argv[1:]):
        main(int(argv[1]))
    else:
        [main(p) for p in range(16)]
