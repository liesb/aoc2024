import numpy as np


DIRECTIONS = {
    "left": (0, -1),
    "right": (0, 1),
    "up": (-1, 0),
    "down": (1, 0)
}

DIRECTION_CHANGE = {
    "up": "right",
    "right": "down",
    "down": "left",
    "left": "up"
}

def read_data(fn):
    # return the np array of individual letter
    with open(fn, "r") as f:
        return np.array(
            [
                list(l.replace("\n", "").replace(".", "0").replace("#", "2").replace("^", "1"))
                for l in f.readlines()
            ]
        ).astype(int)


def find_start_position(maze):
    sp = tuple(x[0] for x in np.where(maze == 1))
    return sp


def still_on_maze(pos, X, Y):
    x, y = pos
    return (
        (x > -1) and (x < X) and 
        (y > -1) and (y < Y)
    )


def add_tuples(tup1, tup2):
    return tuple(x+y for x, y in zip(tup1, tup2))

def get_new_pos(maze, pos, dir):
    X, Y = maze.shape
    new_pos = add_tuples(pos, DIRECTIONS[dir])
    if not still_on_maze(new_pos, X, Y):
        return new_pos, dir
    else:
        if maze[new_pos] != 2:
            return new_pos, dir
        else:
            
            stuck = True
            new_dir = dir
            while stuck:
                new_dir = DIRECTION_CHANGE[new_dir]
                # print("stuck")
                # print("new_dir = {}".format(new_dir))
                new_pos = add_tuples(pos, DIRECTIONS[new_dir])
                # print("new_pos = {}".format(new_pos))
                if not still_on_maze(new_pos, X, Y):
                    return new_pos, dir
                else:
                    stuck = (maze[new_pos] == 2)
            return new_pos, new_dir


def main(fn):
    maze = read_data(fn)
    # print(maze)
    X, Y = maze.shape
    pos = find_start_position(maze)
    dir = "up"
    # print(pos)
    while still_on_maze(pos, X, Y):
        maze[pos] = 1
        pos, dir = get_new_pos(maze, pos, dir)
        # print(pos, dir)
        # print("========")
    # print(maze)
    print(np.mod(maze, 2).sum())

    

if __name__ == "__main__":
    main("day6-input.txt")
