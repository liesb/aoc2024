import numpy as np

PROTO_PROCESSING_DICT = {
    0: [[4, {0: 1, 2: 2, 4: 1}]],
    1: [[3, {0: 1, 2: 2, 4: 1}]],
    2: [[3, {0: 1, 4: 2, 8: 1}]],
    3: [[3, {0: 1, 2: 1, 6: 1, 7: 1}]],
    4: [[3, {0: 1, 6: 1, 8: 1, 9: 1}]],
    5: [[5, {0: 2, 2: 2, 4: 1, 8: 3}]],
    6: [[5, {2: 1, 4: 2, 5: 2, 6: 1, 7: 1, 9: 1}]],
    7: [[5, {0: 1, 2: 2, 3: 1, 6: 2, 7: 1, 8: 1}]],
    8: [
        [5, {2: 2, 3: 1, 6: 1, 7: 2}],
        [4, {8: 1}]
    ],
    9: [[5, {1: 1, 3: 1, 4: 1, 6: 2, 8: 2, 9: 1}]]
}


def arrayify(d):
    out = np.zeros(10, dtype=int)
    for k, v in d.items():
        out[k] = v
    return out


PROCESSING_DICT = {
    k: [[v1, arrayify(v2)] for v1, v2 in v]
    for k, v in PROTO_PROCESSING_DICT.items()
}


def read_data(fn):
    with open(fn, 'r') as f:
        return f.readline().strip().split(" ")


def flatten_list(l):
    return [x for y in l for x in y]


def remove_zeros(num_as_str):
    return str(int(num_as_str))


def apply_rule(num_as_str):
    if num_as_str == "0":
        return ["1"]
    elif len(num_as_str) % 2 == 0:
        mid = int(len(num_as_str) / 2)
        return [num_as_str[:mid], remove_zeros(num_as_str[mid:])]
    else:
        return [
            str(int(num_as_str) * 2024)
        ]


def main(fn):
    stones = read_data(fn)
    # stones = ["0"]
    print(stones)
    # digit_counter[i, j] = total number of digit i that still needs to be processed j times
    digit_counter = np.zeros((10, 76), dtype=np.int64)
    # digit_counter = np.zeros((10, 26), dtype=np.int64)


    # fill up digit counter (i.e. process stones until they are all down to single digits)
    print("start filling up")
    k = 0
    stone_set = stones
    while (len(stone_set) > 0) and (k < 75):
        # TODO this might not be foolproof, if we need more round of this than there are iterations
        print(k)
        print(len(stone_set))
        # deal with single digits
        single_digits = [
            s for s in stone_set
            if len(s) == 1
        ]
        print(len(single_digits))
        for s in single_digits:
            digit_counter[int(s), 75 - k] += 1
            # digit_counter[int(s), 25 - k] += 1
        # deal with rest of the list
        stone_set = [
            s for s in stone_set
            if len(s) > 1
        ]
        # print(stone_set)
        stone_set = flatten_list([
            apply_rule(s)
            for s in stone_set
        ])
        k += 1
        print("---")
        
    print("+++++++")
    print("remaining stones = {}".format(len(stone_set)))
    # # testing the digit_counter
    # xs, ys = np.where(digit_counter > 0)
    # for x, y in zip(xs, ys):
    #     print("digit = {}, count = {}, to_repeat = {}".format(x, digit_counter[x,y], y))
    # print("total stones so far = {}".format(digit_counter.sum()))
    # pretty sure it works up until here

    for round in range(75, 5, -1):
        digits = np.where(digit_counter[:, round] > 0)[0]
        for digit in digits:
            count = digit_counter[digit, round]
            for i in range(len(PROCESSING_DICT[digit])):
                rounds_diff, digit_array = PROCESSING_DICT[digit][i]
                digit_counter[:, round - rounds_diff] += digit_array * count
                digit_counter[digit, round] = 0
        
    print("+++++++++++++++")
    print(np.sum(digit_counter))
    print("+++++++++++++++")

    # last bits
    final_count = len(stone_set)
    xs, ys = np.where(digit_counter > 0)
    for x, y in zip(xs, ys):
        # print("digit = {}, to_repeat = {}, count = {}".format(x, y, digit_counter[x,y]))
        count = digit_counter[x, y]
        stone_set = [str(x)]
        for _ in range(y):
            stone_set = flatten_list([
                apply_rule(s)
                for s in stone_set
            ])
        # print("number of stones = {}".format(len(stone_set)))
        # print("adding = {}".format(len(stone_set * count)))
        final_count += len(stone_set) * count
    print(final_count)


if __name__ == "__main__":
    main("day11-input.txt")