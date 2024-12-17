import numpy as np
import pandas as pd

DIRECTIONS = {
    "E": (0, 1),
    "N": (-1, 0),
    "W": (0, -1),
    "S": (1, 0)
}

OPPOSITE_DIRECTION = {
    "N": "S",
    "S": "N",
    "E": "W",
    "W": "E"
}

COST_DF = pd.DataFrame(
    # index = currently going / direction facing
    # columns = turning to
    np.array([
        [0, 1, 2, 1],
        [1, 0, 1, 2],
        [2, 1, 0, 1],
        [1, 2, 1, 0]
    ], dtype=int) * 1_000,
    index=["E", "N", "W", "S"],
    columns=["E", "N", "W", "S"]
)

def read_data(fn):
    with open(fn, 'r') as f:
        return np.array(
            [
                list(line.strip())
                for line in f.readlines()
            ]
        )


def add_tuples(x, y):
    return (x[0] + y[0], x[1] + y[1])


def subtract_tuples(x, y):
    # returns x - y
    return (x[0] - y[0], x[1] - y[1])


def print_np_mat(pmat_np):
    ll = pmat_np.astype(str).tolist()
    for s in [   
        (("").join(l))
        for l in ll
    ]:
        print(s)


def pad(mat):
    nr, nc = mat.shape
    out = np.zeros((nr+2, nc+2), dtype=mat.dtype)
    out[1:-1, 1:-1] = mat
    return out


def add_walls(grid):
    out = grid.copy()
    # k = 0
    wall_added = 0
    while True:
        # count inner bits
        wall_count = (
            # look to right
            (out[:, 1:] == "#").astype(int)[1:-1, 1:] +
            # look to left
            (out[:, :-1] == "#").astype(int)[1:-1, :-1] +
            # look to top
            (out[:-1, :] == "#").astype(int)[:-1, 1:-1] + 
            # look to bottom
            (out[1:, :] == "#").astype(int)[1:, 1:-1]
        ).astype(int)
        # embed into full scale
        wall_count_with_outer_walls = pad(wall_count)
        cond = (wall_count_with_outer_walls == 3) * (out == ".").astype(int)
        if cond.sum() == 0:
            break
        wall_added += cond.sum()
        out = np.where(cond == 1, "#", out)
    print("added {} walls".format(wall_added))
    return out


def find_nodes(grid):
    # look for non-nodes
    eligible_free_spots = [".", "S", "E"]
    free_spot = np.isin(grid, eligible_free_spots)

    horizontal = (
            # is it a free spot
            free_spot[1:-1, 1:-1] &
            # look to right
            (np.isin(grid[:, 1:], eligible_free_spots))[1:-1, 1:] &
            # look to left
            (np.isin(grid[:, :-1], eligible_free_spots))[1:-1, :-1] &
            # look to top
            (grid[:-1, :] == "#")[:-1, 1:-1] &
            # look to bottom
            (grid[1:, :] == "#")[1:, 1:-1]
        )
    horizontal_with_outer_walls = pad(horizontal)
    vertical = (
            # is it a free spot
            free_spot[1:-1, 1:-1] &
            # look to right
            (grid[:, 1:] == "#")[1:-1, 1:] &
            # look to left
            (grid[:, :-1] == "#")[1:-1, :-1] &
            # look to top
            np.isin(grid[:-1, :], eligible_free_spots)[:-1, 1:-1] &
            # look to bottom
            np.isin(grid[1:, :], eligible_free_spots)[1:, 1:-1]
        )
    vertical_with_outer_walls = pad(vertical)
    # every thing that is a . but no in horizontal or vertical is a node
    # print(horizontal.shape)
    # print(horizontal_with_outer_walls.shape)
    # print(vertical.shape)
    # print(vertical_with_outer_walls.shape)
    nodes = (
        free_spot &
        ~horizontal_with_outer_walls &
        ~vertical_with_outer_walls
    )
    return nodes



