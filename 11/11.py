from functools import cache


def solve_slow(fp: str, num_blinks: int) -> int:
    with open(fp, "r", encoding="utf-8") as f:
        stones = f.read().split()

    for _blink in range(num_blinks):
        new_stones = []
        for stone in stones:
            if int(stone) == 0:
                new_stones.append("1")
            elif (n := len((stone := str(int(stone))))) % 2 == 0:
                new_stones.extend([stone[: n // 2], stone[n // 2 :]])
            else:
                new_stones.append(str(int(stone) * 2024))
        stones = new_stones

    return len(stones)


@cache
def blink(stone: str, blinks_remaining: int) -> int:
    if blinks_remaining == 0:
        return 1
    blinks_remaining -= 1
    if int(stone) == 0:
        return blink("1", blinks_remaining)
    if (n := len((stone := str(int(stone))))) % 2 == 0:
        return blink(stone[: n // 2], blinks_remaining) + blink(
            stone[n // 2 :], blinks_remaining
        )
    return blink(str(int(stone) * 2024), blinks_remaining)


def solve_fast(fp: str, num_blinks: int) -> int:
    with open(fp, "r", encoding="utf-8") as f:
        stones = f.read().split()

    return sum(blink(stone, num_blinks) for stone in stones)


print(solve_slow("11/part1_example.txt", 25))
print(solve_slow("11/part1.txt", 25))
print(solve_fast("11/part1_example.txt", 25))
print(solve_fast("11/part1.txt", 25))
print(solve_fast("11/part1.txt", 75))
