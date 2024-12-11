import re
import numpy as np

def read_input(fn):
     with open(fn, "r") as f:
        return f.readlines()


def get_valid_muls(l):
    return re.findall("mul\(\d{1,3},\d{1,3}\)", l)


def get_mul_result(m):
    return np.prod(
        np.array(
            m
            .replace("mul(", "")
            .replace(")", "")
            .split(",")
        ).astype(int)
    )


def main(fn):
    lines = read_input(fn)
    # lines = [
    #     "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))",
    #     "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    # ]
    valid_muls =[
        get_valid_muls(line)
        for line in lines
    ]
    print(np.sum(np.array(
        [
            get_mul_result(m)
            for vm_list in valid_muls
            for m in vm_list
        ]
    )))
        



if __name__ == "__main__":
    main("day3-input.txt")