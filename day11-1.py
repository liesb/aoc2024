

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
    print(stones)
    final_count = 0
    for stone in stones:
        stone_set = [stone]
        for _ in range(25):
            stone_set = flatten_list([
                apply_rule(s)
                for s in stone_set
            ])
        final_count += len(stone_set)
        print(final_count)
    print(final_count)




if __name__ == "__main__":
    main("day11-input.txt")