#!/usr/bin/env python3
import re
import sys

# Import the class from your module file
from aoc import AoCInput

class day02:
    def __init__(self, input_file):
        self.input = AoCInput(input_file).slurp()

    def find( self, min, max ):
        doubles = []
        num = 11 if (min < 10) else min
        while (num <= max):
             if (re.match( r"^(\d+)\1+$", str(num) )):
                  doubles.append( num )
             num += 1

        return doubles

    def solve(self):
        self.sum = 0
        for range in re.split( ',', self.input ):
            limits = re.search( r"(\d+)-(\d+)", range );
            min = int(limits.group(1))
            max = int(limits.group(2))
            print( f"{range} {min}-{max}" )
            for d in self.find( min, max ):
                self.sum += int(d)

        return self


def main():
    # Check if a command-line argument was provided.
    # sys.argv[0] is the script name itself, so a length > 1 means we have arguments.
    input_file = sys.argv[1] if len(sys.argv) > 1 else "input02.txt"

    puzzle = day02( input_file )
    puzzle.solve()
    print( f"The sum of all the doubles is {puzzle.sum}" )

if __name__ == "__main__":
    main()
