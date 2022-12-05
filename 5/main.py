
import copy

INPUT = "input.txt"
RECORD_SIZE = 4

def read_file():
    with open(INPUT, 'r') as f:
        return f.readlines()

def split_file(input):
    header = []
    ops = []

    preamble = True
    for line in input:
        if line == "\n":
            preamble = False
            continue

        if preamble:
            header.append(line)
        else:
            ops.append(line)
    return header, ops

def prepare_header(header):
    indices = header[len(header) - 1]
    indices = indices.strip().split()

    num_cols = len(indices)

    rows = []
    for row in header[:-1]:
        row_chars = [''] * num_cols
        for col_idx in range(num_cols):
            c = row[(col_idx * RECORD_SIZE) + 1]
            if c != ' ':
                row_chars[col_idx] = c
        rows.append(row_chars)
    
    # Now we invert the stacks
    stacks = []
    for col in range(num_cols):
        stack = []
        for row in rows[::-1]:
            c = row[col]
            if c:
                stack.append(c)
        stacks.append(stack)
    
    return stacks

def prepare_ops(ops):
    # move 1 from 7 to 6
    op_tuples = []
    for op in ops:
        op_split = op.split()
        if not len(op_split) >= 6:
            continue
        num = int(op_split[1])
        from_idx = int(op_split[3])
        to_idx = int(op_split[5])
        op_tuples.append((num, from_idx, to_idx))
    return op_tuples

def execute_ops_9000(stacks, ops):
    """
    Move boxes one-by-one
    """
    for num, from_idx, to_idx in ops:
        for _ in range(num):
            stacks[to_idx - 1].append(stacks[from_idx - 1].pop())

def execute_ops_9001(stacks, ops):
    """
    Move boxes stacked
    """
    for num, from_idx, to_idx in ops:
        boxes = stacks[from_idx - 1][-num:] # read boxes
        stacks[from_idx - 1][-num:] = [] # remove them
        stacks[to_idx - 1].extend(boxes) # add to target

def print_solution(stacks):
    res = ''
    for stack in stacks:
        res += stack[len(stack) - 1]

    print(res)

def solve_9000(stacks, ops):
    stacks = copy.deepcopy(stacks)
    execute_ops_9000(stacks, ops)
    print_solution(stacks)

def solve_9001(stacks, ops):
    stacks = copy.deepcopy(stacks)
    execute_ops_9001(stacks, ops)
    print_solution(stacks)


def main():
    data = read_file()
    header, ops = split_file(data)
    stacks = prepare_header(header)
    ops = prepare_ops(ops)
    solve_9000(stacks, ops)
    solve_9001(stacks, ops)


if __name__ == "__main__":
    main()