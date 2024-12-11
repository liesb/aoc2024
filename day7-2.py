import numpy as np
import itertools

def read_input(fn):
    with open(fn) as f:
        tests = {
            int(l.split(":")[0]): [
                int(x)
                for x in l.replace("\n", "").split(": ")[1].split(" ")
            ]
            for l in f.readlines()
        }  
    return tests


def possible_at_all(goal, vals):
    n_vals = len(vals)
    OPERATIONS = ["+", "*", "CONC"]
    for operators in itertools.product(*([OPERATIONS]*(n_vals-1))):
        res = vals[0]
        for i, (operator, value)in enumerate(zip(operators, vals[1:])):
            if operator == "+":
                res += value
            elif operator == "*":
                res *= value
            else:
                res = int(
                    str(res) + str(value)
                ) 
            if (i == n_vals - 2) and (res == goal):
                return True
            if (i < n_vals - 2) and (res > goal):
                break
    return False


def main(fn):
    tests = read_input(fn)
    res = 0
    for goal, vals in tests.items():
        if possible_at_all(goal, vals):
            print("adding {}".format(goal))
            res += goal
    print(res)


if __name__ == "__main__":
    main("day7-input.txt")