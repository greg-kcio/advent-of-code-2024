from collections import defaultdict
from dataclasses import dataclass


@dataclass(frozen=True)
class CitySize:
    num_rows: int
    num_cols: int


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def near_antinode(self, other: "Position") -> "Position":
        """The position of the antinode closer to this antenna."""
        return Position(self.x + (self.x - other.x), self.y + (self.y - other.y))

    def far_antinode(self, other: "Position") -> "Position":
        """The position of the antinode closer to the other antenna."""
        return other.near_antinode(self)

    def is_in_city(self, city_size: CitySize) -> bool:
        return (
            self.x >= 0
            and self.x < city_size.num_rows
            and self.y >= 0
            and self.y < city_size.num_cols
        )


def parse_input(fp: str) -> tuple[CitySize, defaultdict[list[Position]]]:
    with open(fp, "r", encoding="utf-8") as f:
        city = f.read().splitlines()

    num_rows = len(city)
    num_cols = len(city[0])
    city_size = CitySize(num_rows, num_cols)
    antennas = defaultdict(list)

    for y, row in enumerate(city):
        for x, cell in enumerate(row):
            if cell != ".":
                antennas[cell].append(Position(x, y))

    return city_size, antennas


def valid_antinodes(
    first_position: Position,
    second_position: Position,
    city_size: CitySize,
    part2: bool,
) -> list[Position]:

    if not part2:
        return [
            antinode
            for antinode in [
                first_position.near_antinode(second_position),
                first_position.far_antinode(second_position),
            ]
            if antinode.is_in_city(city_size)
        ]

    # Part 2
    valid_positions = [first_position, second_position]
    antenna_1 = first_position
    antenna_2 = second_position
    while (near_antinode := antenna_1.near_antinode(antenna_2)).is_in_city(city_size):
        valid_positions.append(near_antinode)
        antenna_2 = antenna_1
        antenna_1 = near_antinode
    antenna_1 = first_position
    antenna_2 = second_position
    while (far_antinode := antenna_1.far_antinode(antenna_2)).is_in_city(city_size):
        valid_positions.append(far_antinode)
        antenna_1 = antenna_2
        antenna_2 = far_antinode

    return valid_positions


def antinodes_for_frequency(
    locations: list[Position], city_size: CitySize, part2: bool
) -> int:
    return {
        antinode
        for i, first_position in enumerate(locations[:-1])
        for second_position in locations[i + 1 :]
        for antinode in valid_antinodes(
            first_position, second_position, city_size, part2
        )
    }


def solve(fp: str, part2: bool = False) -> int:
    city_size, antennas = parse_input(fp)

    return len(
        {
            antinode
            for locations in antennas.values()
            for antinode in antinodes_for_frequency(locations, city_size, part2)
        }
    )


print(solve("08/part1_example.txt"))
print(solve("08/part1.txt"))
print(solve("08/part1_example.txt", part2=True))
print(solve("08/part1.txt", part2=True))
