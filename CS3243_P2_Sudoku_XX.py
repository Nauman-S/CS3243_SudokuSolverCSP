# CS3243 Introduction to Artificial Intelligence
# Project 2, Part 1: Sudoku

import sys
import copy
import heapq

# Running script: given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt


# The class varaible represents a cell in the Sudoku class, each varaible can take a value from 1 to 10

class Variable(object):
    def __init__(self,row,col,value = 0):
        self.row = row
        self.col = col
        self.domain = set(range(1,10)) #The domain of each variable is a set of values from 1 - 9 initially
        self.value = value #The value assigned to the variable

    #Returns the number of Remaining Values possible for the variable
    def remainingValue(self):
        return len(self.domain)

    def __lt__ (self,other):
        return self.remainingValue() < other.remainingValue()


class CSP(object):
    def __init__(self,puzzle):
        self.variables = [Variable(row_number,col_number,item) for row_number,row in enumerate(puzzle) for col_number,item in enumerate(row) if item == 0]
        heapq.heapify(self.variables) #Arrange the variables based on minimum-Remaining-Value

    def backTrackingSearch(self):
        while ()


class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists

    def solve(self):

        self.checkComplete(self.ans)
        self.checkValid(self.ans)
        return self.ans





    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY
    # Note that our evaluation scripts only call the solve method.
    # Any other methods that you write should be used within the solve() method.

    # Helper method to check if the puzzle is complete
    def checkComplete(self,puzzle):
        for row in range(len(puzzle)):
            for col in range(len(puzzle[row])):
                if puzzle[row][col] > 9 or puzzle[row][col] < 1:
                    print("row: " + str(row) + ", col: " + str(col) + "has invalid value " + str(puzzle[row][col]))

    def checkValid(self,puzzle):
        self.isValidRow(puzzle,True) #check valid rows
        self.isValidRow([[puzzle[j][i] for j in range(len(puzzle))] for i in range(len(puzzle[0]))],False)#check valid columns


    def isValidRow(self,puzzle,isRow):
        for row in range(len(puzzle)):
            if (sum(puzzle[row]) != 45):
                if isRow:
                    print("invalid row " + str(row))
                else:
                    print("invalid col " + str(row))


if __name__ == "__main__":
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 3:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise IOError("Input file not found!")

    puzzle = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0

    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()

    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")
