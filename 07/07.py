def parse_line(line: str) -> tuple[int, list[int]]:
    target, operands = line.split(":")
    operands = [int(x) for x in operands.split()]
    return int(target), operands


def parse_input(fp: str) -> list[tuple[int, list[int]]]:
    with open(fp, "r", encoding="utf-8") as f:
        return [parse_line(line.strip()) for line in f.readlines()]


def can_be_valid(equation: tuple[int, list[int]], part2: bool = False) -> bool:
    target, operands = equation
    if len(operands) == 1:
        return operands[0] == target

    new_operands = [
        [operands[0] + operands[1]] + operands[2:],
        [operands[0] * operands[1]] + operands[2:],
    ]

    if part2:
        new_operands += [[int(str(operands[0]) + str(operands[1]))] + operands[2:]]

    return any(can_be_valid((target, new_op), part2) for new_op in new_operands)


def solve(fp: str, part2: bool = False) -> int:
    equations = parse_input(fp)
    return sum(e[0] for e in equations if can_be_valid(e, part2))


print(solve("07/part1_example.txt"))
print(solve("07/part1.txt"))
print(solve("07/part1_example.txt", part2=True))
print(solve("07/part1.txt", part2=True))
