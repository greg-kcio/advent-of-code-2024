from dataclasses import dataclass, field


@dataclass
class Position:
    x: int
    y: int

    def adjacent_positions(self) -> "tuple[Position]":
        return (
            Position(self.x, self.y - 1),
            Position(self.x + 1, self.y),
            Position(self.x, self.y + 1),
            Position(self.x - 1, self.y),
        )

    def __hash__(self) -> int:
        return hash((self.x, self.y))


@dataclass
class TrailMap:
    topography: list[list[int]]
    trails: list[list[Position]] = field(default_factory=list)

    def __post_init__(self):
        _ = [
            self.traverse([Position(x, y)])
            for y, row in enumerate(self.topography)
            for x, cell in enumerate(row)
            if cell == 0
        ]

    def traverse(self, visited: list[Position]) -> list[Position]:
        last_visited = visited[-1]
        for adjacent_pos in last_visited.adjacent_positions():
            if (
                next_height := self.topography[adjacent_pos.y][adjacent_pos.x]
            ) == self.topography[last_visited.y][last_visited.x] + 1:
                if next_height == 9:
                    self.trails.append(
                        visited + [Position(adjacent_pos.x, adjacent_pos.y)]
                    )
                else:
                    self.traverse(visited + [Position(adjacent_pos.x, adjacent_pos.y)])

    def score(self) -> int:
        # +1 per unique start/end pair
        unique_trails = {(t[0], t[-1]) for t in self.trails}
        return len(unique_trails)

    def rating(self) -> int:
        return len(self.trails)


def solve(fp: str) -> int:
    with open(fp, "r", encoding="utf-8") as f:
        raw_map = f.readlines()

    # pad the square map
    padded_map = (
        [[-1] * (len(raw_map) + 2)]
        + [[-1] + list(map(int, row.strip())) + [-1] for row in raw_map]
        + [[-1] * (len(raw_map) + 2)]
    )

    trail_map = TrailMap(padded_map)

    return trail_map.score(), trail_map.rating()


print(solve("10/part1_example.txt"))
print(solve("10/part1.txt"))
