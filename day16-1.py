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
    # np.array([
    #     [0, 1, 2, 3],
    #     [3, 0, 1, 2],
    #     [2, 3, 0, 1],
    #     [1, 2, 3, 0]
    # ], dtype=int) * 1_000,
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
                # if iy == 3:
                #     print("+++")
                #     print(ix, jx)
                #     print(has_wall)
                #     print(has_node)
    # print(node_list)
    # print(out[-10:, -10:])
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
        # test_node_1 = (9, 3)
        # if node_i == test_node_1:
        #     print(node_j)
        # test_node_2 = (7, 3)
        # if (node_i == test_node_1) & (node_j == test_node_2):
        #     print("rel new start nodes = {}".format(relevant_new_start_nodes))
        #     print("dir of travel = {}".format(direction_travelling))
        for k, (_, facing_dir) in relevant_new_start_nodes:
            # find the direction you'd be travelling in and filter in the list below
            # you don't want to turn back
            # if (node_i == test_node_1) & (node_j == test_node_2):
            #     print(" facing dir {}".format(facing_dir))
            relevant_new_end_nodes = [
                (j, x)
                for j, x in enumerate(new_list_of_nodes)
                if (x[0] == node_j) and (x[1] != OPPOSITE_DIRECTION[direction_travelling])
            ]
            # if (node_i == test_node_1) & (node_j == test_node_2):
            #     print("  relevant new ned nodes {}".format(relevant_new_end_nodes))
            for l, (_, new_facing_dir)  in relevant_new_end_nodes:
                cost = conn_matrix[i, j]  # walking cost
                cost += COST_DF.loc[facing_dir, direction_travelling]  # turning cost at node_i
                cost += COST_DF.loc[direction_travelling, new_facing_dir]  # turning cost at node_j
                new_conn_matrix[k, l] = cost
    return new_list_of_nodes, new_conn_matrix


def main(fn):
    grid = read_data(fn)
    nr, nc = grid.shape
    start_point = (nr - 2, 1)
    end_point = (1, nc - 2)
    # add walls
    grid = add_walls(grid)
    # print_np_mat(grid)
    nodes = find_nodes(grid)
    print("number of nodes = {}".format(nodes.sum()))
    # print_np_mat(nodes.astype(int))
    # build connection matrix - all nodes
    node_list, conn_matrix = get_conn_matrix(nodes, grid)

    # idx1 = node_list.index((9,3))
    # idx2 = node_list.index((7,3))
    # print(conn_matrix[idx1, idx2])
    # assert False
    # expand node_list, conn_matrix to include "come from, go to"
    node_list, conn_matrix = expand_conn(node_list, conn_matrix, grid, start_point)
    # print(conn_matrix[-10:, -10:])
    # for n in node_list:
    #     print(n)
    # assert False

    # dijkstra
    unvisited = np.ones(len(node_list), dtype=bool)
    shortest_distance = np.ones(len(node_list), dtype=float) * np.inf
    # first round - visit all the starting points
    start_nodes = [
        (i, node)
        for i, node in enumerate(node_list)
        if node[0] == start_point
    ]
    for i, node in start_nodes:
        shortest_distance[i] = COST_DF.loc["E", node[1]]
    ## test
    # node1 = [(11, 1), 'N']
    # node2 = [(11, 3), 'S']
    # n1_idx = node_list.index(node1)
    # n2_idx = node_list.index(node2)
    # print(conn_matrix[n1_idx, n2_idx])
    # assert False


    # now really get going
    # k = 0
    while True:
        # print("=====")
        # select the unvisited node with the shortest distance
        a = np.where(
            unvisited,
            shortest_distance,
            np.inf
        )
        m = np.min(a)
        # print("m = {}".format(m))
        current_node_idx = np.where(
            a == m
        )[0][0]
        current_node = node_list[current_node_idx]
        
        print("visiting node with idx {} = {}".format(current_node_idx, current_node))
        ### TODO what if there is more than one current node with shortest distance??
        # stopping criterion - is current_node as target? TODO
        if current_node[0] == end_point:
            print("found target, distance = {}".format(shortest_distance[current_node_idx]))
            break
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
                # print("new shortest dist for this neighbour is = {}".format(shortest_distance[cnn_idx]))
        # remove current_node from univisted set
        # unvisited[current_node_idx] = False
        # also set all nodes with the same position to false
        set_to_visited = [
            node[0] == current_node[0]
            for node in node_list
        ]
        # print("setting {} other node(s) to visited".format(np.array(also_to_be_set_to_visited).sum()))
        # print([
        #     node for node, v in zip(node_list, also_to_be_set_to_visited) if v
        # ])
        # print_np_mat(grid)
        unvisited[
            set_to_visited
        ] = False

        # k+=1

        





    
    

if __name__ == "__main__":
    main("day16-input.txt")