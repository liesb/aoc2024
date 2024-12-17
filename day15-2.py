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
                grid_list += [
                    list(
                        line
                        .strip()
                        .replace("#", "##")
                        .replace("O", "[]")
                        .replace(".", "..")
                        .replace("@", "@.")
                    )
                ]
            else:
                steps += line.strip()
    return np.array(grid_list), steps


def get_robot_pos(grid):
    return tuple(x[0] for x in np.where(grid == "@"))


def add_tuples(x, y):
    return (x[0] + y[0], x[1] + y[1])


def process_right_step(grid, robot_pos, potential_new_pos):
    pnp_x, pnp_y = potential_new_pos
    sel_line = grid[potential_new_pos[0], :]
    next_wall = [
        x
        for x in np.where(sel_line == "#")[0]
        if (x > pnp_y)
    ][0]
    next_free_spots = [
        x
        for x in np.where(sel_line == ".")[0]
        if (x > pnp_y) and (x < next_wall)
    ]
    if len(next_free_spots) > 0:
        next_free_spot = next_free_spots[0]
        len_queue = next_free_spot - pnp_y
        grid[
            pnp_x,
            (pnp_y + 1):(pnp_y + len_queue + 1),
            
        ] = (
            grid[
                pnp_x,
                pnp_y:(pnp_y + len_queue),
            ]
        )
        grid[robot_pos] = "."
        grid[potential_new_pos] = "."
        return grid, potential_new_pos
    else:
        return grid, robot_pos


def weirdify_pos(pos, s, axis=0):
    if axis == 0:
        return (s - pos[0] - 1, pos[1])
    if axis == 1:
        return (pos[0], s - pos[1] - 1)


def find_zone_of_impact(grid, potential_new_pos):
    # return a matrix like grid, ones where the zone of impact is
    _, nc = grid.shape
    pnp_x, pnp_y = potential_new_pos
    out = np.zeros_like(grid, dtype=int)
    out[potential_new_pos] = 1
    if grid[potential_new_pos] == "[":
        out[pnp_x, pnp_y + 1] = 1
    else:  # "]"
        out[pnp_x, pnp_y - 1] = 1
    k = 1
    while (out[pnp_x + k - 1].sum() > 0):
        for j in range(nc):
            if grid[pnp_x + k, j] == "[":
                out[pnp_x + k, j] = (
                    (out[pnp_x + k - 1, j] == 1) or
                    (out[pnp_x + k - 1, j + 1] == 1)
                ).astype(int)
            elif grid[pnp_x + k, j] == "]":
                out[pnp_x + k, j] = (
                (out[pnp_x + k - 1, j] == 1) or
                (out[pnp_x + k - 1, j - 1] == 1)
            ).astype(int)
        k += 1
    return out


def find_frontiers(zi):
    _, nc = zi.shape
    d = np.concatenate(
        [
            np.zeros((1, nc)).astype(zi.dtype),
            np.diff(zi, axis=0)
        ],
        axis=0
    )
    return (d == -1), (d == 1)


def process_down_step(grid, robot_pos, potential_new_pos):
    _, nc = grid.shape
    # find the zone of impact
    zi = find_zone_of_impact(grid, potential_new_pos)
    # find the frontier
    f_bottom, f_top = find_frontiers(zi)
    # check if spots in the frontier have no walls
    # if walls, do nothing
    wall_parts = ((grid == "#") * (f_bottom)).sum()
    if wall_parts > 0:
        return grid, robot_pos
    # else, move the zone of impact one down
    # make sure to clear the top bits and add a .
    else:
        out = grid.copy()
        for (i, j) in zip(*np.where(zi)):
            out[i+1, j] = grid[i, j]
        for (i, j) in zip(*np.where(f_top)):
            out[i,j] = "."
        return out, potential_new_pos


def do_step(grid, robot_pos, step):
    move = MOVES[step]
    nr, nc = grid.shape
    potential_new_pos = add_tuples(robot_pos, move)
    if grid[potential_new_pos] == "#":
        return grid, robot_pos
    elif grid[potential_new_pos] == ".":
        return grid, potential_new_pos
    else:  # meeting an object "[" or "]"
        if step == ">":
            a, b = process_right_step(grid, robot_pos, potential_new_pos)
            return a, b
        elif step == "<":
            grid_weird, robot_pos_weird = process_right_step(
                grid[:, ::-1],
                weirdify_pos(robot_pos, nc, 1),
                weirdify_pos(potential_new_pos, nc, 1)
            )
            return grid_weird[:, ::-1], weirdify_pos(robot_pos_weird, nc, 1)
        elif step == "v":
            a, b = process_down_step(grid, robot_pos, potential_new_pos)
            return a, b
        elif step == "^":
            grid_weird, robot_pos_weird = process_down_step(
                grid[::-1, :],
                weirdify_pos(robot_pos, nr, 0),
                weirdify_pos(potential_new_pos, nr, 0)
            )
            return grid_weird[::-1, :], weirdify_pos(robot_pos_weird, nr, 0)


def calculate_gps_coor(grid):
    nr, nc = grid.shape
    return (
        (grid == "[") * (100 * np.arange(nr)[:, None] + np.arange(nc)[None, :])
    ).sum()


def print_np_mat(pmat_np, robot_pos):
    ll = pmat_np.astype(str).tolist()
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
    print_np_mat(grid, robot_pos)
    print(len(steps))
    for i, step in enumerate(steps):
        if np.mod(i, 100) == 0:
            print(i)
        grid, robot_pos = do_step(grid, robot_pos, step)
    print_np_mat(grid, robot_pos)
    print(calculate_gps_coor(grid)) 


if __name__ == "__main__":
    main("day15-input.txt")