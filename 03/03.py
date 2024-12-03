def mull_it_over(fp: str, is_part_2: bool = False) -> int:
    with open(fp, "r", encoding="utf-8") as f:
        memory = f.read()

    enabled = True
    total = 0
    for i in range(len(memory) - 6):
        if memory[i:].startswith("do()"):
            enabled = True
            continue
        if memory[i:].startswith("don't()"):
            enabled = False
        if is_part_2 and not enabled:
            continue
        if memory[i : i + 4] != "mul(":
            continue
        if ")" not in memory[i + 4 :]:
            continue
        params = memory[i + 4 :].split(")", 1)[0].split(",")
        if len(params) != 2:
            continue
        if any(len(p) > 3 for p in params):
            continue
        if any(not c.isdigit() for c in params[0]):
            continue
        if any(not c.isdigit() for c in params[1]):
            continue
        params = tuple(map(int, params))
        total += params[0] * params[1]

    return total


print(mull_it_over("03/part1_example.txt"))
print(mull_it_over("03/part1.txt"))
print(mull_it_over("03/part1_example.txt", is_part_2=True))
print(mull_it_over("03/part1.txt", is_part_2=True))
