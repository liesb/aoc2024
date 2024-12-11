import numpy as np
import pandas as pd


def read_data(fn):
    with open(fn, 'r') as f:
        return f.readline().strip()


def main(fn):
    data = read_data(fn)
    print(len(data))
    lengths = np.array(
        list(data)
    ).astype(int)
    startpositions = np.array(
        [0] + np.cumsum(lengths).tolist()
    ).astype(int)
    print(data)
    print(lengths)
    print(startpositions)
    
    filled_spots = {
        k: [int(i/2), v]  #id, length
        for i, (k, v) in enumerate(zip(startpositions, lengths))
        if np.mod(i, 2) == 0
    }

    open_spots = {
        k: v
        for i, (k, v) in enumerate(zip(startpositions, lengths))
        if np.mod(i, 2) == 1 
    }
    print(filled_spots)
    print(open_spots)

    # move shit around
    for id in np.arange(int(len(data)/2)+1)[::-1]:
        # print(id)
        current_pos, current_len = [
            (k, v2)
            for k, (v1, v2) in filled_spots.items()
            if v1 == id
        ][0]
        # print(current_len)
        # print(current_pos)
        better_positions = np.array([
            k
            for k, i in open_spots.items()
            if (i >= current_len) and (k < current_pos)
        ])
        if len(better_positions) > 0:
            best_pos = np.min(better_positions)
            print("moving {} to spot {}".format(id, best_pos))
            filled_spots[best_pos] = [id, current_len]
            # update open spots - don't need to deal with stuff left open by moving
            # do need to update - this is not optimal
            open_spots[best_pos + current_len] = open_spots[best_pos] - current_len
            open_spots[best_pos] = 0
            del filled_spots[current_pos]
        
    # get checksum
    checksum = 0
    for k, (p, l) in filled_spots.items():
        checksum += p * np.arange(k, k+l).sum()
    # print(filled_spots.items())
    print(checksum)


if __name__ == "__main__":
    main("day9-input.txt")