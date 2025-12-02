#!/usr/bin/env python3
import re
import sys

# Import the class from your module file
from aoc import AoCInput

class day01:
    def __init__(self, input_file):
         self.pos = 50
         self.zeros = 0
         self.resets = 0
         try:
             self.turns = input_data = AoCInput(input_file).lines()
         except (FileNotFoundError, RuntimeError) as e:
             print(f"\nError: Could not load puzzle input: {e}")

    def move(self, turn):
        parse = re.search( r"^(\D)(\d+)", turn );
        clicks = int(parse.group(2))
        while (clicks > 0):
            clicks -= 1
            if (parse.group(1) == 'L'):
                self.pos = 99 if (self.pos == 0) else (self.pos - 1)
            else:
                self.pos = 0 if (self.pos == 99) else (self.pos + 1)
            self.resets += 1 if (self.pos == 0) else 0

        self.zeros += 1 if (self.pos == 0) else 0

    def solve(self):
        for t in self.turns:
            self.move(t)
            print( f"The dial is rotated {t} to point at {self.pos}" )
        return self.zeros


def main():
    # Check if a command-line argument was provided.
    # sys.argv[0] is the script name itself, so a length > 1 means we have arguments.
    input_file = sys.argv[1] if len(sys.argv) > 1 else "input01.txt"

    puzzle = day01( input_file )
    puzzle.solve()
    print( f"The password for part one is {puzzle.zeros}" )
    print( f"The password for part two is {puzzle.resets}" )

if __name__ == "__main__":
    main()
