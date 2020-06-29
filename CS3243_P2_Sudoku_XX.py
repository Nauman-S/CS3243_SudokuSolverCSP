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

    #Compare variables based on the Remaining values they have left 
    def __lt__ (self,other):
        return self.remainingValue() < other.remainingValue()

    def __str__ (self):
        return "row = {}, col = {}, val = {} , domain = {}".format(self.row,self.col,self.value,self.domain)


class CSP(object):
    def __init__(self,puzzle):
        #self.variables = [Variable(row_number,col_number,item) for row_number,row in enumerate(puzzle) for col_number,item in enumerate(row) if item == 0]
        #heapq.heapify(self.variables) #Arrange the variables based on minimum-Remaining-Value
        self.assignments = {}  
        self.puzzle = puzzle
        self.unassigned = 0

        # a list of all variables
        self.variables = []

    def initialize (self):

        for row_number, row in enumerate(puzzle):
            for col_number, item in enumerate(row):
                var = Variable(row_number,col_number)
                if item != 0: 
                    var.value = item
                    var.domain=set()
                if item ==0:
                    self.unassigned+=1
                self.assignments[(row_number,col_number)] = var
                self.variables.append(var)
        heapq.heapify(self.variables)


    def least_constraining_value (self,var):
        lim = 25 # At most the value can constrain the row col and grid which is 8 + 8 + 8 =24
        lcv = None
        for val in var.domain:
            counter = 0
            #Checking col constraints
            for row in range(0,9):
                if row != var.row:
                        var_neighbour= self.assignments[(row,var.col)]
                        if val in var_neighbour.domain and var_neighbour.value==0:
                            counter +=1

            #Checking row constraints
            for col in range(0,9):
                if col != var.col:
                    var_neighbour= self.assignments[(var.row,col)]
                    if val in var_neighbour.domain and var_neighbour.value==0:
                        counter +=1
            #Checking grid constraints
            grid_row_number= (var.row//3) * 3
            grid_col_number= (var.col//3) * 3
            for row in range(grid_row_number,grid_row_number+3):
                if row == var.row:
                    continue
                for col in range(grid_col_number,grid_col_number+3):
                    if col == var.col:
                        continue
                    var_neighbour= self.assignments[(row,col)]
                    if val in var_neighbour.domain and var_neighbour.value==0:
                        counter  +=1

            if counter < lim:
                lim = counter
                lcv = val
        return lcv
    

    #This inference only does forward-checking
    def inference(self,var,val,removed):
        for row in range(0,9):
            if row!=var.row:
                var_neighbour= self.assignments[(row,var.col)]
                if var_neighbour.value==0 and val in var_neighbour.domain:
                    var_neighbour.domain.remove(val)
                    removed[(var_neighbour.row,var_neighbour.col)] = val
                    if len(var_neighbour.domain) == 0: #Domain wipeout
                        return False

        for col in range(0,9):
            if col!=var.col:
                var_neighbour = self.assignments[(var.row,col)]
                if var_neighbour.value==0 and val in var_neighbour.domain:
                    var_neighbour.domain.remove(val)
                    removed[(var_neighbour.row,var_neighbour.col)] =val
                    if len(var_neighbour.domain)==0:
                        return False

        #Checking grid constraints

        grid_row_number= (var.row//3) * 3 #0
        grid_col_number= (var.col//3) * 3 #0
        for row in range(grid_row_number,grid_row_number+3):
            if row == var.row:
                continue
            for col in range(grid_col_number,grid_col_number+3):
                if col == var.col:
                    continue
                var_neighbour = self.assignments[(row,col)]
                if var_neighbour.value==0 and val in var_neighbour.domain:
                    var_neighbour.domain.remove(val)
                    removed[(var_neighbour.row,var_neighbour.col)] = val
                    if len(var_neighbour.domain)==0:
                        return False

        return True 


    def backTrackingSearch(self):
        if self.unassigned == 0:
            return self.assignments

        var = heapq.heappop(self.variables) #Use MRV heuristic to select an variable

        if var.value !=0:
            #pre-assigned variable
            if not self.inference(var,var.value,{}):
                print("Not possiblw")
            heapq.heapify(self.variables)
            return self.backTrackingSearch()

        var_values_checked = set()
        while var.domain :
            removed ={} # contains a set of coordinates (i,j) and the value removed from the domain due to inference
            val = self.least_constraining_value(var)
            var.value = val
            var_values_checked.add(val)
            var.domain.remove(val)

            #Since we are doing inferences there is no need to check validity of the above assignment
            if self.inference(var,val,removed):
                self.unassigned -= 1
                heapq.heapify(self.variables)
                output = self.backTrackingSearch()
                if output!=None:
                    return output


            #failure down the current path

            #add back all the removed stuff for the other variables who we inferred for
            for coordinates, values in removed.items():
                row,col = coordinates
                self.assignments[(row,col)].domain.add(values)

        #Failure before current path was even taken
        #Add all the stuff back for the current variable
        var.domain.update(var_values_checked)
        #Make it unassigned again
        var.value = 0
        self.unassigned += 1

        #put the variable back into the heapq
        heapq.heappush(self.variables,var)

        return None













# If in the output file = input file means no valid assignments were found
class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists

    def solve(self):
        csp = CSP(puzzle)
        csp.initialize()
        assignments = csp.backTrackingSearch()
        if assignments!=None:
            #There exists a valid solution, make those assignments in the ans 
            for row in range(0,9):
                for col in range(0,9):
                    if self.ans[row][col] == 0:
                        self.ans[row][col] = assignments[(row,col)].value
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
