#!/usr/bin/env python3
#
# I did have to cheat on the algorithm
#
# https://www.reddit.com/r/adventofcode/comments/1pgnmou/2025_day_7_lets_visualize/
#
# lessons from axlerod:
#    sum( list )
#    str.index( char ) <-- but it *has* to be there or it is an error :-(
#    str[3] = 'a' <-- Strings are immutable! This won't work!
#    deque - queue
#    ** tuples can be keys, you don't need to create a string
#    ** I keep forgetting for loop auto-truncates the end! range( len( line ) )
#
#

from collections import deque
import re
import sys

# Import the class from your module file
from aoc import AoCInput

class Day07:
    def __init__(self, input_file: str):
        self.input = AoCInput(input_file).lines()
        self.size = len( self.input )
        self.grid = [ list( line.strip() ) for line in self.input ]
        self.splits = 0
        self.times = [ 0 ] * self.size
        self.moves = deque( [ [ 1, self.input[0].index( 'S' ) ] ] )
        self.times[self.moves[0][1]] = 1
        self.seen_h = {}
        self.seen( self.moves[0] )

    def seen(self, move):
        # Ignore illegal moves by saying we've seen them
        if (move[1] < 0 or move[1] >= self.size):
           return True

        mkey = f"{move[0]},{move[1]}"
        if (mkey in self.seen_h):
            return True
        else:
            self.seen_h[mkey] = True
        return False

    def next(self, move):
        next_moves = []
        if (move[0] + 1 == self.size):
            return next_moves

        if (self.grid[move[0] + 1][move[1]] == '^'):
            left = [move[0] + 1, move[1] - 1]
            if (not self.seen( left )):
                next_moves.append( left )
            right = [move[0] + 1, move[1] + 1]
            if (not self.seen( right )):
                next_moves.append( right )
            self.splits += 1
        else:
            drop = [move[0] + 1, move[1]]
            if (not self.seen( drop )):
                next_moves.append( drop )
        return next_moves

    def next_b(self, line):
        for col in range( len(line) ):
            if (line[col] == '^'):
                if (col > 0):
                    self.times[col - 1] += self.times[col]
                if (col < self.size - 1):
                    self.times[col + 1] += self.times[col]
                self.times[col] = 0
        return self

    def solve(self):
        while (self.moves):
            next_moves = self.next( self.moves.popleft() )
            self.moves.extend( next_moves )

        for row in range( 1, self.size ):
            self.next_b( self.input[row] )

        return self


def main():
    # Check if a command-line argument was provided.
    # sys.argv[0] is the script name itself, so a length > 1 means we have arguments.
    input_file = sys.argv[1] if len(sys.argv) > 1 else "input07.txt"

    puzzle = Day07( input_file )
    puzzle.solve()
    print( f"The beam is split {puzzle.splits} times" )
    uni = sum( puzzle.times ) 
    print( f"The number of universes is {uni}" )

if __name__ == "__main__":
    main()
