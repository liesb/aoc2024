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
                    entry["goal"] = [x_val, y_val]
    if out[-1] != entry:
        out += [entry]
    
    return out
                    

def main(fn):
    list_of_games = read_data(fn)
    # print(list_of_games)
    cost_of_winning = 0
    # cost matrix
    button_a_cost = (1 + np.arange(100)) * 3
    button_b_bost = (1 + np.arange(100))
    total_cost = button_a_cost[:, None] + button_b_bost[None]
    # print(total_cost)

    for game in list_of_games:
        # print("==========================")
        # print(game)
        # x moves
        button_a_x = (1 + np.arange(100)) * game["A"][0]
        button_b_x = (1 + np.arange(100)) * game["B"][0]
        x_matrix =  button_a_x[:, None] + button_b_x[None]
        # y moves
        button_a_y = (1 + np.arange(100)) * game["A"][1]
        button_b_y = (1 + np.arange(100)) * game["B"][1]
        y_matrix =  button_a_y[:, None] + button_b_y[None]
        # find match for goal
        mask = (x_matrix == game["goal"][0]) * (y_matrix == game["goal"][1])
        if mask.sum() > 0:
            # print("winning game {}".format(game))
            # print("at cost of {}".format(np.min(total_cost[mask])))
            # print("out of {} solutions".format(mask.sum()))
            cost_of_winning += np.min(total_cost[mask])
        else:
            pass
            # print("can't win game {}".format(game))
    print(cost_of_winning)


if __name__ == "__main__":
    main("day13-input.txt")