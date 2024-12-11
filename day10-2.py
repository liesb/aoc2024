import numpy as np

###
# this counts the number of trails leading up to a nine from each tailhead
###


DIRECTIONS =[
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0)
]

def read_data(fn):
    # with open(fn, 'r') as f:
    #     return np.array([
    #         list(l.replace("\n", ""))
    #         for l in f.readlines()
    #     ]).astype(int)

    with open(fn, 'r') as f:
        a = np.array([
            list(l.replace("\n", ""))
            for l in f.readlines()
        ])

        return np.where(a == ".", -10, a).astype(int)


def add_tuples(x, y):
    return (x[0] + y[0], x[1] + y[1])


def still_on_map(pos, nr, nc):
    return (
        (pos[0] < nr) &
        (pos[0] >= 0) &
        (pos[1] < nc) &
        (pos[1] >= 0)
    )


def add_count_paths(terrain, count_map, pos, nr, nc):
    current_value = terrain[pos]
    # print("current value = {}".format(current_value))
    if current_value == 9:
        count_map[pos] = 1
        return 1
    else:
        count = 0
        next_value_up = current_value + 1
        # print("next value up = {}".format(next_value_up))
        for d in DIRECTIONS:
            new_pos = add_tuples(pos, d)
            # print("new pos = {}".format(new_pos))
            if still_on_map(new_pos, nr, nc):  
                new_pos_value = terrain[new_pos]
                # print("new pos value = {}".format(new_pos_value))
                if new_pos_value == next_value_up:
                    if count_map[new_pos] > -1:
                        count += count_map[new_pos]
                    else:
                        # print("HERE")
                        new_pos_path_count = add_count_paths(terrain, count_map, new_pos, nr, nc)
                        count += new_pos_path_count
        count_map[pos] = count
        return count


def main(fn):
    terrain = read_data(fn)
    print(terrain)
    nr, nc = terrain.shape
    count_map = np.ones_like(terrain) * (-1)
    # find zeros on map
    zero_positions = list(zip(*(np.where(terrain == 0))))
    print(zero_positions)
    # assert False
    # loop over zeros
    num_paths = 0
    for zero_pos in zero_positions:
        print("====")
        print("pos = {}".format(zero_pos))
        x = add_count_paths(terrain, count_map, zero_pos, nr, nc)
        num_paths += x
        print("num paths = {}".format(x))
    # FOR TESTING num_paths += add_count_paths(terrain, count_map, (2, 6), nr, nc)
    print(num_paths)
    # print(count_map * (terrain == 0).astype(int)) 
    # print(count_map)
    



if __name__ == "__main__":
    main("day10-input.txt")