def get_conn_matrix(nodes, grid):
    node_list = list(zip(*np.where(nodes == 1)))
    nl = len(node_list)
    out = np.ones((nl, nl), dtype=int) * (-1)
    for i in range(nl-1):
        for j in range(i+1, nl):
            ix, iy = node_list[i]
            jx, jy = node_list[j]
            if ix == jx:
                m = np.minimum(iy, jy)
                M = np.maximum(iy, jy)
                # check no walls between
                has_wall = (grid[ix, m:M] == "#").any()
                # check no nodes between
                has_node = len(
                    [
                        y
                        # for n in node_list
                        for x, y in node_list
                        if (x == ix) and (y > m) and (y < M)
                    ]
                ) > 0
                if not has_node and not has_wall:
                    out[i, j] = M - m
                    out[j, i] = M - m
            elif iy == jy:
                m = np.minimum(ix, jx)
                M = np.maximum(ix, jx)
                # check no walls between
                has_wall = (grid[m:M, iy] == "#").any()
                # check no nodes between
                has_node = len(
                    [
                        y
                        for x, y in node_list
                        if (y == iy) and (x > m) and (x < M)
                    ]
                ) > 0
                if not has_node and not has_wall:
                    out[i, j] = M - m
                    out[j, i] = M - m
    return node_list, out


def get_sign(t):
    return tuple(np.sign(x) for x in t)


def expand_conn(node_list, conn_matrix, grid, start_point):
    # conn matrix has the distances between the points, but not the cost of turning
    new_list_of_nodes = [] # will be of shape ((x,y), direction_you_are_facing)
    for i, node in enumerate(node_list):
        for k, v in DIRECTIONS.items():
            if node == start_point:
                # judge on whether you can go that direction
                if grid[add_tuples(node, v)] == ".":
                    new_list_of_nodes.append([node, k])
            # k is the direction you're facing when arriving at this node
            # so it's about where you come from
            elif grid[subtract_tuples(node, v)] != "#":
                new_list_of_nodes.append([node, k])
    nl = len(new_list_of_nodes)
    new_conn_matrix = np.zeros((nl, nl), dtype=int)
    for i, j in zip(*np.where(conn_matrix > 0)):
        node_i = node_list[i]  # these are just positions
        node_j = node_list[j]
        direction_travelling = [
            k
            for k, v in DIRECTIONS.items()
            if get_sign(subtract_tuples(node_j, node_i)) == v
        ][0]
        relevant_new_start_nodes = [
            (i, x)  # x is [pos, direction] but pos == node_i
            for i, x in enumerate(new_list_of_nodes)
            if x[0] == node_i
        ]
        for k, (_, facing_dir) in relevant_new_start_nodes:
            # find the direction you'd be travelling in and filter in the list below
            # you don't want to turn back
            relevant_new_end_nodes = [
                (j, x)
                for j, x in enumerate(new_list_of_nodes)
                if (x[0] == node_j) and (x[1] != OPPOSITE_DIRECTION[direction_travelling])
            ]
            for l, (_, new_facing_dir)  in relevant_new_end_nodes:
                cost = conn_matrix[i, j]  # walking cost
                cost += COST_DF.loc[facing_dir, direction_travelling]  # turning cost at node_i
                cost += COST_DF.loc[direction_travelling, new_facing_dir]  # turning cost at node_j
                new_conn_matrix[k, l] = cost
    return new_list_of_nodes, new_conn_matrix


def dist(tup1, tup2):
    return np.abs(tup1[0] - tup2[0] + tup1[1] - tup2[1])


def add_to_out(out, tup1, tup2):
    ix, iy = tup1
    jx, jy = tup2
    if ix == jx:
        m = np.minimum(iy, jy)
        M = np.maximum(iy, jy)
        out[ix, m:(M+1)] = 1
    elif iy == jy:
        m = np.minimum(ix, jx)
        M = np.maximum(ix, jx)
        out[m:(M+1), iy] = 1
    return out


