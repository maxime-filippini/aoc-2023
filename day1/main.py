import pathlib

from lib.io import read_file

digits = "0123456789"


spelled = (
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
)

TComparable = int | float
TFoundDigit = tuple[int, str]

root_path = pathlib.Path(__file__).parent

# Ugly af, to be cleaned. Only finds the first and last occurence of each
# digit in the string, which is sufficient for our need.
def find_all_digits(text: str) -> tuple[list[TFoundDigit], list[TFoundDigit]]:
    digit_idx = [
        (x, d) for d in digits for f in (text.find, text.rfind) if (x := f(d)) > -1
    ]

    spelled_idx = [
        (x, str(i))
        for i, s in enumerate(spelled)
        for f in (text.find, text.rfind)
        if (x := f(s)) > -1
    ]
    return digit_idx, spelled_idx


def find_first_and_last(idx_arr: list[tuple[int, str]]) -> tuple[list[int], list[int]]:
    if idx_arr:
        first = min(idx_arr, key=lambda t: t[0])
        last = max(idx_arr, key=lambda t: t[0])

    else:
        first = (2**64, "null")
        last = (-(2**64), "null")

    return first, last


def build_number(
    first_digit: TFoundDigit,
    last_digit: TFoundDigit,
    first_spelled: TFoundDigit,
    last_spelled: TFoundDigit,
):
    first_digit = min((first_digit, first_spelled), key=lambda t: t[0])
    last_digit = max((last_digit, last_spelled), key=lambda t: t[0])

    return first_digit[1] + last_digit[1]


def solve_pt1(inp: list[str]) -> None:
    all_numbers = []

    for line in inp:
        digits_found = [char for char in line if char in digits]
        all_numbers.append(int(digits_found[0] + digits_found[-1]))

    print(sum(all_numbers))


def solve_pt2(inp: list[str]) -> None:
    all_numbers = []

    for line in inp:
        digit_idx, spelled_idx = find_all_digits(line)
        first_digit, last_digit = find_first_and_last(digit_idx)
        first_spelled, last_spelled = find_first_and_last(spelled_idx)

        number = build_number(
            first_digit=first_digit,
            first_spelled=first_spelled,
            last_digit=last_digit,
            last_spelled=last_spelled,
        )

        all_numbers.append(int(number))

    print("Sum:", sum(all_numbers))


if __name__ == "__main__":
    inp = read_file(root_path / "input")
    solve_pt2(inp)
