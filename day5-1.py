import numpy as np


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


def find_midpoint(arr):
    return arr[int(np.floor(len(arr)/2))]


def main(fn):
    rules, changes = read_data(fn)
    # get dict of whether a page is involved in a change
    # left_rule, right_rule = get_rule_indexers(rules, changes)
    # 
    right_order_mask = [
        check_right_order(c, rules)
        for c in changes
    ]
    right_order_midpoints = np.array([
        find_midpoint(c)
        for c, o in zip(changes, right_order_mask)
        if o
    ]).astype(int)
    print(right_order_midpoints.sum())
    
        

if __name__ == "__main__":
    main("day5-input.txt")