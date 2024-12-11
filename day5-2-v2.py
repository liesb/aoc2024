import numpy as np
import pandas as pd


def read_data(fn):
    rules = []
    changes = []
    doing_rules = True
    with open(fn, "r") as f:
        for l in f.readlines():
            if l == "\n":
                doing_rules = False
            elif doing_rules:
                rules += [
                    l.replace("\n", "").split("|")
                ]
            else:
                changes += [
                    [
                        int(i)
                        for i in l.replace("\n", "").split(",")
                    ]
                ]
    return np.array(rules).astype(int), changes



def check_right_order(change, rules):
    # for each page that is changed, find all the rules that apply, check them
    for ic, c in enumerate(change):
        lhs = np.where(rules[:, 0] == c)[0]
        rhs = np.where(rules[:, 1] == c)[0]
        for l in lhs:
            if rules[l, 1] in change:
                io = change.index(rules[l, 1])
                if io < ic:
                    return False
        for r in rhs:
            if rules[r, 0] in change:
                io = change.index(rules[r, 0])
                if ic < io:
                    return False
    return True


def fix_order(change, rules):
    # find only rules that apply to changes on both sides
    applicable_rules = rules[
        [
            (l in change) & (r in change)
            for l, r in zip(rules[:,0], rules[:,1])
        ]
    ].tolist()
    # matrix for rules
    df = pd.DataFrame(0, index=change, columns=change)
    for l, r in applicable_rules:
        df.loc[l,r] = 1
    A = df.values.astype(int)
    A_power = df.values.astype(int)
    while True:
        A_new = np.dot(A_power, A)
        A_new = np.minimum(A_new, 1)
        if (A_new == A_power).all():
            break
        else:
            A_power = A_new
    sums_l = np.sum(A, axis=-1)
    argsort = np.argsort(-sums_l)
    return np.array(change)[argsort]




def find_midpoint(arr):
    return arr[int(np.floor(len(arr)/2))]


def main(fn):
    rules, changes = read_data(fn)
    wrong_order_mask = [
        not check_right_order(c, rules)
        for c in changes
    ]
    fixed_wrong_orders = [
        fix_order(c, rules)
        for c, o in zip(changes, wrong_order_mask)
        if o
    ]
    print("===")
    print(fixed_wrong_orders)
    fixed_wrong_order_midpoints = np.array([
        find_midpoint(c)
        for c in fixed_wrong_orders
    ]).astype(int)
    print(fixed_wrong_order_midpoints)
    print(fixed_wrong_order_midpoints.sum())
    
        

if __name__ == "__main__":
    main("day5-input.txt")