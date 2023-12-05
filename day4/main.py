import pathlib
import re

from lib.io import read_file

root_path = pathlib.Path(__file__).parent

RE_CARD = re.compile("Card\s+(\d+):\s([^\|]+)\s\|\s(.+)")


def _parse_input(line: str):
    match = RE_CARD.match(line)

    card_id, winning, gotten = match.groups()

    return (
        card_id,
        set([x for x in winning.lstrip().split(" ") if x]),
        set([x for x in gotten.lstrip().split(" ") if x]),
    )


def solve_pt1(lines: list[str]) -> None:
    total = 0

    for line in lines:
        id, winning, gotten = _parse_input(line)
        common = len(winning.intersection(gotten))

        if common:
            total += 2 ** (common - 1)

    print(total)


def solve_pt2(lines: list[str]) -> None:
    tracker = {}

    for line in lines:
        id, winning, gotten = _parse_input(line)
        tracker[int(id)] = {"n": 1, "winning": winning, "gotten": gotten}

    for id, data in tracker.items():
        common = len(data["winning"].intersection(data["gotten"]))

        for i in range(common):
            next_id = id + i + 1

            if next_id in tracker:
                tracker[next_id]["n"] += data["n"]
            else:
                break

    print(sum(item["n"] for item in tracker.values()))


if __name__ == "__main__":
    inp = read_file(root_path / "input")
    solve_pt2(inp)
