import numpy as np


def read_data(fn):
    with open(fn, 'r') as f:
        return f.readline().strip()


def main(fn):
    data = read_data(fn)
    print(len(data))
    index_on_disk = 0
    checksum = 0
    left_empty = False
    # right_empty = np.mod(len(data), 2) == 0
    left_index_on_str = 0
    right_index_on_str = len(data) - 1
    left_file_id = 0
    right_index_on_str = len(data) - 1
    right_file_id = int(np.floor(len(data)/2))
    right_file_length = int(data[right_index_on_str])
    right_file_units_left_to_be_processed = right_file_length
    # print("right file id = {}".format(right_file_id))
    while left_index_on_str < right_index_on_str:  # probably wrong
        if not left_empty:
            num_spaces = int(data[left_index_on_str])
            # add to checksum
            checksum += left_file_id * np.arange(index_on_disk, index_on_disk + num_spaces).sum()
            # print("from if: adding {} x {}".format(left_file_id, np.arange(index_on_disk, index_on_disk + num_spaces)))
            # update file number for next file
            left_file_id += 1
            # update index_on_disk
            index_on_disk += num_spaces
            # next bit will be empty
            left_empty = True
        else:
            num_empty_spaces = int(data[left_index_on_str])
            while num_empty_spaces > 0:
                # print(type(num_empty_spaces), type(right_file_units_left_to_be_processed))
                num_spaces = np.minimum(num_empty_spaces, right_file_units_left_to_be_processed)
                checksum += right_file_id * np.arange(index_on_disk, index_on_disk + num_spaces).sum()
                # print("from right, adding : {} x {}".format(right_file_id, np.arange(index_on_disk, index_on_disk + num_spaces)))
                
                num_empty_spaces -= num_spaces
                index_on_disk += num_spaces
                right_file_units_left_to_be_processed -= num_spaces
                # print("left over from the right = {}".format(right_file_units_left_to_be_processed))
                if right_file_units_left_to_be_processed == 0:
                    # print("-- jumping from the right ---")
                    right_index_on_str -= 2
                    right_file_id -= 1
                    right_file_length = int(data[right_index_on_str])
                    right_file_units_left_to_be_processed = right_file_length
                    # print("file id = {}".format(right_file_id))
                    # print("units to process = {}".format(right_file_units_left_to_be_processed))
                    # print("-- end jumping from the right ---")
            # next bit will be a file
            left_empty = False
        left_index_on_str += 1
    # process last bits 
    checksum += right_file_id * np.arange(index_on_disk, index_on_disk + right_file_units_left_to_be_processed).sum() 
    print(checksum)


if __name__ == "__main__":
    main("day9-input.txt")