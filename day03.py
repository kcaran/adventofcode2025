#!/usr/bin/env python3
import re
import sys

# Import the class from your module file
from aoc import AoCInput

class Day03:
    def __init__(self, input_file: str):
        self.input = AoCInput(input_file).lines()

    def joltage_a( self, bank ):
        bats = [int(char) for char in bank]
        tens = 0
        for i in range(1, len(bats) - 1):
            tens = i if (bats[i] > bats[tens]) else tens
        ones = tens + 1
        for i in range(ones + 1, len(bats)):
            if (bats[i] > bats[ones]):
                ones = i

        return bats[tens] * 10 + bats[ones]

    def max_val( self, bank, start, end ):
        val = bank[start]
        idx = [start]
        for i in range(start + 1, end):
           if (bank[i] > val):
              val = bank[i]
              idx = [i]
           elif (bank[i] == val):
               idx.append(i)
        return idx

    def joltage_b( self, bank, nums, start ):
        lenj = 12
        nextnums = []
        if (len(nums[0]) == lenj):
            return nums

        for num in nums:
            end = len(bank) - (lenj - len(num) - 1)
            nextd = self.max_val( bank, start, end )
            for idx in nextd:
              nextnums.extend( self.joltage_b( bank, [num + bank[idx]], idx + 1 ) )

        return nextnums

    def solve(self):
        self.sum_a = 0
        for bank in self.input:
            self.sum_a += self.joltage_a(bank)

        self.sum_b = 0
        for bank in self.input:
            nums = self.joltage_b(bank, [''], 0)
            max_num = nums[0]
            for n in nums:
                max_num = n if (n > max_num) else max_num
            self.sum_b += int( max_num )

        return self


def main():
    # Check if a command-line argument was provided.
    # sys.argv[0] is the script name itself, so a length > 1 means we have arguments.
    input_file = sys.argv[1] if len(sys.argv) > 1 else "input03.txt"

    puzzle = Day03( input_file )
    puzzle.solve()
    print( f"The sum of all the joltages for part a is {puzzle.sum_a}" )
    print( f"The sum of all the joltages for part b is {puzzle.sum_b}" )

if __name__ == "__main__":
    main()
