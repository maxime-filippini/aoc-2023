import pathlib
import re
from dataclasses import dataclass
from dataclasses import field

from lib.io import read_file

root_path = pathlib.Path(__file__).parent

rgx_game = re.compile("Game ([^:]+):\s(.+)")

MIN_GAME = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


@dataclass
class Draw:
    red: int = 0
    green: int = 0
    blue: int = 0


@dataclass
class Game:
    id: str
    draws: list[Draw] = field(default_factory=list)

    _min_red: int = field(init=False)
    _min_green: int = field(init=False)
    _min_blue: int = field(init=False)

    def __post_init__(self) -> None:
        self._min_red = 0
        self._min_green = 0
        self._min_blue = 0

    def add_draw(self, red: int = 0, green: int = 0, blue: int = 0):
        d = Draw(red=red, green=green, blue=blue)
        self.draws.append(d)

        self._min_red = max(self._min_red, d.red)
        self._min_green = max(self._min_green, d.green)
        self._min_blue = max(self._min_blue, d.blue)

    def _check_game(self, min_contents: dict[str, int]) -> bool:
        for k, v in min_contents.items():
            if getattr(self, f"_min_{k}") > v:
                return False
        return True

    def power(self):
        return self._min_blue * self._min_red * self._min_green


def _parse_games(lines: list[str]) -> list[Game]:

    all_games: list[Game] = []

    for line in lines:
        game_id, contents = rgx_game.match(line).groups()
        game = Game(id=int(game_id))

        draws = contents.strip().split("; ")

        for draw in draws:
            draw_content = {
                color: int(n)
                for item in draw.split(", ")
                for n, color in [item.split(" ")]
            }

            game.add_draw(**draw_content)

        all_games.append(game)

    return all_games


def solve_pt1(lines: list[str]) -> None:
    games = _parse_games(lines)
    print(sum([g.id for g in games if g._check_game(min_contents=MIN_GAME)]))


def solve_pt2(lines: list[str]) -> None:
    games = _parse_games(lines)
    print(sum([g.power() for g in games]))


if __name__ == "__main__":
    inp = read_file(root_path / "input")
    solve_pt2(inp)
