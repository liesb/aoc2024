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


def is_safe(line):
    d = np.diff(line)
    return (
        (
            (d > 0).all() or (d < 0).all()
        )
        &
        (np.abs(d) <= 3).all()
    )


def check_safety_with_dampening(line):
    if is_safe(line):
        return True
    
    else:
        for i in range(len(line)):
            if is_safe(np.delete(line, i)):
                return True
    
        return False
        


def main(fn):
    lines = read_input(fn)
    print(
        np.array([
            check_safety_with_dampening(l)
            for l in lines
        ]).sum()
    )
    



if __name__ == "__main__":
    main("day2-input.txt")