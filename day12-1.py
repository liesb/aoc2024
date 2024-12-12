import numpy as np

DIRECTIONS =[
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0)
]


def read_data(fn):
    with open(fn, 'r') as f:
        return np.array([
            list(l.replace("\n", ""))
            for l in f.readlines()
        ])


def get_areas(garden, patches):
    return np.array(
        [
            (garden == patch).sum()
           for patch in patches 
        ]
    )


def still_on_map(pos, nr, nc):
    return (
        (pos[0] < nr) &
        (pos[0] >= 0) &
        (pos[1] < nc) &
        (pos[1] >= 0)
    )


def add_tuples(x, y):
    return (x[0] + y[0], x[1] + y[1])


def get_perimeters(garden, patches):
    out = np.zeros(len(patches), dtype=int)
    nr, nc = garden.shape
    for i in range(nr):
        for j in range(nc):
            patch = garden[i, j]
            for d in DIRECTIONS:
                nearby_pos = add_tuples((i, j), d)
                if still_on_map(nearby_pos, nr, nc) and (garden[nearby_pos] != patch):
                    out[patches.index(patch)] += 1
                elif not still_on_map(nearby_pos, nr, nc):
                    out[patches.index(patch)] += 1
    return out
                    

def revamp_garden(garden):
    out = np.zeros_like(garden, dtype=int)
    new_label = 1
    nr, nc = garden.shape
    for i in range(nr):
        for j in range(nc):
            neighbours = []
            for d in DIRECTIONS:
                neighbour_pos = add_tuples((i, j), d)
                if (
                    still_on_map(neighbour_pos, nr, nc) and
                    (garden[neighbour_pos] == garden[i, j]) and
                    out[neighbour_pos] > 0
                ):
                    neighbours += [out[neighbour_pos]]
            if len(neighbours) == 0:
                out[i, j] = new_label
                new_label += 1
            elif len(neighbours) == 1:
                out[i, j] = neighbours[0]
            else:
                m = np.min(np.array(neighbours))
                # assign the minimum value
                out[i, j] = m
                # assign the minimum value to all other revamped fields where appl
                out = np.where(np.isin(out, neighbours), m, out)
    return out
                    

def main(fn):
    garden = read_data(fn)
    garden_revamp = revamp_garden(garden)
    # print(garden)
    # print(garden_revamp)
    patches = np.unique(garden_revamp).tolist()
    # print(patches)
    areas = get_areas(garden_revamp, patches)
    perimeters = get_perimeters(garden_revamp, patches)
    # print(areas)
    # print(perimeters)
    # for p, a, b, c in zip(patches, areas, perimeters, areas * perimeters):
        # print(p, a, b, c)
    print((areas * perimeters).sum())


if __name__ == "__main__":
    main("day12-input.txt")