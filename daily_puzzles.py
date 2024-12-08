import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "number_crunch.settings")
import django
django.setup()

import sqlite3
import pandas as pd
from itertools import product
from random import choice
from datetime import date, timedelta
from puzzle_moves import get_operation
from game.models import Puzzle


conn = sqlite3.connect('db.sqlite3')

START_DATE = date(2025, 1, 1)
END_DATE = date(2025, 2, 1)
standard_moves = {
    1: '+1',
    -1: '-1',
    20: 'x2',
    -20: '/2',
    100: 'x10',
    -100: '/10',
    2000: '**2',
    -2000: 'root2'
}

extra_moves = [1, 2, 3, 4, 5, 20, 30, 40, 50, 100, 2000, 3000]
wild_moves = []
for x in extra_moves:
    wild_moves.append(x)
    wild_moves.append(-1*x)


class PuzzleCreator:

    def __init__(self, moves: int, up_to: date, mode: str):
        self.moves = moves
        self.up_to = up_to
        self.mode = mode
        if mode != 'wild':
            self.move_set = list(standard_moves.keys())
        else:
            self.move_set = wild_moves
        self._valid_possible_moves()

    def create_and_send_puzzles(self):
        for puzzle_date in self._needed_puzzles():
            start_val = (puzzle_date - START_DATE).days + 1
            print(puzzle_date, start_val)
            while True:
                move_set, final_val = self._generate_random_moves(start_val)
                if self._validate_minimum_steps(start_val, final_val):
                    start_val, final_val, move_set =\
                        self.potential_reverse(start_val, final_val, move_set)
                    puzzle = Puzzle(puzzle_date=puzzle_date,
                                    puzzle_mode=self.mode,
                                    puzzle_type=self.moves,
                                    puzzle_start=start_val,
                                    puzzle_goal=final_val)
                    puzzle.save()
                    print(start_val, final_val, move_set)
                    break

    def _generate_random_moves(self, start_val):
        moves_taken = []
        cur_val = temp = start_val
        for _ in range(self.moves):
            while cur_val == temp:
                while True:
                    move = choice(self.move_set)
                    try:
                        if move != -1*moves_taken[-1]:
                            break
                    except IndexError:
                        break
                temp = get_operation(move)(cur_val, move)
            moves_taken.append(move)
            cur_val = temp
        return [moves_taken, cur_val]

    def potential_reverse(self, start, end, moves):
        coin = choice([0, 1])
        if coin:
            start, end = end, start
            moves = [x*-1 for x in moves[::-1]]
        return [start, end, moves]

    def _validate_minimum_steps(self, start_val, end_val):
        for possible in self.to_check:
            temp = start_val
            for x in possible:
                temp = get_operation(x)(temp, x)
            if temp == end_val:
                return False
        return True

    def _valid_possible_moves(self):
        to_check = []
        for possible in product(self.move_set, repeat=self.moves-1):
            inverse_operation_free = True
            for x in range(1, len(possible)):
                if possible[x] == -1*possible[x-1]:
                    inverse_operation_free = False
                    break
            if inverse_operation_free:
                to_check.append(possible)
        self.to_check = to_check

    def _needed_puzzles(self) -> list[date]:
        query = f"""
            SELECT max(puzzle_date) as last_date
            FROM game_puzzle
            WHERE puzzle_mode = '{self.mode}' and puzzle_type = '{self.moves}'
        """
        df = pd.read_sql(query, conn, parse_dates=['last_date'])
        max_date = df.at[0, 'last_date'].date()
        if pd.isna(max_date):
            max_date = START_DATE - timedelta(1)
        needed = []
        while max_date < self.up_to:
            max_date += timedelta(1)
            needed.append(max_date)
        return needed


if __name__ == '__main__':
    mgr = PuzzleCreator(9, END_DATE, 'standard')
    mgr.create_and_send_puzzles()
    # print(mgr.last_date)
