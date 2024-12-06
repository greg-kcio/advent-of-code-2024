from dataclasses import dataclass


@dataclass
class Position:
    x: int
    y: int

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


@dataclass
class Guard:
    pos: Position
    d: int  # index of direction

    def __hash__(self):
        return hash((self.pos, self.d))

    def __eq__(self, other: "Guard"):
        return self.pos == other.pos and self.d == other.d


DIRECTIONS = (
    Position(0, -1),  # north
    Position(1, 0),  # east
    Position(0, 1),  # south
    Position(-1, 0),  # west
)


def traverse(
    history: list[Guard],
    visited: set[Guard],
    obstacles: set[Position],
    num_rows: int,
    num_cols: int,
) -> list[Guard] | None:

    while True:
        prev = history[-1]
        destination = prev.pos + DIRECTIONS[prev.d]
        if (
            destination.x == num_rows
            or destination.y == num_cols
            or any(c < 0 for c in (destination.x, destination.y))
        ):
            break  # off the map
        if destination in obstacles:
            d = prev.d + 1
            d %= 4  # wraparound
            gnext = Guard(prev.pos, d)
        else:
            gnext = Guard(destination, prev.d)
        if gnext in visited:
            return None  # we're in an inifinite loop
        history.append(gnext)
        visited.add(gnext)

    return history


def parse_input(fp: str):
    with open(fp, "r", encoding="utf-8") as f:
        lab = f.read().splitlines()

    num_rows = len(lab)
    num_cols = len(lab[0])

    history = []
    obstacles = set()
    for y, row in enumerate(lab):
        for x, pos in enumerate(row):
            if pos == "#":
                obstacles.add(Position(x, y))
            elif pos == "^":
                history.append(Guard(Position(x, y), 0))

    visited = set(history)

    return history, visited, obstacles, num_rows, num_cols


def part1(fp: str) -> int:

    history, visited, obstacles, num_rows, num_cols = parse_input(fp)

    guard_path = traverse(history, visited, obstacles, num_rows, num_cols)

    return len(set(g.pos for g in guard_path))


def part2(fp: str) -> int:

    history, visited, obstacles, num_rows, num_cols = parse_input(fp)

    guard_path = traverse(history, visited, obstacles, num_rows, num_cols)

    infinite_loops = set()
    for new_obstacle_idx in range(1, len(guard_path)):
        new_obstacle = guard_path[new_obstacle_idx].pos
        if new_obstacle not in infinite_loops and (
            traverse(
                history[:1],
                set(history[:1]),
                obstacles | {new_obstacle},
                num_rows,
                num_cols,
            )
            is None
        ):
            infinite_loops.add(new_obstacle)
        print(
            f"\rBe patient ({new_obstacle_idx}/{len(guard_path) - 1}) ... ",
            end="",
            flush=True,
        )

    return len(infinite_loops)


print(part1("06/part1_example.txt"))
print(part1("06/part1.txt"))

print(part2("06/part1_example.txt"))
print(part2("06/part1.txt"))
