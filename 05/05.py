from math import floor

Rulebook = dict[str, list[str]]


def parse_rules(text: str) -> Rulebook:
    rules = {}
    for rule in text.splitlines():
        before, after = rule.split("|")
        if before in rules:
            rules[before].append(after)
        else:
            rules[before] = [after]

    return rules


def is_valid(update: str, rules: Rulebook) -> bool:
    sequence = update.split(",")

    return not any(
        x in rules.get(y, []) for i, x in enumerate(sequence) for y in sequence[i + 1 :]
    )


def score(update: str) -> int:
    sequence = update.split(",")

    return int(sequence[floor(len(sequence) / 2)])


def fix_order(update: str, rules: Rulebook) -> str:

    while not is_valid(update, rules):
        sequence = update.split(",")
        reordered_sequence = sequence.copy()
        for i, x in enumerate(sequence):
            for y in sequence[i + 1 :]:
                if x in rules.get(y, []):
                    reordered_sequence = sequence[:i] + sequence[i + 1 :] + [x]
        update = ",".join(reordered_sequence)

    return update


def part1(fp: str) -> int:
    with open(fp, "r", encoding="utf-8") as f:
        rules, updates = f.read().split("\n\n")

    rules = parse_rules(rules)

    return sum(
        score(update) for update in updates.splitlines() if is_valid(update, rules)
    )


def part2(fp: str) -> int:
    with open(fp, "r", encoding="utf-8") as f:
        rules, updates = f.read().split("\n\n")

    rules = parse_rules(rules)

    return sum(
        score(fix_order(update, rules))
        for update in updates.splitlines()
        if not is_valid(update, rules)
    )


print(part1("05/part1_example.txt"))
print(part1("05/part1.txt"))
print(part2("05/part1_example.txt"))
print(part2("05/part1.txt"))
