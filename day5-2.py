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


def fix_order(change, rules):
    # find only rules that apply to changes on both sides
    applicable_rules = rules[
        [
            (l in change) & (r in change)
            for l, r in zip(rules[:,0], rules[:,1])
        ]
    ].tolist()
    # res = applicable_rules.pop(0)
    # while len(applicable_rules) > 0:
    #     to_pop = []
    #     for i, [l, r] in enumerate(applicable_rules):
    #         l_there = l in res
    #         r_there = r in res
    #         if l_there:
    #             il = res.index(l)
    #         if r_there:
    #             ir = res.index(r)

    #     for i in to_pop:
    #         res.pop(i)
    left_d = {}
    for l, r in applicable_rules:
        if left_d.get(l) is None:
            left_d[l] = [r]
        else:
            left_d[l].append(r)
    changing = True
    while changing:
        changing = False
        for k, vs in left_d.items():
            init_len = len(vs)
            new_v = vs
            for v in vs:
                if v in left_d.keys():
                    new_v += [
                        x
                        for x in left_d[v]
                        if x not in new_v
                    ]
            left_d[k] = new_v
            if len(new_v) > init_len:
                changing = True
    count_d = {
        k: len(v)
        for k, v in left_d.items()
    }
    max_count = np.max(np.array(list(count_d.values())))
    print(max_count)
    res = np.ones(max_count + 1) * (-1)
    for k, v in count_d.items():
        res[v] = k
    out = [
        c
        for c in change
        if c not in left_d.keys()
    ] + [
        r
        for r in res
        if r > -1
    ] 

    return np.array(out)[::-1].astype(int)


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