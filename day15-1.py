import numpy as np


MOVES = {
    ">": (0, 1),
    "<": (0, -1),
    "^": (-1, 0),
    "v": (1, 0)
}

def read_data(fn):
    reading_grid = True
    grid_list = []
    steps = ""
    with open(fn, 'r') as f:
        for line in f.readlines():
            if line == "\n":
                reading_grid = False
            if reading_grid:
                grid_list += [list(line.strip())]
            else:
                steps += line.strip()
    return np.array(grid_list), steps


def get_robot_pos(grid):
    return tuple(x[0] for x in np.where(grid == "@"))


def add_tuples(x, y):
    return (x[0] + y[0], x[1] + y[1])


def do_step(grid, robot_pos, step):
    move = MOVES[step]
    potential_new_pos = add_tuples(robot_pos, move)
    if grid[potential_new_pos] == "#":
        return grid, robot_pos
    elif grid[potential_new_pos] == ".":
        return grid, potential_new_pos
    else:  # meeting an object "O"
        if step == ">":
            sel_line = grid[potential_new_pos[0], :]
            next_wall = [
                x
                for x in np.where(sel_line == "#")[0]
                if (x > potential_new_pos[1])
            ][0]
            next_free_spots = [
                x
                for x in np.where(sel_line == ".")[0]
                if (x > potential_new_pos[1]) and (x < next_wall)
            ]
            if len(next_free_spots) > 0:
                grid[robot_pos] = "."
                grid[potential_new_pos] = "."
                grid[potential_new_pos[0], next_free_spots[0]] = "O"
                return grid, potential_new_pos
            else:
                return grid, robot_pos
        elif step == "<":
            sel_line = grid[potential_new_pos[0], :]
            next_wall = [
                x
                for x in np.where(sel_line == "#")[0]
                if (x < potential_new_pos[1])
            ][-1]
            next_free_spots = [
                x
                for x in np.where(sel_line == ".")[0]
                if (x < potential_new_pos[1]) and (x > next_wall)
            ]
            if len(next_free_spots) > 0:
                grid[robot_pos] = "."
                grid[potential_new_pos] = "."
                grid[potential_new_pos[0], next_free_spots[-1]] = "O"
                return grid, potential_new_pos
            else:
                return grid, robot_pos
        elif step == "^":
            sel_line = grid[:, potential_new_pos[1]]
            next_wall = [
                x
                for x in np.where(sel_line == "#")[0]
                if (x < potential_new_pos[0])
            ][-1]
            next_free_spots = [
                x
                for x in np.where(sel_line == ".")[0]
                if (x < potential_new_pos[0]) and (x > next_wall)
            ]
            if len(next_free_spots) > 0:
                grid[robot_pos] = "."
                grid[potential_new_pos] = "."
                grid[next_free_spots[-1], potential_new_pos[1]] = "O"
                return grid, potential_new_pos
            else:
                return grid, robot_pos
        elif step == "v":
            sel_line = grid[:, potential_new_pos[1]]
            next_wall = [
                x
                for x in np.where(sel_line == "#")[0]
                if (x > potential_new_pos[0])
            ][0]
            next_free_spots = [
                x
                for x in np.where(sel_line == ".")[0]
                if (x > potential_new_pos[0]) and (x < next_wall)
            ]
            if len(next_free_spots) > 0:
                grid[robot_pos] = "."
                grid[potential_new_pos] = "."
                grid[next_free_spots[0], potential_new_pos[1]] = "O"
                return grid, potential_new_pos
            else:
                return grid, robot_pos


def calculate_gps_coor(grid):
    nr, nc = grid.shape
    return (
        (grid == "O") * (100 * np.arange(nr)[:, None] + np.arange(nc)[None, :])
    ).sum()


def print_np_mat(pmat_np, robot_pos):
    ll = pmat_np.tolist()
    ll[robot_pos[0]][robot_pos[1]] = "@"
    for s in [   
        (("").join(l))
        for l in ll
    ]:
        print(s)


def main(fn):
    grid, steps = read_data(fn)
    robot_pos = get_robot_pos(grid)
    grid[robot_pos] = "."
    print(robot_pos)
    for step in steps:
        # print(step)
        grid, robot_pos = do_step(grid, robot_pos, step)
    print_np_mat(grid, robot_pos)
    print(calculate_gps_coor(grid)) 


if __name__ == "__main__":
    main("day15-input.txt")