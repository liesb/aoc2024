import numpy as np
import re


def read_data(fn):
    # return the np array of individual letter
    with open(fn, "r") as f:
        return np.array(
            [
                list(l.replace("\n", ""))
                for l in f.readlines()
            ]
        )


def get_horizontal_count(p):
    return np.array([
        len(
            re.findall(
                "XMAS",
                "".join(list(p[line]))
            )
        )
        for line in range(p.shape[0])
    ]).sum()


def get_horizontal_reverse_count(p):
    return get_horizontal_count(p[:,::-1])


def get_vertical_count(p):
    return get_horizontal_count(p.T)


def get_vertical_reverse_count(p):
    return get_horizontal_count(p.T[:,::-1])


def get_diagonal_down_count(p):
    p0, p1 = p.shape
    count = 0
    for i in range(p0):
        count += (
            len(
                re.findall(
                    "XMAS",
                    "".join(list(np.diag(p, -i)))
                )
            )
        )
    for i in range(1, p1):
        count += (
            len(
                re.findall(
                    "XMAS",
                    "".join(list(np.diag(p, i)))
                )
            )
        )
    return count


def get_diagonal_down_reverse_count(p):
    return get_diagonal_down_count(p[::-1, ::-1])


def get_diagonal_up_count(p):
    return get_diagonal_down_count(p[::-1,:])


def get_diagnotal_up_reverse_count(p):
    return get_diagonal_down_reverse_count(p[::-1, :])
                         

def main(fn):
    puzzle = read_data(fn)
    # print(puzzle)
    count = 0
    count += get_horizontal_count(puzzle)
    count += get_horizontal_reverse_count(puzzle)
    count += get_vertical_count(puzzle)
    count += get_vertical_reverse_count(puzzle)
    count += get_diagonal_down_count(puzzle)
    count += get_diagonal_down_reverse_count(puzzle)
    count += get_diagonal_up_count(puzzle)
    count += get_diagnotal_up_reverse_count(puzzle)
    print(count)
        

if __name__ == "__main__":
    main("day4-input.txt")