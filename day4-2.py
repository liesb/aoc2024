import numpy as np
import re

look_for = ["MAS", "SAM"]


def read_data(fn):
    # return the np array of individual letter
    with open(fn, "r") as f:
        return np.array(
            [
                list(l.replace("\n", ""))
                for l in f.readlines()
            ]
        )
                   

def main(fn):
    puzzle = read_data(fn)
    p0, p1 = puzzle.shape
    # print(p0, p1)
    # print("---")
    count = 0
    for i in range(p0 - 2):
        for j in range(p1 - 2):
            # print(i,j)
            submat = puzzle[i:i+3, j:j+3]
            word1 = "".join(list(np.diag(submat)))
            word2 = "".join(list(np.diag(submat[:, ::-1])))
            if (
                (word1 in look_for)
                and
                (word2 in look_for)
            ):
                count += 1
    print(count)
    
        

if __name__ == "__main__":
    main("day4-input.txt")