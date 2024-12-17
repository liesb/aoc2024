import numpy as np
import re


def read_data(fn):
    out = []
    item_counter = 0
    entry = {}
    with open(fn, 'r') as f:
        for line in f:
            if line =="\n":
                item_counter += 1
                out += [entry]
                entry = {}
            else:
                a, b = line.strip().split(": ")
                xis, yis = b.split(", ")
                x_val = int(re.split("\+|=", xis)[1])
                y_val = int(re.split("\+|=", yis)[1])
                if a == "Button A":
                    entry["A"] = [x_val, y_val]
                elif a == "Button B":
                    entry["B"] = [x_val, y_val]
                else:
                    entry["goal"] = [10000000000000 + x_val, 10000000000000 + y_val]
    if out[-1] != entry:
        out += [entry]
    
    return out
                    

def main(fn):
    list_of_games = read_data(fn)
    # print(list_of_games)
    cost_of_winning = 0

    for game in list_of_games:
        print("==========================")
        # print(game)
        
        A = np.array(
            [
                [game["A"][0], game["B"][0]],
                [game["A"][1], game["B"][1]]
            ]
        )
        b =  np.array(game["goal"])
        na, nb = np.linalg.solve(A, b)
        na = np.round(na)
        nb = np.round(nb)
        if (game["goal"] == A @ np.array([na, nb])).all():
            cost = na * 3 + nb
            print("winning game {}".format(game))
            print("at cost of {}".format(np.min(cost)))
            print("moves: {} - {}".format(na, nb))
            cost_of_winning += cost
    print(cost_of_winning)


if __name__ == "__main__":
    main("day13-input.txt")