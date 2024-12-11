import numpy as np


# only test objects they might bump into: 
# this means only places where the original path goes (except start position)
# 

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
                new_pos = add_tuples(pos, DIRECTIONS[new_dir])
                if not still_on_maze(new_pos, X, Y):
                    return new_pos, dir
                else:
                    stuck = (maze[new_pos] == 2)
            return new_pos, new_dir


def test_for_loop_induced(og_maze, new_object_pos):
    maze = og_maze.copy()
    X, Y = maze.shape
    maze[new_object_pos] = 2
    start_pos = find_start_position(maze)
    pos = start_pos
    dir = "up"
    visited = {
        start_pos: [dir],
    }
    while still_on_maze(pos, X, Y):
        maze[pos] = 1
        pos, dir = get_new_pos(maze, pos, dir)
        if pos in visited.keys():
            if dir in visited[pos]:
                return True
            else:
                visited[pos] += dir
        else:
            visited[pos] = dir
    return False

def main(fn):
    og_maze = read_data(fn)
    X, Y = og_maze.shape

    # initial maze run 
    maze = og_maze.copy()
    start_pos = find_start_position(maze)
    pos = start_pos
    dir = "up"
    while still_on_maze(pos, X, Y):
        maze[pos] = 1
        pos, dir = get_new_pos(maze, pos, dir)
    
    # find all positions visited on initial maze run (list of tuples)
    maze[start_pos] = 0
    possible_object_positions = list(zip(*np.where(maze == 1)))
    print(len(possible_object_positions))
    # look for loops
    count = 0
    for i, new_object_pos in enumerate(possible_object_positions):
        print(i)
        # print(new_object_pos)
        loop = test_for_loop_induced(og_maze, new_object_pos)
        if loop:
            count += 1
            print("loop")
        # print("===")
    print(count)
 

if __name__ == "__main__":
    main("day6-input.txt")
