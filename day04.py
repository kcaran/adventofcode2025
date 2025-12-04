#!/usr/bin/env python3

#
# lessons from axlerod:
#   * Create a twod array (list)
#   * walrus while (rem := add()): - Introduced in 3.8!!
#   * use self.grid instead of self.map for variable name
#

import re
import sys

# Import the class from your module file
from aoc import AoCInput

class Day04:
    def __init__(self, input_file: str):
        self.input = AoCInput(input_file).lines()
        self.size = len( self.input )
        self.grid = [ list( line.strip() ) for line in self.input ]

    def adjacents(self, row, col):
        # Don't count ourselves
        adj = -1
        for y in range( row - 1, row + 2 ):
            for x in range( col - 1, col + 2 ):
                if (y >= 0 and y < self.size and x >= 0 and x < self.size):
                    adj += 1 if (self.grid[y][x] == '@') else 0
        return adj

    def forklifts(self):
        forks = []
        for y in range( 0, self.size ):
            for x in range( 0, self.size ):
                if (self.grid[y][x] == '@' and self.adjacents( y, x ) < 4):
                    forks.append( [ y, x ] )

        # Pick up the papaer
        for f in forks:
           self.grid[f[0]][f[1]] = '.'

        return len(forks)

    def solve(self):
        self.parta = self.forklifts()
        self.partb = self.parta

        while (removed := self.forklifts()):
          self.partb += removed

        return self

def main():
    # Check if a command-line argument was provided.
    # sys.argv[0] is the script name itself, so a length > 1 means we have arguments.
    input_file = sys.argv[1] if len(sys.argv) > 1 else "input04.txt"

    puzzle = Day04( input_file )
    puzzle.solve()
    print( f"The forkliftable rolls at first are {puzzle.parta}" )
    print( f"The number of rolls removed are {puzzle.partb}" )

if __name__ == "__main__":
    main()
