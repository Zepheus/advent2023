import collections

INPUT = "input.txt"
PREAMBLE_LEN_1 = 4
PREAMBLE_LEN_2 = 14

def read_file(input_file):
    with open(input_file, 'r') as f:
        return f.readlines()

def parse(input, search_len):
    d = collections.deque(maxlen=search_len)
    for idx, c in enumerate(input[0]):  # Assumption one line
        d.append(c)
        if idx < search_len - 1:
            continue

        if len(set(d)) == search_len:
            return idx + 1 #  +1 since we need start of data, not end of preamble
    return -1

def main():
    data = read_file(INPUT)
    print(f"Total data is {len(data[0])}")
    res_1 = parse(data, PREAMBLE_LEN_1)
    print(f"Part 1 is at {res_1}")

    res_2 = parse(data, PREAMBLE_LEN_2)
    print(f"Pat 2 is at {res_2}")

if __name__ == "__main__":
    main()