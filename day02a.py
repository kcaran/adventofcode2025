#!/usr/bin/env python3
import re
import sys

# Import the class from your module file
from aoc import AoCInput

class day02:
    def __init__(self, input_file):
        self.input = AoCInput(input_file).slurp()

    def norm_min( self, min ):
        # Increase min and/or decrease max to even number of digits
        if (len(min) % 2 == 1):
            min = '1' + '0' * len(min)
        half = int(len(min) / 2)
        d_min = min[0:half]
        rem = min[half:]
        if (d_min < rem):
           d_min = str(int(d_min) + 1)

        return d_min + d_min

    def norm_max( self, max ):
        # Increase min and/or decrease max to even number of digits
        if (len(max) % 2 == 1):
            max = '9' * (len(max) - 1)

        half = int(len(max) / 2)
        d_max = max[0:half]
        rem = max[half:]
        if (d_max > rem):
           d_max = str(int(d_max) - 1)

        return d_max + d_max

    def find( self, min, max ):
        doubles = []
        num = min
        while (int(num) <= int(max) and (len(doubles) == 0 or doubles[-1] != num)):
            doubles.append( num )
            half = int(len(max) / 2)
            next = str(int(num[0:half]) + 1)
            num = next + next

        return doubles

    def solve(self):
        self.sum = 0
        for range in re.split( ',', self.input ):
            limits = re.search( r"(\d+)-(\d+)", range );
            min = self.norm_min( limits.group(1) )
            max = self.norm_max( limits.group(2) )
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
