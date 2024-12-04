def transpose(lines: list[str]) -> list[str]:
    """Transpose a word search."""
    return ["".join(transposed_line) for transposed_line in zip(*lines)]


def shift_forward(lines: list[str]) -> list[str]:
    """Shift each line of the grid forward by its line number."""
    return [line[-i:] + line[:-i] for i, line in enumerate(lines)]


def shift_backward(lines: list[str]) -> list[str]:
    """Shift each line of the grid backward by its line number."""
    return [line[i:] + line[:i] for i, line in enumerate(lines)]


def part1(fp: str) -> int:
    with open(fp, "r", encoding="utf-8") as f:
        lines = f.read().split("\n")

    total = 0
    words = ["XMAS", "SAMX"]

    # search horizontally
    total += sum(line.count(word) for line in lines for word in words)

    # transpose the lines to search vertically
    total += sum(line.count(word) for line in transpose(lines) for word in words)

    # wrap lines with "." so I can shift diagonally without wraparound
    wrapped_lines = [f".{line}." for line in lines]

    # shift each line and then transpose to search diagonally
    total += sum(
        line.count(word)
        for line in transpose(shift_forward(wrapped_lines))
        for word in words
    )

    # shift in the other direction and transpose again to search in the other diagonal direction
    total += sum(
        line.count(word)
        for line in transpose(shift_backward(wrapped_lines))
        for word in words
    )

    return total


def part2(fp: str) -> int:
    with open(fp, "r", encoding="utf-8") as f:
        lines = f.read().split("\n")

    # find every A, then check that the diagonals make an X-MAS
    total = sum(
        1
        for row in range(1, len(lines) - 1)
        for col in range(1, len(lines) - 1)
        if lines[row][col] == "A"
        and all(
            x in ["SM", "MS"]
            for x in [
                f"{lines[row-1][col-1]}{lines[row+1][col+1]}",
                f"{lines[row+1][col-1]}{lines[row-1][col+1]}",
            ]
        )
    )

    return total


print(part1("04/part1_example.txt"))
print(part1("04/part1.txt"))
print(part2("04/part1_example.txt"))
print(part2("04/part1.txt"))
