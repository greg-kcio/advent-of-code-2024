def part1(fp: str) -> int:
    with open(fp, "r", encoding="utf-8") as f:
        lab = f.read().splitlines()

    num_rows = len(lab)
    num_cols = len(lab[0])

    visited = []
    obstacles = set()
    for y, row in enumerate(lab):
        for x, pos in enumerate(row):
            if pos == "#":
                obstacles.add((x, y))
            elif pos == "^":
                visited.append((x, y))

    directions = (
        (0, -1),  # north
        (1, 0),  # east
        (0, 1),  # south
        (-1, 0),  # west
    )
    d = 0  # index of current direction

    while True:
        destination = (
            visited[-1][0] + directions[d][0],
            visited[-1][1] + directions[d][1],
        )
        if destination in obstacles:
            d += 1
            d %= 4  # wraparound
        elif (
            destination[0] == num_rows
            or destination[1] == num_cols
            or any(c < 0 for c in destination)
        ):
            break  # off the map
        else:
            visited.append(destination)

    return len(set(visited))


print(part1("06/part1_example.txt"))
print(part1("06/part1.txt"))
