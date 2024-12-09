from dataclasses import dataclass


def part1(fp: str) -> int:
    with open(fp, "r", encoding="utf-8") as f:
        disk = [
            (i // 2) if i % 2 == 0 else "."
            for i, x in enumerate(f.read())
            for _ in range(int(x))
        ]

    for i in range(len(disk)):  # pylint: disable=consider-using-enumerate
        while disk[-1] == ".":
            del disk[-1]
        try:
            if disk[i] == ".":
                disk[i] = disk.pop()
        except IndexError:
            return sum(i * int(x) for i, x in enumerate(disk) if x != ".")


@dataclass
class Emptiness:
    size: int


@dataclass
class File:
    size: int
    id_: int


def part2(fp: str) -> int:
    with open(fp, "r", encoding="utf-8") as f:
        compressed = f.read()
    disk = [
        File(int(x), i // 2) if i % 2 == 0 else Emptiness(int(x))
        for i, x in enumerate(compressed)
    ]

    for backward_i in range(len(disk) - 1, -1, -1):
        if isinstance(candidate_from_back := disk[backward_i], File):
            for forward_i in range(backward_i):
                if isinstance(candidate_from_front := disk[forward_i], Emptiness):
                    if candidate_from_front.size == candidate_from_back.size:
                        disk[forward_i] = candidate_from_back
                        disk[backward_i] = candidate_from_front
                        break
                    if candidate_from_front.size > candidate_from_back.size:
                        disk[forward_i] = candidate_from_back
                        disk.insert(
                            forward_i + 1,
                            Emptiness(
                                candidate_from_front.size - candidate_from_back.size
                            ),
                        )
                        disk[backward_i + 1] = Emptiness(candidate_from_back.size)
                        break

    flattened_disk = [
        x.id_ if isinstance(x, File) else "." for x in disk for _ in range(x.size)
    ]
    return sum(i * int(x) for i, x in enumerate(flattened_disk) if x != ".")


print(part1("09/part1_example.txt"))
print(part1("09/part1.txt"))
print(part2("09/part1_example.txt"))
print(part2("09/part1.txt"))
