#!/usr/bin/env python3

#
# ** Python's strip() function removes trailing whitespace as well as the line feed.
#   It isn't chomp()!
#
# lessons from axlerod:
#

import re
import sys

# Import the class from your module file
from aoc import AoCInput

class Day06:
    def __init__(self, input_file: str):
        self.input = AoCInput(input_file).lines()
        self.data = [ list( line.strip().split() ) for line in self.input ]
        self.length = max( len(line) for line in self.input )
        self.data_b = []
        self.sum_b = 0
        op = ''
        nums = []
        for col in range( self.length - 1, -1, -1 ):
            if (len(self.input[-1]) > col and self.input[-1][col] != ' '):
                if op:
                    print( f"two ops {col} {op}")
                op = self.input[-1][col]
            next = self.num( col )
            if (next != ''):
                nums.append( next )
            else:
                self.sum_b += self.op_b( op, nums )
                op = ''
                nums = []
        self.sum_b += self.op_b( op, nums )
        return


    def num(self, col: int):
        num = ''
        for row in range( 0, len(self.input) - 1 ):
            if (len(self.input[row]) < col + 1):
                 continue
            num += self.input[row][col] if (self.input[row][col] != ' ') else ''
        print( f"{col}: {num}" )
        return num

    def op_a(self, col: int):
        col_op = self.data[-1][col]
        calc = 1 if (col_op == '*') else 0
        for i in range(0, len(self.data) - 1):
           if (col_op == '+'):
               calc += int(self.data[i][col])
           elif (col_op == '*'):
               calc *= int(self.data[i][col])
        return calc

    def op_b(self, op, nums ):
       calc = 1 if (op == '*') else 0
       for n in nums:
           if (op == '+'):
               calc += int(n)
           elif (op == '*'):
               calc *= int(n)
       return calc

    def solve(self):
        self.sum_a = 0
        for i in range(0, len(self.data[0])):
             self.sum_a += self.op_a( i )
        return self


def main():
    # Check if a command-line argument was provided.
    # sys.argv[0] is the script name itself, so a length > 1 means we have arguments.
    input_file = sys.argv[1] if len(sys.argv) > 1 else "input06.txt"

    puzzle = Day06( input_file )
    puzzle.solve()
    print( f"The sum of all the operations for part a is {puzzle.sum_a}" )
    print( f"The sum of all the operations for part b is {puzzle.sum_b}" )

if __name__ == "__main__":
    main()
