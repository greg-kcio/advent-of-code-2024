from enum import Enum, auto


def is_safe_part1(levels: list[int]) -> int:
    """Return 1 if safe, 0 if unsafe"""

    if len(levels) == 1:
        return 1

    safe_differences = (
        tuple(range(1, 4)) if levels[0] - levels[1] > 0 else tuple(range(-3, 0))
    )

    for i in range(len(levels) - 1):
        difference = levels[i] - levels[i + 1]
        if difference not in safe_differences:
            return 0

    return 1


class Direction(Enum):
    INCREASING = auto()
    DECREASING = auto()
    UNSET = auto()


def is_safe_part2(
    levels: list[int],
    direction: Direction = Direction.UNSET,
    num_removed: int = 0,
) -> bool:
    """Return True if safe, False if unsafe"""

    if len(levels) == 1:
        return True

    if direction == Direction.UNSET:
        return is_safe_part2(levels, Direction.INCREASING) or is_safe_part2(
            levels, Direction.DECREASING
        )

    safe_differences = (
        tuple(range(1, 4)) if direction == Direction.DECREASING else tuple(range(-3, 0))
    )

    for i in range(len(levels) - 1):
        difference = levels[i] - levels[i + 1]
        if difference not in safe_differences:
            if num_removed > 0:
                return False
            remaining_line_with_current_level_removed = levels[i + 1 :]
            if i > 0:
                remaining_line_with_current_level_removed.insert(0, levels[i - 1])
            if i == len(levels) - 2:
                return True  # if the last pair is the broken one then this line is safe
            remaining_line_with_next_level_removed = [levels[i]] + levels[i + 2 :]
            return is_safe_part2(
                remaining_line_with_current_level_removed, direction, 1
            ) or is_safe_part2(remaining_line_with_next_level_removed, direction, 1)

    return True


def count_safe_lines(fp: str, is_safe: callable) -> int:
    with open(fp, "r", encoding="utf-8") as f:
        lines = f.readlines()

    return sum(is_safe(list(map(int, line.split()))) for line in lines)


print(count_safe_lines("02/part1_example.txt", is_safe_part1))
print(count_safe_lines("02/part1.txt", is_safe_part1))
print(count_safe_lines("02/part1_example.txt", is_safe_part2))
print(count_safe_lines("02/part1.txt", is_safe_part2))
