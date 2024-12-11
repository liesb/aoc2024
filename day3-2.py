import re
import numpy as np

def read_input(fn):
    with open(fn, "r") as f:
        return f.readlines()


def get_valid_instructions(l):
    return re.findall("mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)", l)


def parse_instrutions(list_of_instr):
    res = 0
    on = True
    for i in range(len(list_of_instr)):
        instr = list_of_instr[i]
        if instr == "do()":
            on = True
        elif instr == "don't()":
            on = False
        elif on:
            res += get_mul_result(instr)
    return res

def get_mul_result(m):
    return np.prod(
        np.array(
            m
            .replace("mul(", "")
            .replace(")", "")
            .split(",")
        ).astype(int)
    )


def flatten_list_of_lists(ll):
    return [ x for l in ll for x in l]
 

def main(fn):
    lines = read_input(fn)
    # lines = [
    #     "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    # ]
    valid_instructions = flatten_list_of_lists(
        [
            get_valid_instructions(line)
            for line in lines
        ])
    print(valid_instructions)
    print(parse_instrutions(valid_instructions))
        



if __name__ == "__main__":
    main("day3-input.txt")