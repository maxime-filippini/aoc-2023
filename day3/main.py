import pathlib
from collections import defaultdict
from math import prod

from lib.io import read_file

root_path = pathlib.Path(__file__).parent

_offsets = [
    (-1, 0),
    (-1, -1),
    (-1, +1),
    (+1, 0),
    (+1, -1),
    (+1, +1),
    (0, -1),
    (0, +1),
]


def solve_pt1(lines: list[str]) -> None:
    numbers = []
    n_cols = len(lines[0])

    # Expand the grid to avoid having to handle the edges
    lines = (
        ["." * (n_cols + 2)] + [f".{line}." for line in lines] + ["." * (n_cols + 2)]
    )

    found = False
    current_number = []

    for i_line, line in enumerate(lines):
        for i_char, char in enumerate(line):
            if char not in "0123456789":
                if found:
                    numbers.append(int("".join(current_number)))

                current_number = []
                found = False
                continue

            # Check for part if not found
            current_number.append(char)

            if not found:
                for i_offset, j_offset in _offsets:
                    char_test = lines[i_line + i_offset][i_char + j_offset]

                    if char_test != "." and char_test not in "0123456789":
                        found = True

    print(sum(numbers))


def solve_pt2(lines: list[str]) -> None:
    gears = defaultdict(list)
    n_cols = len(lines[0])

    lines = (
        ["." * (n_cols + 2)] + [f".{line}." for line in lines] + ["." * (n_cols + 2)]
    )

    found = None
    current_number = []

    for i_line, line in enumerate(lines):
        for i_char, char in enumerate(line):
            if char not in "0123456789":
                if found:
                    gears[found].append(int("".join(current_number)))

                current_number = []
                found = None
                continue

            # Check for part if not found
            current_number.append(char)

            if not found:
                for i_offset, j_offset in _offsets:
                    char_test = lines[i_line + i_offset][i_char + j_offset]

                    if char_test == "*":
                        found = (i_line + i_offset, i_char + j_offset)

    print(sum(prod(numbers) for numbers in gears.values() if len(numbers) == 2))


if __name__ == "__main__":
    inp = read_file(root_path / "input")
    solve_pt2(inp)
