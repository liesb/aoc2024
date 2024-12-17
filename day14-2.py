import numpy as np


def read_data(fn):
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


def make_np_mat(pmat, tall, wide):
    out = np.zeros((tall, wide))
    for i in range(pmat.shape[0]):
        out[pmat[i,0], pmat[i,1]] = 1
    return out.astype(int)


def print_np_mat(pmat_np):
    ll = pmat_np.astype(str).tolist()
    for s in [   
        (("").join(l)).replace("0", " ").replace("1", "*")
        for l in ll
    ]:
        print(s)
    

# def get_sec_score(pmat, tall, wide):
#     tall1 = int(np.floor(tall/2))
#     wide1 = int(np.floor(wide/2))
#     tl = ((pmat[:, 0] < tall1) * (pmat[:,1] < wide1)).sum()
#     tr = ((pmat[:, 0] < tall1) * (pmat[:,1] > wide1)).sum()
#     bl = ((pmat[:, 0] > tall1) * (pmat[:,1] < wide1)).sum()
#     br = ((pmat[:, 0] > tall1) * (pmat[:,1] > wide1)).sum()
#     print(tl, tr, bl, br)
#     return tl * tr * bl * br


def get_2plus_heuristic(pmat_np):
    out = np.zeros_like(pmat_np, dtype=int)
    # check below
    out[:-1, :] += pmat_np[1:, :]
    # check top
    out[1:, :] += pmat_np[:-1, :]
    # check left
    out[:, 1:] += pmat_np[:, :-1]
    # check right
    out[:, :-1] += pmat_np[:, 1:]
    # check top left
    out[1:, 1:] += pmat_np[:-1, :-1]
    # check top right
    out[1:, :-1] += pmat_np[:-1, 1:]
    # check bottom left
    out[:-1, 1:] += pmat_np[1:, :-1]
    # check bottom right
    out[:-1, :-1] += pmat_np[1:, 1:]
    # print(out)
    return [
        ((out >= 2) * (pmat_np > 0)).sum(),  # 2+
        ((out == 2) * (pmat_np > 0)).sum()  # exactly 2
    ]



def main(fn, tall, wide):
    pos_mat, vel_mat = read_data(fn)
    # print_pmat(pos_mat, tall, wide)
    max2p = 0
    max2 = 0
    for i in range(tall*wide):
    # for i in range(2):
        pos_mat = update_positions(pos_mat, vel_mat, tall, wide)
        pos_mat_np = make_np_mat(pos_mat, tall, wide)
        twoplus_heuristic, two_heuristic = get_2plus_heuristic(pos_mat_np)
        if max2p < twoplus_heuristic:
            max2p = twoplus_heuristic
        if max2 < two_heuristic:
            max2 = two_heuristic
        print("===={}====".format(i))
        print(two_heuristic, twoplus_heuristic)
        if twoplus_heuristic > 350:
            print_np_mat(pos_mat_np)
            break
    print("max2p = {}".format(max2p))
    print("max2 = {}".format(max2))
        

    # print_pmat(pos_mat, tall, wide)
    # security_score = get_2plus_heuristic(pos_mat)
    # print(security_score)
    

if __name__ == "__main__":
    # main("day14-test-input.txt", 7, 11)
    main("day14-input.txt", 103, 101)