#!/usr/bin/env python3

#
# lessons from axlerod:
#   * Sorting a list from one of its members:
#       self.input.sort( key=lambda pair: pair[0] )
#   * Python prefers True/False to 1/0

import re
import sys

# Import the class from your module file
from aoc import AoCInput

class Day05:
    def __init__(self, input_file: str):
        self.input = []
        self.ingred = []
        self.fresh = 0
        for l in AoCInput(input_file).lines():
            if (r := re.search( r"^(\d+)-(\d+)", l )):
                self.input.append( [ int(r[1]), int(r[2]) ] )
            elif l:
                self.ingred.append( int(l) )
        self.input.sort( key=lambda pair: pair[0] )
        self.calc_ranges()

    def calc_ranges( self ):
        self.ranges = [ self.input[0] ]

        for next_r in (self.input[1:]):
            # Check if start is contained in previous range
            if (next_r[0] > self.ranges[-1][1]):
                self.ranges.append( next_r )
            elif (next_r[1] > self.ranges[-1][1]):
                self.ranges[-1][1] = next_r[1]

        return self

    def check_fresh( self, ingred:int ):
        for fresh in self.ranges:
           if (ingred >= fresh[0] and ingred <= fresh[1]):
               return 1
        return 0

    def solve( self ):
        for i in self.ingred:
            self.fresh +=1 if self.check_fresh( i ) else 0
        self.sum = 0
        for r in (self.ranges):
             self.sum += (r[1] - r[0] + 1)

        return self

def main():
    # Check if a command-line argument was provided.
    # sys.argv[0] is the script name itself, so a length > 1 means we have arguments.
    input_file = sys.argv[1] if len(sys.argv) > 1 else "input05.txt"

    puzzle = Day05( input_file )
    puzzle.solve()
    print( f"The number of fresh ingredients is {puzzle.fresh}" )
    print( f"The total number of fresh ingredients is {puzzle.sum}" )

if __name__ == "__main__":
    main()
