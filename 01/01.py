def part1(fp: str) -> int:
    with open(fp, "r", encoding="utf-8") as f:
        ids = (line.split() for line in f)
        list1, list2 = zip(*((int(a), int(b)) for a, b in ids))

    return sum(abs(id2 - id1) for id1, id2 in zip(sorted(list1), sorted(list2)))


def part2(fp: str) -> int:
    with open(fp, "r", encoding="utf-8") as f:
        ids = (line.split() for line in f)
        list1, list2 = zip(*((int(a), int(b)) for a, b in ids))

    return sum(id1 * sum(1 for id2 in list2 if id2 == id1) for id1 in list1)


print(part1("01/part1_example.txt"))
print(part1("01/part1.txt"))
print(part2("01/part1_example.txt"))
print(part2("01/part1.txt"))