def main(fn):
    grid = read_data(fn)
    nr, nc = grid.shape
    start_point = (nr - 2, 1)
    end_point = (1, nc - 2)
    # add walls
    grid = add_walls(grid)
    nodes = find_nodes(grid)
    print("number of nodes = {}".format(nodes.sum()))
    # build connection matrix - all nodes
    node_list, conn_matrix = get_conn_matrix(nodes, grid)
    # expand node_list, conn_matrix to include "come from, go to"
    node_list, conn_matrix = expand_conn(node_list, conn_matrix, grid, start_point)

    # dijkstra ad infinitum
    print("dijkstra")
    unvisited = np.ones(len(node_list), dtype=bool)
    shortest_distance = np.ones(len(node_list), dtype=float) * np.inf
    came_from = {}
    # first round - visit all the starting points
    start_nodes = [
        (i, node)
        for i, node in enumerate(node_list)
        if node[0] == start_point
    ]
    for i, node in start_nodes:
        shortest_distance[i] = COST_DF.loc["E", node[1]]
    end_node_indicator = np.zeros(len(node_list), dtype=bool)
    end_nodes = [
        (i, node)
        for i, node in enumerate(node_list)
        if node[0] == end_point
    ]
    for i, node in end_nodes:
        end_node_indicator[i] = True
    # now really get going
    while ((unvisited * end_node_indicator).sum() > 0):
        # print("=====")
        # select the unvisited node with the shortest distance
        a = np.where(
            unvisited,
            shortest_distance,
            np.inf
        )
        m = np.min(a)
        # print("m = {}".format(m))
        current_node_idxes = np.where(
            a == m
        )[0]
        if len(current_node_idxes) > 0:
            current_node_idx = current_node_idxes[0]
        else:
            break
        current_node = node_list[current_node_idx]
        # print("visiting node with idx {} = {}".format(current_node_idx, current_node))
        # stopping criterion - is current_node as target? TODO -- think this is in the while now and ok
        if current_node[0] == end_point:
            print("found target, distance = {}".format(shortest_distance[current_node_idx]))
        # find all the neighbours of current_node and
        # update the distance
        current_node_neighbours_idxs = np.where(
            (conn_matrix[current_node_idx, :] > 0) & (unvisited == True)
        )[0]
        for cnn_idx in current_node_neighbours_idxs:
            # print("visiting neighbour at {}".format(node_list[cnn_idx]))
            potential_new_dist = m + conn_matrix[current_node_idx, cnn_idx]
            if potential_new_dist < shortest_distance[cnn_idx]:
                shortest_distance[cnn_idx] = potential_new_dist
                came_from[cnn_idx] = [current_node_idx]
            elif potential_new_dist == shortest_distance[cnn_idx]: 
                came_from[cnn_idx].append(current_node_idx)
        # remove current_node from univisted set
        # unvisited[current_node_idx] = False
        # also set all nodes with the same position to false
        unvisited[
            current_node_idx
        ] = False
    
    # find good spots
    a = np.where(end_node_indicator, shortest_distance, np.inf)
    m = np.min(np.where(end_node_indicator, shortest_distance, np.inf))
    out = np.zeros_like(grid, dtype=int)
    nodes_involved = np.zeros(len(node_list), dtype=bool)
    nodes_to_process = [
        i
        for i in range(len(a))
        if a[i] == m
    ]
    while len(nodes_to_process) > 0:
        processing = nodes_to_process.pop()
        # print(processing)
        if not nodes_involved[processing]:
            nodes_involved[processing] = True
            if processing in came_from.keys():
                nodes_to_process += came_from[processing]
        # print(len(nodes_to_process))

    for k, v in came_from.items():
        if nodes_involved[k]:
            for vv in v:
                out = add_to_out(out, node_list[k][0], node_list[vv][0])
    print(out.sum())

if __name__ == "__main__":
    main("day16-input.txt")