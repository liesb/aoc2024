import numpy as np


def read_data(fn):
    # d = {}
    px_list = []
    py_list = []
    vx_list = []
    vy_list = []
    with open(fn, 'r') as f:
        for line in f.readlines():
            pos, vel = line.strip().split(" ")
            px, py = [
                int(a)
                for a in pos.split("=")[1].split(",")
            ]
            vx, vy = [
                int(a)
                for a in vel.split("=")[1].split(",")
            ]
            px_list.append(px)
            py_list.append(py)
            vx_list.append(vx)
            vy_list.append(vy)
    n = len(vx_list)
    pos_mat = np.zeros((n, 2), dtype=int)
    vel_mat = np.zeros_like(pos_mat)
    pos_mat[:, 0] = py_list
    pos_mat[:, 1] = px_list
    vel_mat[:, 0] = vy_list
    vel_mat[:, 1] = vx_list
    return pos_mat, vel_mat


def update_positions(pmat, vmat, tall, wide):
    new_pmat = pmat + vmat
    new_pmat[:, 0] = np.mod(new_pmat[:, 0], tall)
    new_pmat[:, 1] = np.mod(new_pmat[:, 1], wide)
    return new_pmat


def print_pmat(pmat, tall, wide):
    out = np.zeros((tall, wide))
    for i in range(pmat.shape[0]):
        out[pmat[i,0], pmat[i,1]] += 1
    print(out)
    

def get_sec_score(pmat, tall, wide):
    tall1 = int(np.floor(tall/2))
    wide1 = int(np.floor(wide/2))
    tl = ((pmat[:, 0] < tall1) * (pmat[:,1] < wide1)).sum()
    tr = ((pmat[:, 0] < tall1) * (pmat[:,1] > wide1)).sum()
    bl = ((pmat[:, 0] > tall1) * (pmat[:,1] < wide1)).sum()
    br = ((pmat[:, 0] > tall1) * (pmat[:,1] > wide1)).sum()
    print(tl, tr, bl, br)
    return tl * tr * bl * br


def main(fn, tall, wide):
    pos_mat, vel_mat = read_data(fn)
    # print_pmat(pos_mat, tall, wide)
    for i in range(100):
        pos_mat = update_positions(pos_mat, vel_mat, tall, wide)
    # print_pmat(pos_mat, tall, wide)
    security_score = get_sec_score(pos_mat, tall, wide)
    print(security_score)


if __name__ == "__main__":
    # main("day14-test-input.txt", 7, 11)
    main("day14-input.txt", 103, 101)