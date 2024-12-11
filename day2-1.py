import numpy as np
import pandas as pd

def read_input(fn):
    with open(fn) as f:
        lines = [
            np.array(
                l.replace("\n", "").split(" ")
            ).astype(int)
            for l in f.readlines()
        ]
    return lines


def check_safety(line):
    d = np.diff(line)
    return (
        (
            (d > 0).all() or (d < 0).all()
        )
        &
        (np.abs(d) <= 3).all()
    )


def main(fn):
    lines = read_input(fn)
    print(
        np.array([
            check_safety(l)
            for l in lines
        ]).sum()
    )
    



if __name__ == "__main__":
    main("day2-input.txt")