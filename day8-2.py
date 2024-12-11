import numpy as np


def read_input(fn):
    with open(fn, 'r') as f:
        return np.array(
            [
                list(line.replace("\n", ""))
                for line in f.readlines()
            ]
        )
    
def add_tuples(tup1, tup2):
    return tuple(x+y for x, y in zip(tup1, tup2))


def subtract_tuples(tup1, tup2):
    # tup1 - tup 2
    return tuple(x - y for x, y in zip(tup1, tup2))


def still_on_maze(pos, X, Y):
    x, y = pos
    return (
        (x > -1) and (x < X) and 
        (y > -1) and (y < Y)
    )


def add_antinodes(map, uv, antinode_map):
    locations = list(zip(*np.where(map == uv)))
    X, Y = map.shape
    nl = len(locations)
    for i in range(nl - 1):
        tup1 = locations[i]
        antinode_map[tup1] = 1
        for j in range(i+1, nl):
            tup2 = locations[j]
            antinode_map[tup2] = 1
            # find slope def
            slope = subtract_tuples(tup2, tup1)
            # along first point
            potential = tup1
            while True:
                potential = subtract_tuples(potential, slope)
                if still_on_maze(potential, X, Y):
                    antinode_map[potential] = 1 
                else:
                    break
            # along second point
            potential = tup2
            while True:
                potential = add_tuples(potential, slope)
                if still_on_maze(potential, X, Y):
                    antinode_map[potential] = 1
                else:
                    break


def main(fn):
    map = read_input(fn)
    # print(map)
    unique_vals = [
        x
        for x in np.unique(map)
        if x != '.'
    ]
    # print(unique_vals)
    antinode_map = np.zeros_like(map, dtype=np.int32)
    for uv in unique_vals:
        add_antinodes(map, uv, antinode_map)
    # print(antinode_map)
    print(antinode_map.sum())



if __name__ == "__main__":
    main("day8-input.txt")